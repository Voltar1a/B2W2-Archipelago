from __future__ import annotations

import os
import struct
from zipfile import ZipFile
from typing import TYPE_CHECKING, Any, Dict

try:
    import orjson
except ImportError:
    import json as orjson
try:
    import NetUtils
except ImportError:
    NetUtils = None
try:
    import Utils
except ImportError:
    Utils = None
try:
    from settings import get_settings
except ImportError:
    get_settings = None
try:
    from worlds.Files import APAutoPatchInterface
except ImportError:
    APAutoPatchInterface = object

if TYPE_CHECKING:
    from . import PokemonB2W2World
    from .nds_compat import NintendoDSRom


class PokemonB2W2Patch(APAutoPatchInterface):
    game = "Pokemon Black 2 and White 2"
    patch_file_ending = ".apb2w2"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None, server: str = ""):
        self.world = world
        self.player_name = player_name
        self.player = player
        self.files: dict[str, bytes] = {}
        self.path = path
        self.server = server
        if APAutoPatchInterface is not object:
            super().__init__(path, player, player_name, server)
        if os.path.isfile(path) and not world:
            try:
                self.read()
            except Exception:
                pass
        if os.path.isfile(path) and not world:
            try:
                self.read()
            except Exception:
                pass

    def write_contents(self, opened_zipfile: ZipFile) -> None:
        super().write_contents(opened_zipfile)
        if self.world:
            slot_data = NetUtils.convert_to_base_types(self.world.fill_slot_data())
            if getattr(self, "server", None):
                slot_data["server"] = self.server
            opened_zipfile.writestr(
                "slot_data.json",
                orjson.dumps(slot_data)
            )
            opened_zipfile.writestr(
                "seed_name.txt",
                self.world.multiworld.seed_name.encode("utf-8")
            )

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest["b2w2_patch_version"] = 1
        if getattr(self, "server", None):
            manifest["server"] = self.server
        return manifest

    def read(self) -> None:
        if APAutoPatchInterface is not object and hasattr(super(), "read"):
            super().read()
            return
        with ZipFile(self.path, "r") as z:
            self.read_contents(z)

    def read_contents(self, opened_zipfile: ZipFile) -> Dict[str, Any]:
        manifest = super().read_contents(opened_zipfile) if APAutoPatchInterface is not object and hasattr(super(), "read_contents") else {}
        if not manifest and "archipelago.json" in opened_zipfile.namelist():
            try:
                manifest = orjson.loads(opened_zipfile.read("archipelago.json"))
            except Exception:
                pass
        for name in opened_zipfile.namelist():
            if name != "archipelago.json":
                self.files[name] = opened_zipfile.read(name)
        if "seed_name.txt" in self.files:
            self.seed_name = self.files["seed_name.txt"].decode("utf-8", errors="ignore").strip()
        elif hasattr(self, "world") and self.world:
            self.seed_name = self.world.multiworld.seed_name
        else:
            self.seed_name = ""
        if manifest.get("server"):
            self.server = manifest["server"]
        elif "slot_data.json" in self.files:
            try:
                sd = orjson.loads(self.files["slot_data.json"])
                if sd.get("server"):
                    self.server = sd["server"]
            except Exception:
                pass
        return manifest

    def get_file(self, file_name: str) -> bytes:
        if file_name not in self.files:
            self.read()
        return self.files[file_name]

    def patch(self, target: str) -> None:
        self.read()
        try:
            from .nds_compat import NintendoDSRom
        except (ImportError, ValueError):
            from nds_compat import NintendoDSRom

        version = "black2"
        slot_data: dict[str, Any] = {}
        options: dict[str, Any] = {}
        if "slot_data.json" in self.files:
            try:
                slot_data = orjson.loads(self.files["slot_data.json"])
                options = slot_data.get("options", {})
                version = options.get("version", "black2")
            except Exception:
                pass
        options["slot_data"] = slot_data

        base_rom_path = get_base_rom_path(version)
        with open(base_rom_path, "rb") as f:
            base_data = f.read()

        rom = NintendoDSRom(base_data)
        is_white2 = (b"IRDO" in rom.name or rom.name[8:10] == b"W2" or rom.idCode[:4] == b"IRDO")

        if options.get("skip_intro", True):
            try:
                from .nds_compat import saveOverlayTable
            except (ImportError, ValueError):
                from nds_compat import saveOverlayTable
            ov_table = rom.loadArm9Overlays()
            ov162 = ov_table[162]
            ov_data = bytearray(ov162.data)

            addr = (
                (0x021A04D8, 0x0219CEC0, 0x3330)
                if is_white2
                else (0x021A0460, 0x0219CE80, 0x32F8)
            )
            strcopy_addr = 0x020486E4 if is_white2 else 0x020486B8

            custom_name = options.get("trainer_name")
            name = (
                str(custom_name).strip() if custom_name else self.player_name
            )[:7]
            if not name:
                name = "Player"
            gender = options.get("skip_intro_gender", "male")
            if str(gender).casefold() in ("random", "2"):
                import random
                gender = "female" if random.random() < 0.5 else "male"
            rival = (str(options.get("rival_name", "Hugh")).strip() or "Hugh")[:7]

            from_int = lambda num: num.to_bytes(2, byteorder="little")
            output = bytearray()
            output += b"\xe1\x6a"
            output += b"\xa0\x6d"
            output += b"\x09\x6a"
            output += (
                b"\x01\x22"
                if str(gender).casefold() in ("female", "1")
                else b"\x00\x22"
            )
            output += from_int(0x2300 + len(name))
            output += b"\x8b\x70"

            for i in range(len(name)):
                enc = name[i].encode("utf-16-le")
                output += from_int(0x2300 + enc[0])
                output += from_int(0x700B + 0x40 * (i * 2 + 8))
                output += from_int(0x2300 + enc[1])
                output += from_int(0x700B + 0x40 * (i * 2 + 9))

            output += b"\xff\x23"
            output += from_int(0x700B + 0x40 * (len(name) * 2 + 8))
            output += from_int(0x700B + 0x40 * (len(name) * 2 + 9))

            offset = (addr[0] - (addr[1] + addr[2] + len(output) + 4)) & 0x7FFFFF
            output += from_int(
                ((offset >> 12) & 0x07FF) | 0xF000
            ) + from_int(((offset >> 1) & 0x07FF) | 0xF800)

            output += b"\x21\x1c\x64\x31"

            for i in range(len(rival)):
                enc = rival[i].encode("utf-16-le")
                output += from_int(0x2300 + enc[0])
                output += from_int(0x700B + 0x40 * (i * 2))
                output += from_int(0x2300 + enc[1])
                output += from_int(0x700B + 0x40 * (i * 2 + 1))

            output += b"\xff\x23"
            output += from_int(0x700B + 0x40 * (len(rival) * 2))
            output += from_int(0x700B + 0x40 * (len(rival) * 2 + 1))

            output += b"\x01\x20\xf8\xbd"

            ov_data[addr[2] : addr[2] + len(output)] = output
            ov162.data = bytes(ov_data)
            rom.files[ov162.fileID] = ov162.save(compress=ov162.compressed)
            rom.arm9OverlayTable = saveOverlayTable(ov_table)

        try:
            from .patch.faster_story import apply_faster_story
        except (ImportError, ValueError):
            from patch.faster_story import apply_faster_story
        apply_faster_story(rom, is_white2, options)

        try:
            from .patch.story_roadblocks import apply_story_roadblocks
        except (ImportError, ValueError):
            from patch.story_roadblocks import apply_story_roadblocks
        apply_story_roadblocks(rom, is_white2, options)

        import hashlib
        try:
            from .randomise import apply_randomisation
        except (ImportError, ValueError):
            from randomise import apply_randomisation
        p_num = getattr(self, "player", 0) or options.get("player", 0) or 0
        seed_base = getattr(self, "seed_name", "") or str(options.get("seed", 0))
        seed_str = f"{seed_base}_{p_num}" if seed_base else str(p_num)
        seed_int = int.from_bytes(hashlib.sha256(seed_str.encode("utf-8")).digest()[:8], "little")
        apply_randomisation(rom, options, is_white2, seed=seed_int)

        if options.get("living_room_starter", True):
            try:
                from .patch.living_room_starter import apply_living_room_starter
            except (ImportError, ValueError):
                from patch.living_room_starter import apply_living_room_starter
            apply_living_room_starter(rom, options)

        apply_qol_patches(rom, options)

        try:
            from .patch.text import apply_check_text
        except (ImportError, ValueError):
            from patch.text import apply_check_text
        apply_check_text(rom, slot_data)

        try:
            from .patch.scripts import patch_scripts_from_rom
        except (ImportError, ValueError):
            from patch.scripts import patch_scripts_from_rom
        patch_scripts_from_rom(rom, slot_data)

        try:
            from .patch.aptransceiver import apply_aptransceiver
        except (ImportError, ValueError):
            from patch.aptransceiver import apply_aptransceiver
        apply_aptransceiver(rom, options)

        if getattr(rom, "_decompressed_arm9", None) is not None:
            try:
                from .nds_compat import codeCompression
            except (ImportError, ValueError):
                from nds_compat import codeCompression
            old_end_addr = rom.arm9RamAddress + len(rom.arm9)
            arm9_comp = bytearray(codeCompression.compress(bytes(rom._decompressed_arm9), isArm9=True))
            new_end_addr = rom.arm9RamAddress + len(arm9_comp)
            target_bytes = struct.pack("<I", old_end_addr)
            ptr_idx = arm9_comp[:0x4000].find(target_bytes)
            if ptr_idx != -1:
                struct.pack_into("<I", arm9_comp, ptr_idx, new_end_addr)
            elif len(arm9_comp) >= 0xFC8:
                struct.pack_into("<I", arm9_comp, 0xFC4, new_end_addr)
            rom.arm9 = bytes(arm9_comp)

        p_name = getattr(self, "player_name", "") or options.get("trainer_name", "Volt")
        player_name_bytes = p_name.encode("utf-8")[:31]
        seed_bytes = getattr(self, "seed_name", "").encode("utf-8")
        avail_seed = 31 - len(player_name_bytes)
        if avail_seed > 4 and seed_bytes:
            header_name_field = player_name_bytes + b"\0" + seed_bytes[:avail_seed]
        else:
            header_name_field = player_name_bytes

        pad = rom.pad088[:0x15] + b"\x01\x00\x00" + header_name_field
        rom.pad088 = pad + bytes(0x38 - len(pad))

        with open(target, "wb") as f:
            finished = rom.save(updateDeviceCapacity=True)
            k = 1
            while k < len(finished):
                k <<= 1
            f.write(finished + b"\0" * (k - len(finished)))


