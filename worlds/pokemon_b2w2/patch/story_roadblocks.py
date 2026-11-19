from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..nds_compat import NintendoDSRom


def _replace_scr_block(s, scr_name: str, new_lines: list) -> None:
    idx = s.find_label(scr_name)
    if idx == -1:
        return
    next_idx = len(s.lines)
    for i in range(idx + 1, len(s.lines)):
        if s.lines[i].type == "label" and not s.lines[i].parts[0].startswith("lbl") and not s.lines[i].parts[0].startswith("act"):
            next_idx = i
            break
    s.lines[idx:next_idx] = new_lines


def _inject_bag_key_gate(
    scr,
    caught_flag: int,
    var_id: int,
    item_id: int,
    anchor_label: str,
    tag: str,
) -> bool:
    from .script_editing import Line

    idx = scr.find_label(anchor_label)
    if idx == -1:
        return False
    lbl_done = f"lbl_{tag}_done"
    lbl_missing = f"lbl_{tag}_missing"
    scr.lines[idx + 1 : idx + 1] = [
        Line("command", ["StackPushFlag", caught_flag]),
        Line("command", ["StackPushConst", 0]),
        Line("command", ["StackCmp", 1]),
        Line("command", ["VMJumpIf", 255, lbl_done]),
        Line("command", ["StackPush", var_id]),
        Line("command", ["StackPushConst", 2]),
        Line("command", ["StackCmp", 0]),
        Line("command", ["VMJumpIf", 255, lbl_done]),
        Line("command", ["CheckItemBagNumber", item_id, 1, 32804]),
        Line("command", ["StackPush", 32804]),
        Line("command", ["StackPushConst", 1]),
        Line("command", ["StackCmp", 1]),
        Line("command", ["VMJumpIf", 255, lbl_missing]),
        Line("command", ["WorkSetConst", var_id, 1]),
        Line("command", ["VMJump", lbl_done]),
        Line("label", [lbl_missing]),
        Line("command", ["WorkSetConst", var_id, 0]),
        Line("label", [lbl_done]),
    ]
    return True


