from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

from ..items import AP_ID_TO_NAME, ITEM_TABLE

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonB2W2Client
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import NetworkItem

RECEIVED_ITEMS_VAR = 0x1A6
LOG_FILTER_VAR = 0x197
LOG_VARS = [0x1A1, 0x1A2, 0x1A3, 0x1A4, 0x1A5]


async def _ensure_bag_buffers(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> list[bytearray]:
    if client.bag_buffers is None:
        base = client.save_data_address
        reads = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (base + client.main_items_bag_offset, client.main_items_bag_size * 4, client.ram_Segment),
                (base + client.key_items_bag_offset, client.key_items_bag_size * 4, client.ram_Segment),
                (base + client.tm_hm_bag_offset, client.tm_hm_bag_size * 4, client.ram_Segment),
                (base + client.medicine_bag_offset, client.medicine_bag_size * 4, client.ram_Segment),
                (base + client.berry_bag_offset, client.berry_bag_size * 4, client.ram_Segment),
            ],
        )
        client.bag_buffers = [bytearray(r) for r in reads]
    return client.bag_buffers


async def receive_items(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    if getattr(client, "is_battle", False) or not getattr(client, "is_field", False):
        return
    if not getattr(client, "bag_valid", False):
        return
    if not ctx.items_received:
        return

    base = client.save_data_address
    read_res = await bizhawk.read(
        ctx.bizhawk_ctx,
        [
            (base + client.var_offset + (2 * RECEIVED_ITEMS_VAR), 2, client.ram_Segment),
            (base + client.badges_offset, 1, client.ram_Segment),
            (base + client.var_offset + (2 * LOG_FILTER_VAR), 2, client.ram_Segment),
        ],
    )
    received_count = int.from_bytes(read_res[0], "little")
    if received_count == 0xFFFF:
        return
    if received_count < getattr(client, "_cached_received_count", -1):
        client.bag_buffers = None
        client._candies_slot_offset = -1
        client._repels_slot_offset = -1
    if received_count >= len(ctx.items_received):
        client._cached_received_count = received_count
        return

    filter_mode = int.from_bytes(read_res[2], "little")
    new_received = received_count
    recent_logged_ids: list[int] = []

    for idx in range(received_count, len(ctx.items_received)):
        next_item: "NetworkItem" = ctx.items_received[idx]
        if not await write_item(client, ctx, next_item):
            break
        new_received += 1

        item_name = AP_ID_TO_NAME.get(next_item.item)
        if item_name in ITEM_TABLE:
            info = ITEM_TABLE[item_name]
            item_flags = getattr(next_item, "flags", 0)
            if filter_mode == 0:
                should_log = bool(item_flags & 1)
            elif filter_mode == 1:
                should_log = bool(item_flags & 3)
            else:
                should_log = True
            if should_log:
                if info.pocket == "badge":
                    recent_logged_ids.append(1000 + info.internal_id)
                elif info.pocket == "special":
                    if 400101 <= info.ap_id <= 400104:
                        recent_logged_ids.append(1010 + info.internal_id)
                    elif 400120 <= info.ap_id <= 400126:
                        recent_logged_ids.append(1020 + info.internal_id)
                elif getattr(info, "internal_id", 0):
                    recent_logged_ids.append(info.internal_id)

    if new_received > received_count:
        writes: list[tuple[int, bytes, str]] = [
            (
                base + client.var_offset + (2 * RECEIVED_ITEMS_VAR),
                new_received.to_bytes(2, "little"),
                client.ram_Segment,
            )
        ]
        if recent_logged_ids:
            old_logs = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(base + client.var_offset + (2 * v), 2, client.ram_Segment) for v in LOG_VARS[:4]],
            )
            prev_vals = [
                int.from_bytes(b, "little") if int.from_bytes(b, "little") != 0xFFFF else 0
                for b in old_logs
            ]
            combined = ( list(reversed(recent_logged_ids[-5:])) + prev_vals )[:5]
            for slot_i, var_id in enumerate(LOG_VARS):
                writes.append((
                    base + client.var_offset + (2 * var_id),
                    combined[slot_i].to_bytes(2, "little"),
                    client.ram_Segment,
                ))
        await bizhawk.write(ctx.bizhawk_ctx, writes)
        client._cached_received_count = new_received