class PokemonB2Patch(PokemonB2W2Patch):
    game = "Pokemon Black 2 and White 2"
    patch_file_ending = ".apb2"
    result_file_ending = ".nds"


class PokemonW2Patch(PokemonB2W2Patch):
    game = "Pokemon Black 2 and White 2"
    patch_file_ending = ".apw2"
    result_file_ending = ".nds"


def make_bl(from_addr: int, to_addr: int) -> bytes:
    diff = to_addr - (from_addr + 4)
    imm24 = diff >> 1
    h1 = 0xF000 | ((imm24 >> 11) & 0x7FF)
    h2 = 0xF800 | (imm24 & 0x7FF)
    return h1.to_bytes(2, "little") + h2.to_bytes(2, "little")


def apply_qol_patches(rom: "NintendoDSRom", options: dict[str, Any]) -> None:
    # QoL patches to ARM9, overlays 36 & 167, and NARCs based on user options
    try:
        from .nds_compat import codeCompression
        from .nds_compat import saveOverlayTable
        from .nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import codeCompression
        from nds_compat import saveOverlayTable
        from nds_compat import NARC

    battle_style = str(options.get("battle_style", "shift")).casefold()
    battle_scene = str(options.get("battle_scene", "on")).casefold()
    instant_text = bool(options.get("instant_text", False))
    is_white2 = (b"IRDO" in rom.name or rom.name[8:10] == b"W2" or rom.idCode[:4] == b"IRDO")

    arm9 = getattr(rom, "_decompressed_arm9", None)
    if arm9 is None:
        arm9 = bytearray(codeCompression.decompress(rom.arm9))
        rom._decompressed_arm9 = arm9
    ov_chk_pat = b"\xF0\xB5\x97\xB0\x05\x1C\x0E\x1C\x17\x1C\x12\xAA\x00\x21\x14\x22\x1C\x1C"
    ov_chk_idx = arm9.find(ov_chk_pat)
    if ov_chk_idx != -1:
        arm9[ov_chk_idx : ov_chk_idx + 4] = b"\x01\x20\x70\x47"

    if battle_style in ("set", "1") or battle_scene in ("off", "turned_off", "1") or instant_text:
        is_white2 = (b"IRDO" in rom.name or rom.name[8:10] == b"W2" or rom.idCode[:4] == b"IRDO")
        if instant_text:
            if is_white2:
                arm9[0x1E57A:0x1E580] = b"\xff\x24\x00\xe0\xff\x24"
                arm9[0x1E644:0x1E646] = b"\x00\x20"
            else:
                arm9[0x1E54E:0x1E554] = b"\xff\x24\x00\xe0\xff\x24"
                arm9[0x1E618:0x1E61A] = b"\x00\x20"

            a002_data = rom.getFileByName("a/0/0/2")
            if a002_data is not None:
                a002 = NARC(a002_data)
                try:
                    from .patch.text import decode, encode
                except (ImportError, ValueError):
                    from patch.text import decode, encode
                texts = decode(a002.files[19])
                modified = False
                for idx in (7, 8, 9, 10, 54):
                    if idx < len(texts[0]) and "[End]" in texts[0][idx].line:
                        texts[0][idx].line = texts[0][idx].line.replace("[End]", "")
                        modified = True
                if modified:
                    a002.files[19] = encode(texts)
                    rom.setFileByName("a/0/0/2", a002.save())

        cfg_pat = b"\x0F\x20\x81\x43\x01\x20"
        cfg_idx = arm9.find(cfg_pat)
        if cfg_idx != -1:
            if instant_text:
                arm9[cfg_idx + 4] = 0x02  # Default to fast text speed in config_init
            if battle_style in ("set", "1") and arm9[cfg_idx + 0x16 : cfg_idx + 0x18] == b"\x40\x21":
                arm9[cfg_idx + 0x18] = 0x0A  # Set mode bit
            if battle_scene in ("off", "turned_off", "1") and arm9[cfg_idx + 0x1E : cfg_idx + 0x20] == b"\x80\x21":
                arm9[cfg_idx + 0x20] = 0x0A  # Battle scene off bit

    hold_a_turbo_enabled = bool(options.get("hold_a_turbo", False))
    auto_run_enabled = bool(options.get("auto_run", False))
    guaranteed_escape_enabled = bool(options.get("guaranteed_escape", False))
    fast_fishing_enabled = bool(options.get("fast_fishing", True))
    bike_everywhere_enabled = bool(options.get("bike_everywhere", True))

    arm9_base = rom.arm9RamAddress
    delta = 0x2C if is_white2 else 0
    get_repeat_addr = 0x0203DEFC + delta
    freespot_pat = b"\xf8\x43\x2d\xe9\x00\x60\xa0\xe1\xba\x30\xd6\xe1\x01\x50\xa0\xe1\x02\x40\xa0\xe1\x20\x00\x53\xe3"
    freespot_idx = arm9.find(freespot_pat)
    dwc_base = (arm9_base + freespot_idx) if freespot_idx != -1 else (0x02059178 if is_white2 else 0x0205914C)

    # IsQoLEnabled(R0=work_sub_off, R1=default_on) helper at dwc_base + 0x00 (0x34 bytes)
    helper_addr = dwc_base
    helper_code = bytearray()
    helper_code += b"\x30\xb5\x04\x1c\x0d\x1c"
    helper_code += make_bl(helper_addr + 0x06, 0x020072FC)
    helper_code += b"\x00\x28\x0c\xd0\x2d\x21"
    helper_code += make_bl(helper_addr + 0x10, 0x02017A5C)
    helper_code += b"\x00\x28\x07\xd0"
    helper_code += b"\x03\x21\x09\x02\x09\x19\x40\x5a"
    helper_code += b"\x01\x28\x03\xd0\x02\x28\x03\xd0"
    helper_code += b"\x28\x1c\x30\xbd\x01\x20\x30\xbd\x00\x20\x30\xbd"
    assert len(helper_code) == 0x34

    # BikeHook(R0=zone_header_ptr) at dwc_base + 0x34 (0x20 bytes)
    bike_hook_addr = dwc_base + 0x34
    bike_code = bytearray()
    bike_code += b"\x10\xb5\xc4\x8b\x64\x05\xe4\x0f"
    bike_code += b"\x54\x20" + (b"\x01\x21" if bike_everywhere_enabled else b"\x00\x21")
    bike_code += make_bl(bike_hook_addr + 0x0C, helper_addr)
    bike_code += b"\x00\x28\x01\xd0\x01\x20\x10\xbd\x20\x1c\x10\xbd\xc0\x46\xc0\x46"
    assert len(bike_code) == 0x20

    # AutoRunGridHook() at dwc_base + 0x54 (0x20 bytes)
    autorun_grid_addr = dwc_base + 0x54
    autorun_grid_code = bytearray()
    autorun_grid_code += b"\x0d\xb5\x4e\x20" + (b"\x01\x21" if auto_run_enabled else b"\x00\x21")
    autorun_grid_code += make_bl(autorun_grid_addr + 0x06, helper_addr)
    autorun_grid_code += b"\x01\x9a\x02\x21\x0a\x40\x52\x08\x50\x40\x00\x28\x02\xd1\x03\x98\x0c\x30\x03\x90\x0d\xbd"
    assert len(autorun_grid_code) == 0x20

    # AutoRunRailHook() at dwc_base + 0x74 (0x20 bytes)
    autorun_rail_addr = dwc_base + 0x74
    autorun_rail_code = bytearray()
    autorun_rail_code += b"\x0d\xb5\x4e\x20" + (b"\x01\x21" if auto_run_enabled else b"\x00\x21")
    autorun_rail_code += make_bl(autorun_rail_addr + 0x06, helper_addr)
    autorun_rail_code += b"\x02\x9a\x02\x21\x0a\x40\x52\x08\x50\x40\x00\x28\x02\xd1\x03\x98\x06\x30\x03\x90\x0d\xbd"
    assert len(autorun_rail_code) == 0x20

    # FishTimerHook() at dwc_base + 0x94 (0x18 bytes)
    fish_timer_addr = dwc_base + 0x94
    fish_timer_code = bytearray()
    fish_timer_code += b"\x00\xb5\x52\x20" + (b"\x01\x21" if fast_fishing_enabled else b"\x00\x21")
    fish_timer_code += make_bl(fish_timer_addr + 0x06, helper_addr)
    fish_timer_code += b"\x00\x28\x00\xd1\x5a\x20"
    fish_timer_code += make_bl(fish_timer_addr + 0x10, 0x02005784)
    fish_timer_code += b"\x00\xbd\xc0\x46"
    assert len(fish_timer_code) == 0x18

    # FishBiteHook() at dwc_base + 0xAC (0x1C bytes)
    fish_bite_addr = dwc_base + 0xAC
    fish_bite_code = bytearray()
    fish_bite_code += b"\x0f\xb5\x52\x20" + (b"\x01\x21" if fast_fishing_enabled else b"\x00\x21")
    fish_bite_code += make_bl(fish_bite_addr + 0x06, helper_addr)
    fish_bite_code += b"\x00\x28\x02\xd1\x00\x98\xa0\x42\x02\xd8\x04\x98\x06\x30\x04\x90\x0f\xbd"
    assert len(fish_bite_code) == 0x1C

    # EscapeHook() at dwc_base + 0xC8 (0x1C bytes)
    escape_hook_addr = dwc_base + 0xC8
    escape_code = bytearray()
    escape_code += b"\x0f\xb5\x50\x20" + (b"\x01\x21" if guaranteed_escape_enabled else b"\x00\x21")
    escape_code += make_bl(escape_hook_addr + 0x06, helper_addr)
    escape_code += b"\x00\x28\x02\xd1\x01\x99\x8c\x42\x02\xd9\x04\x98\x24\x30\x04\x90\x0f\xbd"
    assert len(escape_code) == 0x1C

    # Debounces 30vs60 a press problems
    turbo_keypad_addr = dwc_base + 0xE4
    copy_p30_addr = dwc_base + 0x10C
    raw_pressed_addr = dwc_base + 0x120
    raw_p60_addr = raw_pressed_addr + 0x1C

    turbo_keypad_code = bytearray()
    turbo_keypad_code += b"\xe0\x60\x0d\xb5\x21\x69\x07\x4a\x11\x60\x53\x68\x0b\x43\x53\x60\x36\x20"
    turbo_keypad_code += (b"\x01\x21" if hold_a_turbo_enabled else b"\x00\x21")
    turbo_keypad_code += make_bl(turbo_keypad_addr + 0x14, helper_addr)
    turbo_keypad_code += b"\x00\x28\x01\xd0\x61\x69\x00\xe0\x21\x69\x0d\xbd"
    turbo_keypad_code += struct.pack("<I", raw_p60_addr)
    assert len(turbo_keypad_code) == 0x28

    copy_p30_code = bytearray()
    copy_p30_code += b"\x60\x6b\xa0\x62\x02\x48\x41\x68\x81\x60\x00\x21\x41\x60\x70\x47"
    copy_p30_code += struct.pack("<I", raw_p60_addr)
    assert len(copy_p30_code) == 0x14

    get_mgr_addr = 0x0203D2D8 + delta
    raw_pressed_code = bytearray()
    raw_pressed_code += b"\x10\xb5"
    raw_pressed_code += make_bl(raw_pressed_addr + 0x02, get_mgr_addr)
    raw_pressed_code += b"\x3d\x30\x04\x78\x03\x48\x1e\x2c\x01\xd1\x80\x68\x10\xbd\x00\x68\x10\xbd"
    raw_pressed_code += struct.pack("<I", raw_p60_addr)
    raw_pressed_code += b"\x00" * 12
    assert len(raw_pressed_code) == 0x28

    qol_blob = (
        helper_code + bike_code + autorun_grid_code + autorun_rail_code
        + fish_timer_code + fish_bite_code + escape_code
        + turbo_keypad_code + copy_p30_code + raw_pressed_code
    )
    assert len(qol_blob) == 0x148
    dwc_off = dwc_base - arm9_base
    arm9[dwc_off : dwc_off + len(qol_blob)] = qol_blob

    keypad_pat = bytes.fromhex("e0602169e161a06160692062201c")
    keypad_idx = arm9.find(keypad_pat)
    if keypad_idx != -1:
        arm9[keypad_idx : keypad_idx + 4] = make_bl(arm9_base + keypad_idx, turbo_keypad_addr)
        if arm9[keypad_idx + 0x3C : keypad_idx + 0x40] == b"\x60\x6b\xa0\x62":
            arm9[keypad_idx + 0x3C : keypad_idx + 0x40] = make_bl(
                arm9_base + keypad_idx + 0x3C, copy_p30_addr
            )

    # Stop Turbo A at choices
    for menu_off in (
        0x218A8, 0x276D2, 0x276EC, 0x27700, 0x27714, 0x27738,
        0x2774C, 0x277F4, 0x27808, 0x27952, 0x27964, 0x27976, 0x29F44,
    ):
        site_off = menu_off + delta
        arm9[site_off : site_off + 4] = make_bl(arm9_base + site_off, raw_pressed_addr)

    bike_allowed_pat = b"\xc0\x8b\x40\x05\xc0\x0f\x08\xbd"
    bike_allowed_off = arm9.find(bike_allowed_pat)
    if bike_allowed_off != -1:
        arm9[bike_allowed_off : bike_allowed_off + 6] = make_bl(
            arm9_base + bike_allowed_off, bike_hook_addr
        ) + b"\xc0\x46"

    ov_table = rom.loadArm9Overlays()

    if 167 in ov_table:
        ov167 = ov_table[167]
        ov167_data = bytearray(ov167.data)
        modified_ov167 = False

        # Dynamic catch rate (var 16792) and EXP (var 16793) multiplier hooks
        if len(ov167_data) >= 0x20600:
            hook_exp_off = 0x2053c
            hook_exp_ram = ov167.ramAddress + hook_exp_off
            exp_code = bytearray()
            exp_code += b"\x10\xb5"
            exp_code += make_bl(hook_exp_ram + 0x02, 0x20137f0)
            exp_code += b"\x04\x1c"
            exp_code += make_bl(hook_exp_ram + 0x08, 0x20072fc)
            exp_code += b"\x00\x28\x0b\xd0"
            exp_code += b"\x2d\x21"
            exp_code += make_bl(hook_exp_ram + 0x12, 0x2017a5c)
            exp_code += b"\x00\x28\x06\xd0"
            exp_code += b"\xcc\x21\x89\x00\x02\x31\x41\x5a"
            exp_code += b"\x01\x29\x00\xdd\x4c\x43"
            exp_code += b"\x20\x1c\x10\xbd"
            assert len(exp_code) == 44
            ov167_data[hook_exp_off : hook_exp_off + len(exp_code)] = exp_code
            ov167_data[0x157b0 : 0x157b4] = make_bl(ov167.ramAddress + 0x157b0, hook_exp_ram)

            hook_cap_off = 0x20568
            hook_cap_ram = ov167.ramAddress + hook_cap_off
            cap_code = bytearray()
            cap_code += b"\x10\xb5"
            cap_code += make_bl(hook_cap_ram + 0x02, 0x2013838)
            cap_code += b"\x04\x1c"
            cap_code += make_bl(hook_cap_ram + 0x08, 0x20072fc)
            cap_code += b"\x00\x28\x0f\xd0"
            cap_code += b"\x2d\x21"
            cap_code += make_bl(hook_cap_ram + 0x12, 0x2017a5c)
            cap_code += b"\x00\x28\x0a\xd0"
            cap_code += b"\xcc\x21\x89\x00\x41\x5a"
            cap_code += b"\xff\x29\x02\xd1"
            cap_code += b"\xff\x20\x00\x03\x10\xbd"
            cap_code += b"\x01\x29\x00\xdd\x4c\x43"
            cap_code += b"\x20\x1c\x10\xbd"
            assert len(cap_code) == 52
            ov167_data[hook_cap_off : hook_cap_off + len(cap_code)] = cap_code
            ov167_data[0x15f26 : 0x15f2a] = make_bl(ov167.ramAddress + 0x15f26, hook_cap_ram)
            modified_ov167 = True

        esc_pat = b"\x8C\x42\x11\xD8"
        esc_pos = ov167_data.find(esc_pat)
        if esc_pos != -1:
            ov167_data[esc_pos : esc_pos + 4] = make_bl(ov167.ramAddress + esc_pos, escape_hook_addr)
            modified_ov167 = True

        if modified_ov167:
            ov167.data = bytes(ov167_data)
            rom.files[ov167.fileID] = ov167.save(compress=ov167.compressed)
            rom.arm9OverlayTable = saveOverlayTable(ov_table)

    ov_table = rom.loadArm9Overlays()
    if 33 in ov_table:
        ov33 = ov_table[33]
        ov33_data = bytearray(ov33.data)
        if ov33_data[0x294C : 0x294E] == b"\x5A\x20":
            ov33_data[0x294C : 0x2952] = make_bl(ov33.ramAddress + 0x294C, fish_timer_addr) + b"\xc0\x46"
            ov33.data = bytes(ov33_data)
            rom.files[ov33.fileID] = ov33.save(compress=ov33.compressed)
            rom.arm9OverlayTable = saveOverlayTable(ov_table)

    ov_table = rom.loadArm9Overlays()
    ov36 = ov_table[36]
    ov36_data = bytearray(ov36.data)
    modified_ov36 = False

    # Dynamic blind trainers (var 16794)
    if len(ov36_data) >= 0x28ADC:
        hook_off = 0x28AAC
        hook_ram = ov36.ramAddress + hook_off
        vanilla_func = ov36.ramAddress + 0x26894

        blind_trainers_enabled = bool(options.get("blind_trainers", False))
        hook_code = bytearray()
        hook_code += b"\x12\xb5"  # push {r1, r4, lr}
        # Bypass blind trainers in Nimbasa Gym
        hook_code += b"\xe8\x23\xc3\x5a\x3f\x2b\x07\xd0"
        hook_code += b"\x6b\x23"
        hook_code += b"\x9b\x00"
        hook_code += b"\xfc\x58"
        hook_code += b"\xcd\x23"
        hook_code += b"\x9b\x00"
        hook_code += b"\xe3\x5c"
        if blind_trainers_enabled:
            # Blind if var 16794 != 2 (1=on or 0=uninit)
            hook_code += b"\x02\x2b"
            hook_code += b"\x03\xd1"
        else:
            # Blind if var 16794 == 1 (1=on)
            hook_code += b"\x01\x2b"
            hook_code += b"\x03\xd0"
        hook_code += b"\x00\x99"  # ldr r1, [sp, #0] (preserve caller's r1)
        hook_code += make_bl(hook_ram + 0x1C, vanilla_func)
        hook_code += b"\x12\xbd"  # pop {r1, r4, pc}
        hook_code += b"\x00\x20"
        hook_code += b"\x12\xbd"  # pop {r1, r4, pc}
        hook_code += b"\xc0\x46" * ((48 - len(hook_code)) // 2)
        assert len(hook_code) == 48

        for sight_call_off in (0x26744, 0x2678A, 0x267BE):
            ov36_data[sight_call_off : sight_call_off + 4] = make_bl(ov36.ramAddress + sight_call_off, hook_ram)
        ov36_data[hook_off : hook_off + len(hook_code)] = hook_code
        modified_ov36 = True

    if len(ov36_data) >= 0x2245E:
        if ov36_data[0x2245A : 0x2245E] == b"\xa0\x42\x02\xd9":
            ov36_data[0x2245A : 0x2245E] = make_bl(ov36.ramAddress + 0x2245A, fish_bite_addr)
            modified_ov36 = True

    grid_pat = b"\x31\x42\x08\xD0\x6A\x68\x02\x21\x11\x42\x04\xD0"
    grid_pos = ov36_data.find(grid_pat)
    if grid_pos != -1:
        ov36_data[grid_pos + 6 : grid_pos + 12] = make_bl(ov36.ramAddress + grid_pos + 6, autorun_grid_addr) + b"\xc0\x46"
        modified_ov36 = True

    rail_pat = b"\x02\x20\x18\x42\x01\xD0"
    rail_pos = ov36_data.find(rail_pat)
    if rail_pos != -1:
        ov36_data[rail_pos : rail_pos + 6] = make_bl(ov36.ramAddress + rail_pos, autorun_rail_addr) + b"\xc0\x46"
        modified_ov36 = True

    # Turbo A debouncer for cutscene starts
    fep_pat = b"\x70\xb5\x0e\x1c\x14\x1c\x00\x21\x40\x22\x05\x1c"
    fep_search = 0
    while True:
        fep_pos = ov36_data.find(fep_pat, fep_search)
        if fep_pos == -1 or fep_pos + 0x3C > len(ov36_data):
            break
        if ov36_data[fep_pos + 0x34 : fep_pos + 0x36] == b"\xa8\x62":
            ov36_data[fep_pos + 0x30 : fep_pos + 0x34] = make_bl(
                ov36.ramAddress + fep_pos + 0x30, raw_pressed_addr
            )
            modified_ov36 = True
            break
        fep_search = fep_pos + 2

    # Skip HM field move cutscenes
    is_fast_hm = True
    surf_pat = b"\x06\x28\x02\xD0\x02\xB0\x0A\x48\xF8\xBD"
    surf_pos = ov36_data.find(surf_pat)
    if surf_pos != -1:
        ov36_data[surf_pos + 2 : surf_pos + 4] = b"\xC0\x46"
        modified_ov36 = True

    if modified_ov36:
        ov36.data = bytes(ov36_data)
        rom.files[ov36.fileID] = ov36.save(compress=ov36.compressed)
        rom.arm9OverlayTable = saveOverlayTable(ov_table)

    ov_table = rom.loadArm9Overlays()
    if 302 in ov_table:
        ov302 = ov_table[302]
        ov302_data = bytearray(ov302.data)
        modified_ov302 = False

        # Pokedexcommon_createlist return patch: ldr r0, [sp, #4] -> adds r0, r7, #0
        ret_pat = b"\x02\x99\x00\x98\x01\x60\x01\x98\x03\xb0\xf0\xbd"
        ret_idx = ov302_data.find(ret_pat)
        if ret_idx != -1:
            ov302_data[ret_idx + 6 : ret_idx + 8] = b"\x38\x1c"
            modified_ov302 = True

        # Pokedexcommon_getconditions patch: unconditionally set conditions[0..2] = 1 and return
        cond_pat = b"\x70\xb5\x08\x4e\x05\x1c\x0c\x1c\x01\x20"
        cond_idx = ov302_data.find(cond_pat)
        if cond_idx != -1:
            ov302_data[cond_idx : cond_idx + 10] = b"\x01\x21\x01\x60\x41\x60\x81\x60\x70\x47"
            modified_ov302 = True

        if modified_ov302:
            ov302.data = bytes(ov302_data)
            rom.files[ov302.fileID] = ov302.save(compress=ov302.compressed)
            rom.arm9OverlayTable = saveOverlayTable(ov_table)

    if is_fast_hm:
        try:
            from .patch.script_editing import disassemble, assemble, Line
        except (ImportError, ValueError):
            from patch.script_editing import disassemble, assemble, Line
        a056 = NARC(rom.getFileByName("a/0/5/6"))
        sf1243 = disassemble(a056.files[1243])
        new_lines: list[Line] = []
        skip_until: str | None = None
        for l in sf1243.lines:
            lbl = l.parts[0] if l.type == "label" and l.parts else None
            if skip_until is not None:
                if lbl == skip_until:
                    skip_until = None
                else:
                    continue

            if lbl == "scr0":
                # Strength: check HM04 (423) in bag or strength (70) in party, skip yes/no prompt
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["PlaySound", 1351]),
                    Line("command", ["FlagGet", 2404, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl1_1"]),
                    Line("command", ["VMCall", "sub9"]),
                    Line("command", ["VMJump", "lbl1_3"]),
                    Line("label", ["lbl1_1"]),
                    Line("command", ["CheckItemBagNumber", 423, 1, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl1_2"]),
                    Line("command", ["PokePartyHasMoveAny", 32784, 70]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 6]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl1_2"]),
                    Line("command", ["VMCall", "sub8"]),
                    Line("command", ["VMJump", "lbl1_3"]),
                    Line("label", ["lbl1_2"]),
                    Line("command", ["VMCall", "sub4"]),
                    Line("label", ["lbl1_3"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "sub9"
            elif lbl == "sub4":
                # Strength effect without PlayHMCutInEffect (safe when used from bag with party index 6)
                new_lines.extend([
                    l,
                    Line("command", ["FlagSet", 2404]),
                    Line("command", ["BroadcastGameBeacon", 1, 70, 0]),
                    Line("command", ["MsgSystem", 11, 2]),
                    Line("command", ["InputWaitLast"]),
                    Line("command", ["MsgSystemClose"]),
                    Line("command", ["VMReturn"]),
                ])
                skip_until = "scr1"
            elif lbl == "scr2":
                # Surf water interaction: check HM03 (422) in bag or surf (57) in party, check partner flag 2406
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["CheckItemBagNumber", 422, 1, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl3_14"]),
                    Line("command", ["PokePartyHasMoveAny", 32784, 57]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 6]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl3_14"]),
                    Line("command", ["VMJump", "lbl3_16"]),
                    Line("label", ["lbl3_14"]),
                    Line("command", ["StackPushFlag", 2406]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl3_15"]),
                    Line("command", ["WordSetMoveName", 0, 57]),
                    Line("command", ["VMCall", "sub18"]),
                    Line("command", ["VMJump", "lbl3_16"]),
                    Line("label", ["lbl3_15"]),
                    Line("command", ["PlaySound", 1351]),
                    Line("command", ["VMCall", "sub17"]),
                    Line("label", ["lbl3_16"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "sub17"
            elif lbl == "sub17":
                # Sub17: surf
                new_lines.extend([
                    l,
                    Line("command", ["PlayerSetSpecialSequence", 1]),
                    Line("command", ["SurfAnimation"]),
                    Line("command", ["BroadcastGameBeacon", 1, 57, 0]),
                    Line("command", ["VMReturn"]),
                ])
                skip_until = "scr3"
            elif lbl == "scr3":
                # Scr3: party menu surf
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["PlayerSetSpecialSequence", 1]),
                    Line("command", ["SurfAnimation"]),
                    Line("command", ["BroadcastGameBeacon", 1, 57, 0]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "scr4"
            elif lbl == "scr4":
                # Cut: check HM01 (420) in bag or cut (15) in party, skip yes/no prompt
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["PlaySound", 1351]),
                    Line("command", ["CheckItemBagNumber", 420, 1, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl5_22"]),
                    Line("command", ["PokePartyHasMoveAny", 32784, 15]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 6]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl5_22"]),
                    Line("command", ["VMCall", "sub26"]),
                    Line("command", ["VMJump", "lbl5_25"]),
                    Line("label", ["lbl5_22"]),
                    Line("command", ["VMCall", "sub24"]),
                    Line("label", ["lbl5_25"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "sub26"
            elif lbl == "sub24":
                # Cut effect without PlayHMCutInEffect
                new_lines.extend([
                    l,
                    Line("command", ["SpecialAnimation2"]),
                    Line("command", ["BroadcastGameBeacon", 1, 15, 0]),
                    Line("command", ["VMSleep", 3]),
                    Line("command", ["ActorDelete", 32785]),
                    Line("command", ["PlaySound", 1651]),
                    Line("command", ["VMSleep", 1]),
                    Line("command", ["VMReturn"]),
                ])
                skip_until = "scr5"
            elif lbl == "scr6":
                # Waterfall: check HM05 (424) in bag or waterfall (127) in party, skip yes/no prompt
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["PlaySound", 1351]),
                    Line("command", ["CheckItemBagNumber", 424, 1, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl7_30"]),
                    Line("command", ["PokePartyHasMoveAny", 32784, 127]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 6]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl7_30"]),
                    Line("command", ["VMCall", "sub34"]),
                    Line("command", ["VMJump", "lbl7_32"]),
                    Line("label", ["lbl7_30"]),
                    Line("command", ["StackPushFlag", 2406]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl7_31"]),
                    Line("command", ["WordSetMoveName", 0, 127]),
                    Line("command", ["VMCall", "sub18"]),
                    Line("command", ["VMJump", "lbl7_32"]),
                    Line("label", ["lbl7_31"]),
                    Line("command", ["VMCall", "sub33"]),
                    Line("label", ["lbl7_32"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "sub34"
            elif lbl == "sub33":
                # Waterfall effect without PlayHMCutInEffect
                new_lines.extend([
                    l,
                    Line("command", ["SpecialAnimation", 0]),
                    Line("command", ["BroadcastGameBeacon", 1, 127, 0]),
                    Line("command", ["VMReturn"]),
                ])
                skip_until = "scr7"
            elif lbl == "scr11":
                # Dive: check HM06 (425) in bag or dive (291) in party, skip yes/no prompt
                new_lines.extend([
                    l,
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["CheckItemBagNumber", 425, 1, 32784]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl12_40"]),
                    Line("command", ["PokePartyHasMoveAny", 32784, 291]),
                    Line("command", ["StackPush", 32784]),
                    Line("command", ["StackPushConst", 6]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl12_40"]),
                    Line("command", ["MsgSystem", 30, 2]),
                    Line("command", ["InputWaitLast"]),
                    Line("command", ["MsgSystemClose"]),
                    Line("command", ["VMJump", "lbl12_42"]),
                    Line("label", ["lbl12_40"]),
                    Line("command", ["StackPushFlag", 2406]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl12_41"]),
                    Line("command", ["WordSetMoveName", 0, 291]),
                    Line("command", ["VMCall", "sub18"]),
                    Line("command", ["VMJump", "lbl12_42"]),
                    Line("label", ["lbl12_41"]),
                    Line("command", ["VMCall", "sub43"]),
                    Line("label", ["lbl12_42"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                skip_until = "sub43"
            elif lbl == "sub43":
                # Dive effect without PlayHMCutInEffect
                new_lines.extend([
                    l,
                    Line("command", ["CallAnimation", 0]),
                    Line("command", ["BroadcastGameBeacon", 1, 291, 0]),
                    Line("command", ["VMReturn"]),
                ])
                skip_until = "scr12"
            else:
                if l.type == "command" and (
                    l.parts == ["VMCall", "sub5"]
                    or l.parts == ["VMCall", "sub7"]
                    or (l.parts and l.parts[0] == "PlayHMCutInEffect")
                ):
                    continue
                new_lines.append(l)
        sf1243.lines = new_lines
        a056.files[1243] = bytes(assemble(sf1243))
        rom.setFileByName("a/0/5/6", a056.save())

    # (Catch rate and exp multipliers are handled dynamically in ov167 via var 16792 / var 16793)
    if (options.get("fast_hatch", False) or options.get("tmhm_fully_compatible", False)
            or options.get("max_friendship", False)):
        a016 = NARC(rom.getFileByName("a/0/1/6"))
        for i in range(1, min(709, len(a016.files))):
            pdata = bytearray(a016.files[i])
            if len(pdata) == 76:
                if options.get("fast_hatch", False):
                    pdata[0x13] = 0x01
                if options.get("tmhm_fully_compatible", False):
                    pdata[0x28:0x35] = b"\xFF" * 12 + b"\x1F"
                if options.get("max_friendship", False):
                    pdata[0x14] = 0xFF
                a016.files[i] = bytes(pdata)
        rom.setFileByName("a/0/1/6", a016.save())

    # Convert trade and single-branch time-based evolutions in a/0/1/9
    # - Plain/species trade (5, 7) -> level 37 (4)
    # - Held item trade (6) -> level up while holding item, day and night (19 & 20)
    # - Friendship Day/Night (2, 3) -> Friendship anytime (1), except Eevee (133)
    # - Held item Day-only (19) or Night-only (20) -> both day and night (19 & 20)
    a019_data = rom.getFileByName("a/0/1/9")
    if a019_data is not None:
        a019 = NARC(a019_data)
        modified_019 = False
        for i in range(len(a019.files)):
            edata = a019.files[i]
            if len(edata) < 6:
                continue
            num_slots = len(edata) // 6
            existing: list[tuple[int, int, int]] = []
            for s in range(num_slots):
                m, p, t = struct.unpack_from("<HHH", edata, s * 6)
                if m != 0:
                    existing.append((m, p, t))
            new_entries: list[tuple[int, int, int]] = []
            seen: set[tuple[int, int, int]] = set()
            changed = False

            def _add(entry: tuple[int, int, int]) -> None:
                if entry not in seen:
                    seen.add(entry)
                    new_entries.append(entry)

            for m, p, t in existing:
                if m in (5, 7):
                    _add((4, 37, t))
                    changed = True
                elif m == 6:
                    _add((19, p, t))
                    _add((20, p, t))
                    changed = True
                elif m in (2, 3) and i != 133:
                    _add((1, p, t))
                    changed = True
                elif m in (19, 20):
                    _add((19, p, t))
                    _add((20, p, t))
                    if (19 if m == 20 else 20, p, t) not in existing:
                        changed = True
                else:
                    _add((m, p, t))
            if changed:
                out = bytearray(num_slots * 6)
                for idx, (m, p, t) in enumerate(new_entries[:num_slots]):
                    struct.pack_into("<HHH", out, idx * 6, m, p, t)
                a019.files[i] = bytes(out)
                modified_019 = True
        if modified_019:
            rom.setFileByName("a/0/1/9", a019.save())

    a012_data = rom.getFileByName("a/0/1/2")
    if a012_data is not None:
        a012 = NARC(a012_data)
        headers = bytearray(a012.files[0])
        num_headers = len(headers) // 48
        remove_surf_bike = bool(options.get("remove_surf_bike_music", True))
        if remove_surf_bike:
            for h in range(num_headers):
                headers[h * 48 + 31] &= ~0x40
            a012.files[0] = bytes(headers)
            rom.setFileByName("a/0/1/2", a012.save())

    # Recolor unused font palette slots (#1_6 progression, #1_3 useful) so vanilla #1_2 key items stay untouched
    a023_data = rom.getFileByName("a/0/2/3")
    if a023_data is not None:
        def _bgr555(r: int, g: int, b: int) -> int:
            return ((b >> 3) << 10) | ((g >> 3) << 5) | (r >> 3)

        light_updates = {
            7: _bgr555(56, 96, 216),
            8: _bgr555(160, 184, 248),
            13: _bgr555(120, 80, 216),
            14: _bgr555(192, 176, 240),
        }
        dark_updates = {
            7: _bgr555(104, 136, 232),
            8: _bgr555(40, 56, 104),
            13: _bgr555(176, 152, 240),
            14: _bgr555(72, 56, 112),
        }
        a023 = NARC(a023_data)
        palette_specs = ((5, light_updates), (6, light_updates), (7, dark_updates))
        modified_a023 = False
        for pal_idx, updates in palette_specs:
            if pal_idx < len(a023.files):
                pdata = bytearray(a023.files[pal_idx])
                ttlp = pdata.find(b"TTLP")
                if ttlp != -1 and len(pdata) >= ttlp + 0x18 + 30:
                    for col_idx, bgr in updates.items():
                        struct.pack_into("<H", pdata, ttlp + 0x18 + col_idx * 2, bgr)
                    a023.files[pal_idx] = bytes(pdata)
                    modified_a023 = True
        if modified_a023:
            rom.setFileByName("a/0/2/3", a023.save())


def validate(version: str, file_name: str) -> None:
    with open(file_name, "rb", buffering=0) as f:
        header = f.read(18)
    full = (b'POKEMON B2\0\0IREO01', b'POKEMON W2\0\0IRDO01')

    if version == "black2":
        if header != full[0]:
            raise ValueError(f"Supplied base ROM appears to not be an English copy of Pokémon Black 2 ({header}).")
    elif version == "white2":
        if header != full[1]:
            raise ValueError(f"Supplied base ROM appears to not be an English copy of Pokémon White 2 ({header}).")


def get_base_rom_path(version: str = "black2", file_name: str = "") -> str:
    if not file_name:
        v_str = str(version).lower()
        if v_str in ("white2", "white_2", "w2", "1"):
            key, default_name = "white2", "PokemonWhite2.nds"
        else:
            key, default_name = "black2", "PokemonBlack2.nds"
        if get_settings is not None:
            try:
                file_name = get_settings()["pokemon_b2w2_settings"][f"{key}_rom"]
            except Exception:
                pass
        if not file_name:
            file_name = default_name
    if not os.path.exists(file_name) and Utils is not None:
        file_name = Utils.user_path(file_name)
    return file_name
