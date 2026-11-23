from __future__ import annotations

import struct
from typing import TYPE_CHECKING, Any

try:
    from ..nds_compat import NARC
except (ImportError, ValueError):
    try:
        from worlds.pokemon_b2w2.nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import NARC

try:
    from ..nds_compat import saveOverlayTable
except (ImportError, ValueError):
    try:
        from worlds.pokemon_b2w2.nds_compat import saveOverlayTable
    except (ImportError, ValueError):
        from nds_compat import saveOverlayTable

if TYPE_CHECKING:
    from ..nds_compat import NintendoDSRom

from .script_editing import Line, assemble, disassemble
from .text import decode, encode, insert_line


# Town fly data for B2W2: (town_id, visit_flag, text_id, (zone_id, x, z, dir))
# Castelia city (zone 28) is a rail map and uses WarpRail (28, 3, 8, 4, 1) - dumb, why...
TOWN_FLY_DATA = [
    (1, 2488, 135, (427, 47, 762, 1)),    # Aspertia City
    (2, 2491, 136, (439, 105, 694, 1)),   # Floccesy Town
    (3, 2489, 137, (448, 210, 650, 1)),   # Virbank City
    (16, 2469, 270, (566, 31, 50, 1)),    # Pokéstar Studios
    (4, 2476, 138, (28, 3, 1, 8)),        # Castelia City (rail: line=3, frontpos=8, sidepos=1, dir=1)
    (5, 2477, 139, (62, 406, 469, 1)),    # Nimbasa City
    (6, 2478, 140, (96, 188, 414, 1)),    # Driftveil City
    (17, 2471, 271, (191, 197, 469, 1)),  # PWT (outdoor plaza)
    (7, 2479, 141, (107, 108, 306, 1)),   # Mistralton City
    (8, 2492, 142, (458, 634, 305, 1)),   # Lentimas Town
    (11, 2485, 145, (412, 760, 301, 1)),  # Undella Town
    (10, 2482, 144, (406, 660, 186, 1)),  # Lacunosa Town
    (9, 2481, 143, (120, 425, 174, 1)),   # Opelucid City
    (12, 2490, 146, (465, 775, 178, 1)),  # Humilau City
    (18, 2530, 272, (573, 43, 18, 1)),    # Victory Road
    (13, 2483, 147, (136, 19, 49, 1)),    # Pokémon League
    (20, 2484, 274, (0, 42, 38, 1)),      # Black City (replaced with White Forest in W2)
    (19, 2480, 273, (113, 184, 197, 1)),  # Icirrus City
    (15, 2475, 149, (16, 637, 599, 1)),   # Nacrene City
    (14, 2474, 148, (6, 781, 589, 1)),    # Striaton City
    (21, 2473, 275, (397, 796, 659, 1)),  # Accumula Town
    (22, 2472, 276, (389, 782, 750, 1)),  # Nuvema Town
]


def _get_town_fly_data(is_white2: bool) -> list[tuple[int, int, int, tuple[int, int, int, int]]]:
    if not is_white2:
        return TOWN_FLY_DATA
    return [
        (20, 2484, 274, (424, 45, 37, 1)) if entry[0] == 20 else entry
        for entry in TOWN_FLY_DATA
    ]


