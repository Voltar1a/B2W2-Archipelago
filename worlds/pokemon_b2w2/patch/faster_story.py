from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..nds_compat import NintendoDSRom


def _make_pwt_skip_cmds(flash_black: bool) -> list:
    from .script_editing import Line

    cmds = [
        Line("command", ["ActorPauseAll"]),
    ]
    if flash_black:
        cmds.append(Line("command", ["FlashBlackInstant"]))
    cmds.extend([
        Line("command", ["MapReplaceSetEvent", 4, 1, 1]),
        Line("command", ["MapReplaceSetEvent", 3, 0, 0]),
        Line("command", ["FlagSet", 894]),
        Line("command", ["FlagSet", 893]),
        Line("command", ["FlagSet", 892]),
        Line("command", ["FlagSet", 891]),
        Line("command", ["WorkSetConst", 16452, 0]),
        Line("command", ["FlagReset", 2441]),
        Line("command", ["FlagReset", 1001]),
        Line("command", ["WorkSetConst", 16693, 2]),
        Line("command", ["FlagReset", 710]),
        Line("command", ["WorkSetConst", 16582, 3]),
        Line("command", ["FlagSet", 711]),
        Line("command", ["FlagSet", 712]),
        Line("command", ["FlagSet", 890]),
        Line("command", ["FlagReset", 830]),
        Line("command", ["FlagReset", 831]),
        Line("command", ["FlagReset", 829]),
        Line("command", ["WorkSetConst", 16624, 1]),
        Line("command", ["HollowRivalSetValue", 1, 15]),
        Line("command", ["HollowRivalSetValue", 2, 3]),
        Line("command", ["RTFinishSubEvents"]),
        Line("command", ["ActorUnlockAll"]),
        Line("command", ["VMHalt"]),
    ])
    return cmds


def apply_faster_story(rom: NintendoDSRom, is_white2: bool, options: dict[str, Any]) -> None:
    """Applies streamlined cutscene skips using native script and overlay edits."""
    skip_catching = options.get("skip_catching_tutorial", True)
    skip_pwt = bool(options.get("skip_pwt", True))
    skip_join = options.get("skip_join_avenue", True)
    skip_cinematics = options.get("skip_cinematic_movies", True)

    if not (skip_catching or skip_pwt or skip_join or skip_cinematics):
        return

    try:
        from ..nds_compat import NARC, saveOverlayTable
    except (ImportError, ValueError):
        try:
            from worlds.pokemon_b2w2.nds_compat import NARC, saveOverlayTable
        except (ImportError, ValueError):
            from nds_compat import NARC, saveOverlayTable

    from .script_editing import Line, assemble, disassemble

    narc_056 = NARC(rom.getFileByName("a/0/5/6"))
    narc_126 = NARC(rom.getFileByName("a/1/2/6")) if skip_join else None

    modified_056 = False
    modified_126 = False

    if skip_catching:
        try:
            s874 = disassemble(narc_056.files[874])
            scr0_874 = s874.find_label("scr0")
            if scr0_874 != -1 and scr0_874 + 1 < len(s874.lines):
                s874.lines[scr0_874 + 1 : scr0_874 + 1] = [
                    Line("command", ["WorkSetConst", 16547, 2]),
                    Line("command", ["FlagSet", 738]),
                    Line("command", ["FlagSet", 987]),
                    Line("command", ["FlagReset", 739]),
                    Line("command", ["FlagSet", 744]),
                    Line("command", ["FlagSet", 743]),
                    Line("command", ["FlagReset", 740]),
                    Line("command", ["FlagReset", 803]),
                    Line("command", ["HollowRivalSetValue", 4, 0]),
                    Line("command", ["WorkSetConst", 16545, 8]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ]
                narc_056.files[874] = bytes(assemble(s874))
                modified_056 = True
        except Exception:
            pass

    if skip_pwt:
        try:
            s384 = disassemble(narc_056.files[384])
            scr7_384 = s384.find_label("scr7")
            if scr7_384 != -1:
                s384.lines[scr7_384 + 1 : scr7_384 + 1] = [
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["ActorDelete", 13]),
                    Line("command", ["MapReplaceSetEvent", 4, 1, 1]),
                    Line("command", ["MapReplaceSetEvent", 3, 0, 0]),
                    Line("command", ["FlagSet", 894]),
                    Line("command", ["FlagSet", 893]),
                    Line("command", ["FlagSet", 892]),
                    Line("command", ["FlagSet", 891]),
                    Line("command", ["FlagReset", 890]),
                    Line("command", ["WorkSetConst", 16582, 2]),
                    Line("command", ["WorkSetConst", 16452, 0]),
                    Line("command", ["FlagReset", 2441]),
                    Line("command", ["FlagReset", 1001]),
                    Line("command", ["HollowRivalSetValue", 1, 14]),
                    Line("command", ["HollowRivalSetValue", 2, 2]),
                    Line("command", ["WorkSetConst", 16693, 2]),
                    Line("command", ["ActorAdd", 17]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ]
                narc_056.files[384] = bytes(assemble(s384))
                modified_056 = True
        except Exception:
            pass

    if skip_join and narc_126 is not None:
        try:
            s124 = disassemble(narc_056.files[124])
            new_124 = [
                l for l in s124.lines
                if not (l.type == "command" and l.parts == ["FlagSet", 242])
            ]
            if len(new_124) != len(s124.lines):
                s124.lines = new_124
                narc_056.files[124] = bytes(assemble(s124))
                modified_056 = True
        except Exception:
            pass

        if len(narc_126.files) > 66:
            d66 = bytearray(narc_126.files[66])
            if len(d66) >= 0x4BC:
                dest_zone = 551 if is_white2 else 326
                d66[0x4B8:0x4BC] = dest_zone.to_bytes(2, "little") + (6).to_bytes(2, "little")
                narc_126.files[66] = bytes(d66)
                modified_126 = True

        for ev_id in (482, 497):
            if len(narc_126.files) > ev_id:
                d_gate = bytearray(narc_126.files[ev_id])
                if len(d_gate) >= 8:
                    furn_c, npc_c, warp_c = d_gate[4], d_gate[5], d_gate[6]
                    warp_off = 8 + furn_c * 0x14 + npc_c * 0x24 + 6 * 0x14
                    if warp_c > 6 and warp_off + 4 <= len(d_gate):
                        d_gate[warp_off : warp_off + 4] = (62).to_bytes(2, "little") + (0).to_bytes(2, "little")
                        narc_126.files[ev_id] = bytes(d_gate)
                        modified_126 = True

    if modified_056:
        rom.setFileByName("a/0/5/6", narc_056.save())
    if modified_126 and narc_126 is not None:
        rom.setFileByName("a/1/2/6", narc_126.save())

    if skip_cinematics:
        ov_table = rom.loadArm9Overlays()
        table_modified = False

        if 35 in ov_table:
            try:
                ov35 = ov_table[35]
                ov35_data = bytearray(ov35.data)
                if len(ov35_data) > 6:
                    ov35_data[6] = 0x0A
                    ov35.data = bytes(ov35_data)
                    rom.files[ov35.fileID] = ov35.save(compress=ov35.compressed)
                    table_modified = True
            except Exception:
                pass

        if table_modified:
            rom.arm9OverlayTable = saveOverlayTable(ov_table)