async def write_item(client: "PokemonB2W2Client", ctx: "BizHawkClientContext", net_item: "NetworkItem") -> bool:
    item_name = AP_ID_TO_NAME.get(net_item.item)
    if item_name is None or item_name not in ITEM_TABLE:
        client.logger.warning(f"Unknown Archipelago item ID {net_item.item}; skipping.")
        return True

    info = ITEM_TABLE[item_name]
    buffers = await _ensure_bag_buffers(client, ctx)

    if info.pocket == "badge":
        return await write_badge(client, ctx, info.internal_id)
    elif info.pocket == "special":
        if 400101 <= info.ap_id <= 400104:
            await client.write_set_flag(ctx, 3040)
            await client.write_set_flag(ctx, 3041 + info.internal_id)
            return True
        elif 400120 <= info.ap_id <= 400126:
            await client.write_set_flag(ctx, 3045 + info.internal_id)
            return True
        return True
    elif info.pocket == "key_items":
        return await write_to_bag(
            client, ctx, buffers[1],
            client.key_items_bag_offset, client.key_items_bag_size,
            info.internal_id, unique=True,
        )
    elif info.pocket == "tm_hm":
        return await write_to_bag(
            client, ctx, buffers[2],
            client.tm_hm_bag_offset, client.tm_hm_bag_size,
            info.internal_id, unique=True,
        )
    elif info.pocket == "medicine":
        return await write_to_bag(
            client, ctx, buffers[3],
            client.medicine_bag_offset, client.medicine_bag_size,
            info.internal_id, unique=False,
        )
    elif info.pocket == "berries":
        return await write_to_bag(
            client, ctx, buffers[4],
            client.berry_bag_offset, client.berry_bag_size,
            info.internal_id, unique=False,
        )
    else:
        return await write_to_bag(
            client, ctx, buffers[0],
            client.main_items_bag_offset, client.main_items_bag_size,
            info.internal_id, unique=False,
        )


async def write_badge(client: "PokemonB2W2Client", ctx: "BizHawkClientContext", badge_bit: int) -> bool:
    addr = client.save_data_address + client.badges_offset
    current = (await bizhawk.read(ctx.bizhawk_ctx, [(addr, 1, client.ram_Segment)]))[0][0]
    if (current & (1 << badge_bit)) != 0:
        return True
    new_val = current | (1 << badge_bit)
    await bizhawk.write(
        ctx.bizhawk_ctx,
        [(addr, new_val.to_bytes(1, "little"), client.ram_Segment)],
    )
    client._last_badges_byte = new_val
    return True


async def write_to_bag(
    client: "PokemonB2W2Client",
    ctx: "BizHawkClientContext",
    pocket_buffer: bytearray,
    pocket_offset: int,
    pocket_size: int,
    internal_id: int,
    unique: bool = False,
) -> bool:
    pocket_addr = client.save_data_address + pocket_offset

    for _ in range(3):
        target_slot = -1
        new_bytes = b""
        old_bytes = b""
        for i in range(pocket_size):
            slot_offset = i * 4
            slot_bytes = bytes(pocket_buffer[slot_offset:slot_offset + 4])
            slot_id = int.from_bytes(slot_bytes[:2], "little")
            slot_qty = int.from_bytes(slot_bytes[2:], "little")

            if slot_id == internal_id:
                if unique:
                    return True
                new_qty = min(slot_qty + 1, 999)
                new_bytes = internal_id.to_bytes(2, "little") + new_qty.to_bytes(2, "little")
                old_bytes = slot_bytes
                target_slot = slot_offset
                break
            elif slot_id == 0 and target_slot == -1:
                new_bytes = internal_id.to_bytes(2, "little") + (1).to_bytes(2, "little")
                old_bytes = slot_bytes
                target_slot = slot_offset
                break

        if target_slot == -1:
            client.logger.warning(f"Bag pocket at +0x{pocket_offset:X} is full! Could not insert item ID {internal_id}.")
            return False

        if await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(pocket_addr + target_slot, new_bytes, client.ram_Segment)],
            [(pocket_addr + target_slot, old_bytes, client.ram_Segment)],
        ):
            pocket_buffer[target_slot:target_slot + 4] = new_bytes
            return True

        fresh = await bizhawk.read(
            ctx.bizhawk_ctx,
            [(pocket_addr, pocket_size * 4, client.ram_Segment)],
        )
        pocket_buffer[:] = fresh[0]

    return False


