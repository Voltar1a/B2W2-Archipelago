from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus

from ..locations import LOCATION_ID_TO_INFO

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonB2W2Client
    from worlds._bizhawk.context import BizHawkClientContext


async def check_flag_locations(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    from .setup import early_return

    flags_block_size = 386
    vars_block_size = 0x35E
    base = client.save_data_address

    reads = [
        (base + client.flags_offset, flags_block_size, client.ram_Segment),
        (base + client.badges_offset, 1, client.ram_Segment),
        (base + client.var_offset, vars_block_size, client.ram_Segment),
    ]

    is_battle = getattr(client, "is_battle", False)
    if not is_battle:
        reads.append((base + client.map_id_offset, 2, client.ram_Segment))

    import time
    now = time.time()
    should_read_dex = False
    if not is_battle and getattr(client, "_last_dex_read", 0.0) + 60.0 < now:
        reads.append((base + client.dex_offset + 0x08, 420, client.ram_Segment))
        should_read_dex = True

    read_result = await bizhawk.read(ctx.bizhawk_ctx, reads)
    flag_bytes = read_result[0]
    badges_byte = read_result[1][0]
    var_bytes = read_result[2]

    result_idx = 3
    if not is_battle:
        client._latest_map_bytes = read_result[result_idx]
        result_idx += 1
    if should_read_dex:
        client.dex_caught_buffer = read_result[result_idx]
        client._last_dex_read = now

    flag_bits = sum(b.bit_count() for b in flag_bytes)
    if flag_bits >= 2500 or flag_bits == 0:
        early_return(client)
        return

    client.vars_cache = bytearray(var_bytes)

    has_scanned = getattr(client, "_has_initial_scanned", False)
    prev_buffer = client.flags_buffer
    if has_scanned and prev_buffer is not None and bytes(prev_buffer) == flag_bytes and getattr(client, "_last_badges_byte", -1) == badges_byte:
        return

    client.flags_cache = bytearray(flag_bytes)
    client.flags_buffer = list(flag_bytes)
    client._last_badges_byte = badges_byte
    client._has_initial_scanned = True

    newly_checked: list[int] = []
    for loc_id in ctx.missing_locations:
        info = LOCATION_ID_TO_INFO.get(loc_id)
        if info is None:
            continue

        if info.flag_id is not None and any(client.flag_cached(f) for f in (info.flag_id, *info.alt_flags)):
            newly_checked.append(loc_id)

    if newly_checked:
        await ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": newly_checked,
        }])


async def check_goal(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    if client.goal_checked:
        return

    from .goals import get_method
    goal_fn = get_method(client, ctx)
    is_completed = await goal_fn(client, ctx)
    if is_completed:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": ClientStatus.CLIENT_GOAL,
        }])
        client.goal_checked = True
