import time
from typing import TYPE_CHECKING, Dict, Any
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object


class PokemonB2W2Client(BizHawkClient):
    game = "Pokemon Black 2 and White 2"
    system = "NDS"
    patch_suffix = (".apb2w2", ".apb2", ".apw2")

    ram_Segment = "Main RAM"
    header_address = 0x3FFA80  # DSi-enhanced header copy in main RAM
    pointer_address = 0x000024  # Fallback pointer slot

    # All offsets below are relative to save_data_address:
    # - Block 25 (save_block_bag):               raw + 0x18400 (BagSave size = 0x9ec)
    #   - Main items:                            raw + 0x18400 (310 slots * 4 bytes = 1240 bytes)
    #   - Key items:                             raw + 0x188d8 (83 slots * 4 bytes = 332 bytes)
    #   - TM & HM:                               raw + 0x18a24 (109 slots * 4 bytes = 436 bytes)
    #   - Medicine:                              raw + 0x18bd8 (48 slots * 4 bytes = 192 bytes)
    #   - Berries:                               raw + 0x18c98 (64 slots * 4 bytes = 256 bytes)
    # - Block 26 (save_block_party):             raw + 0x18e00
    # - Block 27 (save_block_trainer_data):      raw + 0x19400
    # - Block 28 (save_block_player):            raw + 0x19500 (location.zoneid at +0x80 -> 0x19580)
    # - Block 45 (save_block_event_work / vars): raw + 0x1ff00 (431 u16 variables = 862 bytes)
    # - Block 45 (event flags):                  raw + 0x2025e (3088 bit flags = 386 bytes)
    # - Block 52 (save_block_trainer_game_info): raw + 0x21100 (badges at +0x04 -> 0x21104)
    # - Block 54 (save_block_pokedex):           raw + 0x21400 (caught at +0x08 -> 0x21408)
    # - Block 66 (save_block_misc / rivaldata):  raw + 0x23b00 (rivalname at +0xa4 -> 0x23ba4)

    main_items_bag_offset = 0x18400
    key_items_bag_offset = 0x188D8
    tm_hm_bag_offset = 0x18A24
    medicine_bag_offset = 0x18BD8
    berry_bag_offset = 0x18C98

    main_items_bag_size = 310
    key_items_bag_size = 83
    tm_hm_bag_size = 109
    medicine_bag_size = 48
    berry_bag_size = 64

    party_offset = 0x18E00
    trainer_data_offset = 0x19400
    player_save_offset = 0x19500
    map_id_offset = 0x19580
    var_offset = 0x1FF00
    flags_offset = 0x2025E
    badges_offset = 0x21104
    dex_offset = 0x21400

    flags_amount = 3088  # 386 Bytes (0x182) in block 45

    data_address_confirmed = False
    save_data_address = 0
    current_map = -1
    goal_checked = False
    flags_cache: bytearray
    vars_cache: bytearray
    missing_flags: list[int]
    flags_buffer: list[int] | None = None
    bag_buffers: list[bytearray] | None = None
    dex_caught_buffer: bytes | None = None

    logger = logging.getLogger("Client")

    def __init__(self):
        super().__init__()
        self.flags_cache = bytearray(self.flags_amount // 8)
        self.vars_cache = bytearray(0x240)
        self.missing_flags = []
        self._cleared_legendaries: set[str] = set()
        self.flags_buffer = None
        self.bag_buffers = None
        self.dex_caught_buffer = None
        self.data_address_confirmed = False
        self.save_data_address = 0
        self.ctrl_inner_address = 0
        self.bag_valid = False
        self.is_field = False
        self.is_battle = False
        self.game_version = -1
        self.ctrl_ptr_address = 0
        self._scan_attempts = 0
        self.current_map = -1
        self.local_seen_pokemon = None
        self.local_caught_pokemon = None
        self.local_tracked_events = None

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        import asyncio
        from CommonClient import logger

        header = b""
        for _ in range(10):
            try:
                rom_info = await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [
                        (0x3FFA80, 0xC0, self.ram_Segment),
                        (0x3FFDE0, 0xC0, self.ram_Segment),
                    ]
                )
                if rom_info and rom_info[0][:10] in (b"POKEMON B2", b"POKEMON W2"):
                    header = rom_info[0]
                    break
                elif rom_info and len(rom_info) > 1 and rom_info[1][:10] in (b"POKEMON B2", b"POKEMON W2"):
                    header = rom_info[1]
                    break
            except Exception:
                pass

            await asyncio.sleep(0.5)

        game_title = header[:12].decode("ascii", errors="ignore").strip("\x00")
        game_code = header[12:16].decode("ascii", errors="ignore")

        if game_title not in ("POKEMON B2", "POKEMON W2"):
            return False
        if game_code not in ("IREO", "IRDO"):
            logger.warning(f"Loaded ROM has game code {game_code}. Only English/European (IREO/IRDO) ROMs are supported.")
            return False

        if game_code == "IREO":
            self.game_version = 0  # Black 2
            self.ctrl_ptr_address = 0x140F60
        else:
            self.game_version = 1  # White 2
            self.ctrl_ptr_address = 0x140FA0

        parts = [p for p in header[0xA0:0xC0].split(b"\x00") if p]
        self.player_name = parts[0].decode("utf-8", errors="ignore").strip() if parts else ""
        self.rom_seed_name = parts[1].decode("utf-8", errors="ignore").strip() if len(parts) > 1 else None
        if self.rom_seed_name:
            self.rom_seed_name = self.rom_seed_name.replace("\x00", "").strip()

        if ctx.seed_name and self.rom_seed_name:
            if not ctx.seed_name.startswith(self.rom_seed_name):
                msg = f"ERROR: Loaded ROM seed '{self.rom_seed_name}' does not match server seed '{ctx.seed_name}'! Please load the correct ROM in BizHawk."
                logger.error(msg)
                ctx.gui_error("Wrong ROM loaded", msg)
                return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1

        from .client.setup import early_setup
        early_setup(self)

        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        if getattr(self, "player_name", None):
            ctx.auth = self.player_name

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot_data is None:
            if self.save_data_address != 0:
                from .client.setup import early_return
                early_return(self)
            try:
                await bizhawk.ping(ctx.bizhawk_ctx)
            except Exception:
                pass
            return

        from .client.setup import (
            check_save_address, check_Dynamic_addresses, late_setup,
        )
        from .client.locations import check_flag_locations, check_goal
        from .client.items import receive_items, ensure_infinite_rare_candies, ensure_infinite_repels
        from .client.tracker import sync_datastorage

        try:
            if not await check_save_address(self, ctx):
                return
            if not await check_Dynamic_addresses(self, ctx):
                return

            if not self.data_address_confirmed:
                await late_setup(self, ctx)

            await check_flag_locations(self, ctx)
            if getattr(self, "bag_valid", False) and not getattr(self, "is_battle", False) and getattr(self, "is_field", False):
                await receive_items(self, ctx)
            await check_goal(self, ctx)
            await sync_datastorage(self, ctx)

            opts = ctx.slot_data.get("options", {})
            want_candies = bool(ctx.slot_data.get("infinite_rare_candies", opts.get("infinite_rare_candies", 0)))
            want_repels = bool(ctx.slot_data.get("infinite_repels", opts.get("infinite_repels", 0)))

            if not getattr(self, "is_battle", False) and getattr(self, "bag_valid", False) and (want_candies or want_repels):
                now = time.time()
                if getattr(self, "_last_bag_check", 0.0) + 10.0 < now:
                    self._last_bag_check = now
                    if want_candies:
                        await ensure_infinite_rare_candies(self, ctx)
                    if want_repels:
                        await ensure_infinite_repels(self, ctx)

        except (bizhawk.RequestFailedError, bizhawk.ConnectorError, TimeoutError, Exception):
            pass

    async def ensure_infinite_rare_candies(self, ctx: BizHawkClientContext) -> None:
        from .client.items import ensure_infinite_rare_candies
        await ensure_infinite_rare_candies(self, ctx)

    async def ensure_infinite_repels(self, ctx: BizHawkClientContext) -> None:
        from .client.items import ensure_infinite_repels
        await ensure_infinite_repels(self, ctx)

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args.get("seed_name", "")
            if self.rom_seed_name and not ctx.seed_name.startswith(self.rom_seed_name):
                msg = f"ERROR: Loaded ROM seed '{self.rom_seed_name}' does not match server seed '{ctx.seed_name}'! Please load the correct ROM in BizHawk."
                self.logger.error(msg)
                ctx.gui_error("Wrong ROM loaded", msg)
                import asyncio
                asyncio.create_task(ctx.disconnect(allow_autoreconnect=False))
                return
        elif cmd == "Connected":
            self._cleared_legendaries = set()
            self._cleared_legendaries_loaded = False
            self._synced_cleared_legendaries = set()
            if getattr(ctx, "slot", None) is not None and getattr(ctx, "team", None) is not None:
                import asyncio
                key = f"pokemon_b2w2_cleared_legendaries_{ctx.team}_{ctx.slot}"
                asyncio.create_task(ctx.send_msgs([{"cmd": "Get", "keys": [key]}]))
        elif cmd == "Retrieved":
            if getattr(ctx, "slot", None) is not None and getattr(ctx, "team", None) is not None:
                key = f"pokemon_b2w2_cleared_legendaries_{ctx.team}_{ctx.slot}"
                keys = args.get("keys", {})
                if key in keys:
                    val = keys[key]
                    if not hasattr(self, "_cleared_legendaries") or self._cleared_legendaries is None:
                        self._cleared_legendaries = set()
                    if isinstance(val, list):
                        server_set = {str(x) for x in val}
                        self._cleared_legendaries.update(server_set)
                        self._synced_cleared_legendaries = server_set
                    else:
                        self._synced_cleared_legendaries = set()
                    self._cleared_legendaries_loaded = True
        elif cmd == "Bounced":
            pass

    async def read_var(self, ctx: BizHawkClientContext, var_id: int) -> int:
        # Reads 16-bit script variable 0x4000 + var_id (var_id is 0..430)
        index = var_id - 0x4000 if var_id >= 0x4000 else var_id
        data = await bizhawk.read(
            ctx.bizhawk_ctx,
            [(self.save_data_address + self.var_offset + (2 * index), 2, self.ram_Segment)]
        )
        return int.from_bytes(data[0], "little")

    async def write_var(self, ctx: BizHawkClientContext, var_id: int, value: int) -> None:
        # Writes 16-bit script variable 0x4000 + var_id (var_id is 0..430)
        index = var_id - 0x4000 if var_id >= 0x4000 else var_id
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(self.save_data_address + self.var_offset + (2 * index), value.to_bytes(2, "little"), self.ram_Segment)]
        )

    async def write_set_flag(self, ctx: BizHawkClientContext, flag_id: int) -> None:
        byte_offset = flag_id // 8
        bit_mask = 1 << (flag_id % 8)
        for _ in range(3):
            if await bizhawk.guarded_write(
                ctx.bizhawk_ctx,
                [(
                    self.save_data_address + self.flags_offset + byte_offset,
                    (self.flags_cache[byte_offset] | bit_mask).to_bytes(1, "little"),
                    self.ram_Segment
                )],
                [(
                    self.save_data_address + self.flags_offset + byte_offset,
                    self.flags_cache[byte_offset].to_bytes(1, "little"),
                    self.ram_Segment
                )]
            ):
                break
            byte = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(self.save_data_address + self.flags_offset + byte_offset, 1, self.ram_Segment)]
            )
            self.flags_cache[byte_offset] = byte[0][0]
        self.flags_cache[byte_offset] |= bit_mask

    async def write_unset_flag(self, ctx: BizHawkClientContext, flag_id: int) -> None:
        byte_offset = flag_id // 8
        bit_mask = 255 - (1 << (flag_id % 8))
        for _ in range(3):
            if await bizhawk.guarded_write(
                ctx.bizhawk_ctx,
                [(
                    self.save_data_address + self.flags_offset + byte_offset,
                    (self.flags_cache[byte_offset] & bit_mask).to_bytes(1, "little"),
                    self.ram_Segment
                )],
                [(
                    self.save_data_address + self.flags_offset + byte_offset,
                    self.flags_cache[byte_offset].to_bytes(1, "little"),
                    self.ram_Segment
                )]
            ):
                break
            byte = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(self.save_data_address + self.flags_offset + byte_offset, 1, self.ram_Segment)]
            )
            self.flags_cache[byte_offset] = byte[0][0]
        self.flags_cache[byte_offset] &= bit_mask

    def flag_cached(self, flag_id: int) -> bool:
        byte_idx = flag_id // 8
        if 0 <= byte_idx < len(self.flags_cache):
            return (self.flags_cache[byte_idx] & (1 << (flag_id % 8))) != 0
        return False

    def get_flag(self, flag_id: int) -> bool:
        return self.flag_cached(flag_id)

    def get_var(self, var_id: int) -> int:
        # Cached 16-bit script variable 0x4000 + index (0 if uncached)
        index = var_id - 0x4000 if var_id >= 0x4000 else var_id
        byte_idx = index * 2
        cache = getattr(self, "vars_cache", b"")
        if 0 <= byte_idx and byte_idx + 2 <= len(cache):
            return int.from_bytes(cache[byte_idx : byte_idx + 2], "little")
        return 0


def register_client() -> None:
    from worlds._bizhawk.client import BizHawkClient
    _ = PokemonB2W2Client