async def ensure_infinite_rare_candies(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    if client.save_data_address == 0 or getattr(client, "is_battle", False):
        return

    try:
        med_pocket_addr = client.save_data_address + client.medicine_bag_offset
        RARE_CANDY_ID = 0x0032
        TARGET_QTY = 999

        cached_slot = getattr(client, "_candies_slot_offset", -1)
        if cached_slot != -1:
            fast_res = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(med_pocket_addr + cached_slot, 4, client.ram_Segment)],
            )
            if fast_res and len(fast_res[0]) >= 4:
                item_id = int.from_bytes(fast_res[0][:2], "little")
                qty = int.from_bytes(fast_res[0][2:], "little")
                if item_id == RARE_CANDY_ID:
                    if qty < TARGET_QTY:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(med_pocket_addr + cached_slot + 2, TARGET_QTY.to_bytes(2, "little"), client.ram_Segment)],
                        )
                    return

        read_res = await bizhawk.read(
            ctx.bizhawk_ctx,
            [(med_pocket_addr, client.medicine_bag_size * 4, client.ram_Segment)],
        )
        if not read_res or not read_res[0]:
            return
        med_bytes = bytearray(read_res[0])

        found = False
        empty_slot = -1
        for i in range(client.medicine_bag_size):
            offset = i * 4
            item_id = int.from_bytes(med_bytes[offset:offset + 2], "little")
            qty = int.from_bytes(med_bytes[offset + 2:offset + 4], "little")
            if item_id == RARE_CANDY_ID:
                found = True
                client._candies_slot_offset = offset
                if qty < TARGET_QTY:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(med_pocket_addr + offset + 2, TARGET_QTY.to_bytes(2, "little"), client.ram_Segment)],
                    )
                break
            elif item_id == 0 and empty_slot == -1:
                empty_slot = offset

        if not found and empty_slot != -1:
            entry = RARE_CANDY_ID.to_bytes(2, "little") + TARGET_QTY.to_bytes(2, "little")
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(med_pocket_addr + empty_slot, entry, client.ram_Segment)],
            )
            client._candies_slot_offset = empty_slot
    except Exception:
        pass


async def ensure_infinite_repels(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    if client.save_data_address == 0 or getattr(client, "is_battle", False):
        return

    try:
        items_pocket_addr = client.save_data_address + client.main_items_bag_offset
        MAX_REPEL_ID = 0x004D
        TARGET_QTY = 999

        cached_slot = getattr(client, "_repels_slot_offset", -1)
        if cached_slot != -1:
            fast_res = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(items_pocket_addr + cached_slot, 4, client.ram_Segment)],
            )
            if fast_res and len(fast_res[0]) >= 4:
                item_id = int.from_bytes(fast_res[0][:2], "little")
                qty = int.from_bytes(fast_res[0][2:], "little")
                if item_id == MAX_REPEL_ID:
                    if qty < TARGET_QTY:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(items_pocket_addr + cached_slot + 2, TARGET_QTY.to_bytes(2, "little"), client.ram_Segment)],
                        )
                    return

        read_res = await bizhawk.read(
            ctx.bizhawk_ctx,
            [(items_pocket_addr, client.main_items_bag_size * 4, client.ram_Segment)],
        )
        if not read_res or not read_res[0]:
            return
        bag_bytes = bytearray(read_res[0])

        found = False
        empty_slot = -1
        for i in range(client.main_items_bag_size):
            offset = i * 4
            item_id = int.from_bytes(bag_bytes[offset:offset + 2], "little")
            qty = int.from_bytes(bag_bytes[offset + 2:offset + 4], "little")
            if item_id == MAX_REPEL_ID:
                found = True
                client._repels_slot_offset = offset
                if qty < TARGET_QTY:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(items_pocket_addr + offset + 2, TARGET_QTY.to_bytes(2, "little"), client.ram_Segment)],
                    )
                break
            elif item_id == 0 and empty_slot == -1:
                empty_slot = offset

        if not found and empty_slot != -1:
            entry = MAX_REPEL_ID.to_bytes(2, "little") + TARGET_QTY.to_bytes(2, "little")
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(items_pocket_addr + empty_slot, entry, client.ram_Segment)],
            )
            client._repels_slot_offset = empty_slot
    except Exception:
        pass


async def reload_key_items(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    # Re-adds any received key items, TMs/HMs, or badges if the player reset without saving
    received_count = await client.read_var(ctx, RECEIVED_ITEMS_VAR)
    if received_count == 0xFFFF or received_count == 0:
        return
    buffers = await _ensure_bag_buffers(client, ctx)
    for i in range(min(received_count, len(ctx.items_received))):
        net_item = ctx.items_received[i]
        item_name = AP_ID_TO_NAME.get(net_item.item)
        if item_name is None or item_name not in ITEM_TABLE:
            continue
        info = ITEM_TABLE[item_name]
        if info.pocket == "badge":
            await write_badge(client, ctx, info.internal_id)
        elif info.pocket == "special":
            if 400101 <= info.ap_id <= 400104:
                await client.write_set_flag(ctx, 3040)
                await client.write_set_flag(ctx, 3041 + info.internal_id)
            elif 400120 <= info.ap_id <= 400126:
                await client.write_set_flag(ctx, 3045 + info.internal_id)
        elif info.pocket == "key_items":
            await write_to_bag(
                client, ctx, buffers[1],
                client.key_items_bag_offset, client.key_items_bag_size,
                info.internal_id, unique=True,
            )
        elif info.pocket == "tm_hm":
            await write_to_bag(
                client, ctx, buffers[2],
                client.tm_hm_bag_offset, client.tm_hm_bag_size,
                info.internal_id, unique=True,
            )