def apply_story_roadblocks(rom: "NintendoDSRom", is_white2: bool, options: dict[str, Any]) -> None:
    try:
        from ..nds_compat import NARC
    except (ImportError, ValueError):
        try:
            from worlds.pokemon_b2w2.nds_compat import NARC
        except (ImportError, ValueError):
            from nds_compat import NARC

    from .script_editing import disassemble, assemble, Line

    scripts_narc = NARC(rom.getFileByName("a/0/5/6"))
    a126_data = rom.getFileByName("a/1/2/6")
    a126 = NARC(a126_data) if a126_data is not None else None
    modified_scripts = False
    modified_entities = False

    skip_cinematics = bool(options.get("skip_cinematic_movies", True))

    try:
        if a126 is not None and len(a126.files) > 181:
            f181 = bytearray(a126.files[181])
            n_furn = f181[4]
            base = 8 + 20 * n_furn
            cap_offset = base + 36 * 2
            f181[cap_offset + 8 : cap_offset + 10] = (0).to_bytes(2, "little")
            hugh_offset = base + 36 * 3
            f181[hugh_offset + 8 : hugh_offset + 10] = (2801).to_bytes(2, "little")
            a126.files[181] = bytes(f181)
            modified_entities = True

        if len(scripts_narc.files) > 905:
            sf_905 = disassemble(scripts_narc.files[905])
            sf_905.lines = [
                Line("label", ["scr0"]),
                Line("command", ["FlagReset", 723]),
                Line("command", ["FlagSet", 722]),
                Line("command", ["VMHalt"]),
            ]
            scripts_narc.files[905] = bytes(assemble(sf_905))
            modified_scripts = True

        sf_904 = disassemble(scripts_narc.files[904])
        scr2_idx = sf_904.find_label("scr2")
        if scr2_idx != -1:
            new_scr2: list[Line] = [
                Line("label", ["scr2"]),
                Line("command", ["ActorPauseAll"]),
                Line("command", ["PlaySound", 1351]),
                Line("command", ["ActorSetEyeToEye"]),
                Line("command", ["StoreBadge", 32804, 1]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_no_toxic"]),
                Line("command", ["MsgActorEx", 1024, 4, 2, 2, 0]),
                Line("command", ["YesNoWin", 32784]),
                Line("command", ["StackPush", 32784]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl3_5"]),
                Line("command", ["MsgActorEx", 1024, 5, 2, 2, 0]),
                Line("command", ["MsgWinCloseAll"]),
                *(
                    [
                        Line("command", ["BGMFadeOut", 30]),
                        Line("command", ["FadeIntoBlack"]),
                        Line("command", ["Xtransciever7 (0x1A7)"]),
                    ]
                    if skip_cinematics
                    else [
                        Line("command", ["Xtransciever4 (0x1A4)"]),
                        Line("command", ["BGMFadeOut", 30]),
                        Line("command", ["Xtransciever7 (0x1A7)"]),
                        Line("command", ["FieldClose"]),
                        Line("command", ["Call3DDemo", 26, 0]),
                        Line("command", ["FieldOpen"]),
                    ]
                ),
                Line("command", ["FlagSet", 748]),
                Line("command", ["WorkSetConst", 16558, 2]),
                Line("command", ["FlagGet", 2476, 32804]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl3_harlequin_ok"]),
                Line("command", ["WorkSetConst", 16610, 1]),
                Line("command", ["FlagGet", 312, 32804]),
                Line("command", ["WorkAdd", 16610, 32804]),
                Line("command", ["FlagGet", 313, 32804]),
                Line("command", ["WorkAdd", 16610, 32804]),
                Line("command", ["FlagGet", 314, 32804]),
                Line("command", ["WorkAdd", 16610, 32804]),
                Line("label", ["lbl3_harlequin_ok"]),
                Line("command", ["RTReserveScript", 3]),
                Line("command", ["MapChangeCore", 38, 12, 0, 10, 2]),
                Line("command", ["VMJump", "lbl3_6"]),
                Line("label", ["lbl3_5"]),
                Line("command", ["MsgActorEx", 1024, 6, 2, 2, 0]),
                Line("command", ["InputWaitLast"]),
                Line("command", ["MsgWinCloseAll"]),
                Line("command", ["VMJump", "lbl3_6"]),
                Line("label", ["lbl_no_toxic"]),
                Line("command", ["MsgActorEx", 1024, 7, 2, 2, 0]),
                Line("command", ["InputWaitLast"]),
                Line("command", ["MsgWinCloseAll"]),
                Line("label", ["lbl3_6"]),
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
            ]
            _replace_scr_block(sf_904, "scr2", new_scr2)
            _replace_scr_block(sf_904, "scr3", [
                Line("label", ["scr3"]),
                Line("command", ["VMJump", "scr2"]),
            ])
            scripts_narc.files[904] = bytes(assemble(sf_904))
            modified_scripts = True
    except Exception:
        pass

    try:
        if len(scripts_narc.files) > 60:
            sf_60 = disassemble(scripts_narc.files[60])
            _replace_scr_block(sf_60, "scr2", [
                Line("label", ["scr2"]),
                Line("command", ["WorkSetConst", 16564, 2]),
                Line("command", ["FlagSet", 756]),
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
            ])
            scripts_narc.files[60] = bytes(assemble(sf_60))
            modified_scripts = True

        if a126 is not None and len(a126.files) > 482:
            f482 = bytearray(a126.files[482])
            nf, nn, nw, nt = f482[4], f482[5], f482[6], f482[7]
            base = 8 + 20 * nf
            col_off = base + 36 * 15
            f482[col_off + 8 : col_off + 10] = (757).to_bytes(2, "little")
            if nt > 0:
                p_trig = base + 36 * nn + 20 * nw
                f482[p_trig + 2 : p_trig + 4] = (0).to_bytes(2, "little")  # Var_val = 0
            a126.files[482] = bytes(f482)
            modified_entities = True

        sf_652 = disassemble(scripts_narc.files[652])
        scr4_idx = sf_652.find_label("scr4")
        if scr4_idx != -1:
            sf_652.lines[scr4_idx + 2 : scr4_idx + 2] = [
                Line("command", ["StoreBadge", 32804, 2]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_colress_no_badge"]),
                Line("label", ["lbl_colress_vanilla_start"]),
            ]
        _replace_scr_block(sf_652, "scr6", [
            Line("label", ["scr6"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["ActorSetEyeToEye"]),
            Line("command", ["StoreBadge", 32804, 2]),
            Line("command", ["WorkCmpConst", 32804, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_colress_vanilla_start"]),
            Line("command", ["VMJump", "lbl_colress_no_badge"]),
        ])
        sf_652.lines.extend([
            Line("label", ["lbl_colress_no_badge"]),
            Line("command", ["MsgActorEx", 1024, 19, 15, 0, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["PlayerGetGPos", 32801, 32802]),
            Line("command", ["StackPush", 32802]),
            Line("command", ["StackPushConst", 584]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_colress_no_push"]),
            Line("command", ["ActorCmdExec", 255, "act_colress_push_south"]),
            Line("command", ["ActorCmdWait"]),
            Line("label", ["lbl_colress_no_push"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
            Line("label", ["act_colress_push_south"]),
            Line("action", ["WalkS8F", 1]),
            Line("action", ["EndAction", 0]),
        ])
        scripts_narc.files[652] = bytes(assemble(sf_652))
        modified_scripts = True
    except Exception:
        pass

    try:
        if a126 is not None and len(a126.files) > 497:
            f497 = bytearray(a126.files[497])
            nf, nn, nw, nt = f497[4], f497[5], f497[6], f497[7]
            base = 8 + 20 * nf
            col_off = base + 36 * 14
            f497[col_off + 8 : col_off + 10] = (757).to_bytes(2, "little")
            if nt > 0:
                p_trig = base + 36 * nn + 20 * nw
                f497[p_trig + 2 : p_trig + 4] = (0).to_bytes(2, "little")
            a126.files[497] = bytes(f497)
            modified_entities = True

        sf_1102 = disassemble(scripts_narc.files[1102])
        scr1_idx = sf_1102.find_label("scr1")
        if scr1_idx != -1:
            sf_1102.lines[scr1_idx + 2 : scr1_idx + 2] = [
                Line("command", ["StoreBadge", 32804, 2]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_colress_no_badge"]),
                Line("label", ["lbl_colress_vanilla_start"]),
            ]
        _replace_scr_block(sf_1102, "scr3", [
            Line("label", ["scr3"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["ActorSetEyeToEye"]),
            Line("command", ["StoreBadge", 32804, 2]),
            Line("command", ["WorkCmpConst", 32804, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_colress_vanilla_start"]),
            Line("command", ["VMJump", "lbl_colress_no_badge"]),
        ])
        sf_1102.lines.extend([
            Line("label", ["lbl_colress_no_badge"]),
            Line("command", ["MsgActorEx", 1024, 20, 14, 0, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["PlayerGetGPos", 32801, 32802]),
            Line("command", ["StackPush", 32802]),
            Line("command", ["StackPushConst", 578]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_colress_no_push"]),
            Line("command", ["ActorCmdExec", 255, "act_colress_push_south"]),
            Line("command", ["ActorCmdWait"]),
            Line("label", ["lbl_colress_no_push"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
            Line("label", ["act_colress_push_south"]),
            Line("action", ["WalkS8F", 1]),
            Line("action", ["EndAction", 0]),
        ])
        scripts_narc.files[1102] = bytes(assemble(sf_1102))
        modified_scripts = True
    except Exception:
        pass

    try:
        sf_390 = disassemble(scripts_narc.files[390])
        scr0_idx = sf_390.find_label("scr0")
        scr1_idx = sf_390.find_label("scr1")
        if scr0_idx != -1 and scr1_idx != -1:
            sf_390.lines[scr0_idx + 1 : scr1_idx] = [
                Line("command", ["StoreBadge", 32804, 4]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_no_quake"]),
                Line("command", ["FlagSet", 788]),
                Line("command", ["FlagSet", 962]),
                Line("command", ["WorkSetConst", 16594, 1]),
                Line("command", ["VMHalt"]),
                Line("label", ["lbl_no_quake"]),
                Line("command", ["FlagReset", 788]),
                Line("command", ["FlagReset", 962]),
                Line("command", ["VMHalt"]),
            ]
            scripts_narc.files[390] = bytes(assemble(sf_390))
            modified_scripts = True
    except Exception:
        pass

    try:
        sf_222 = disassemble(scripts_narc.files[222])
        scr5_idx = sf_222.find_label("scr5")
        if scr5_idx != -1:
            for i in range(scr5_idx, scr5_idx + 10):
                if sf_222.lines[i].type == "command" and sf_222.lines[i].parts == ["StackPush", 16587]:
                    sf_222.lines[i:i+4] = [
                        Line("command", ["StoreBadge", 32804, 5]),
                        Line("command", ["WorkCmpConst", 32804, 1]),
                        Line("command", ["VMJumpIf", 1, "lbl6_45"]),  # Jump to flight when Jet badge == 1
                    ]
                    break
        if skip_cinematics:
            sf_222.lines = [
                l for l in sf_222.lines
                if not (l.type == "command" and l.parts == ["Call3DDemo", 24, 0])
            ]
        scripts_narc.files[222] = bytes(assemble(sf_222))
        modified_scripts = True
    except Exception:
        pass

    try:
        sf_828 = disassemble(scripts_narc.files[828])
        scr3_idx = sf_828.find_label("scr3")
        if scr3_idx != -1:
            for i in range(scr3_idx, scr3_idx + 10):
                if sf_828.lines[i].type == "command" and sf_828.lines[i].parts == ["StackPush", 16670]:
                    sf_828.lines[i:i+4] = [
                        Line("command", ["StoreBadge", 32804, 6]),
                        Line("command", ["WorkCmpConst", 32804, 1]),
                        Line("command", ["VMJumpIf", 1, "lbl4_4"]), # Jump to welcome when Legend badge == 1
                    ]
                    break
        scr4_idx = sf_828.find_label("scr4")
        if scr4_idx != -1:
            insert_pos = scr4_idx + 2
            sf_828.lines[insert_pos:insert_pos] = [
                Line("command", ["StoreBadge", 32804, 6]),
                Line("command", ["WorkCmpConst", 32804, 1]),
                Line("command", ["VMJumpIf", 1, "lbl_tube_open"]), # Allow passage when Legend badge == 1
            ]
            halt_pos = None
            for j in range(insert_pos, len(sf_828.lines)):
                if sf_828.lines[j].type == "command" and sf_828.lines[j].parts[0] == "VMHalt":
                    halt_pos = j
                    break
            if halt_pos is not None:
                sf_828.lines[halt_pos:halt_pos] = [
                    Line("label", ["lbl_tube_open"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                ]
            scripts_narc.files[828] = bytes(assemble(sf_828))
            modified_scripts = True
    except Exception:
        pass

    try:
        sf_462 = disassemble(scripts_narc.files[462])
        sub1_idx = sf_462.find_label("sub1")
        scr0_idx = sf_462.find_label("scr0")
        if sub1_idx != -1 and scr0_idx != -1:
            sf_462.lines[sub1_idx + 1 : scr0_idx] = [
                Line("command", ["StackPushFlag", 885]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl1_2"]),
                Line("command", ["FlagSet", 364]),
                Line("command", ["ObjInitWarpGPos", 1, 34, 0, 47]),
                Line("command", ["VMJump", "lbl1_3"]),
                Line("label", ["lbl1_2"]),
                Line("command", ["FlagReset", 364]),
                Line("command", ["ObjInitWarpGPos", 2, 34, 0, 47]),
                Line("label", ["lbl1_3"]),
                Line("command", ["VMReturn"]),
            ]
        scr0_idx = sf_462.find_label("scr0")
        scr7_idx = sf_462.find_label("scr7")
        if scr0_idx != -1 and scr7_idx != -1:
            sf_462.lines[scr0_idx + 1 : scr7_idx] = [
                Line("command", ["VMCall", "sub1"]),
                Line("command", ["CheckItemBagNumber", 475, 1, 32804]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_no_card_key"]),
                Line("command", ["FlagSet", 876]),
                Line("command", ["VMJump", "lbl_check_splicers"]),
                Line("label", ["lbl_no_card_key"]),
                Line("command", ["FlagReset", 876]),
                Line("label", ["lbl_check_splicers"]),
                Line("command", ["CheckItemBagNumber", 628, 1, 32804]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_no_splicers"]),
                Line("command", ["FlagSet", 879]),
                Line("command", ["VMJump", "lbl_chasm_done"]),
                Line("label", ["lbl_no_splicers"]),
                Line("command", ["FlagReset", 879]),
                Line("label", ["lbl_chasm_done"]),
                Line("command", ["VMHalt"]),
            ]
        scripts_narc.files[462] = bytes(assemble(sf_462))
        modified_scripts = True
    except Exception:
        pass

    try:
        sf_466 = disassemble(scripts_narc.files[466])
        mod_466 = False
        for sname in ("scr7", "scr8"):
            idx = sf_466.find_label(sname)
            if idx != -1:
                lbl_reset = f"lbl_chasm_sync_reset_{sname}"
                lbl_done = f"lbl_chasm_sync_done_{sname}"
                sf_466.lines[idx + 1 : idx + 1] = [
                    Line("command", ["StackPushFlag", 885]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, lbl_reset]),
                    Line("command", ["FlagSet", 364]),
                    Line("command", ["VMJump", lbl_done]),
                    Line("label", [lbl_reset]),
                    Line("command", ["FlagReset", 364]),
                    Line("label", [lbl_done]),
                ]
                mod_466 = True
        if mod_466:
            scripts_narc.files[466] = bytes(assemble(sf_466))
            modified_scripts = True
    except Exception:
        pass

    try:
        sf_468 = disassemble(scripts_narc.files[468])
        sub1_idx = sf_468.find_label("sub1")
        scr0_idx = sf_468.find_label("scr0")
        if sub1_idx != -1 and scr0_idx != -1:
            sf_468.lines[sub1_idx + 1 : scr0_idx] = [
                Line("command", ["StackPushFlag", 885]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl1_2"]),
                Line("command", ["FlagSet", 364]),
                Line("command", ["ObjInitWarpGPos", 0, 25, 0, 25]),
                Line("command", ["VMJump", "lbl1_3"]),
                Line("label", ["lbl1_2"]),
                Line("command", ["FlagReset", 364]),
                Line("command", ["ObjInitWarpGPos", 1, 25, 0, 25]),
                Line("label", ["lbl1_3"]),
                Line("command", ["VMReturn"]),
            ]
            scripts_narc.files[468] = bytes(assemble(sf_468))
            modified_scripts = True
    except Exception:
        pass

    blind_trainers_enabled = bool(options.get("blind_trainers", False)) if options else False
    gym_sight_scripts = {
        194: ["scr17", "scr18", "scr19", "scr20", "scr21", "scr22", "scr23"],
        126: ["scr3", "scr4", "scr5"],
    }
    for gym_sid, scr_names in gym_sight_scripts.items():
        if len(scripts_narc.files) <= gym_sid:
            continue
        try:
            gs = disassemble(scripts_narc.files[gym_sid])
            gs_mod = False
            for sname in scr_names:
                s_idx = gs.find_label(sname)
                if s_idx == -1:
                    continue
                skip_lbl = f"lbl_blind_skip_{sname}"
                if blind_trainers_enabled:
                    check_lines = [
                        Line("command", ["WorkCmpConst", 16794, 2]),
                        Line("command", ["VMJumpIf", 5, skip_lbl]),
                    ]
                else:
                    check_lines = [
                        Line("command", ["WorkCmpConst", 16794, 1]),
                        Line("command", ["VMJumpIf", 1, skip_lbl]),
                    ]
                gs.lines[s_idx + 1 : s_idx + 1] = check_lines
                gs.lines.extend([
                    Line("label", [skip_lbl]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
                gs_mod = True
            if gs_mod:
                scripts_narc.files[gym_sid] = bytes(assemble(gs))
                modified_scripts = True
        except Exception:
            pass

    # Gate Heatran (magma stone = 458) and Cresselia (lunar wing = 453) on items
    for heatran_sid in (1068, 1080):
        try:
            sf_h = disassemble(scripts_narc.files[heatran_sid])
            if _inject_bag_key_gate(sf_h, 380, 16500, 458, "lbl1_1", f"magma_{heatran_sid}"):
                scripts_narc.files[heatran_sid] = bytes(assemble(sf_h))
                modified_scripts = True
        except Exception:
            pass

    try:
        sf_774 = disassemble(scripts_narc.files[774])
        mod_774 = False
        new_774 = []
        for l in sf_774.lines:
            if l.type == "command" and l.parts == ["WorkSetConst", 16500, 1]:
                mod_774 = True
                continue
            if l.type == "command" and l.parts == ["WorkSet", 32768, 458]:
                new_774.append(Line("command", ["WorkSet", 32768, 29]))
                mod_774 = True
                continue
            new_774.append(l)
        if mod_774:
            sf_774.lines = new_774
            scripts_narc.files[774] = bytes(assemble(sf_774))
            modified_scripts = True
    except Exception:
        pass

    try:
        sf_526 = disassemble(scripts_narc.files[526])
        if _inject_bag_key_gate(sf_526, 379, 16499, 453, "lbl1_1", "lunar_526"):
            scripts_narc.files[526] = bytes(assemble(sf_526))
            modified_scripts = True
    except Exception:
        pass

    try:
        sf_1026 = disassemble(scripts_narc.files[1026])
        mod_1026 = False
        new_1026 = []
        for l in sf_1026.lines:
            if l.type == "command" and l.parts == ["WorkSetConst", 16499, 1]:
                mod_1026 = True
                continue
            new_1026.append(l)
        if mod_1026:
            sf_1026.lines = new_1026
            scripts_narc.files[1026] = bytes(assemble(sf_1026))
            modified_scripts = True
    except Exception:
        pass

    # Make time-dependent events/checks always active regardless of IRL time of day:
    # - s822 (Lacunosa Town - Gift: Executive in northeast house (Night)): always reset hide-flag 786
    try:
        if len(scripts_narc.files) > 822:
            sf_822 = disassemble(scripts_narc.files[822])
            _replace_scr_block(sf_822, "scr0", [
                Line("label", ["scr0"]),
                Line("command", ["FlagReset", 786]),
                Line("command", ["VMHalt"]),
            ])
            scripts_narc.files[822] = bytes(assemble(sf_822))
            modified_scripts = True
    except Exception:
        pass

    # - s78 (Castelia City - Royal Unova): always allow boarding regardless of time of day
    try:
        if len(scripts_narc.files) > 78:
            sf_78 = disassemble(scripts_narc.files[78])
            for idx, line in enumerate(sf_78.lines[:-1]):
                if (
                    line.type == "command"
                    and line.parts == ["StoreVar0xCD", 32801]
                    and sf_78.lines[idx + 1].type == "command"
                    and sf_78.lines[idx + 1].parts == ["StackPush", 32801]
                ):
                    sf_78.lines[idx + 1] = Line("command", ["StackPushConst", 2])
                    scripts_narc.files[78] = bytes(assemble(sf_78))
                    modified_scripts = True
                    break
    except Exception:
        pass

    # incomplete stadium bypass
    for stadium_sid in (158, 168):
        try:
            if len(scripts_narc.files) > stadium_sid:
                sf_st = disassemble(scripts_narc.files[stadium_sid])
                new_st = [
                    l for l in sf_st.lines
                    if not (l.type == "command" and l.parts == ["FlagSet", 220])
                ]
                if len(new_st) != len(sf_st.lines):
                    sf_st.lines = new_st
                    scripts_narc.files[stadium_sid] = bytes(assemble(sf_st))
                    modified_scripts = True
        except Exception:
            pass

    # s928 (Marine Tube): give Black Sludge check without requiring a held Poison Barb
    try:
        if len(scripts_narc.files) > 928:
            sf_928 = disassemble(scripts_narc.files[928])
            changed_928 = False
            new_928 = []
            for l in sf_928.lines:
                if l.type == "command" and l.parts == ["StackPush", 32803] and any(
                    nl.type == "command" and nl.parts == ["VMJumpIf", 255, "lbl8_21"]
                    for nl in sf_928.lines
                ):
                    new_928.append(Line("command", ["StackPushConst", 1]))
                    changed_928 = True
                elif l.type == "command" and l.parts == ["MsgActor", 1024, 10, 0, 0]:
                    changed_928 = True
                    continue
                else:
                    new_928.append(l)
            if changed_928:
                sf_928.lines = new_928
                scripts_narc.files[928] = bytes(assemble(sf_928))
                modified_scripts = True
    except Exception:
        pass

    # s516 (Village Bridge): Fisherman gives Dive Ball check whenever talked to (no daily fish quest)
    try:
        if len(scripts_narc.files) > 516:
            sf_516 = disassemble(scripts_narc.files[516])
            idx_scr0 = sf_516.find_label("scr0")
            if idx_scr0 != -1:
                sf_516.lines[idx_scr0 + 1 : idx_scr0 + 1] = [
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["PlaySound", 1351]),
                    Line("command", ["ActorSetEyeToEye"]),
                    Line("command", ["StackPushFlag", 299]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, "lbl1_4"]),
                    Line("command", ["StackPush", 32768]),
                    Line("command", ["StackPush", 32769]),
                    Line("command", ["WorkSet", 32768, 7]),
                    Line("command", ["WorkSet", 32769, 5]),
                    Line("command", ["RTCallGlobal", 2806]),
                    Line("command", ["StackPop", 32769]),
                    Line("command", ["StackPop", 32768]),
                    Line("command", ["FlagSet", 299]),
                    Line("command", ["VMJump", "lbl1_4"]),
                ]
                scripts_narc.files[516] = bytes(assemble(sf_516))
                modified_scripts = True
    except Exception:
        pass

    # s1030 (Seaside Cave 1F): gate Black Belt Rocky & Crustle on Colress MCHN (item 635)
    try:
        if len(scripts_narc.files) > 1030:
            sf_1030 = disassemble(scripts_narc.files[1030])
            new_1030 = []
            i = 0
            changed_1030 = False
            lines_1030 = sf_1030.lines
            while i < len(lines_1030):
                l = lines_1030[i]
                if (
                    i + 2 < len(lines_1030)
                    and l.type == "command"
                    and (l.parts == ["StackPush", 16600] or l.parts == ["StackPushFlag", 368])
                    and lines_1030[i + 1].type == "command"
                    and lines_1030[i + 1].parts in (["StackPushConst", 2], ["StackPushConst", 1])
                    and lines_1030[i + 2].type == "command"
                    and lines_1030[i + 2].parts == ["StackCmp", 1]
                ):
                    new_1030.extend([
                        Line("command", ["CheckItemBagNumber", 635, 1, 32800]),
                        Line("command", ["StackPush", 32800]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                    ])
                    changed_1030 = True
                    i += 3
                    continue
                new_1030.append(l)
                i += 1
            if changed_1030:
                sf_1030.lines = new_1030
                scripts_narc.files[1030] = bytes(assemble(sf_1030))
                modified_scripts = True
    except Exception:
        pass

    # Driftveil Drawbridge (Script 506): remove Charizard party requirement from Youngster gift (flag 282)
    try:
        raw_506 = scripts_narc.files[506]
        if raw_506:
            sf_506 = disassemble(raw_506)
            changed_506 = False
            for i, line in enumerate(sf_506.lines):
                if (
                    line.type == "command"
                    and len(line.parts) >= 2
                    and line.parts[0] == "PokePartyFindBySpecies"
                    and line.parts[1] == 6
                ):
                    for j in range(i + 1, min(i + 6, len(sf_506.lines))):
                        jl = sf_506.lines[j]
                        if jl.type == "command" and jl.parts[0] == "VMJumpIf":
                            sf_506.lines[j] = Line("command", ["VMJump", jl.parts[-1]])
                            changed_506 = True
                            break
                    break
            if changed_506:
                scripts_narc.files[506] = bytes(assemble(sf_506))
                modified_scripts = True
    except Exception:
        pass

    # Icirrus City Fan Club Chairman (Script 238): grant flags 201/202/203 (25/50/99 levels) for any non-Egg Pokemon
    try:
        raw_238 = scripts_narc.files[238]
        if raw_238:
            sf_238 = disassemble(raw_238)
            changed_238 = False
            new_238 = []
            for line in sf_238.lines:
                new_238.append(line)
                if not changed_238 and line.type == "command" and line.parts == ["WorkSub", 32804, 32803]:
                    new_238.extend([
                        Line("command", ["StackPushFlag", 201]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "ap_fanclub_chk202"]),
                        Line("command", ["WorkSetConst", 32804, 25]),
                        Line("command", ["VMJump", "ap_fanclub_done"]),
                        Line("label", ["ap_fanclub_chk202"]),
                        Line("command", ["StackPushFlag", 202]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "ap_fanclub_chk203"]),
                        Line("command", ["WorkSetConst", 32804, 50]),
                        Line("command", ["VMJump", "ap_fanclub_done"]),
                        Line("label", ["ap_fanclub_chk203"]),
                        Line("command", ["StackPushFlag", 203]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "ap_fanclub_done"]),
                        Line("command", ["WorkSetConst", 32804, 99]),
                        Line("label", ["ap_fanclub_done"]),
                    ])
                    changed_238 = True
            if changed_238:
                sf_238.lines = new_238
                scripts_narc.files[238] = bytes(assemble(sf_238))
                modified_scripts = True
    except Exception:
        pass

    # Striaton City Pokemon Center (Script 16): remove Shaymin requirement from Gracidea gift (flag 381)
    try:
        raw_16 = scripts_narc.files[16]
        if raw_16:
            sf_16 = disassemble(raw_16)
            changed_16 = False
            for i, line in enumerate(sf_16.lines):
                if (
                    line.type == "command"
                    and len(line.parts) >= 2
                    and line.parts[0] == "PokePartyFindEx"
                    and line.parts[1] == 492
                ):
                    sf_16.lines[i] = Line("command", ["WorkSetConst", 32801, 1])
                    changed_16 = True
                    break
            if changed_16:
                scripts_narc.files[16] = bytes(assemble(sf_16))
                modified_scripts = True
    except Exception:
        pass

    # P2 Laboratory Scientist Dudley (Script 478): remove Genesect requirement and tag his two Drive gifts
    try:
        raw_478 = scripts_narc.files[478]
        if raw_478:
            sf_478 = disassemble(raw_478)
            changed_478 = False
            new_478 = []
            gift_idx = 0
            gift_flags = (2443, 2461)
            for line in sf_478.lines:
                if (
                    line.type == "command"
                    and len(line.parts) >= 2
                    and line.parts[0] == "PokePartyFindEx"
                    and line.parts[1] == 649
                ):
                    new_478.append(Line("command", ["WorkSetConst", 32784, 1]))
                    changed_478 = True
                    continue
                new_478.append(line)
                if line.type == "command" and line.parts == ["RTCallGlobal", 2805] and gift_idx < 2:
                    new_478.append(Line("command", ["FlagSet", gift_flags[gift_idx]]))
                    gift_idx += 1
                    changed_478 = True
            if changed_478:
                sf_478.lines = new_478
                scripts_narc.files[478] = bytes(assemble(sf_478))
                modified_scripts = True
    except Exception:
        pass

    # Driftveil City Grand Hotel (Script 202): remove 70+ Seen requirement from Old Man gift
    try:
        raw_202 = scripts_narc.files[202]
        if raw_202:
            sf_202 = disassemble(raw_202)
            changed_202 = False
            for i, line in enumerate(sf_202.lines):
                if line.type == "command" and line.parts == ["PokeDexGetCount", 0, 32800]:
                    sf_202.lines[i] = Line("command", ["WorkSetConst", 32800, 70])
                    changed_202 = True
                    break
            if changed_202:
                scripts_narc.files[202] = bytes(assemble(sf_202))
                modified_scripts = True
    except Exception:
        pass

    # Driftveil City Market (Script 210): remove Lv 30+ Pokemon requirement from Man in black gift (flag 324)
    try:
        raw_210 = scripts_narc.files[210]
        if raw_210:
            sf_210 = disassemble(raw_210)
            changed_210 = False
            for i, line in enumerate(sf_210.lines):
                if (
                    line.type == "command"
                    and line.parts == ["StackPush", 32808]
                    and i + 2 < len(sf_210.lines)
                    and sf_210.lines[i + 1].parts == ["StackPushConst", 1]
                    and sf_210.lines[i + 2].parts == ["StackCmp", 4]
                ):
                    sf_210.lines[i] = Line("command", ["StackPushConst", 1])
                    changed_210 = True
                    break
            if changed_210:
                scripts_narc.files[210] = bytes(assemble(sf_210))
                modified_scripts = True
    except Exception:
        pass

    # Accumula Town (Script 794): remove <=20cm (flag 2766) and >=5m (flag 2767) Pokemon requirements
    try:
        raw_794 = scripts_narc.files[794]
        if raw_794:
            sf_794 = disassemble(raw_794)
            changed_794 = False
            for i, line in enumerate(sf_794.lines):
                if (
                    line.type == "command"
                    and line.parts in (["StackPush", 32804], ["StackPush", 32805])
                    and i + 2 < len(sf_794.lines)
                    and sf_794.lines[i + 1].parts == ["StackPushConst", 1]
                    and sf_794.lines[i + 2].parts == ["StackCmp", 1]
                ):
                    sf_794.lines[i] = Line("command", ["StackPushConst", 1])
                    changed_794 = True
            if changed_794:
                scripts_narc.files[794] = bytes(assemble(sf_794))
                modified_scripts = True
    except Exception:
        pass

    # Accumula Town Pianist (Script 810): remove Kricketot and Whismur party requirements (flag 2335)
    try:
        raw_810 = scripts_narc.files[810]
        if raw_810:
            sf_810 = disassemble(raw_810)
            changed_810 = False
            for i, line in enumerate(sf_810.lines):
                if (
                    line.type == "command"
                    and line.parts == ["StackPush", 32806]
                    and i + 2 < len(sf_810.lines)
                    and sf_810.lines[i + 1].parts == ["StackPushConst", 1]
                    and sf_810.lines[i + 2].parts == ["StackCmp", 1]
                ):
                    sf_810.lines[i] = Line("command", ["StackPushConst", 1])
                    changed_810 = True
            if changed_810:
                scripts_narc.files[810] = bytes(assemble(sf_810))
                modified_scripts = True
    except Exception:
        pass

    # Humilau City Nurse (Script 938): remove Luvdisc party requirement (flag 342)
    try:
        raw_938 = scripts_narc.files[938]
        if raw_938:
            sf_938 = disassemble(raw_938)
            changed_938 = False
            for i, line in enumerate(sf_938.lines):
                if (
                    line.type == "command"
                    and line.parts == ["StackPush", 32803]
                    and i + 2 < len(sf_938.lines)
                    and sf_938.lines[i + 1].parts == ["StackPushConst", 1]
                    and sf_938.lines[i + 2].parts == ["StackCmp", 1]
                ):
                    sf_938.lines[i] = Line("command", ["StackPushConst", 1])
                    changed_938 = True
                    break
            if changed_938:
                scripts_narc.files[938] = bytes(assemble(sf_938))
                modified_scripts = True
    except Exception:
        pass

    # Bypass restrictive party/stat requirements on gift checks:
    # - s638 (Route 2 Lady): Solid Rock ability check -> any non-Egg Pokemon
    # - s514 (Village Bridge Baker): Honey Gather ability check -> any non-Egg Pokemon
    # - s654 / s1058 (Route 4 Ace Trainer): random 50..200 Speed/Attack check -> >= 0
    for sid, old_push, nxt_cmd, new_val in (
        (638, ["StackPush", 32804], ["StackPushConst", 116], 116),
        (514, ["StackPush", 32802], ["StackPushConst", 118], 118),
        (654, ["StackPush", 16775], ["StackCmp", 4], 0),
        (1058, ["StackPush", 16775], ["StackCmp", 4], 0),
    ):
        try:
            if len(scripts_narc.files) > sid and scripts_narc.files[sid]:
                sf_g = disassemble(scripts_narc.files[sid])
                changed_g = False
                for i, line in enumerate(sf_g.lines[:-1]):
                    if line.type == "command" and line.parts == old_push and sf_g.lines[i + 1].parts == nxt_cmd:
                        sf_g.lines[i] = Line("command", ["StackPushConst", new_val])
                        changed_g = True
                        break
                if changed_g:
                    scripts_narc.files[sid] = bytes(assemble(sf_g))
                    modified_scripts = True
        except Exception:
            pass

    # Mistralton Cargo Service Pilot (Script 222 sub63): bypass Flying/Psychic type check (flag 472)
    try:
        if len(scripts_narc.files) > 222 and scripts_narc.files[222]:
            sf_222 = disassemble(scripts_narc.files[222])
            changed_222 = False
            for i, line in enumerate(sf_222.lines[:-1]):
                if (
                    line.type == "command"
                    and line.parts == ["VMJumpIf", 255, "lbl10_65"]
                    and sf_222.lines[i + 1].type == "command"
                    and sf_222.lines[i + 1].parts == ["StackPush", 32808]
                ):
                    sf_222.lines[i] = Line("command", ["VMJumpIf", 255, "lbl_pilot_any_mon"])
                    sf_222.lines.insert(i + 1, Line("label", ["lbl_pilot_any_mon"]))
                    changed_222 = True
                    break
            if changed_222:
                scripts_narc.files[222] = bytes(assemble(sf_222))
                modified_scripts = True
    except Exception:
        pass

    # Chargestone Cave Nugget Brothers (Script 392): split Nugget (296) and Big Nugget (2585)
    try:
        if len(scripts_narc.files) > 392 and scripts_narc.files[392]:
            sf_392 = disassemble(scripts_narc.files[392])
            sub3_idx = sf_392.find_label("sub3")
            if sub3_idx != -1:
                new_392: list[Line] = []
                active_item: int | None = None
                in_sub3 = False
                changed_392 = False
                for line in sf_392.lines:
                    if line.type == "label" and line.parts == ["sub3"]:
                        in_sub3 = True
                    elif in_sub3 and line.type == "command" and line.parts == ["VMReturn"]:
                        in_sub3 = False
                    if in_sub3 and line.type == "command":
                        if line.parts in (["WorkSet", 32768, 92], ["WorkSet", 32768, 581]):
                            active_item = line.parts[2]
                        elif line.parts == ["FlagSet", 296]:
                            changed_392 = True
                            continue
                    new_392.append(line)
                    if in_sub3 and line.type == "command" and line.parts == ["RTCallGlobal", 2805]:
                        if active_item == 92:
                            new_392.append(Line("command", ["FlagSet", 296]))
                            changed_392 = True
                        elif active_item == 581:
                            new_392.append(Line("command", ["FlagSet", 2585]))
                            changed_392 = True
                if changed_392:
                    sf_392.lines = new_392
                    scripts_narc.files[392] = bytes(assemble(sf_392))
                    modified_scripts = True
    except Exception:
        pass

    if modified_scripts:
        rom.setFileByName("a/0/5/6", scripts_narc.save())
    if modified_entities and a126 is not None:
        rom.setFileByName("a/1/2/6", a126.save())

    apply_roadblock_texts(rom)
    _patch_tmhm_hunt_collector(rom, options)


def _patch_tmhm_hunt_collector(rom: "NintendoDSRom", options: dict | None) -> None:
    # When tmhm_hunt is an active goal patches the Mistralton city Pokémon center TM collector
    if not options:
        return
    goal_opt = options.get("goal", [])
    if isinstance(goal_opt, str):
        active_goals = {goal_opt.lower()}
    elif isinstance(goal_opt, (list, set, tuple)):
        active_goals = {str(g).lower() for g in goal_opt}
    else:
        active_goals = set()
    if "tmhm_hunt" not in active_goals:
        return

    try:
        from ..nds_compat import NARC
    except (ImportError, ValueError):
        try:
            from worlds.pokemon_b2w2.nds_compat import NARC
        except (ImportError, ValueError):
            from nds_compat import NARC

    from .script_editing import disassemble, assemble, Line
    from .text import decode, encode, Entry

    target = max(0, min(101, int(options.get("tmhm_hunt", 60))))

    story_narc = NARC(rom.getFileByName("a/0/0/3"))
    t131 = decode(story_narc.files[131])
    idx_progress = len(t131[0])
    idx_goal = idx_progress + 1
    msg_progress = (
        "If your goal is TM/HM Hunt, you need [c_201_#1_1]![NextLine]"
        "You currently have [c_201_#1_0]/[c_201_#1_1] TMs & HMs."
    )
    msg_goal = (
        "Congratulations! You have [c_201_#1_0]/[c_201_#1_1][NextLine]"
        "TMs & HMs! Your TM/HM Hunt goal is complete!"
    )
    for blk in t131:
        blk.append(Entry(msg_progress))
        blk.append(Entry(msg_goal))
    story_narc.files[131] = encode(t131)
    rom.setFileByName("a/0/0/3", story_narc.save())

    scripts_narc = NARC(rom.getFileByName("a/0/5/6"))
    sf = disassemble(scripts_narc.files[224])
    lbl9_idx = sf.find_label("lbl2_9")
    if lbl9_idx == -1:
        return

    flag455_seen = False
    for idx in range(lbl9_idx):
        l = sf.lines[idx]
        if l.type == "command" and l.parts == ["StackPushFlag", 455]:
            flag455_seen = True
        elif flag455_seen and l.type == "command" and l.parts == ["VMJump", "lbl2_20"]:
            l.parts = ["VMJump", "lbl_tmhm_hunt"]
            break

    block = [
        Line("label", ["lbl_tmhm_hunt"]),
        Line("command", ["ItemGetTMCount", 32802]),
        Line("command", ["CheckItemBagNumber", 420, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["CheckItemBagNumber", 421, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["CheckItemBagNumber", 422, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["CheckItemBagNumber", 423, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["CheckItemBagNumber", 424, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["CheckItemBagNumber", 425, 1, 32804]),
        Line("command", ["WorkAdd", 32802, 32804]),
        Line("command", ["WorkSetConst", 32803, target]),
        Line("command", ["WordSetNumber", 0, 32802, 3]),
        Line("command", ["WordSetNumber", 1, 32803, 3]),
        Line("command", ["StackPush", 32802]),
        Line("command", ["StackPushConst", target]),
        Line("command", ["StackCmp", 4]),
        Line("command", ["VMJumpIf", 255, "lbl_tmhm_need_more"]),
        Line("command", ["MsgActor", 1024, idx_goal, 0, 0]),
        Line("command", ["InputWaitLast"]),
        Line("command", ["MsgWinCloseAll"]),
        Line("command", ["FlagSet", 3055]),
        Line("command", ["VMJump", "lbl2_20"]),
        Line("label", ["lbl_tmhm_need_more"]),
        Line("command", ["MsgActor", 1024, idx_progress, 0, 0]),
        Line("command", ["InputWaitLast"]),
        Line("command", ["MsgWinCloseAll"]),
        Line("command", ["VMJump", "lbl2_20"]),
    ]
    sf.lines[lbl9_idx + 1 : lbl9_idx + 1] = block
    scripts_narc.files[224] = bytes(assemble(sf))
    rom.setFileByName("a/0/5/6", scripts_narc.save())


def apply_roadblock_texts(rom: "NintendoDSRom") -> None:
    # Updates text banks in a/0/0/3 so blocker NPCs state the required badge
    try:
        from ..nds_compat import NARC
    except (ImportError, ValueError):
        try:
            from worlds.pokemon_b2w2.nds_compat import NARC
        except (ImportError, ValueError):
            from nds_compat import NARC

    from .text import decode, encode

    story_narc = NARC(rom.getFileByName("a/0/0/3"))
    text_modified = False

    try:
        t253 = decode(story_narc.files[253])
        t253[0][5].line = (
            "Bianca: The bridge fell apart,[NextLine]and it can't be fixed right now![End][NextLine]"
            "You'll need the Quake Badge[NextLine]before you can cross!"
        )
        t253[0][6].line = (
            "The bridge collapsed, so there's no way[NextLine]through to Mistralton City yet.[End][NextLine]"
            "Find the Quake Badge while we work!"
        )
        story_narc.files[253] = encode(t253)
        text_modified = True
    except Exception:
        pass

    try:
        t187 = decode(story_narc.files[187])
        t187[0][7].line = (
            "The ship to Castelia City[NextLine]departs from here![End][NextLine]"
            "We can only welcome Trainers who[NextLine]have earned the Toxic Badge!"
        )
        story_narc.files[187] = encode(t187)
        text_modified = True
    except Exception:
        pass

    try:
        from .text import Entry
        t525 = decode(story_narc.files[525])
        while len(t525[0]) <= 19:
            t525[0].append(Entry("", key=None))
        t525[0][19].line = (
            "Colress: These Crustle are blocking[NextLine]the road.[End][NextLine]"
            "I need to test my device with a[NextLine]Trainer who holds the Insect Badge!"
        )
        story_narc.files[525] = encode(t525)
        text_modified = True
    except Exception:
        pass

    try:
        from .text import Entry
        t540 = decode(story_narc.files[540])
        while len(t540[0]) <= 20:
            t540[0].append(Entry("", key=None))
        t540[0][20].line = (
            "Colress: These Crustle are blocking[NextLine]the road.[End][NextLine]"
            "I need to test my device with a[NextLine]Trainer who holds the Insect Badge!"
        )
        story_narc.files[540] = encode(t540)
        text_modified = True
    except Exception:
        pass

    try:
        t130 = decode(story_narc.files[130])
        t130[0][10].line = (
            "Hello![NextLine]This is Mistralton Cargo Service.[End][NextLine]“Deliver a lot of cargo quickly!\"[End][NextLine]"
            "To board our passenger flights, you'll[NextLine]need the Jet Badge!"
        )
        story_narc.files[130] = encode(t130)
        text_modified = True
    except Exception:
        pass

    try:
        t399 = decode(story_narc.files[399])
        t399[0][0].line = (
            "Hm![End][NextLine]If you want past here,[NextLine]you have to defeat me,[Scroll][NextLine]"
            "and my Roggenrola![End][NextLine]Come back once you have[NextLine]the Colress MCHN!"
        )
        story_narc.files[399] = encode(t399)
        text_modified = True
    except Exception:
        pass

    try:
        t643 = decode(story_narc.files[643])
        t643[0][0].line = (
            "The Marine Tube is just ahead.[End][NextLine]"
            "Entry is restricted until you[NextLine]obtain the Legend Badge!"
        )
        t643[0][2].line = (
            "Wait! Entry is not permitted until[NextLine]you show the Legend Badge![End]"
        )
        story_narc.files[643] = encode(t643)
        text_modified = True
    except Exception:
        pass

    try:
        t290 = decode(story_narc.files[290])
        t290[0][0].line = (
            "We're under strict orders not to[NextLine]let anyone past without the Card Key![End]"
        )
        t290[0][1].line = (
            "This is our important task! Nobody[NextLine]enters Giant Chasm without the Card Key![End]"
        )
        t290[0][12].line = (
            "Team Plasma: Nobody's getting past[NextLine]to Route 23! Not unless you hold[Scroll][NextLine]"
            "the DNA Splicers!"
        )
        story_narc.files[290] = encode(t290)
        text_modified = True
    except Exception:
        pass

    try:
        t541 = decode(story_narc.files[541])
        t541[0][0].line = (
            "I'm a heartbreaker...[NextLine]My name... Charles.[End][NextLine]"
            "Now, I'm having a Triple Battle[NextLine]with the opponent in front of me![End][NextLine]"
            "Come back once you have[NextLine]the Bolt Badge!"
        )
        t541[0][10].line = (
            "I'm a heartbreaker...[NextLine]My name... Charles.[End][NextLine]"
            "Now, I'm having a Rotation Battle[NextLine]with the opponent in front of me![End][NextLine]"
            "Come back once you have[NextLine]the Bolt Badge!"
        )
        t541[0][26].line = (
            "The Trainer called Charles[NextLine]is quite tough to beat.[End][NextLine]"
            "If you have the Bolt Badge,[NextLine]you might be a match for him."
        )
        story_narc.files[541] = encode(t541)
        text_modified = True
    except Exception:
        pass

    if text_modified:
        rom.setFileByName("a/0/0/3", story_narc.save())