def apply_aptransceiver(rom: NintendoDSRom, options: dict[str, Any]) -> None:
    is_white2 = (b"IRDO" in rom.name or rom.name[8:10] == b"W2" or rom.idCode[:4] == b"IRDO")
    fly_data = _get_town_fly_data(is_white2)
    a003_data = rom.getFileByName("a/0/0/3")
    if a003_data is not None:
        a003 = NARC(a003_data)
        text_479 = decode(a003.files[479])

        insert_line(text_479, 0, 93, "APtransceiver")
        insert_line(text_479, 0, 94, "PC")
        insert_line(text_479, 0, 98, "Seasons")
        insert_line(text_479, 0, 99, "Which season would you like?")
        insert_line(text_479, 0, 100, "Spring")
        insert_line(text_479, 0, 101, "Summer")
        insert_line(text_479, 0, 102, "Autumn")
        insert_line(text_479, 0, 103, "Winter")
        insert_line(text_479, 0, 104, "Changed to Spring.")
        insert_line(text_479, 0, 105, "Changed to Summer.")
        insert_line(text_479, 0, 106, "Changed to Autumn.")
        insert_line(text_479, 0, 107, "Changed to Winter.")

        insert_line(text_479, 0, 170, "Days")
        insert_line(text_479, 0, 171, "Which day would you like?")
        insert_line(text_479, 0, 172, "Sunday")
        insert_line(text_479, 0, 173, "Monday")
        insert_line(text_479, 0, 174, "Tuesday")
        insert_line(text_479, 0, 175, "Wednesday")
        insert_line(text_479, 0, 176, "Thursday")
        insert_line(text_479, 0, 177, "Friday")
        insert_line(text_479, 0, 178, "Saturday")
        insert_line(text_479, 0, 180, "Changed to Sunday.")
        insert_line(text_479, 0, 181, "Changed to Monday.")
        insert_line(text_479, 0, 182, "Changed to Tuesday.")
        insert_line(text_479, 0, 183, "Changed to Wednesday.")
        insert_line(text_479, 0, 184, "Changed to Thursday.")
        insert_line(text_479, 0, 185, "Changed to Friday.")
        insert_line(text_479, 0, 186, "Changed to Saturday.")

        insert_line(text_479, 0, 120, "Field Moves")
        insert_line(text_479, 0, 121, "Check log")
        insert_line(text_479, 0, 122, "Level cap")
        insert_line(text_479, 0, 123, "Close")
        insert_line(text_479, 0, 124, "Teleport")
        insert_line(text_479, 0, 125, "Dig")
        insert_line(text_479, 0, 126, "Fly")
        insert_line(text_479, 0, 127, "Modifiers")
        insert_line(text_479, 0, 212, "Flash")

        insert_line(text_479, 0, 133, "It can't be used here.")
        insert_line(text_479, 0, 134, "Where would you like to fly?")

        town_names = {
            135: "Aspertia City",
            136: "Floccesy Town",
            137: "Virbank City",
            138: "Castelia City",
            139: "Nimbasa City",
            140: "Driftveil City",
            141: "Mistralton City",
            142: "Lentimas Town",
            143: "Opelucid City",
            144: "Lacunosa Town",
            145: "Undella Town",
            146: "Humilau City",
            147: "Pokémon League",
            148: "Striaton City",
            149: "Nacrene City",
            270: "Pokéstar Studios",
            271: "PWT",
            272: "Victory Road",
            273: "Icirrus City",
            274: "White Forest" if is_white2 else "Black City",
            275: "Accumula Town",
            276: "Nuvema Town",
        }
        for _, _, text_id, _ in fly_data:
            insert_line(text_479, 0, text_id, town_names[text_id])

        insert_line(text_479, 0, 150, "Your current level cap is [c_100_#1_0].")
        insert_line(text_479, 0, 151, "Recent items received:[NextLine]- [c_109_#1_0]")
        insert_line(text_479, 0, 152, "No new items logged since last opened.")
        insert_line(text_479, 0, 153, "Recent items received:[NextLine]- [c_109_#1_0][Scroll][NextLine]- [c_109_#1_1]")
        insert_line(text_479, 0, 154, "Recent items received:[NextLine]- [c_109_#1_0][Scroll][NextLine]- [c_109_#1_1][Scroll][NextLine]- [c_109_#1_2]")
        insert_line(text_479, 0, 155, "Recent items received:[NextLine]- [c_109_#1_0][Scroll][NextLine]- [c_109_#1_1][Scroll][NextLine]- [c_109_#1_2][Scroll][NextLine]- [c_109_#1_3]")
        insert_line(text_479, 0, 156, "Recent items received:[NextLine]- [c_109_#1_0][Scroll][NextLine]- [c_109_#1_1][Scroll][NextLine]- [c_109_#1_2][Scroll][NextLine]- [c_109_#1_3][Scroll][NextLine]- [c_109_#1_4]")

        insert_line(text_479, 0, 160, "Catch Rate Multiplier: [c_100_#1_0]x")
        insert_line(text_479, 0, 161, "EXP Multiplier: [c_100_#1_0]x")
        insert_line(text_479, 0, 162, "+1")
        insert_line(text_479, 0, 163, "+5")
        insert_line(text_479, 0, 164, "-1")
        insert_line(text_479, 0, 165, "-5")
        insert_line(text_479, 0, 166, "Cancel")
        insert_line(text_479, 0, 167, "Catch Rate")
        insert_line(text_479, 0, 168, "EXP Rate")
        insert_line(text_479, 0, 187, "Blind Trainers: OFF")
        insert_line(text_479, 0, 188, "Hold A Turbo: OFF")
        insert_line(text_479, 0, 189, "Log Filter")
        insert_line(text_479, 0, 190, "Trainers will not battle on sight.")
        insert_line(text_479, 0, 191, "Trainers will battle on sight.")
        insert_line(text_479, 0, 192, "Holding A advances text rapidly.")
        insert_line(text_479, 0, 193, "Holding A advances text normally.")
        insert_line(text_479, 0, 194, "Current Log: Progression Only")
        insert_line(text_479, 0, 195, "Current Log: Progression + Useful")
        insert_line(text_479, 0, 196, "Current Log: All Checks")
        insert_line(text_479, 0, 197, "Catch Rate: 100% Guaranteed")
        insert_line(text_479, 0, 198, "Select EXP Multiplier:")
        insert_line(text_479, 0, 199, "Select Catch Multiplier:")
        insert_line(text_479, 0, 200, "1x")
        insert_line(text_479, 0, 201, "2x")
        insert_line(text_479, 0, 202, "3x")
        insert_line(text_479, 0, 203, "5x")
        insert_line(text_479, 0, 204, "10x")
        insert_line(text_479, 0, 205, "Guaranteed")
        insert_line(text_479, 0, 206, "Progression Only")
        insert_line(text_479, 0, 207, "Progression + Useful")
        insert_line(text_479, 0, 208, "All Checks")
        insert_line(text_479, 0, 210, "Blind Trainers: ON")
        insert_line(text_479, 0, 211, "Hold A Turbo: ON")
        insert_line(text_479, 0, 250, "Auto Run: OFF")
        insert_line(text_479, 0, 251, "Auto Run: ON")
        insert_line(text_479, 0, 252, "Running Shoes are toggled automatically.")
        insert_line(text_479, 0, 253, "Hold B to use Running Shoes.")
        insert_line(text_479, 0, 254, "Guaranteed Escape: OFF")
        insert_line(text_479, 0, 255, "Guaranteed Escape: ON")
        insert_line(text_479, 0, 256, "Fleeing from wild battles always succeeds.")
        insert_line(text_479, 0, 257, "Fleeing from wild battles uses normal odds.")
        insert_line(text_479, 0, 258, "Fast Fishing: OFF")
        insert_line(text_479, 0, 259, "Fast Fishing: ON")
        insert_line(text_479, 0, 260, "Fishing bites occur quickly.")
        insert_line(text_479, 0, 261, "Fishing uses normal timing and bite rates.")
        insert_line(text_479, 0, 262, "Bike Everywhere: OFF")
        insert_line(text_479, 0, 263, "Bike Everywhere: ON")
        insert_line(text_479, 0, 264, "Bicycle can be ridden indoors.")
        insert_line(text_479, 0, 265, "Bicycle follows normal area restrictions.")

        special_log_names = {
            220: "Basic Badge", 221: "Toxic Badge", 222: "Insect Badge", 223: "Bolt Badge",
            224: "Quake Badge", 225: "Jet Badge", 226: "Legend Badge", 227: "Wave Badge",
            230: "Spring", 231: "Summer", 232: "Autumn", 233: "Winter",
            240: "Sunday", 241: "Monday", 242: "Tuesday", 243: "Wednesday",
            244: "Thursday", 245: "Friday", 246: "Saturday",
        }
        for tid, label in special_log_names.items():
            insert_line(text_479, 0, tid, f"Recent items received:[NextLine]- {label}")

        a003.files[479] = encode(text_479)
        rom.setFileByName("a/0/0/3", a003.save())

    a012_data = rom.getFileByName("a/0/1/2")
    outdoor_zids: list[int] = []
    cave_zids: list[int] = []
    dark_zids: list[int] = []
    if a012_data is not None:
        a012 = NARC(a012_data)
        z_bytes = a012.files[0]
        for zid in range(len(z_bytes) // 48):
            entry = z_bytes[zid * 48 : (zid + 1) * 48]
            if entry[31] & 0x20:
                outdoor_zids.append(zid)
            if entry[31] & 0x10:
                cave_zids.append(zid)
            if (entry[31] & 0x10) or entry[27] == 12 or (241 <= zid <= 248):
                dark_zids.append(zid)

    a056_data = rom.getFileByName("a/0/5/6")
    if a056_data is not None:
        a056 = NARC(a056_data)
        s1244 = disassemble(a056.files[1244])

        sub6_idx = s1244.find_label("sub6")
        lbl1_8_idx = s1244.find_label("lbl1_8")
        if sub6_idx != -1 and lbl1_8_idx != -1:
            msg_idx = -1
            for i in range(sub6_idx, lbl1_8_idx):
                if s1244.lines[i].type == "command" and s1244.lines[i].parts == ["MsgSystem", 14, 2]:
                    msg_idx = i
                    break
            if msg_idx != -1:
                s1244.lines[msg_idx + 1 : lbl1_8_idx] = [Line("command", ["VMJump", "lbl1_8"])]

        s1244.script_links[1] = "scr1"

        # has_level_cap = bool(options.get("level_cap_type", 0) != 0 or options.get("progressive_level_cap", 0) != 0)

        new_scr1: list[Line] = [
            Line("label", ["scr1"]),
            Line("command", ["StorePartyCountMore", 32800, 0]),
            Line("command", ["WorkCmpConst", 32800, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_phone_exit"]),
            Line("command", ["FieldGetZoneID", 32800]),
            Line("command", ["WorkCmpConst", 32800, 428]),
            Line("command", ["VMJumpIf", 1, "lbl_check_starter_flag"]),
            Line("command", ["VMJump", "lbl_phone_ok"]),
            Line("label", ["lbl_check_starter_flag"]),
            Line("command", ["FlagGet", 2401, 32800]),
            Line("command", ["WorkCmpConst", 32800, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_phone_ok"]),
            Line("label", ["lbl_phone_exit"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_phone_ok"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["WorkSetConst", 32800, 0]),
            Line("label", ["lbl_root_menu"]),
            Line("command", ["MsgSystem", 93, 2]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32800]),
            Line("command", ["ListMenuAdd", 94, 65535, 1]),
            Line("command", ["ListMenuAdd", 120, 65535, 2]),
            Line("command", ["FlagGet", 3040, 32801]),
            Line("command", ["WorkCmpConst", 32801, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_add_seasons"]),
            Line("command", ["VMJump", "lbl_skip_seasons"]),
            Line("label", ["lbl_add_seasons"]),
            Line("command", ["ListMenuAdd", 98, 65535, 3]),
            Line("label", ["lbl_skip_seasons"]),
            Line("command", ["ListMenuAdd", 121, 65535, 4]),
        ]

        # if has_level_cap:
        #     New_scr1.append(Line("command", ["ListMenuAdd", 122, 65535, 5]))  # Level cap

        new_scr1.extend([
            Line("command", ["ListMenuAdd", 170, 65535, 7]),
            Line("command", ["ListMenuAdd", 127, 65535, 6]),
            Line("command", ["ListMenuAdd", 123, 65535, 0]),
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32800, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_pc"]),
            Line("command", ["WorkCmpConst", 32800, 2]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_travel"]),
            Line("command", ["WorkCmpConst", 32800, 3]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_seasons"]),
            Line("command", ["WorkCmpConst", 32800, 4]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_check_log"]),
            # Line("command", ["WorkCmpConst", 32800, 5]),
            # Line("command", ["VMJumpIf", 1, "lbl_menu_level_cap"]),
            Line("command", ["WorkCmpConst", 32800, 6]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_modifiers"]),
            Line("command", ["WorkCmpConst", 32800, 7]),
            Line("command", ["VMJumpIf", 1, "lbl_menu_days"]),
            Line("command", ["WorkSetConst", 32800, 0]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_menu_pc"]),
            Line("command", ["VMCall", "sub6"]),
            Line("command", ["VMJump", "lbl_root_menu"]),

            Line("label", ["lbl_menu_travel"]),
            Line("command", ["VMCall", "sub_travel"]),
            Line("command", ["VMJump", "lbl_root_menu"]),

            Line("label", ["lbl_menu_seasons"]),
            Line("command", ["VMCall", "sub_seasons_menu"]),
            Line("command", ["VMJump", "lbl_root_menu"]),

            Line("label", ["lbl_menu_days"]),
            Line("command", ["VMCall", "sub_days_menu"]),
            Line("command", ["VMJump", "lbl_root_menu"]),

            Line("label", ["lbl_menu_check_log"]),
            Line("command", ["VMCall", "sub_check_log"]),
            Line("command", ["VMJump", "lbl_root_menu"]),

            # Line("label", ["lbl_menu_level_cap"]),
            # Line("command", ["VMCall", "sub_level_cap"]),
            # Line("command", ["VMJump", "lbl_root_menu"]),

            Line("label", ["lbl_menu_modifiers"]),
            Line("command", ["VMCall", "sub_modifiers"]),
            Line("command", ["VMJump", "lbl_root_menu"]),
        ])

        sub_travel: list[Line] = [
            Line("label", ["sub_travel"]),
            Line("command", ["MsgSystem", 120, 2]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32784]),
            Line("command", ["ListMenuAdd", 124, 65535, 1]),  # Teleport
            Line("command", ["ListMenuAdd", 125, 65535, 2]),  # Dig
            # TESTING: always show Fly menu option
            Line("command", ["ListMenuAdd", 126, 65535, 3]),  # Fly
            Line("command", ["CheckItemBagNumber", 397, 1, 32800]),  # TM70 Flash
            Line("command", ["WorkCmpConst", 32800, 1]),
            Line("command", ["VMJumpIf", 5, "lbl_travel_no_flash"]),
            Line("command", ["ListMenuAdd", 212, 65535, 4]),  # Flash
            Line("label", ["lbl_travel_no_flash"]),
            Line("command", ["ListMenuAdd", 166, 65535, 0]),  # Cancel
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32784, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_travel_tp"]),
            Line("command", ["WorkCmpConst", 32784, 2]),
            Line("command", ["VMJumpIf", 1, "lbl_travel_dig"]),
            Line("command", ["WorkCmpConst", 32784, 3]),
            Line("command", ["VMJumpIf", 1, "lbl_travel_fly"]),
            Line("command", ["WorkCmpConst", 32784, 4]),
            Line("command", ["VMJumpIf", 1, "lbl_travel_flash"]),
            Line("command", ["VMReturn"]),

            Line("label", ["lbl_travel_flash"]),
            Line("command", ["VMCall", "sub_check_dark"]),
            Line("command", ["WorkCmpConst", 32801, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_flash_exec"]),
            Line("command", ["MsgSystem", 133, 2]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["VMJump", "sub_travel"]),

            Line("label", ["lbl_flash_exec"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1350]),
            Line("command", ["FieldSetWeather", 0, 0]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_travel_tp"]),
            Line("command", ["VMCall", "sub_check_outdoors"]),
            Line("command", ["WorkCmpConst", 32801, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_tp_exec"]),
            Line("command", ["MsgSystem", 133, 2]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["VMJump", "sub_travel"]),

            Line("label", ["lbl_tp_exec"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1350]),
            Line("command", ["VMSleep", 8]),
            Line("command", ["MapChangeFlyWarp", 0]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_travel_dig"]),
            Line("command", ["VMCall", "sub_check_caves"]),
            Line("command", ["WorkCmpConst", 32801, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_dig_exec"]),
            Line("command", ["MsgSystem", 133, 2]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["VMJump", "sub_travel"]),

            Line("label", ["lbl_dig_exec"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1350]),
            Line("command", ["VMSleep", 8]),
            Line("command", ["MapChangeFlyWarp", 1]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_travel_fly"]),
            Line("command", ["VMCall", "sub_check_outdoors"]),
            Line("command", ["WorkCmpConst", 32801, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_fly_exec"]),
            Line("command", ["MsgSystem", 133, 2]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["VMJump", "sub_travel"]),

            Line("label", ["lbl_fly_exec"]),
            Line("command", ["MsgSystem", 134, 2]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32808]),
        ]

        # TESTING: always show all fly locations
        for town_id, flag_id, text_id, _ in fly_data:
            sub_travel.append(
                Line("command", ["ListMenuAdd", text_id, 65535, town_id])
            )

        sub_travel.extend([
            Line("command", ["ListMenuAdd", 166, 65535, 0]),
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32808, 0]),
            Line("command", ["VMJumpIf", 1, "sub_travel"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1350]),
            Line("command", ["VMSleep", 8]),
        ])

        for town_id, _, _, coords in fly_data:
            sub_travel.extend([
                Line("command", ["WorkCmpConst", 32808, town_id]),
                Line("command", ["VMJumpIf", 1, f"lbl_fly_to_{town_id}"]),
            ])

        sub_travel.append(Line("command", ["VMReturn"]))

        for town_id, _, _, coords in fly_data:
            warp_cmd = (
                Line("command", ["MapChangeWarpRail", 28, 3, 1, 8, 1])
                if coords[0] == 28
                else Line("command", ["TeleportWarp", coords[0], coords[1], coords[2], coords[3]])
            )
            sub_travel.extend([
                Line("label", [f"lbl_fly_to_{town_id}"]),
                warp_cmd,
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
            ])

        sub_check_outdoors: list[Line] = [
            Line("label", ["sub_check_outdoors"]),
            Line("command", ["FieldGetZoneID", 32800]),
            Line("command", ["WorkSetConst", 32801, 0]),
        ]
        for zid in outdoor_zids:
            sub_check_outdoors.extend([
                Line("command", ["WorkCmpConst", 32800, zid]),
                Line("command", ["VMJumpIf", 1, "lbl_is_outdoor"]),
            ])
        sub_check_outdoors.extend([
            Line("command", ["VMReturn"]),
            Line("label", ["lbl_is_outdoor"]),
            Line("command", ["WorkSetConst", 32801, 1]),
            Line("command", ["VMReturn"]),
        ])

        sub_check_caves: list[Line] = [
            Line("label", ["sub_check_caves"]),
            Line("command", ["FieldGetZoneID", 32800]),
            Line("command", ["WorkSetConst", 32801, 0]),
        ]
        for zid in cave_zids:
            sub_check_caves.extend([
                Line("command", ["WorkCmpConst", 32800, zid]),
                Line("command", ["VMJumpIf", 1, "lbl_is_cave"]),
            ])
        sub_check_caves.extend([
            Line("command", ["VMReturn"]),
            Line("label", ["lbl_is_cave"]),
            Line("command", ["WorkSetConst", 32801, 1]),
            Line("command", ["VMReturn"]),
        ])

        sub_check_dark: list[Line] = [
            Line("label", ["sub_check_dark"]),
            Line("command", ["FieldGetZoneID", 32800]),
            Line("command", ["WorkSetConst", 32801, 0]),
        ]
        for zid in dark_zids:
            sub_check_dark.extend([
                Line("command", ["WorkCmpConst", 32800, zid]),
                Line("command", ["VMJumpIf", 1, "lbl_is_dark"]),
            ])
        sub_check_dark.extend([
            Line("command", ["VMReturn"]),
            Line("label", ["lbl_is_dark"]),
            Line("command", ["WorkSetConst", 32801, 1]),
            Line("command", ["VMReturn"]),
        ])

        # sub_level_cap: list[line] = [
        #     Line("label", ["sub_level_cap"]),
        #     Line("command", ["StackPush", 32800]),
        #     Line("command", ["WorkSet", 32800, 16797]),
        #     Line("command", ["WordSetNumber", 0, 32800, 3]),
        #     Line("command", ["MsgSystem", 150, 2]),
        #     Line("command", ["InputWaitLast"]),
        #     Line("command", ["MsgSystemClose"]),
        #     Line("command", ["StackPop", 32800]),
        #     Line("command", ["VMReturn"]),
        # ]

        sub_check_log: list[Line] = [
            Line("label", ["sub_check_log"]),
            Line("command", ["StackPush", 32800]),
            Line("command", ["WorkCmpConst", 16801, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_log_empty"]),
        ]
        for slot_idx, var_id in enumerate((16801, 16802, 16803, 16804, 16805)):
            lbl_item = f"lbl_log_slot_{slot_idx}_item"
            lbl_next = f"lbl_log_slot_{slot_idx}_next"
            sub_check_log.extend([
                Line("command", ["WorkCmpConst", var_id, 0]),
                Line("command", ["VMJumpIf", 1, "lbl_log_done"]),
                Line("command", ["WorkSet", 32800, var_id]),
                Line("command", ["WorkCmpConst", 32800, 1000]),
                Line("command", ["VMJumpIf", 0, lbl_item]),  # < 1000 -> real item ID
                Line("command", ["WorkSetConst", 32801, 780]),
                Line("command", ["WorkSub", 32800, 32801]),
                Line("command", ["MsgSystem", 32800, 2]),
                Line("command", ["VMJump", lbl_next]),
                Line("label", [lbl_item]),
                Line("command", ["WordSetItemName", 0, 32800]),
                Line("command", ["MsgSystem", 151, 2]),
                Line("label", [lbl_next]),
                Line("command", ["InputWaitLast"]),
            ])
        sub_check_log.extend([
            Line("command", ["VMJump", "lbl_log_done"]),
            Line("label", ["lbl_log_empty"]),
            Line("command", ["MsgSystem", 152, 2]),
            Line("command", ["InputWaitLast"]),
            Line("label", ["lbl_log_done"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkSetConst", 16801, 0]),
            Line("command", ["WorkSetConst", 16802, 0]),
            Line("command", ["WorkSetConst", 16803, 0]),
            Line("command", ["WorkSetConst", 16804, 0]),
            Line("command", ["WorkSetConst", 16805, 0]),
            Line("command", ["StackPop", 32800]),
            Line("command", ["VMReturn"]),
        ])

        # Seasons menu: dynamically show unlocked seasons from flags 3041..3044
        sub_seasons_menu: list[Line] = [
            Line("label", ["sub_seasons_menu"]),
            Line("command", ["StackPush", 32800]),
            Line("command", ["ListMenuInitTR", 31, 10, 0, 0, 32808]),
        ]
        for s_idx, s_name_id in enumerate(range(100, 104)):
            sub_seasons_menu.extend([
                Line("command", ["FlagGet", 3041 + s_idx, 32801]),
                Line("command", ["WorkCmpConst", 32801, 1]),
                Line("command", ["VMJumpIf", 1, f"lbl_add_season_{s_idx}"]),
                Line("command", ["VMJump", f"lbl_skip_season_{s_idx}"]),
                Line("label", [f"lbl_add_season_{s_idx}"]),
                Line("command", ["ListMenuAdd", s_name_id, 65535, s_idx]),
                Line("label", [f"lbl_skip_season_{s_idx}"]),
            ])

        sub_seasons_menu.extend([
            Line("command", ["ListMenuAdd", 166, 65535, 99]),
            Line("command", ["MsgSystem", 99, 0]),
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32808, 99]),
            Line("command", ["VMJumpIf", 1, "lbl_seasons_back"]),
            Line("command", ["WorkCmpConst", 32808, 4]),
            Line("command", ["VMJumpIf", 2, "lbl_seasons_back"]),
            Line("command", ["WorkSet", 16800, 32808]),
            Line("command", ["WorkSetConst", 32800, 104]),
            Line("command", ["WorkAdd", 32800, 16800]),
            Line("command", ["MsgSystem", 32800, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("label", ["lbl_seasons_back"]),
            Line("command", ["StackPop", 32800]),
            Line("command", ["VMReturn"]),
        ])

        sub_days_menu: list[Line] = [
            Line("label", ["sub_days_menu"]),
            Line("command", ["StackPush", 32800]),
            Line("command", ["ListMenuInitTR", 31, 10, 0, 0, 32808]),
        ]
        for d_idx, d_name_id in enumerate(range(172, 179)):
            sub_days_menu.extend([
                Line("command", ["FlagGet", 3045 + d_idx, 32801]),
                Line("command", ["WorkCmpConst", 32801, 1]),
                Line("command", ["VMJumpIf", 1, f"lbl_add_day_{d_idx}"]),
                Line("command", ["VMJump", f"lbl_skip_day_{d_idx}"]),
                Line("label", [f"lbl_add_day_{d_idx}"]),
                Line("command", ["ListMenuAdd", d_name_id, 65535, d_idx]),
                Line("label", [f"lbl_skip_day_{d_idx}"]),
            ])

        sub_days_menu.extend([
            Line("command", ["ListMenuAdd", 166, 65535, 99]),
            Line("command", ["MsgSystem", 171, 0]),
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32808, 99]),
            Line("command", ["VMJumpIf", 1, "lbl_days_back"]),
            Line("command", ["WorkCmpConst", 32808, 7]),
            Line("command", ["VMJumpIf", 2, "lbl_days_back"]),
            Line("command", ["WorkSet", 16799, 32808]),
            Line("command", ["WorkSetConst", 32800, 180]),
            Line("command", ["WorkAdd", 32800, 16799]),
            Line("command", ["MsgSystem", 32800, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgSystemClose"]),
            Line("label", ["lbl_days_back"]),
            Line("command", ["StackPop", 32800]),
            Line("command", ["VMReturn"]),
        ])

        blind_trainers_opt = 1 if bool(options.get("blind_trainers", False)) else 2
        hold_a_turbo_opt = 1 if bool(options.get("hold_a_turbo", False)) else 2
        auto_run_opt = 1 if bool(options.get("auto_run", False)) else 2
        guaranteed_escape_opt = 1 if bool(options.get("guaranteed_escape", False)) else 2
        fast_fishing_opt = 1 if bool(options.get("fast_fishing", True)) else 2
        bike_everywhere_opt = 1 if bool(options.get("bike_everywhere", True)) else 2

        def _toggle_init(var_id: int, default_val: int, tag: str) -> list[Line]:
            return [
                Line("command", ["WorkCmpConst", var_id, 0]),
                Line("command", ["VMJumpIf", 1, f"lbl_init_{tag}"]),
                Line("command", ["VMJump", f"lbl_next_{tag}"]),
                Line("label", [f"lbl_init_{tag}"]),
                Line("command", ["WorkSetConst", var_id, default_val]),
                Line("label", [f"lbl_next_{tag}"]),
            ]

        def _toggle_menu_add(var_id: int, off_tid: int, on_tid: int, choice_id: int, tag: str) -> list[Line]:
            return [
                Line("command", ["WorkCmpConst", var_id, 1]),
                Line("command", ["VMJumpIf", 1, f"lbl_add_{tag}_on"]),
                Line("command", ["ListMenuAdd", off_tid, 65535, choice_id]),
                Line("command", ["VMJump", f"lbl_add_{tag}_done"]),
                Line("label", [f"lbl_add_{tag}_on"]),
                Line("command", ["ListMenuAdd", on_tid, 65535, choice_id]),
                Line("label", [f"lbl_add_{tag}_done"]),
            ]

        def _toggle_handler(var_id: int, on_msg: int, off_msg: int, tag: str) -> list[Line]:
            return [
                Line("label", [f"lbl_mod_{tag}"]),
                Line("command", ["WorkCmpConst", var_id, 1]),
                Line("command", ["VMJumpIf", 1, f"lbl_{tag}_off"]),
                Line("command", ["WorkSetConst", var_id, 1]),
                Line("command", ["MsgSystem", on_msg, 0]),
                Line("command", ["InputWaitLast"]),
                Line("command", ["MsgSystemClose"]),
                Line("command", ["VMJump", "lbl_mod_root"]),
                Line("label", [f"lbl_{tag}_off"]),
                Line("command", ["WorkSetConst", var_id, 2]),
                Line("command", ["MsgSystem", off_msg, 0]),
                Line("command", ["InputWaitLast"]),
                Line("command", ["MsgSystemClose"]),
                Line("command", ["VMJump", "lbl_mod_root"]),
            ]

        sub_modifiers: list[Line] = [
            Line("label", ["sub_modifiers"]),
            Line("command", ["StackPush", 32800]),
            Line("label", ["lbl_mod_root"]),
            *_toggle_init(16794, blind_trainers_opt, "blind"),
            *_toggle_init(16795, hold_a_turbo_opt, "turbo"),
            *_toggle_init(16807, auto_run_opt, "autorun"),
            *_toggle_init(16808, guaranteed_escape_opt, "escape"),
            *_toggle_init(16809, fast_fishing_opt, "fishing"),
            *_toggle_init(16810, bike_everywhere_opt, "bike"),
            Line("command", ["WorkCmpConst", 16792, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_init_catch"]),
            Line("command", ["VMJump", "lbl_check_init_exp"]),
            Line("label", ["lbl_init_catch"]),
            Line("command", ["WorkSetConst", 16792, 1]),
            Line("label", ["lbl_check_init_exp"]),
            Line("command", ["WorkCmpConst", 16793, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_init_exp"]),
            Line("command", ["VMJump", "lbl_init_done"]),
            Line("label", ["lbl_init_exp"]),
            Line("command", ["WorkSetConst", 16793, 1]),
            Line("label", ["lbl_init_done"]),
            Line("command", ["MsgSystem", 127, 2]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32800]),

            *_toggle_menu_add(16794, 187, 210, 1, "blind"),
            *_toggle_menu_add(16795, 188, 211, 2, "turbo"),
            *_toggle_menu_add(16807, 250, 251, 6, "autorun"),
            *_toggle_menu_add(16808, 254, 255, 7, "escape"),
            *_toggle_menu_add(16809, 258, 259, 8, "fishing"),
            *_toggle_menu_add(16810, 262, 263, 9, "bike"),

            Line("command", ["ListMenuAdd", 167, 65535, 3]),  # Catch rate
            Line("command", ["ListMenuAdd", 168, 65535, 4]),  # exp rate
            Line("command", ["ListMenuAdd", 189, 65535, 5]),  # log filter
            Line("command", ["ListMenuAdd", 166, 65535, 0]),  # cancel
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32800, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_blind"]),
            Line("command", ["WorkCmpConst", 32800, 2]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_turbo"]),
            Line("command", ["WorkCmpConst", 32800, 6]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_autorun"]),
            Line("command", ["WorkCmpConst", 32800, 7]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_escape"]),
            Line("command", ["WorkCmpConst", 32800, 8]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_fishing"]),
            Line("command", ["WorkCmpConst", 32800, 9]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_bike"]),
            Line("command", ["WorkCmpConst", 32800, 3]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_catch"]),
            Line("command", ["WorkCmpConst", 32800, 4]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_exp"]),
            Line("command", ["WorkCmpConst", 32800, 5]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_filter"]),
            Line("command", ["StackPop", 32800]),
            Line("command", ["VMReturn"]),

            *_toggle_handler(16794, 190, 191, "blind"),
            *_toggle_handler(16795, 192, 193, "turbo"),
            *_toggle_handler(16807, 252, 253, "autorun"),
            *_toggle_handler(16808, 256, 257, "escape"),
            *_toggle_handler(16809, 260, 261, "fishing"),
            *_toggle_handler(16810, 264, 265, "bike"),

            Line("label", ["lbl_mod_catch"]),
            Line("command", ["WorkCmpConst", 16792, 255]),
            Line("command", ["VMJumpIf", 1, "lbl_catch_disp_guar"]),
            Line("command", ["WorkGet", 32800, 16792]),
            Line("command", ["WordSetNumber", 0, 32800, 2]),
            Line("command", ["MsgSystem", 160, 0]),
            Line("command", ["VMJump", "lbl_catch_menu"]),
            Line("label", ["lbl_catch_disp_guar"]),
            Line("command", ["MsgSystem", 197, 0]),
            Line("label", ["lbl_catch_menu"]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32800]),
            Line("command", ["ListMenuAdd", 200, 65535, 1]),   # 1x
            Line("command", ["ListMenuAdd", 201, 65535, 2]),   # 2x
            Line("command", ["ListMenuAdd", 202, 65535, 3]),   # 3x
            Line("command", ["ListMenuAdd", 203, 65535, 5]),   # 5x
            Line("command", ["ListMenuAdd", 204, 65535, 10]),  # 10x
            Line("command", ["ListMenuAdd", 205, 65535, 255]), # guaranteed
            Line("command", ["ListMenuAdd", 166, 65535, 0]),   # cancel
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32800, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_root"]),
            Line("command", ["WorkGet", 16792, 32800]),
            Line("command", ["VMJump", "lbl_mod_root"]),

            Line("label", ["lbl_mod_exp"]),
            Line("command", ["WorkGet", 32800, 16793]),
            Line("command", ["WordSetNumber", 0, 32800, 2]),
            Line("command", ["MsgSystem", 161, 0]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32800]),
            Line("command", ["ListMenuAdd", 200, 65535, 1]),   # 1x
            Line("command", ["ListMenuAdd", 201, 65535, 2]),   # 2x
            Line("command", ["ListMenuAdd", 202, 65535, 3]),   # 3x
            Line("command", ["ListMenuAdd", 203, 65535, 5]),   # 5x
            Line("command", ["ListMenuAdd", 204, 65535, 10]),  # 10x
            Line("command", ["ListMenuAdd", 166, 65535, 0]),   # cancel
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32800, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_root"]),
            Line("command", ["WorkGet", 16793, 32800]),
            Line("command", ["VMJump", "lbl_mod_root"]),

            Line("label", ["lbl_mod_filter"]),
            Line("command", ["WorkCmpConst", 16791, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_filter_disp_0"]),
            Line("command", ["WorkCmpConst", 16791, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_filter_disp_1"]),
            Line("command", ["MsgSystem", 196, 0]),
            Line("command", ["VMJump", "lbl_filter_menu"]),
            Line("label", ["lbl_filter_disp_0"]),
            Line("command", ["MsgSystem", 194, 0]),
            Line("command", ["VMJump", "lbl_filter_menu"]),
            Line("label", ["lbl_filter_disp_1"]),
            Line("command", ["MsgSystem", 195, 0]),
            Line("label", ["lbl_filter_menu"]),
            Line("command", ["ListMenuInitTR", 31, 1, 0, 1, 32800]),
            Line("command", ["ListMenuAdd", 206, 65535, 0]),   # Progression only
            Line("command", ["ListMenuAdd", 207, 65535, 1]),   # progression + useful
            Line("command", ["ListMenuAdd", 208, 65535, 2]),   # all checks
            Line("command", ["ListMenuAdd", 166, 65535, 99]),  # cancel
            Line("command", ["ListMenuShow2"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["WorkCmpConst", 32800, 99]),
            Line("command", ["VMJumpIf", 1, "lbl_mod_root"]),
            Line("command", ["WorkSet", 16791, 32800]),
            Line("command", ["VMJump", "lbl_mod_root"]),
        ]

        s1244.lines.extend(new_scr1)
        s1244.lines.extend(sub_travel)
        s1244.lines.extend(sub_check_outdoors)
        s1244.lines.extend(sub_check_caves)
        s1244.lines.extend(sub_check_dark)
        # s1244.lines.extend(sub_level_cap)
        s1244.lines.extend(sub_check_log)
        s1244.lines.extend(sub_seasons_menu)
        s1244.lines.extend(sub_days_menu)
        s1244.lines.extend(sub_modifiers)





        a056.files[1244] = bytes(assemble(s1244))

        if not options.get("living_room_starter", True):
            starting_day = options.get("starting_day", 0)
            starting_season = options.get("starting_season", 0)
            blind_trainers = 1 if bool(options.get("blind_trainers", False)) else 2
            hold_a_turbo = 1 if bool(options.get("hold_a_turbo", False)) else 2
            auto_run = 1 if bool(options.get("auto_run", False)) else 2
            guaranteed_escape = 1 if bool(options.get("guaranteed_escape", False)) else 2
            fast_fishing = 1 if bool(options.get("fast_fishing", True)) else 2
            bike_everywhere = 1 if bool(options.get("bike_everywhere", True)) else 2
            catch_mult = 255 if bool(options.get("guaranteed_catch", False)) else int(options.get("catch_rate_multiplier", 1))
            if catch_mult == 0:
                catch_mult = 1
            exp_mult = int(options.get("exp_multiplier", 1))
            log_filter = int(options.get("check_log_filter", 0))
            s856 = disassemble(a056.files[856])
            scr16_856 = s856.find_label("scr16")
            if scr16_856 != -1:
                init_cmds = [
                    Line("command", ["FlagSet", 2488]),
                    Line("command", ["WorkSetConst", 16791, log_filter]),
                    Line("command", ["WorkSetConst", 16792, catch_mult]),
                    Line("command", ["WorkSetConst", 16793, exp_mult]),
                    Line("command", ["WorkSetConst", 16794, blind_trainers]),
                    Line("command", ["WorkSetConst", 16795, hold_a_turbo]),
                    Line("command", ["WorkSetConst", 16807, auto_run]),
                    Line("command", ["WorkSetConst", 16808, guaranteed_escape]),
                    Line("command", ["WorkSetConst", 16809, fast_fishing]),
                    Line("command", ["WorkSetConst", 16810, bike_everywhere]),
                    Line("command", ["WorkSetConst", 16799, starting_day]),
                    Line("command", ["WorkSetConst", 16800, starting_season]),
                    Line("command", ["FlagSet", 3040]),
                    Line("command", ["FlagSet", 3041 + starting_season]),
                    Line("command", ["FlagSet", 3045 + starting_day]),
                ]
                for cmd_i, cmd in enumerate(init_cmds):
                    s856.lines.insert(scr16_856 + 1 + cmd_i, cmd)
                a056.files[856] = bytes(assemble(s856))

        rom.setFileByName("a/0/5/6", a056.save())

    def _encode_thumb_bl(src_addr: int, dst_addr: int) -> bytes:
        rel = (dst_addr - (src_addr + 4)) & 0x7FFFFF
        hw1 = 0xF000 | ((rel >> 12) & 0x7FF)
        hw2 = 0xF800 | ((rel >> 1) & 0x7FF)
        return hw1.to_bytes(2, "little") + hw2.to_bytes(2, "little")

    ov_table = rom.loadArm9Overlays()

    if 12 in ov_table:
        ov12 = ov_table[12]
        ov12_data = bytearray(ov12.data)

        # Override weekday getter (ov12 + 0x12DB0) with var 16799 (EventWork + 0x33E)
        dow_off = 0x12DB0
        dow_patch = (
            b"\x08\xb5"
            + _encode_thumb_bl(ov12.ramAddress + dow_off + 0x02, 0x02017394)
            + b"\xcf\x21"
            + b"\x89\x00"
            + b"\x02\x31"
            + b"\x40\x5a"
            + b"\x08\xbd"
        )
        assert len(dow_patch) == 16
        ov12_data[dow_off : dow_off + len(dow_patch)] = dow_patch

        # Enable DiscoverOnVisit (|= 0x02 at +2) in respawn_zone_info (ov12 + 0x1bf7c, 20 bytes/entry
        # for Castelia (4), Driftveil (6), Opelucid (9), Lacunosa (10), Virbank (21), Victory Road (55):
        respawn_table_off = 0x1BF7C
        for entry_idx in (4, 6, 9, 10, 21, 55):
            flag_byte_off = respawn_table_off + entry_idx * 20 + 2
            if flag_byte_off < len(ov12_data):
                ov12_data[flag_byte_off] |= 0x02

        ov12.data = bytes(ov12_data)
        rom.files[ov12.fileID] = ov12.save(compress=ov12.compressed)

    if 36 in ov_table:
        ov36 = ov_table[36]
        ov36_data = bytearray(ov36.data)

        cmd28a_off = 0x28C64
        cmd28a_ram = ov36.ramAddress + cmd28a_off
        cmd28a_patch = (
            b"\x38\xb5"
            b"\x0d\x1c"
            + _encode_thumb_bl(cmd28a_ram + 0x04, 0x020159E8)
            + b"\x04\x1c"
            + b"\x28\x1c"
            + _encode_thumb_bl(cmd28a_off + 0x0C, -0x2A494)
            + b"\x05\x1c"
            + b"\x00\x2c"
            + b"\x02\xd1"
            + _encode_thumb_bl(cmd28a_off + 0x16, -0x18AC)
            + b"\x01\xe0"
            + _encode_thumb_bl(cmd28a_off + 0x1C, -0x1900)
            + b"\x04\x1c"
            + b"\x28\x1c"
            + _encode_thumb_bl(cmd28a_ram + 0x24, 0x02016AE8)
            + b"\x21\x1c"
            + _encode_thumb_bl(cmd28a_ram + 0x2A, 0x02016D68)
            + b"\x01\x20"
            + b"\x38\xbd"
            + b"\x00\x00"
        )
        ov36_data[cmd28a_off : cmd28a_off + len(cmd28a_patch)] = cmd28a_patch

        # Patch button-to-action mapper in ov36 + 0x278a
        ov36_data[0x278A:0x2798] = (
            b"\x01\x40"
            b"\x11\x43"
            b"\xe9\x63"
            b"\xaa\x6a"
            b"\x81\x21"
            b"\xc9\x00"
            b"\x11\x42"
        )

        tramp_off = 0x28C98
        tramp_ram = ov36.ramAddress + tramp_off
        field_start_script_addr = ov_table[12].ramAddress + 0x32AC
        open_x_menu_addr = ov_table[12].ramAddress + 0xA3E4

        tramp_patch = (
            b"\x10\xb5"
            b"\x06\x4b"
            b"\x1b\x88"
            b"\x1b\x09"
            b"\x02\xd3"
            + _encode_thumb_bl(tramp_ram + 0x0A, open_x_menu_addr)
            + b"\x10\xbd"
            + b"\x13\x1c"
            + b"\x03\x49"
            + b"\x00\x22"
            + _encode_thumb_bl(tramp_ram + 0x16, field_start_script_addr)
            + b"\x10\xbd"
            + b"\x30\x01\x00\x04"
            + (10091).to_bytes(4, "little")
        )
        ov36_data[tramp_off : tramp_off + len(tramp_patch)] = tramp_patch
        ov36_data[0x21F0:0x21F4] = _encode_thumb_bl(ov36.ramAddress + 0x21F0, tramp_ram)
        ov36_data[0x2652:0x2656] = _encode_thumb_bl(ov36.ramAddress + 0x2652, tramp_ram)

        ov36.data = bytes(ov36_data)
        rom.files[ov36.fileID] = ov36.save(compress=ov36.compressed)

    rom.arm9OverlayTable = saveOverlayTable(ov_table)

    # ARM9 season engine hook
    try:
        from ..nds_compat import codeCompression
    except (ImportError, ValueError):
        try:
            from worlds.pokemon_b2w2.nds_compat import codeCompression
        except (ImportError, ValueError):
            from nds_compat import codeCompression

    season_rt_addr = 0x02034F98 if is_white2 else 0x02034F6C

    arm9 = getattr(rom, "_decompressed_arm9", None)
    if arm9 is None:
        arm9 = bytearray(codeCompression.decompress(rom.arm9))
        rom._decompressed_arm9 = arm9
    arm9_base = rom.arm9RamAddress  # 0x02004000

    season_rt_patch = (
        b"\x08\xb5"
        + _encode_thumb_bl(season_rt_addr + 0x02, 0x020072FC)
        + b"\x2d\x21"
        + _encode_thumb_bl(season_rt_addr + 0x08, 0x02017A5C)
        + b"\xd0\x21"
        + b"\x89\x00"
        + b"\x40\x5c"
        + b"\xc0\x46"
        + b"\x03\x21"
        + b"\x08\x40"
        + b"\x08\xbd"
    )
    season_rt_off = season_rt_addr - arm9_base
    arm9[season_rt_off : season_rt_off + len(season_rt_patch)] = season_rt_patch
