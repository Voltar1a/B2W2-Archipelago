import time
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

from ..locations import ALL_LOCATION_TABLE

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonB2W2Client
    from worlds._bizhawk.context import BizHawkClientContext


SAVE_SIZE_MAGIC = b"\xA4\x5F\x02\x00"
B2W2_SAVE_SIZE = 0x00025FA4


def early_return(client: "PokemonB2W2Client") -> bool:
    client.save_data_address = 0
    client.ctrl_inner_address = 0
    client.data_address_confirmed = False
    client.bag_valid = False
    client.is_field = False
    client.is_battle = False
    client._cached_received_count = -1
    client.flags_buffer = None
    client.vars_cache = bytearray(0x35E)
    client.bag_buffers = None
    client.dex_caught_buffer = None
    client.local_seen_pokemon = []
    client.local_caught_pokemon = []
    client.local_tracked_events = -1
    client._has_initial_scanned = False
    return False


def early_setup(client: "PokemonB2W2Client") -> None:
    if not hasattr(client, "_cleared_legendaries"):
        client._cleared_legendaries = set()
        client._cleared_legendaries_loaded = False
        client._synced_cleared_legendaries = set()
    client.flags_cache = bytearray(386)
    client.missing_flags = [
        loc.flag_id for loc in ALL_LOCATION_TABLE.values()
        if loc.flag_id is not None
    ]
    early_return(client)
    client._scan_attempts = 0
    client.current_map = -1
    client.local_seen_pokemon = None
    client.local_caught_pokemon = None
    client.local_tracked_events = None


async def _verify_save_address(
    client: "PokemonB2W2Client",
    ctx: "BizHawkClientContext",
    raw_save_addr: int,
    ctrl_inner: int = 0,
) -> bool:
    try:
        read_bytes = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (raw_save_addr + 0x1FF00, 862, client.ram_Segment),
                (raw_save_addr + 0x2025E, 386, client.ram_Segment),
            ],
        )
        var_bytes = read_bytes[0]
        flag_bytes = read_bytes[1]

        bits_flags = sum(b.bit_count() for b in flag_bytes)
        bits_vars = sum(b.bit_count() for b in var_bytes)

        if 0 < bits_flags < 2500 and 0 <= bits_vars < 5000:
            client.ctrl_inner_address = ctrl_inner or (raw_save_addr - 0x30)
            client.save_data_address = raw_save_addr
            client._cached_save_addr = raw_save_addr

            client.flags_offset = 0x2025E
            client.var_offset = 0x1FF00
            client.badges_offset = 0x21104
            client.dex_offset = 0x21400
            client.party_offset = 0x18E00
            client.trainer_data_offset = 0x19400
            client.player_save_offset = 0x19500
            client.map_id_offset = 0x19580

            client.main_items_bag_offset = 0x18400
            client.key_items_bag_offset = 0x188D8
            client.tm_hm_bag_offset = 0x18A24
            client.medicine_bag_offset = 0x18BD8
            client.berry_bag_offset = 0x18C98

            client.bag_valid = True

            return True
    except Exception:
        pass
    return False


OV36_MAGIC = b"\xf8\xb5\x0d\x1c\x06\x1c\x28\x68"
OV167_MAGIC = b"\xf8\xb5\x82\xb0\x0f\x1c\x05\x1c"


async def check_ingame_state(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    # Verifies that the player is actively ingame
    try:
        reads = [
            (0x17F600, 8, client.ram_Segment),
            (0x17F640, 8, client.ram_Segment),
            (0x1998C0, 8, client.ram_Segment),
            (0x199900, 8, client.ram_Segment),
        ]

        read_bytes = await bizhawk.read(ctx.bizhawk_ctx, reads)
        if not read_bytes or len(read_bytes) < 4:
            return False

        is_field = (read_bytes[0] == OV36_MAGIC or read_bytes[1] == OV36_MAGIC)
        is_battle = (read_bytes[2] == OV167_MAGIC or read_bytes[3] == OV167_MAGIC)

        client.is_field = is_field
        client.is_battle = is_battle

        if not (is_field or is_battle):
            return False

        return True
    except Exception:
        return False


async def check_save_address(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    # Finds and verifies save_data_address in main RAM only when actively ingame
    if not await check_ingame_state(client, ctx):
        return False

    if client.save_data_address != 0:
        return True

    now = time.time()
    if getattr(client, "_last_scan_time", 0.0) + 2.0 > now:
        return False
    client._last_scan_time = now

    ctrl_addrs = [client.ctrl_ptr_address] if getattr(client, "ctrl_ptr_address", 0) else [0x140F60, 0x140FA0]
    for ctrl_addr in ctrl_addrs:
        if not ctrl_addr:
            continue
        try:
            ctrl_res = await bizhawk.read(ctx.bizhawk_ctx, [(ctrl_addr, 4, client.ram_Segment)])
            ctrl_ptr = int.from_bytes(ctrl_res[0], "little")
            if not (0x02000000 <= ctrl_ptr < 0x02400000):
                continue

            sv_res = await bizhawk.read(ctx.bizhawk_ctx, [((ctrl_ptr & 0xFFFFFF) + 0x10, 4, client.ram_Segment)])
            sv_ptr = int.from_bytes(sv_res[0], "little")
            if not (0x02000000 <= sv_ptr < 0x02400000):
                continue

            data_res = await bizhawk.read(
                ctx.bizhawk_ctx,
                [((sv_ptr & 0xFFFFFF) + 0x34, 4, client.ram_Segment)],
            )
            data_ptr = int.from_bytes(data_res[0], "little")

            if not (0x02000000 <= data_ptr < 0x02400000):
                continue

            if await _verify_save_address(client, ctx, data_ptr & 0xFFFFFF, sv_ptr & 0xFFFFFF):
                return True
        except Exception:
            pass

    cached = getattr(client, "_cached_save_addr", 0)
    if cached and 0x02000000 <= (cached | 0x02000000) < 0x02400000:
        if await _verify_save_address(client, ctx, cached):
            return True

    return False


async def check_Dynamic_addresses(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    return client.ctrl_inner_address != 0 and client.save_data_address != 0


async def late_setup(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> None:
    from .items import reload_key_items

    read_result = await bizhawk.read(
        ctx.bizhawk_ctx,
        [(client.save_data_address + client.flags_offset, client.flags_amount // 8, client.ram_Segment)]
    )
    client.flags_cache = bytearray(read_result[0])
    client.flags_buffer = list(read_result[0])

    await reload_key_items(client, ctx)
    client.data_address_confirmed = True
