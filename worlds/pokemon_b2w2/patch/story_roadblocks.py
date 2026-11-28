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

    def _skip_demo_with_fade(lines: list[Any], demo_ids: set[int]) -> tuple[list[Any], bool]:
        out: list[Any] = []
        changed = False
        i = 0
        while i < len(lines):
            if (
                i + 2 < len(lines)
                and lines[i].type == "command" and lines[i].parts == ["FieldClose"]
                and lines[i + 1].type == "command" and lines[i + 1].parts[0] == "Call3DDemo"
                and lines[i + 1].parts[1] in demo_ids
                and lines[i + 2].type == "command" and lines[i + 2].parts == ["FieldOpen"]
            ):
                out.append(Line("command", ["FadeIntoBlack"]))
                changed = True
                i += 3
                continue
            out.append(lines[i])
            i += 1
        return out, changed

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
                Line("command", ["WorkSetConst", 16594, 1]),
                Line("command", ["VMHalt"]),
                Line("label", ["lbl_no_quake"]),
                Line("command", ["FlagReset", 788]),
                Line("command", ["FlagReset", 962]),
                Line("command", ["WorkSetConst", 16594, 1]),
                Line("command", ["VMHalt"]),
            ]
            # Disperse Bianca (13) across bridge and Workers (12, 14) offscreen when talking with Quake Badge
            msg_b1 = 14
            msg_b2 = 15
            a003_cc = rom.getFileByName("a/0/0/3")
            if a003_cc is not None:
                from .text import decode, encode, insert_line
                cc_narc = NARC(a003_cc)
                cc_t = decode(cc_narc.files[253])
                msg_b1 = len(cc_t[0])
                msg_b2 = msg_b1 + 1
                insert_line(cc_t, 0, msg_b1, "Thanks for waiting - looks like the[NextLine]bridge is finished being repaired now![End]")
                insert_line(cc_t, 0, msg_b2, "I'm going further in - see you later![End]")
                cc_narc.files[253] = encode(cc_t)
                rom.setFileByName("a/0/0/3", cc_narc.save())

            for talk_lbl in ("scr4", "scr5"):
                t_idx = sf_390.find_label(talk_lbl)
                if t_idx != -1:
                    sf_390.lines[t_idx + 1 : t_idx + 1] = [
                        Line("command", ["StoreBadge", 32804, 4]),
                        Line("command", ["WorkCmpConst", 32804, 1]),
                        Line("command", ["VMJumpIf", 1, "lbl_disp_390"]),
                    ]
            sf_390.lines.extend([
                Line("label", ["lbl_disp_390"]),
                Line("command", ["ActorPauseAll"]),
                Line("command", ["ActorSetEyeToEye"]),
                Line("command", ["PlayerGetGPos", 32801, 32802]),
                Line("command", ["WorkCmpConst", 32801, 38]),
                Line("command", ["VMJumpIf", 5, "lbl_390_aligned"]),
                Line("command", ["ActorCmdExec", 255, "act_390_p_left"]),
                Line("command", ["VMSleep", 10]),
                Line("label", ["lbl_390_aligned"]),
                Line("command", ["MsgActorEx", 1024, msg_b1, 13, 0, 0]),
                Line("command", ["MsgActorEx", 1024, msg_b2, 13, 0, 0]),
                Line("command", ["MsgWinCloseAll"]),
                Line("command", ["ActorCmdExec", 255, "act_390_p_step_look"]),
                Line("command", ["ActorCmdExec", 13, "act_390_bianca"]),
                Line("command", ["ActorCmdExec", 12, "act_390_w12"]),
                Line("command", ["ActorCmdExec", 14, "act_390_w14"]),
                Line("command", ["VMSleep", 115]),
                Line("command", ["ActorDelete", 13]),
                Line("command", ["ActorDelete", 12]),
                Line("command", ["ActorDelete", 14]),
                Line("command", ["FlagSet", 788]),
                Line("command", ["FlagSet", 962]),
                Line("command", ["WorkSetConst", 16594, 1]),
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
                Line("label", ["act_390_p_left"]),
                Line("action", ["WalkW8F", 1]),
                Line("action", ["TurnS8F", 1]),
                Line("action", ["EndAction", 0]),
                Line("label", ["act_390_p_step_look"]),
                Line("action", ["WalkW8F", 1]),
                Line("action", ["TurnE8F", 1]),
                Line("action", ["EndAction", 0]),
                Line("label", ["act_390_bianca"]),
                Line("action", ["WalkS8F", 4]),
                Line("action", ["WalkE8F", 10]),
                Line("action", ["EndAction", 0]),
                Line("label", ["act_390_w12"]),
                Line("action", ["WalkN8F", 7]),
                Line("action", ["WalkW8F", 1]),
                Line("action", ["WalkN8F", 4]),
                Line("action", ["EndAction", 0]),
                Line("label", ["act_390_w14"]),
                Line("action", ["WalkS8F", 1]),
                Line("action", ["WalkE8F", 10]),
                Line("action", ["EndAction", 0]),
            ])
            scripts_narc.files[390] = bytes(assemble(sf_390))
            modified_scripts = True
            if a126 is not None and len(a126.files) > 244:
                f244 = bytearray(a126.files[244])
                nf244 = f244[4]
                nn244 = f244[5]
                if nn244 > 14:
                    npc14_off = 8 + 20 * nf244 + 36 * 14
                    f244[npc14_off + 4 : npc14_off + 6] = (0).to_bytes(2, "little")
                    a126.files[244] = bytes(f244)
                    modified_entities = True
    except Exception:
        pass

    try:
        sf_222 = disassemble(scripts_narc.files[222])
        # Remove Skyla/Juniper/Bianca Cargo Service cutscene (scr2) so it never flies without Jet Badge
        scr2_idx = sf_222.find_label("scr2")
        if scr2_idx != -1 and sf_222.find_label("lbl3_25") != -1:
            sf_222.lines[scr2_idx + 1 : scr2_idx + 1] = [
                Line("command", ["ActorPauseAll"]),
                Line("command", ["FlagSet", 767]),
                Line("command", ["FlagSet", 768]),
                Line("command", ["FlagSet", 769]),
                Line("command", ["VMJump", "lbl3_25"]),
            ]
        # Skip Lentimas arrival cutscene state when flying via Pilot (sub52)
        sub52_idx = sf_222.find_label("sub52")
        if sub52_idx != -1:
            for i in range(sub52_idx, min(sub52_idx + 12, len(sf_222.lines))):
                if sf_222.lines[i].type == "command" and sf_222.lines[i].parts[0] == "MapChangeCore":
                    sf_222.lines[i:i] = [
                        Line("command", ["FlagSet", 777]),
                        Line("command", ["WorkSetConst", 16587, 2]),
                        Line("command", ["WorkSetConst", 16672, 1]),
                        Line("command", ["HollowRivalSetValue", 3, 4]),
                        Line("command", ["HollowRivalSetValue", 0, 4]),
                    ]
                    break
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

    # Keep Skyla (767) and Juniper (768) out of Cargo Service after Mistralton runway (Script 214 scr5)
    try:
        sf_214 = disassemble(scripts_narc.files[214])
        changed_214 = False
        scr5_214 = sf_214.find_label("scr5")
        if scr5_214 != -1:
            for i in range(scr5_214, min(scr5_214 + 65, len(sf_214.lines))):
                if sf_214.lines[i].type == "command" and sf_214.lines[i].parts in (["FlagReset", 767], ["FlagReset", 768]):
                    sf_214.lines[i] = Line("command", ["FlagSet", sf_214.lines[i].parts[1]])
                    changed_214 = True
        if changed_214:
            scripts_narc.files[214] = bytes(assemble(sf_214))
            modified_scripts = True
    except Exception:
        pass

    # Celestial Tower 1F Juniper (Script 676 scr1) fixes
    try:
        if len(scripts_narc.files) > 676 and scripts_narc.files[676]:
            sf_676 = disassemble(scripts_narc.files[676])
            scr1_676 = sf_676.find_label("scr1")
            if scr1_676 != -1:
                for i in range(scr1_676, min(scr1_676 + 15, len(sf_676.lines))):
                    if sf_676.lines[i].type == "command" and sf_676.lines[i].parts == ["StoreBadge", 32776, 5]:
                        sf_676.lines[i] = Line("command", ["FlagGet", 1675, 32776])
                        break
                for i in range(scr1_676, min(scr1_676 + 15, len(sf_676.lines))):
                    if sf_676.lines[i].type == "command" and sf_676.lines[i].parts == ["StackPush", 16578]:
                        # If Skyla is defeated, jump straight to departure block else if Flag 1711 == 0, jump to pre-Skyla gift block
                        sf_676.lines[i : i + 4] = [
                            Line("command", ["WorkCmpConst", 32776, 1]),
                            Line("command", ["VMJumpIf", 1, "lbl_676_depart"]),
                            Line("command", ["FlagGet", 2289, 32776]),
                            Line("command", ["WorkCmpConst", 32776, 1]),
                            Line("command", ["VMJumpIf", 1, "lbl_676_depart"]),
                            Line("command", ["FlagGet", 1711, 32776]),
                            Line("command", ["WorkCmpConst", 32776, 0]),
                            Line("command", ["VMJumpIf", 1, "lbl_676_give_gift"]),
                            Line("command", ["VMJump", "lbl_676_wait_msg"]),
                            Line("label", ["lbl_676_give_gift"]),
                        ]
                        # Only increment 16578 if it was 1
                        for j in range(i + 10, min(i + 40, len(sf_676.lines))):
                            if sf_676.lines[j].type == "command" and sf_676.lines[j].parts == ["WorkAdd", 16578, 1]:
                                sf_676.lines[j : j + 1] = [
                                    Line("command", ["StackPush", 16578]),
                                    Line("command", ["StackPushConst", 1]),
                                    Line("command", ["StackCmp", 1]),
                                    Line("command", ["VMJumpIf", 255, "lbl_676_no_inc"]),
                                    Line("command", ["WorkAdd", 16578, 1]),
                                    Line("label", ["lbl_676_no_inc"]),
                                ]
                                break
                        # Mark departure block right after VMJumpIf 255, lbl2_4
                        for k in range(i + 10, min(i + 60, len(sf_676.lines))):
                            if sf_676.lines[k].type == "command" and sf_676.lines[k].parts == ["StackCmp", 7]:
                                if k + 1 < len(sf_676.lines) and sf_676.lines[k + 1].parts[:2] == ["VMJumpIf", 255]:
                                    sf_676.lines.insert(k + 2, Line("label", ["lbl_676_depart"]))
                                    break
                        # Skip duplicate Flag 1711 RTCallGlobal 2805 in departure block if Flag 1711 is already set
                        dep_idx = sf_676.find_label("lbl_676_depart")
                        if dep_idx != -1:
                            for k in range(dep_idx, min(dep_idx + 60, len(sf_676.lines))):
                                if sf_676.lines[k].type == "command" and sf_676.lines[k].parts == ["FlagSet", 1711]:
                                    start_g = k - 2 if k >= 2 and sf_676.lines[k - 2].parts == ["StackPush", 32768] else k
                                    sf_676.lines[start_g:start_g] = [
                                        Line("command", ["FlagGet", 1711, 32776]),
                                        Line("command", ["WorkCmpConst", 32776, 1]),
                                        Line("command", ["VMJumpIf", 1, "lbl_676_skip_dup_gift"]),
                                    ]
                                    for m in range(start_g + 4, min(start_g + 16, len(sf_676.lines))):
                                        if sf_676.lines[m].type == "command" and sf_676.lines[m].parts == ["StackPop", 32768]:
                                            sf_676.lines.insert(m + 1, Line("label", ["lbl_676_skip_dup_gift"]))
                                            break
                                    break
                        lbl2_4_idx = sf_676.find_label("lbl2_4")
                        if lbl2_4_idx != -1:
                            for k in range(lbl2_4_idx, min(lbl2_4_idx + 10, len(sf_676.lines))):
                                if sf_676.lines[k].type == "command" and sf_676.lines[k].parts[:2] == ["VMJumpIf", 255]:
                                    sf_676.lines[k] = Line("command", ["VMJumpIf", 255, "lbl_676_wait_msg"])
                                    sf_676.lines.insert(k + 1, Line("label", ["lbl_676_wait_msg"]))
                                    break
                        scripts_narc.files[676] = bytes(assemble(sf_676))
                        modified_scripts = True
                        break
    except Exception:
        pass

    # Skip Lentimas Town arrival cutscene (Script 916 scr0) & init Reversal Mountain Bianca state (scr8)
    try:
        sf_916 = disassemble(scripts_narc.files[916])
        scr8_916 = sf_916.find_label("scr8")
        if scr8_916 != -1:
            sf_916.lines[scr8_916 + 1 : scr8_916 + 1] = [
                Line("command", ["StackPush", 16672]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, "lbl_916_bianca_ok"]),
                Line("command", ["FlagSet", 777]),
                Line("command", ["WorkSetConst", 16587, 2]),
                Line("command", ["WorkSetConst", 16672, 1]),
                Line("command", ["FlagReset", 959]),
                Line("label", ["lbl_916_bianca_ok"]),
            ]
        scr0_916 = sf_916.find_label("scr0")
        if scr0_916 != -1:
            sf_916.lines[scr0_916 + 1 : scr0_916 + 1] = [
                Line("command", ["ActorPauseAll"]),
                Line("command", ["FlagSet", 777]),
                Line("command", ["WorkSetConst", 16587, 2]),
                Line("command", ["WorkSetConst", 16672, 1]),
                Line("command", ["FlagReset", 959]),
                Line("command", ["HollowRivalSetValue", 3, 4]),
                Line("command", ["HollowRivalSetValue", 0, 4]),
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
            ]
            if skip_cinematics:
                sf_916.lines, _ = _skip_demo_with_fade(sf_916.lines, {25})
            scripts_narc.files[916] = bytes(assemble(sf_916))
            modified_scripts = True
    except Exception:
        pass

    # Ensure Reversal Mountain (B2 s1066 / W2 s1078) initializes Bianca follower state (16672=1, reset 959) if 16672==0
    for rev_sid in (1066, 1078):
        try:
            if len(scripts_narc.files) > rev_sid and scripts_narc.files[rev_sid]:
                sf_rev = disassemble(scripts_narc.files[rev_sid])
                scr0_rev = sf_rev.find_label("scr0")
                if scr0_rev != -1:
                    sf_rev.lines[scr0_rev + 1 : scr0_rev + 1] = [
                        Line("command", ["StackPush", 16672]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, f"lbl_rev_{rev_sid}_ok"]),
                        Line("command", ["WorkSetConst", 16672, 1]),
                        Line("command", ["FlagReset", 959]),
                        Line("label", [f"lbl_rev_{rev_sid}_ok"]),
                    ]
                    scripts_narc.files[rev_sid] = bytes(assemble(sf_rev))
                    modified_scripts = True
        except Exception:
            pass

    # Humilau Gym (s946 scr3): never block the player if they bypassed the Humilau bridge splash (var 16671 == 0)
    try:
        if len(scripts_narc.files) > 946 and scripts_narc.files[946]:
            sf_946 = disassemble(scripts_narc.files[946])
            scr3_946 = sf_946.find_label("scr3")
            if scr3_946 != -1:
                sf_946.lines[scr3_946 + 1 : scr3_946 + 1] = [
                    Line("command", ["ActorPauseAll"]),
                    Line("command", ["WorkSetConst", 16671, 1]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ]
                scripts_narc.files[946] = bytes(assemble(sf_946))
                modified_scripts = True
    except Exception:
        pass

    # Skip Castelia/Virbank boat, Royal Unova, and Route 21 Frigate departure 3D demos when skip_cinematics is enabled
    if skip_cinematics:
        for demo_sid, demo_ids in ((72, {10}), (74, {4}), (904, {23}), (1112, {13})):
            try:
                if len(scripts_narc.files) > demo_sid and scripts_narc.files[demo_sid]:
                    sf_demo = disassemble(scripts_narc.files[demo_sid])
                    sf_demo.lines, changed_demo = _skip_demo_with_fade(sf_demo.lines, demo_ids)
                    if changed_demo:
                        scripts_narc.files[demo_sid] = bytes(assemble(sf_demo))
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

    # Keep Marine Tube gated on Legend Badge even after beating Drayden (prevent s240 from setting var 16670 = 1)
    # Also skip Opelucid Plasma Frigate freeze 3D demos (Call3DDemo 14/15) with FadeIntoBlack before MapChangeCore
    try:
        if len(scripts_narc.files) > 240 and scripts_narc.files[240]:
            sf_240 = disassemble(scripts_narc.files[240])
            mod_240 = False
            new_240 = [
                l for l in sf_240.lines
                if not (l.type == "command" and l.parts == ["WorkSetConst", 16670, 1])
            ]
            if len(new_240) != len(sf_240.lines):
                mod_240 = True
            if skip_cinematics:
                new_240, changed_240_demo = _skip_demo_with_fade(new_240, {14, 15})
                if changed_240_demo:
                    mod_240 = True
            if mod_240:
                sf_240.lines = new_240
                scripts_narc.files[240] = bytes(assemble(sf_240))
                modified_scripts = True
    except Exception:
        pass

    if skip_cinematics:
        try:
            if len(scripts_narc.files) > 1208 and scripts_narc.files[1208]:
                sf_1208 = disassemble(scripts_narc.files[1208])
                new_1208, changed_1208 = _skip_demo_with_fade(sf_1208.lines, {16, 17, 18, 19, 20, 21, 22})
                if changed_1208:
                    sf_1208.lines = new_1208
                    scripts_narc.files[1208] = bytes(assemble(sf_1208))
                    modified_scripts = True
        except Exception:
            pass

    # Autocollect missable Opelucid City gifts (flags 236, 240, 241) after Drayden's Kyurem talk in his house (s246 scr2)
    try:
        if len(scripts_narc.files) > 246 and scripts_narc.files[246]:
            sf_246 = disassemble(scripts_narc.files[246])
            scr2_246 = sf_246.find_label("scr2")
            if scr2_246 != -1:
                for i in range(scr2_246, min(scr2_246 + 80, len(sf_246.lines))):
                    if sf_246.lines[i].type == "command" and sf_246.lines[i].parts == ["FlagSet", 800]:
                        sf_246.lines[i + 1 : i + 1] = [
                            Line("command", ["FlagSet", 236]),
                            Line("command", ["FlagSet", 240]),
                            Line("command", ["FlagSet", 241]),
                        ]
                        scripts_narc.files[246] = bytes(assemble(sf_246))
                        modified_scripts = True
                        break
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
                Line("command", ["CheckItemBagNumber", 633, 1, 32804]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 1, "lbl_check_splicers"]),
                Line("command", ["FlagReset", 876]),
                Line("label", ["lbl_check_splicers"]),
                Line("command", ["CheckItemBagNumber", 628, 1, 32804]),
                Line("command", ["StackPush", 32804]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 1, "lbl_chasm_done"]),
                Line("command", ["FlagReset", 879]),
                Line("label", ["lbl_chasm_done"]),
                Line("command", ["VMHalt"]),
            ]
        # Disperse Route 22 Grunts (scr2) with Plasma Card (633) and Left Grunts (scr4/scr5) with Splicers (628) or Ghetsis (885)
        scr2_462 = sf_462.find_label("scr2")
        if scr2_462 != -1:
            sf_462.lines[scr2_462 + 1 : scr2_462 + 1] = [
                Line("command", ["CheckItemBagNumber", 633, 1, 32804]),
                Line("command", ["WorkCmpConst", 32804, 1]),
                Line("command", ["VMJumpIf", 1, "lbl_disp_r22_grunts"]),
            ]
        # Disable Giant Chasm Hugh cutscene (scr6) after Route 21 Frigate so it never bypasses the Plasma Card check (Flag 876)
        _replace_scr_block(sf_462, "scr6", [
            Line("label", ["scr6"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["WorkSetConst", 16496, 2]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
        ])
        for left_lbl in ("scr4", "scr5"):
            l_idx = sf_462.find_label(left_lbl)
            if l_idx != -1:
                sf_462.lines[l_idx + 1 : l_idx + 1] = [
                    Line("command", ["CheckItemBagNumber", 628, 1, 32804]),
                    Line("command", ["WorkCmpConst", 32804, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_disp_left_grunts"]),
                ]
        msg_r22_panic = 14
        msg_left_1 = 15
        msg_left_2 = 16
        a003_gc = rom.getFileByName("a/0/0/3")
        if a003_gc is not None:
            from .text import decode, encode, insert_line
            gc_narc = NARC(a003_gc)
            gc_t = decode(gc_narc.files[290])
            msg_r22_panic = len(gc_t[0])
            msg_left_1 = msg_r22_panic + 1
            msg_left_2 = msg_r22_panic + 2
            insert_line(gc_t, 0, msg_r22_panic, "W-what?! You have a Plasma Card?![NextLine]Run for it!![End]")
            insert_line(gc_t, 0, msg_left_1, "W-wait! You have the DNA Splicers![End]")
            insert_line(gc_t, 0, msg_left_2, "I guess it's all over now...[NextLine]Let's get out of here![End]")
            gc_narc.files[290] = encode(gc_t)
            rom.setFileByName("a/0/0/3", gc_narc.save())

        sf_462.lines.extend([
            Line("label", ["lbl_disp_r22_grunts"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["ActorSetEyeToEye"]),
            Line("command", ["MsgActor", 1024, msg_r22_panic, 0, 0]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["ActorCmdExec", 6, "act_462_s8"]),
            Line("command", ["ActorCmdExec", 11, "act_462_s8"]),
            Line("command", ["VMSleep", 36]),
            Line("command", ["ActorDelete", 6]),
            Line("command", ["ActorDelete", 11]),
            Line("command", ["FlagSet", 876]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["lbl_disp_left_grunts"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["ActorSetEyeToEye"]),
            Line("command", ["MsgActorEx", 1024, msg_left_1, 7, 0, 0]),
            Line("command", ["MsgActorEx", 1024, msg_left_2, 8, 0, 0]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["PlayerGetGPos", 32801, 32802]),
            Line("command", ["WorkCmpConst", 32801, 2]),
            Line("command", ["VMJumpIf", 5, "lbl_left_aligned"]),
            Line("command", ["ActorCmdExec", 255, "act_462_p_east"]),
            Line("command", ["VMSleep", 10]),
            Line("label", ["lbl_left_aligned"]),
            Line("command", ["ActorCmdExec", 8, "act_462_bot_line"]),
            Line("command", ["ActorCmdExec", 7, "act_462_top_line"]),
            Line("command", ["VMSleep", 48]),
            Line("command", ["ActorDelete", 7]),
            Line("command", ["ActorDelete", 8]),
            Line("command", ["FlagSet", 879]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["act_462_s8"]),
            Line("action", ["WalkS4F", 8]),
            Line("action", ["EndAction", 0]),
            Line("label", ["act_462_p_east"]),
            Line("action", ["WalkE8F", 1]),
            Line("action", ["TurnW8F", 1]),
            Line("action", ["EndAction", 0]),
            Line("label", ["act_462_bot_line"]),
            Line("action", ["WalkS4F", 2]),
            Line("action", ["WalkE4F", 2]),
            Line("action", ["WalkS4F", 6]),
            Line("action", ["EndAction", 0]),
            Line("label", ["act_462_top_line"]),
            Line("action", ["WalkS4F", 3]),
            Line("action", ["WalkE4F", 2]),
            Line("action", ["WalkS4F", 6]),
            Line("action", ["EndAction", 0]),
        ])
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
        678: ["scr3"],
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
                        Line("command", ["StoreBadge", 32800, 6]),
                        Line("command", ["StackPush", 32800]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["StackCmp", 6]),
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


    # z563 (ow 354, s1124): add sleeping grunt blocking south door (warp1 -> z554, Route 21 Hugh multi-battle room) in Giant Chasm
    try:
        import struct

        if a126 is not None and len(a126.files) > 354 and len(scripts_narc.files) > 1124 and scripts_narc.files[1124]:
            raw_354 = bytearray(a126.files[354])
            n_furn, n_npc, n_warp, n_trig = raw_354[4], raw_354[5], raw_354[6], raw_354[7]
            off_npcs = 8 + n_furn * 20
            if n_npc == 5 and len(raw_354) >= off_npcs + 36:
                npc5 = bytearray(raw_354[off_npcs : off_npcs + 36])
                struct.pack_into("<6H", npc5, 0, 5, 293, 0, 0, 2616, 9)
                struct.pack_into("<H", npc5, 12, 1)  # face south
                struct.pack_into("<2H", npc5, 28, 32, 15)  # in front of north loading zone (32, 14)
                tail_off = off_npcs + n_npc * 36
                orig_sz = struct.unpack_from("<I", raw_354, 0)[0]
                new_354 = bytearray(raw_354[:tail_off]) + npc5 + raw_354[tail_off:]
                new_354[5] = n_npc + 1
                struct.pack_into("<I", new_354, 0, orig_sz + 36)
                a126.files[354] = bytes(new_354)
                modified_entities = True

                msg_sleep_563 = 6
                a003_563 = rom.getFileByName("a/0/0/3")
                if a003_563 is not None:
                    from .text import decode, encode, insert_line
                    narc_563 = NARC(a003_563)
                    t_563 = decode(narc_563.files[363])
                    msg_sleep_563 = len(t_563[0])
                    insert_line(t_563, 0, msg_sleep_563, "Zzz...")
                    narc_563.files[363] = encode(t_563)
                    rom.setFileByName("a/0/0/3", narc_563.save())

                sf_1124 = disassemble(scripts_narc.files[1124])
                sub11_idx = sf_1124.find_label("sub11")
                if sub11_idx != -1:
                    sf_1124.lines[sub11_idx + 1 : sub11_idx + 1] = [
                        Line("command", ["StackPushFlag", 2609]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "lbl_1124_chk_m3"]),
                        Line("command", ["ObjInitWarpGPos", 0, 0, 0, 0]),
                        Line("command", ["ObjInitWarpGPos", 2, 0, 0, 0]),
                        Line("command", ["ObjInitWarpGPos", 3, 0, 0, 0]),
                        Line("command", ["VMJump", "lbl_1124_show_blocker"]),
                        Line("label", ["lbl_1124_chk_m3"]),
                        Line("command", ["StackPushFlag", 2608]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "lbl_1124_hide_blocker"]),
                        Line("command", ["StackPushFlag", 975]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, "lbl_1124_show_blocker"]),
                        Line("label", ["lbl_1124_hide_blocker"]),
                        Line("command", ["FlagSet", 2616]),
                        Line("command", ["VMJump", "lbl_1124_blocker_done"]),
                        Line("label", ["lbl_1124_show_blocker"]),
                        Line("command", ["FlagReset", 2616]),
                        Line("label", ["lbl_1124_blocker_done"]),
                    ]
                    sf_1124.lines.extend([
                        Line("label", ["scr8"]),
                        Line("command", ["ActorPauseAll"]),
                        Line("command", ["PlaySound", 1351]),
                        Line("command", ["MsgActor", 1024, msg_sleep_563, 0, 0]),
                        Line("command", ["InputWaitLast"]),
                        Line("command", ["MsgActorClose"]),
                        Line("command", ["RTFinishSubEvents"]),
                        Line("command", ["ActorUnlockAll"]),
                        Line("command", ["VMHalt"]),
                    ])
                    sf_1124.script_links[8] = "scr8"
                    scripts_narc.files[1124] = bytes(assemble(sf_1124))
                    modified_scripts = True
    except Exception:
        pass

    # Isolate all 4 Plasma Frigate instances (1=PWT, 2=Route 21, 3=Giant Chasm, 4=P2 Lab) via persistent flags 2606..2609
    # (Work vars >= 16700 are temporary/volatile across map loads; EventFlags 2604..2618 persist in save data)
    try:
        import struct

        if a126 is not None:
            for ow_id, npc_flag_pairs in (
                (350, ((3, 997), (4, 997), (5, 998), (6, 998))),
                (352, ((0, 976),)),
                (365, ((3, 976), (6, 976))),
            ):
                if len(a126.files) > ow_id and a126.files[ow_id]:
                    raw_ow = bytearray(a126.files[ow_id])
                    if len(raw_ow) >= 8:
                        fc_ow, nc_ow = raw_ow[4], raw_ow[5]
                        npc_off = 8 + fc_ow * 20
                        changed_ow = False
                        for npc_idx, new_flag in npc_flag_pairs:
                            if npc_idx < nc_ow and npc_off + (npc_idx + 1) * 36 <= len(raw_ow):
                                struct.pack_into("<H", raw_ow, npc_off + npc_idx * 36 + 8, new_flag)
                                changed_ow = True
                        if changed_ow:
                            a126.files[ow_id] = bytes(raw_ow)
                            modified_entities = True

        def _inj_after_cmd(sf, target_parts: list[Any], extra: list[Any]) -> bool:
            for idx, ln in enumerate(sf.lines):
                if ln.type == "command" and ln.parts == target_parts:
                    sf.lines[idx + 1 : idx + 1] = extra
                    return True
            return False

        def _set_mode(mode: int) -> list[Any]:
            return [Line("command", ["FlagSet" if k == mode else "FlagReset", 2605 + k]) for k in (1, 2, 3, 4)]

        def _jump_if_not_mode(mode: int, lbl: str) -> list[Any]:
            return [
                Line("command", ["StackPushFlag", 2605 + mode]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, lbl]),
            ]

        def _jump_if_mode(mode: int, lbl: str) -> list[Any]:
            return [
                Line("command", ["StackPushFlag", 2605 + mode]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, lbl]),
            ]

        def _flag_branch(chk_flag: int, tag_b: str, on_true: list[Any], on_false: list[Any]) -> list[Any]:
            return [
                Line("command", ["StackPushFlag", chk_flag]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag_b}_f"]),
                *on_true,
                Line("command", ["VMJump", f"lbl_{tag_b}_e"]),
                Line("label", [f"lbl_{tag_b}_f"]),
                *on_false,
                Line("label", [f"lbl_{tag_b}_e"]),
            ]

        def _build_mode2_state(tag: str, include_warp: bool = False) -> list[Any]:
            def _m2_stage_cmds(is_w2: bool) -> list[Any]:
                ver = "w2" if is_w2 else "b2"
                active_var, inactive_var = (16625, 16626) if is_w2 else (16626, 16625)
                set_997, rst_998 = ("FlagSet", "FlagReset") if is_w2 else ("FlagReset", "FlagSet")
                nr_set, nr_rst = (836, 835) if is_w2 else (835, 836)
                s2_extra = [Line("command", ["FlagSet", 832])] if is_w2 else []
                return [
                    Line("command", [set_997, 997]),
                    Line("command", [rst_998, 998]),
                    Line("command", ["WorkSetConst", inactive_var, 0]),
                    Line("command", ["StackPushFlag", 2611]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_{ver}_s1"]),
                    Line("command", ["WorkSetConst", active_var, 3]),
                    *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632, 16635)],
                    Line("command", ["FlagSet", nr_set]),
                    Line("command", ["FlagReset", nr_rst]),
                    *s2_extra,
                    Line("command", ["FlagSet", 830]),
                    Line("command", ["WorkSetConst", 16640, 1]),
                    Line("command", ["StackPushFlag", 2602]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_{ver}_c1"]),
                    Line("command", ["WorkSetConst", 16639, 2]),
                    Line("command", ["FlagSet", 1036]),
                    Line("command", ["VMJump", f"lbl_{tag}_g19_chk"]),
                    Line("label", [f"lbl_{tag}_{ver}_c1"]),
                    Line("command", ["WorkSetConst", 16639, 1]),
                    Line("command", ["FlagReset", 1036]),
                    Line("command", ["VMJump", f"lbl_{tag}_g19_chk"]),
                    Line("label", [f"lbl_{tag}_{ver}_s1"]),
                    *(
                        [
                            cmd
                            for k in range(4)
                            for cmd in _flag_branch(
                                2619 + k,
                                f"{tag}_{ver}_sw{k}",
                                [Line("command", ["WorkSetConst", 16629 + k, 1])],
                                [Line("command", ["WorkSetConst", 16629 + k, 0])],
                            )
                        ]
                        if not is_w2
                        else [Line("command", ["WorkSetConst", v, 0]) for v in (16629, 16630, 16631, 16632)]
                    ),
                    Line("command", ["WorkSetConst", 16635, 0]),
                    Line("command", ["FlagReset", 835]),
                    Line("command", ["FlagReset", 836]),
                    Line("command", ["FlagReset", 830]),
                    Line("command", ["FlagReset", 1036]),
                    Line("command", ["WorkSetConst", 16639, 0]),
                    Line("command", ["WorkSetConst", 16640, 0]),
                    Line("command", ["StackPushFlag", 2603]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_{ver}_s0"]),
                    Line("command", ["WorkSetConst", active_var, 2]),
                    Line("command", ["VMJump", f"lbl_{tag}_g19_chk"]),
                    Line("label", [f"lbl_{tag}_{ver}_s0"]),
                    Line("command", ["WorkSetConst", active_var, 1]),
                ]

            cmds: list[Any] = [
                *_set_mode(2),
                Line("command", ["WorkSetConst", 16452, 1]),
                Line("command", ["WorkSetConst", 16624, 4]),
                Line("command", ["WorkSetConst", 16582, 4]),
                Line("command", ["FlagSet", 829]),
                Line("command", ["FlagSet", 1029]),
                Line("command", ["FlagReset", 975]),
                Line("command", ["FlagReset", 364]),
                Line("command", ["StackPushFlag", 2618]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_m2_done_chk"]),
                Line("command", ["FlagReset", 909]),
                Line("command", ["FlagReset", 976]),
                Line("command", ["FlagSet", 977]),
                Line("command", ["FlagSet", 831]),
                Line("command", ["FlagSet", 833]),
                Line("command", ["FlagSet", 834]),
                Line("command", ["FlagReset", 837]),
                Line("command", ["FlagReset", 838]),
                Line("command", ["FlagSet", 839]),
                Line("command", ["StackPush", 16642]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_16642_ok"]),
                Line("command", ["WorkSetConst", 16642, 1]),
                Line("label", [f"lbl_{tag}_16642_ok"]),
                Line("command", ["StackPush", 16643]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_16643_ok"]),
                Line("command", ["WorkSetConst", 16643, 1]),
                Line("label", [f"lbl_{tag}_16643_ok"]),
                Line("command", ["StoreVersion", 32800]),
                Line("command", ["WorkCmpConst", 32800, 23]),
                Line("command", ["VMJumpIf", 5, f"lbl_{tag}_w2"]),
                *_m2_stage_cmds(False),
                Line("command", ["VMJump", f"lbl_{tag}_g19_chk"]),
                Line("label", [f"lbl_{tag}_w2"]),
                *_m2_stage_cmds(True),
                Line("label", [f"lbl_{tag}_g19_chk"]),
                Line("command", ["StackPushFlag", 2590]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_g19_set"]),
                Line("command", ["FlagReset", 832]),
                Line("command", ["VMJump", f"lbl_{tag}_cut_chk"]),
                Line("label", [f"lbl_{tag}_g19_set"]),
                Line("command", ["FlagSet", 832]),
                Line("label", [f"lbl_{tag}_cut_chk"]),
            ]
            if include_warp:
                cmds.extend([
                    Line("command", ["StackPushFlag", 2612]),
                    Line("command", ["StackPushConst", 1]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_chk_cutscene"]),
                    Line("command", ["WorkSetConst", 16646, 3]),
                    Line("command", ["ObjInitWarpGPos", 2, 800, 65531, 241]),
                    Line("command", ["MapReplaceSetEvent", 5, 0, 0]),
                    Line("command", ["MapReplaceSetEvent", 6, 1, 1]),
                    Line("command", ["FlagReset", 1002]),
                    Line("command", ["FlagSet", 855]),
                    Line("command", ["FlagSet", 856]),
                    Line("command", ["VMJump", f"lbl_{tag}_done"]),
                    Line("label", [f"lbl_{tag}_chk_cutscene"]),
                    Line("command", ["StackPush", 16646]),
                    Line("command", ["StackPushConst", 2]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_mr_pre"]),
                    Line("command", ["VMJump", f"lbl_{tag}_done"]),
                    Line("label", [f"lbl_{tag}_mr_pre"]),
                    Line("command", ["MapReplaceSetEvent", 5, 1, 1]),
                    Line("command", ["MapReplaceSetEvent", 6, 0, 0]),
                    Line("command", ["StackPush", 16646]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["StackPush", 16646]),
                    Line("command", ["StackPushConst", 3]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["StackCmp", 6]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{tag}_done"]),
                    Line("command", ["WorkSetConst", 16646, 1]),
                    Line("command", ["VMJump", f"lbl_{tag}_done"]),
                ])
            else:
                cmds.append(Line("command", ["VMJump", f"lbl_{tag}_done"]))
            cmds.extend([
                Line("label", [f"lbl_{tag}_m2_done_chk"]),
                Line("command", ["WorkSetConst", 16625, 0]),
                Line("command", ["WorkSetConst", 16626, 0]),
                *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632, 16635)],
                Line("command", ["WorkSetConst", 16639, 2]),
                Line("command", ["WorkSetConst", 16640, 2]),
                Line("command", ["WorkSetConst", 16642, 2]),
                Line("command", ["WorkSetConst", 16643, 2]),
                Line("command", ["WorkSetConst", 16646, 4]),
                *[Line("command", ["FlagSet", fl]) for fl in (830, 831, 832, 835, 836, 837, 997, 998, 1036)],
                Line("label", [f"lbl_{tag}_done"]),
            ])
            return cmds

        def _build_mode3_state(tag: str) -> list[Any]:
            w2_switches = []
            for k in range(4):
                w2_switches.extend(_flag_branch(
                    2593 + k,
                    f"{tag}_w2sw{k}",
                    [Line("command", ["WorkSetConst", 16629 + k, 1])],
                    [Line("command", ["WorkSetConst", 16629 + k, 0])],
                ))
            return [
                *_set_mode(3),
                Line("command", ["WorkSetConst", 16452, 2]),
                Line("command", ["WorkSetConst", 16624, 4]),
                Line("command", ["WorkSetConst", 16582, 4]),
                Line("command", ["FlagSet", 829]),
                Line("command", ["FlagSet", 1029]),
                Line("command", ["FlagSet", 975]),
                Line("command", ["FlagSet", 364]),
                Line("command", ["WorkSetConst", 16625, 0]),
                Line("command", ["WorkSetConst", 16626, 0]),
                Line("command", ["StackPushFlag", 2615]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_m3_prog"]),
                Line("command", ["WorkSetConst", 16627, 3]),
                Line("command", ["WorkSetConst", 16628, 4]),
                *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632, 16634, 16635, 16644, 16645)],
                *[Line("command", ["WorkSetConst", v, 2]) for v in (16639, 16640, 16641, 16642, 16643, 16677)],
                *[Line("command", ["FlagSet", fl]) for fl in list(range(830, 846)) + [847, 848, 854, 909, 976, 977, 997, 998, 1026, 1036]],
                Line("command", ["FlagReset", 846]),
                Line("command", ["VMJump", f"lbl_{tag}_done"]),
                Line("label", [f"lbl_{tag}_m3_prog"]),
                Line("command", ["FlagReset", 976]),
                Line("command", ["FlagSet", 977]),
                Line("command", ["FlagReset", 1026]),
                Line("command", ["FlagReset", 846]),
                Line("command", ["FlagSet", 833]),
                Line("command", ["FlagSet", 834]),
                Line("command", ["FlagSet", 830]),
                Line("command", ["FlagSet", 831]),
                Line("command", ["StackPushFlag", 2610]),
                Line("command", ["StackPushConst", 1]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_r1126_open"]),
                Line("command", ["WorkSetConst", 16635, 1]),
                Line("command", ["WorkSetConst", 16640, 1]),
                Line("command", ["StoreVersion", 32800]),
                Line("command", ["WorkCmpConst", 32800, 23]),
                Line("command", ["VMJumpIf", 5, f"lbl_{tag}_m3_w2"]),
                Line("command", ["FlagSet", 836]),
                Line("command", ["FlagReset", 835]),
                *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632)],
                Line("command", ["VMJump", f"lbl_{tag}_m3_c_chk"]),
                Line("label", [f"lbl_{tag}_m3_w2"]),
                Line("command", ["FlagSet", 835]),
                Line("command", ["FlagReset", 836]),
                *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632)],
                Line("label", [f"lbl_{tag}_m3_c_chk"]),
                *_flag_branch(
                    2601,
                    f"{tag}_m3_c35",
                    [Line("command", ["WorkSetConst", 16639, 2]), Line("command", ["FlagSet", 1036])],
                    [Line("command", ["WorkSetConst", 16639, 1]), Line("command", ["FlagReset", 1036])],
                ),
                Line("command", ["VMJump", f"lbl_{tag}_lower_chk"]),
                Line("label", [f"lbl_{tag}_r1126_open"]),
                *w2_switches,
                Line("command", ["WorkSetConst", 16635, 0]),
                Line("command", ["FlagReset", 835]),
                Line("command", ["FlagReset", 836]),
                Line("command", ["FlagReset", 1036]),
                Line("command", ["WorkSetConst", 16639, 0]),
                Line("command", ["WorkSetConst", 16640, 0]),
                Line("label", [f"lbl_{tag}_lower_chk"]),
                *_flag_branch(
                    2597,
                    f"{tag}_m3_34",
                    [Line("command", ["WorkSetConst", 16634, 1])],
                    [Line("command", ["WorkSetConst", 16634, 0])],
                ),
                *_flag_branch(
                    2598,
                    f"{tag}_m3_44",
                    [Line("command", ["WorkSetConst", 16644, 1]), Line("command", ["WorkSetConst", 16645, 1]), Line("command", ["FlagSet", 842]), Line("command", ["FlagSet", 843])],
                    [Line("command", ["WorkSetConst", 16644, 0]), Line("command", ["WorkSetConst", 16645, 0]), Line("command", ["FlagSet", 842]), Line("command", ["FlagSet", 843])],
                ),
                *_flag_branch(
                    2599,
                    f"{tag}_m3_27a",
                    [Line("command", ["WorkSetConst", 16627, 3])],
                    _flag_branch(
                        2598,
                        f"{tag}_m3_27b",
                        [Line("command", ["WorkSetConst", 16627, 1])],
                        [Line("command", ["WorkSetConst", 16627, 0])],
                    ),
                ),
                *_flag_branch(
                    2600,
                    f"{tag}_m3_77a",
                    [Line("command", ["WorkSetConst", 16677, 2]), Line("command", ["FlagSet", 840]), Line("command", ["FlagSet", 841])],
                    [
                        Line("command", ["FlagReset", 840]),
                        Line("command", ["FlagReset", 841]),
                        *_flag_branch(
                            2599,
                            f"{tag}_m3_77b",
                            [Line("command", ["WorkSetConst", 16677, 1])],
                            [Line("command", ["WorkSetConst", 16677, 0])],
                        ),
                    ],
                ),
                *_flag_branch(
                    2592,
                    f"{tag}_m3_28a",
                    [
                        Line("command", ["WorkSetConst", 16628, 4]),
                        Line("command", ["WorkSetConst", 16641, 2]),
                        *[Line("command", ["FlagSet", fl]) for fl in (844, 845, 847, 848, 909)],
                        Line("command", ["FlagReset", 854]),
                    ],
                    _flag_branch(
                        2591,
                        f"{tag}_m3_28b",
                        [
                            Line("command", ["WorkSetConst", 16628, 2]),
                            Line("command", ["WorkSetConst", 16641, 1]),
                            *[Line("command", ["FlagReset", fl]) for fl in (844, 845, 848, 854)],
                            Line("command", ["FlagSet", 847]),
                            Line("command", ["FlagSet", 909]),
                        ],
                        [
                            Line("command", ["WorkSetConst", 16641, 0]),
                            *[Line("command", ["FlagReset", fl]) for fl in (844, 845, 847, 909)],
                            Line("command", ["FlagSet", 848]),
                            Line("command", ["FlagSet", 854]),
                            *_flag_branch(
                                2599,
                                f"{tag}_m3_28c",
                                [Line("command", ["WorkSetConst", 16628, 1])],
                                [Line("command", ["WorkSetConst", 16628, 0])],
                            ),
                        ],
                    ),
                ),
                Line("command", ["StackPushFlag", 2614]),
                Line("command", ["StackPushConst", 0]),
                Line("command", ["StackCmp", 1]),
                Line("command", ["VMJumpIf", 255, f"lbl_{tag}_g19_set"]),
                Line("command", ["FlagReset", 832]),
                Line("command", ["VMJump", f"lbl_{tag}_done"]),
                Line("label", [f"lbl_{tag}_g19_set"]),
                Line("command", ["FlagSet", 832]),
                Line("label", [f"lbl_{tag}_done"]),
            ]

        def _build_p2_state(tag: str) -> list[Any]:
            return [
                *_set_mode(4),
                Line("command", ["WorkSetConst", 16452, 3]),
                Line("command", ["WorkSetConst", 16582, 4]),
                Line("command", ["WorkSetConst", 16624, 4]),
                Line("command", ["WorkSetConst", 16625, 0]),
                Line("command", ["WorkSetConst", 16626, 0]),
                Line("command", ["WorkSetConst", 16627, 3]),
                Line("command", ["WorkSetConst", 16628, 4]),
                *[Line("command", ["WorkSetConst", v, 1]) for v in (16629, 16630, 16631, 16632, 16634, 16635, 16644, 16645)],
                *[Line("command", ["WorkSetConst", v, 2]) for v in (16639, 16640, 16641, 16642, 16643)],
                Line("command", ["WorkSetConst", 16677, 0]),
                Line("command", ["FlagReset", 364]),
                Line("command", ["FlagReset", 840]),
                Line("command", ["FlagReset", 841]),
                Line("command", ["FlagReset", 977]),
                Line("command", ["FlagReset", 2616]),
                *[Line("command", ["FlagSet", fl]) for fl in list(range(829, 840)) + [842, 843, 844, 845, 847, 848, 854, 909, 975, 976, 997, 998, 1026, 1036]],
                Line("command", ["FlagReset", 2793]),
                *_flag_branch(
                    429,
                    f"{tag}_p2_429",
                    [Line("command", ["FlagReset", 1029]), Line("command", ["FlagSet", 846])],
                    [Line("command", ["FlagReset", 846]), Line("command", ["FlagSet", 1029])],
                ),
            ]

        def _hide_p2_balls(tag: str, pairs: list[tuple[int, int]], extra: list[Any] | None = None) -> list[Any]:
            cmds: list[Any] = [*_jump_if_not_mode(4, f"lbl_{tag}_balls_skip")]
            if extra:
                cmds.extend(extra)
            for idx_b, (actor_id, item_flag) in enumerate(pairs):
                lbl_b = f"lbl_{tag}_ball_{idx_b}"
                cmds.extend([
                    Line("command", ["StackPushFlag", item_flag]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["VMJumpIf", 255, lbl_b]),
                    Line("command", ["ActorSetGPos", actor_id, 0, 0, 0, 0]),
                    Line("label", [lbl_b]),
                ])
            cmds.append(Line("label", [f"lbl_{tag}_balls_skip"]))
            return cmds

        # PWT (s382): set mode 1 when PWT Frigate starts (flag 2613) and restore on map load until done (flag 2617)
        if len(scripts_narc.files) > 382 and scripts_narc.files[382]:
            sf_382 = disassemble(scripts_narc.files[382])
            mod_382 = _inj_after_cmd(sf_382, ["WorkSetConst", 16624, 1], [
                *_set_mode(1),
                Line("command", ["FlagReset", 2604]),
                Line("command", ["FlagReset", 2605]),
                Line("command", ["WorkSetConst", 16452, 0]),
                Line("command", ["FlagSet", 2613]),
                Line("command", ["FlagSet", 1029]),
                Line("command", ["FlagReset", 829]),
                Line("command", ["FlagReset", 830]),
                Line("command", ["FlagReset", 831]),
                Line("command", ["FlagReset", 975]),
                Line("command", ["FlagReset", 364]),
            ])
            for lbl_382 in ("scr4", "scr16"):
                idx_382 = sf_382.find_label(lbl_382)
                if idx_382 != -1:
                    t_382 = f"pwt_{lbl_382}"
                    sf_382.lines[idx_382 + 1 : idx_382 + 1] = [
                        Line("command", ["StackPushFlag", 2613]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["StackPushFlag", 2617]),
                        Line("command", ["StackPushConst", 0]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["StackCmp", 7]),
                        Line("command", ["VMJumpIf", 255, f"lbl_{t_382}_done"]),
                        *_set_mode(1),
                        Line("command", ["WorkSetConst", 16582, 3]),
                        Line("command", ["WorkSetConst", 16452, 0]),
                        Line("command", ["WorkSetConst", 16624, 1]),
                        Line("command", ["StackPushFlag", 2604]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, f"lbl_{t_382}_chk3"]),
                        Line("command", ["WorkSetConst", 16624, 2]),
                        Line("label", [f"lbl_{t_382}_chk3"]),
                        Line("command", ["StackPushFlag", 2605]),
                        Line("command", ["StackPushConst", 1]),
                        Line("command", ["StackCmp", 1]),
                        Line("command", ["VMJumpIf", 255, f"lbl_{t_382}_flags"]),
                        Line("command", ["WorkSetConst", 16624, 3]),
                        Line("label", [f"lbl_{t_382}_flags"]),
                        Line("command", ["FlagSet", 1029]),
                        Line("command", ["FlagReset", 829]),
                        Line("command", ["FlagReset", 830]),
                        Line("command", ["FlagReset", 831]),
                        Line("command", ["FlagReset", 975]),
                        Line("command", ["FlagReset", 364]),
                        Line("label", [f"lbl_{t_382}_done"]),
                    ]
                    mod_382 = True
            if mod_382:
                scripts_narc.files[382] = bytes(assemble(sf_382))
                modified_scripts = True

        def _sync_ow_init(ow_id: int, new_init: bytes) -> None:
            nonlocal modified_entities
            if a126 is None or len(a126.files) <= ow_id or not a126.files[ow_id]:
                return
            raw_ow = bytearray(a126.files[ow_id])
            if len(raw_ow) < 8:
                return
            calc = 8 + raw_ow[4] * 20 + raw_ow[5] * 36 + raw_ow[6] * 20 + raw_ow[7] * 22
            if calc <= len(raw_ow):
                a126.files[ow_id] = bytes(raw_ow[:calc]) + new_init
                modified_entities = True

        # Route 21 / Seaside Cave (s926, s1028, s1030): set mode 2 & load Route 21 state on map load / boarding,
        # and ensure Frigate model (MapReplaceSetEvent 5, 1, 1) is queued in Seaside Cave (z514/z515) before scr3
        for sc_sid, sc_ow in ((1028, 327), (1030, 390)):
            if len(scripts_narc.files) > sc_sid and scripts_narc.files[sc_sid]:
                sf_sc = disassemble(scripts_narc.files[sc_sid])
                new_idx = (max(sf_sc.script_links.keys()) + 1) if sf_sc.script_links else 0
                new_lbl = f"scr{new_idx}"
                sf_sc.lines.extend([
                    Line("label", [new_lbl]),
                    Line("command", ["StackPushFlag", 2612]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["StackPushFlag", 2618]),
                    Line("command", ["StackPushConst", 0]),
                    Line("command", ["StackCmp", 1]),
                    Line("command", ["StackCmp", 7]),
                    Line("command", ["VMJumpIf", 255, f"lbl_{sc_sid}_skip_mr"]),
                    Line("command", ["MapReplaceSetEvent", 5, 1, 1]),
                    Line("command", ["MapReplaceSetEvent", 6, 0, 0]),
                    Line("label", [f"lbl_{sc_sid}_skip_mr"]),
                    Line("command", ["VMHalt"]),
                ])
                sf_sc.script_links[new_idx] = new_lbl
                scripts_narc.files[sc_sid] = bytes(assemble(sf_sc))
                init_sc = struct.pack("<HHHHHHH", 2, new_idx + 1, 0, 4, new_idx + 1, 0, 0)
                if len(scripts_narc.files) > sc_sid + 1:
                    scripts_narc.files[sc_sid + 1] = init_sc
                _sync_ow_init(sc_ow, init_sc)
                modified_scripts = True
        if len(scripts_narc.files) > 926 and scripts_narc.files[926]:
            sf_926 = disassemble(scripts_narc.files[926])
            mod_926 = _inj_after_cmd(sf_926, ["WorkSetConst", 16646, 3], [Line("command", ["FlagSet", 2612])])
            for lbl in ("scr0", "scr1", "scr2"):
                idx_l = sf_926.find_label(lbl)
                if idx_l != -1:
                    sf_926.lines[idx_l + 1 : idx_l + 1] = _build_mode2_state(f"r21_{lbl}", include_warp=True)
                    mod_926 = True
            if mod_926:
                scripts_narc.files[926] = bytes(assemble(sf_926))
                modified_scripts = True

        # Giant Chasm (s462, s466): set mode 3 & load Giant Chasm state on map load
        for gc_sid, gc_lbls in ((462, ("scr0", "scr1", "scr7")), (466, ("scr7", "scr8"))):
            if len(scripts_narc.files) > gc_sid and scripts_narc.files[gc_sid]:
                sf_gc = disassemble(scripts_narc.files[gc_sid])
                mod_gc = False
                for lbl in gc_lbls:
                    idx_l = sf_gc.find_label(lbl)
                    if idx_l != -1:
                        sf_gc.lines[idx_l + 1 : idx_l + 1] = _build_mode3_state(f"gc_{gc_sid}_{lbl}")
                        mod_gc = True
                if mod_gc:
                    scripts_narc.files[gc_sid] = bytes(assemble(sf_gc))
                    modified_scripts = True

        # Postgame P2 Lab (s476 z238 exterior + s478 z239 interior): set mode 4 on map load AND on z238 gangplank step trigger
        if len(scripts_narc.files) > 476 and scripts_narc.files[476]:
            sf_p2e = disassemble(scripts_narc.files[476])
            new_idx_476 = (max(sf_p2e.script_links.keys()) + 1) if sf_p2e.script_links else 0
            new_lbl_476 = f"scr{new_idx_476}"
            trig_idx_476 = new_idx_476 + 1
            trig_lbl_476 = f"scr{trig_idx_476}"
            sf_p2e.lines.extend([
                Line("label", [new_lbl_476]),
                *_build_p2_state("476"),
                Line("command", ["VMHalt"]),
                Line("label", [trig_lbl_476]),
                Line("command", ["WorkSetConst", 16713, 1]),
                *_jump_if_mode(4, "lbl_476_trig_done"),
                *_build_p2_state("476_trig"),
                Line("label", ["lbl_476_trig_done"]),
                Line("command", ["VMHalt"]),
            ])
            sf_p2e.script_links[new_idx_476] = new_lbl_476
            sf_p2e.script_links[trig_idx_476] = trig_lbl_476
            scripts_narc.files[476] = bytes(assemble(sf_p2e))
            init_477 = struct.pack("<HHHHHHH", 2, new_idx_476 + 1, 0, 4, new_idx_476 + 1, 0, 0)
            if len(scripts_narc.files) > 477:
                scripts_narc.files[477] = init_477
            if a126 is not None and len(a126.files) > 294 and a126.files[294]:
                raw_294 = bytearray(a126.files[294])
                if len(raw_294) >= 8:
                    fc_294, nc_294, wc_294, tc_294 = raw_294[4], raw_294[5], raw_294[6], raw_294[7]
                    trig_off_294 = 8 + fc_294 * 20 + nc_294 * 36 + wc_294 * 20 + tc_294 * 22
                    if trig_off_294 <= len(raw_294):
                        trig_rec_294 = struct.pack("<11H", trig_idx_476 + 1, 0, 16713, 0, 0, 728, 716, 1, 1, 0, 0)
                        new_294 = bytearray(raw_294[:trig_off_294]) + trig_rec_294 + init_477
                        new_294[7] = tc_294 + 1
                        struct.pack_into("<I", new_294, 0, trig_off_294 + 22 - 4)
                        a126.files[294] = bytes(new_294)
                        modified_entities = True
            modified_scripts = True
        if len(scripts_narc.files) > 478 and scripts_narc.files[478]:
            sf_478 = disassemble(scripts_narc.files[478])
            mod_478 = False
            for lbl in ("scr2", "scr4"):
                idx_l = sf_478.find_label(lbl)
                if idx_l != -1:
                    sf_478.lines[idx_l + 1 : idx_l + 1] = _build_p2_state(f"478_{lbl}")
                    mod_478 = True
            if mod_478:
                scripts_narc.files[478] = bytes(assemble(sf_478))
                modified_scripts = True

        # s1110 (Bridge): allow P2 Lab Colress battle/gift (scr5 -> lbl6_13) before Hall of Fame when in mode 4, and track 16627=3 -> 2599 in mode 3
        if len(scripts_narc.files) > 1110 and scripts_narc.files[1110]:
            sf_1110 = disassemble(scripts_narc.files[1110])
            mod_1110 = _inj_after_cmd(sf_1110, ["WorkSetConst", 16627, 3], [
                *_jump_if_not_mode(3, "lbl_1110_2533_skip"),
                Line("command", ["FlagSet", 2599]),
                Line("label", ["lbl_1110_2533_skip"]),
            ])
            scr5_1110 = sf_1110.find_label("scr5")
            if scr5_1110 != -1 and sf_1110.find_label("lbl6_13") != -1:
                sf_1110.lines[scr5_1110 + 2 : scr5_1110 + 2] = _jump_if_mode(4, "lbl6_13")
                mod_1110 = True
            if mod_1110:
                scripts_narc.files[1110] = bytes(assemble(sf_1110))
                modified_scripts = True

        def _make_deck_sync(tag: str) -> list[Any]:
            return [
                *_jump_if_not_mode(2, f"lbl_{tag}_not_m2"),
                *_build_mode2_state(f"{tag}_m2", include_warp=False),
                Line("command", ["VMJump", f"lbl_{tag}_sync_end"]),
                Line("label", [f"lbl_{tag}_not_m2"]),
                *_jump_if_not_mode(3, f"lbl_{tag}_not_m3"),
                *_build_mode3_state(f"{tag}_m3"),
                Line("command", ["VMJump", f"lbl_{tag}_sync_end"]),
                Line("label", [f"lbl_{tag}_not_m3"]),
                *_jump_if_not_mode(4, f"lbl_{tag}_sync_end"),
                *_build_p2_state(f"{tag}_m4"),
                Line("label", [f"lbl_{tag}_sync_end"]),
            ]

        # s1104 (Deck): guard Postgame Colress (1029) to mode 4, set PWT done (2617), track Grunt 19 & PWT mid-progress, hide item balls in mode 4
        if len(scripts_narc.files) > 1104 and scripts_narc.files[1104]:
            sf_1104 = disassemble(scripts_narc.files[1104])
            mod_1104 = False
            for pwt_step, pwt_flag in ((2, 2604), (3, 2605)):
                if _inj_after_cmd(sf_1104, ["WorkSetConst", 16624, pwt_step], [
                    *_jump_if_not_mode(1, f"lbl_1104_pwt_s{pwt_step}"),
                    Line("command", ["FlagSet", pwt_flag]),
                    Line("label", [f"lbl_1104_pwt_s{pwt_step}"]),
                ]):
                    mod_1104 = True
            if _inj_after_cmd(sf_1104, ["WorkSetConst", 16624, 4], [Line("command", ["FlagSet", 2617])]):
                mod_1104 = True
            for r21_step_var in (16626, 16625):
                if _inj_after_cmd(sf_1104, ["WorkSetConst", r21_step_var, 2], [
                    Line("command", ["FlagSet", 2603]),
                ]):
                    mod_1104 = True
            if _inj_after_cmd(sf_1104, ["FlagSet", 832], [
                *_jump_if_not_mode(2, "lbl_1104_not_r21"),
                Line("command", ["FlagSet", 2590]),
                Line("command", ["ObjInitWarpGPos", 2, 17, 0, 43]),
                Line("label", ["lbl_1104_not_r21"]),
                *_jump_if_not_mode(3, "lbl_1104_not_gc"),
                Line("command", ["FlagSet", 2614]),
                Line("label", ["lbl_1104_not_gc"]),
            ]):
                mod_1104 = True
            scr2_1104 = sf_1104.find_label("scr2")
            if scr2_1104 != -1:
                ins_scr2 = scr2_1104 + 2 if (scr2_1104 + 1 < len(sf_1104.lines) and sf_1104.lines[scr2_1104 + 1].parts[:1] == ["VMCall"]) else scr2_1104 + 1
                sf_1104.lines[ins_scr2 : ins_scr2] = [
                    *_jump_if_mode(4, "lbl_1104_allow_p2"),
                    Line("command", ["FlagSet", 1029]),
                    Line("command", ["VMHalt"]),
                    Line("label", ["lbl_1104_allow_p2"]),
                ]
                mod_1104 = True
            lbl1_8_1104 = sf_1104.find_label("lbl1_8")
            lbl1_10_1104 = sf_1104.find_label("lbl1_10")
            lbl1_11_1104 = sf_1104.find_label("lbl1_11")
            if lbl1_8_1104 != -1 and lbl1_10_1104 != -1 and lbl1_11_1104 != -1:
                # Insert lbl_1104_p2_warps before ObjInitWarpGPos 4, 0, 0, 0 under lbl1_10 and dispatch all 4 modes on flags 2606..2609
                for k in range(lbl1_10_1104 + 1, min(len(sf_1104.lines), lbl1_10_1104 + 10)):
                    if sf_1104.lines[k].type == "command" and sf_1104.lines[k].parts == ["ObjInitWarpGPos", 4, 0, 0, 0]:
                        sf_1104.lines.insert(k, Line("label", ["lbl_1104_p2_warps"]))
                        sf_1104.lines[lbl1_8_1104 + 1 : lbl1_8_1104 + 1] = [
                            *_jump_if_not_mode(1, "lbl_1104_chk2"),
                            Line("command", ["ObjInitWarpGPos", 6, 0, 0, 0]),
                            Line("command", ["ObjInitWarpGPos", 7, 0, 0, 0]),
                            Line("command", ["VMJump", "lbl1_11"]),
                            Line("label", ["lbl_1104_chk2"]),
                            *_jump_if_not_mode(2, "lbl_1104_chk34"),
                            Line("command", ["ObjInitWarpGPos", 4, 0, 0, 0]),
                            Line("command", ["ObjInitWarpGPos", 7, 0, 0, 0]),
                            Line("command", ["StackPushFlag", 2590]),
                            Line("command", ["StackPushConst", 0]),
                            Line("command", ["StackCmp", 1]),
                            Line("command", ["VMJumpIf", 255, "lbl_1104_stairs_ok"]),
                            Line("command", ["ObjInitWarpGPos", 2, 0, 0, 0]),
                            Line("label", ["lbl_1104_stairs_ok"]),
                            Line("command", ["VMJump", "lbl1_11"]),
                            Line("label", ["lbl_1104_chk34"]),
                            *_jump_if_mode(3, "lbl_1104_p2_warps"),
                            *_jump_if_not_mode(4, "lbl_1104_p2_warps"),
                            Line("command", ["ObjInitWarpGPos", 0, 0, 0, 0]),
                            Line("command", ["ObjInitWarpGPos", 1, 0, 0, 0]),
                            Line("command", ["ObjInitWarpGPos", 2, 0, 0, 0]),
                            Line("command", ["ObjInitWarpGPos", 3, 0, 0, 0]),
                        ]
                        mod_1104 = True
                        break
            for lbl_s in ("scr0", "scr1"):
                idx_s = sf_1104.find_label(lbl_s)
                if idx_s != -1:
                    sf_1104.lines[idx_s + 1 : idx_s + 1] = [
                        *_make_deck_sync(f"1104_{lbl_s}"),
                        *_hide_p2_balls(f"1104_{lbl_s}", [(26, 1478), (27, 1479)]),
                    ]
                    mod_1104 = True
            scr22_1104 = sf_1104.find_label("scr22")
            if scr22_1104 != -1:
                sf_1104.lines[scr22_1104 + 1 : scr22_1104 + 1] = [
                    Line("command", ["FlagGet", 2590, 32800]),
                    Line("command", ["WorkCmpConst", 32800, 1]),
                    Line("command", ["VMJumpIf", 5, "lbl_1104_scr22_ensure"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                    Line("label", ["lbl_1104_scr22_ensure"]),
                    Line("command", ["FlagGet", 832, 32800]),
                    Line("command", ["WorkCmpConst", 32800, 0]),
                    Line("command", ["VMJumpIf", 1, "lbl_1104_scr22_ok"]),
                    Line("command", ["FlagReset", 832]),
                    Line("command", ["ActorAdd", 14]),
                    Line("command", ["ActorAdd", 15]),
                    Line("label", ["lbl_1104_scr22_ok"]),
                ]
                mod_1104 = True
            if mod_1104:
                scripts_narc.files[1104] = bytes(assemble(sf_1104))
                modified_scripts = True

        # Dynamic progress hooks for North Rooms (s1106 B2 R21 / W2 Chasm, s1126 W2 R21 / B2 Chasm)
        for room_sid, room_src_flag in (
            (1106, 835),
            (1126, 836),
        ):
            if len(scripts_narc.files) > room_sid and scripts_narc.files[room_sid]:
                sf_rm = disassemble(scripts_narc.files[room_sid])
                extra_rm: list[Any] = [
                    *_jump_if_not_mode(2, f"lbl_rm_{room_sid}_chk3"),
                    Line("command", ["FlagSet", 2611]),
                ]
                if room_sid == 1126:
                    extra_rm.append(Line("command", ["FlagSet", 2590]))
                extra_rm.extend([
                    Line("label", [f"lbl_rm_{room_sid}_chk3"]),
                    *_jump_if_not_mode(3, f"lbl_rm_{room_sid}_skip"),
                    Line("command", ["FlagSet", 2610]),
                    Line("label", [f"lbl_rm_{room_sid}_skip"]),
                ])
                if _inj_after_cmd(sf_rm, ["FlagSet", room_src_flag], extra_rm):
                    if room_sid == 1106:
                        for sw_k in range(4):
                            _inj_after_cmd(sf_rm, ["WorkSetConst", 16629 + sw_k, 1], [
                                *_jump_if_not_mode(2, f"lbl_rm1106_sw{sw_k}_chk3"),
                                Line("command", ["FlagSet", 2619 + sw_k]),
                                Line("label", [f"lbl_rm1106_sw{sw_k}_chk3"]),
                                *_jump_if_not_mode(3, f"lbl_rm1106_sw{sw_k}_skip"),
                                Line("command", ["FlagSet", 2593 + sw_k]),
                                Line("label", [f"lbl_rm1106_sw{sw_k}_skip"]),
                            ])
                    scripts_narc.files[room_sid] = bytes(assemble(sf_rm))
                    modified_scripts = True

        # Enforce active mode state table on s1116 (1F Deck) & clear NPCs/barriers in P2 Lab mode (flag 2609)
        if len(scripts_narc.files) > 1116 and scripts_narc.files[1116]:
            sf_1116 = disassemble(scripts_narc.files[1116])
            mod_1116 = False
            if _inj_after_cmd(sf_1116, ["WorkSetConst", 16639, 2], [
                *_jump_if_not_mode(2, "lbl_1116_c_chk3"),
                Line("command", ["FlagSet", 2602]),
                Line("label", ["lbl_1116_c_chk3"]),
                *_jump_if_not_mode(3, "lbl_1116_c_skip"),
                Line("command", ["FlagSet", 2601]),
                Line("label", ["lbl_1116_c_skip"]),
            ]):
                mod_1116 = True
            scr1_1116 = sf_1116.find_label("scr1")
            if scr1_1116 != -1 and sf_1116.find_label("lbl2_7") != -1:
                sf_1116.lines[scr1_1116 + 1 : scr1_1116 + 1] = _make_deck_sync("1116_s1")
                lbl2_7_pos = sf_1116.find_label("lbl_1116_s1_sync_end")
                sf_1116.lines[lbl2_7_pos + 2 : lbl2_7_pos + 2] = [
                    *_jump_if_not_mode(4, "lbl_1116_not_p2"),
                    Line("command", ["FlagSet", 837]),
                    Line("command", ["FlagSet", 997]),
                    Line("command", ["FlagSet", 998]),
                    Line("command", ["VMJump", "lbl2_7"]),
                    Line("label", ["lbl_1116_not_p2"]),
                ]
                mod_1116 = True
            scr2_1116 = sf_1116.find_label("scr2")
            if scr2_1116 != -1:
                sf_1116.lines[scr2_1116 + 1 : scr2_1116 + 1] = _make_deck_sync("1116_s2")
                mod_1116 = True
            if mod_1116:
                scripts_narc.files[1116] = bytes(assemble(sf_1116))
                modified_scripts = True

        # Enforce active mode state table on s1124 (z562 Giant Chasm deck)
        if len(scripts_narc.files) > 1124 and scripts_narc.files[1124]:
            sf_1124_sync = disassemble(scripts_narc.files[1124])
            mod_1124_sync = False
            for lbl_1124 in ("scr5", "scr6", "scr7"):
                idx_1124 = sf_1124_sync.find_label(lbl_1124)
                if idx_1124 != -1:
                    sf_1124_sync.lines[idx_1124 + 1 : idx_1124 + 1] = _make_deck_sync(f"1124_{lbl_1124}")
                    mod_1124_sync = True
            if mod_1124_sync:
                scripts_narc.files[1124] = bytes(assemble(sf_1124_sync))
                modified_scripts = True

        # Hide Frigate item balls in Mode 4 (without setting item flags) & track Mode 3 lower-deck milestones
        m3_hooks: dict[int, list[tuple[list[Any], int]]] = {
            1114: [(["WorkSetConst", 16628, 2], 2591), (["WorkSetConst", 16641, 2], 2592)],
            1122: [(["WorkSetConst", 16634, 1], 2597), (["WorkSetConst", 16644, 1], 2598), (["WorkSetConst", 16677, 2], 2600)],
            1128: [
                *[(["WorkSetConst", 16629 + k, 1], 2593 + k) for k in range(4)],
                (["WorkSetConst", 16645, 1], 2598),
                (["WorkSetConst", 16677, 2], 2600),
            ],
        }
        for hk_sid, hk_list in m3_hooks.items():
            if len(scripts_narc.files) > hk_sid and scripts_narc.files[hk_sid]:
                sf_hk = disassemble(scripts_narc.files[hk_sid])
                mod_hk = False
                for cmd_parts, dst_flag in hk_list:
                    if _inj_after_cmd(sf_hk, cmd_parts, [
                        *_jump_if_not_mode(3, f"lbl_{hk_sid}_{dst_flag}_skip"),
                        Line("command", ["FlagSet", dst_flag]),
                        Line("label", [f"lbl_{hk_sid}_{dst_flag}_skip"]),
                    ]):
                        mod_hk = True
                if hk_sid in (1122, 1128):
                    idx_scr0 = sf_hk.find_label("scr0")
                    if idx_scr0 != -1:
                        sf_hk.lines[idx_scr0 + 1 : idx_scr0 + 1] = [
                            *_jump_if_not_mode(4, f"lbl_{hk_sid}_scr0_p2_skip"),
                            *_build_p2_state(f"{hk_sid}_scr0_p2"),
                            Line("label", [f"lbl_{hk_sid}_scr0_p2_skip"]),
                        ]
                        mod_hk = True
                    extra_balls = [Line("command", ["WorkSetConst", v, 1]) for v in range(16714, 16719)] if hk_sid == 1122 else None
                    pairs_balls = [(12, 1287), (13, 1288), (14, 1290), (15, 1292 if hk_sid == 1122 else 1293)]
                    idx_scr1 = sf_hk.find_label("scr1")
                    if idx_scr1 != -1:
                        sf_hk.lines[idx_scr1 + 1 : idx_scr1 + 1] = _hide_p2_balls(f"{hk_sid}_scr1", pairs_balls, extra_balls)
                        mod_hk = True
                    if hk_sid == 1122:
                        # Password machine (scr11): never require Plasma Card / Flag 356 in either frigate
                        for idx_pw, ln_pw in enumerate(sf_hk.lines):
                            if ln_pw.type == "command" and ln_pw.parts == ["StackPushFlag", 356]:
                                sf_hk.lines[idx_pw] = Line("command", ["StackPushConst", 1])
                                mod_hk = True
                                break
                if mod_hk:
                    scripts_narc.files[hk_sid] = bytes(assemble(sf_hk))
                    modified_scripts = True

        for rm_sid, rm_ow, rm_pairs, preserve_init in (
            (1152, 358, [(0, 1291)], False),
            (1166, 365, [(2, 1289)], True),
        ):
            if len(scripts_narc.files) > rm_sid and scripts_narc.files[rm_sid]:
                sf_rm_b = disassemble(scripts_narc.files[rm_sid])
                new_idx_rm = (max(sf_rm_b.script_links.keys()) + 1) if sf_rm_b.script_links else 0
                new_lbl_rm = f"scr{new_idx_rm}"
                sf_rm_b.lines.extend([
                    Line("label", [new_lbl_rm]),
                    *_hide_p2_balls(f"{rm_sid}_p2", rm_pairs),
                    Line("command", ["VMHalt"]),
                ])
                sf_rm_b.script_links[new_idx_rm] = new_lbl_rm
                scripts_narc.files[rm_sid] = bytes(assemble(sf_rm_b))
                if len(scripts_narc.files) > rm_sid + 1:
                    hdr_rm = struct.pack("<HHH", 4, new_idx_rm + 1, 0)
                    orig_init = bytes(scripts_narc.files[rm_sid + 1]) if preserve_init else b""
                    if orig_init and orig_init != b"\x00\x00\x00\x00":
                        new_init_rm = hdr_rm + orig_init
                    else:
                        new_init_rm = hdr_rm + b"\x00\x00"
                    scripts_narc.files[rm_sid + 1] = new_init_rm
                    _sync_ow_init(rm_ow, new_init_rm)
                modified_scripts = True

        # s1112 (Route 21 departure): mark Route 21 Frigate done (2618) and keep 16452=1 (Route 21)
        if len(scripts_narc.files) > 1112 and scripts_narc.files[1112]:
            sf_1112 = disassemble(scripts_narc.files[1112])
            mod_1112 = _inj_after_cmd(sf_1112, ["WorkSetConst", 16646, 4], [Line("command", ["FlagSet", 2618])])
            for idx_12, ln_12 in enumerate(sf_1112.lines):
                if ln_12.type == "command" and ln_12.parts == ["WorkSetConst", 16452, 2]:
                    sf_1112.lines[idx_12] = Line("command", ["WorkSetConst", 16452, 1])
                    mod_1112 = True
            if mod_1112:
                scripts_narc.files[1112] = bytes(assemble(sf_1112))
                modified_scripts = True

        # s1208 (Giant Chasm Kyurem): mark Giant Chasm Frigate done (2615) and keep western roadblock (879) gated on DNA Splicers
        if len(scripts_narc.files) > 1208 and scripts_narc.files[1208]:
            sf_1208 = disassemble(scripts_narc.files[1208])
            mod_1208 = _inj_after_cmd(sf_1208, ["FlagSet", 885], [Line("command", ["FlagSet", 2615])])
            new_1208_lines = [l for l in sf_1208.lines if not (l.type == "command" and l.parts == ["FlagSet", 879])]
            if len(new_1208_lines) != len(sf_1208.lines):
                sf_1208.lines = new_1208_lines
                mod_1208 = True
            if mod_1208:
                scripts_narc.files[1208] = bytes(assemble(sf_1208))
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

    # Abundant Shrine (Script 752): remove Landorus party + Dream Radar Therian Landorus requirements from Elder gift
    try:
        raw_752 = scripts_narc.files[752]
        if raw_752:
            sf_752 = disassemble(raw_752)
            changed_752 = False
            for i, line in enumerate(sf_752.lines):
                if line.type == "command" and line.parts == ["PokePartyFindEx", 645, 0, 32803, 32804]:
                    sf_752.lines[i] = Line("command", ["WorkSetConst", 32804, 1])
                    changed_752 = True
                elif line.type == "command" and line.parts == ["IsOneShotDRObtained_02F2", 7, 32805]:
                    sf_752.lines[i] = Line("command", ["WorkSetConst", 32805, 1])
                    changed_752 = True
            if changed_752:
                scripts_narc.files[752] = bytes(assemble(sf_752))
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

    # Opelucid Gym (Script 242): skip badge 3D cutscene + heap free/create when talk_to_trainer_without_battling is enabled
    if options and options.get("talk_to_trainer_without_battling", False):
        try:
            raw_242 = scripts_narc.files[242]
            if raw_242:
                sf_242 = disassemble(raw_242)
                new_242 = [
                    l for l in sf_242.lines
                    if not (l.type == "command" and l.parts and l.parts[0] in ("OpelucidGymFreeHeap", "OpelucidGymCreateHeap", "Animate19B"))
                ]
                if len(new_242) != len(sf_242.lines):
                    sf_242.lines = new_242
                    scripts_narc.files[242] = bytes(assemble(sf_242))
                    modified_scripts = True
        except Exception:
            pass

    # Dragonspiral Tower Top (Script 426): keep Dark Stone (617) / Light Stone (616) in bag so Cedric entrance gift (s412) stays reachable
    try:
        raw_426 = scripts_narc.files[426]
        if raw_426:
            sf_426 = disassemble(raw_426)
            new_426 = [
                l for l in sf_426.lines
                if not (l.type == "command" and l.parts and l.parts[0] == "TakeItem" and l.parts[1] in (616, 617))
            ]
            if len(new_426) != len(sf_426.lines):
                sf_426.lines = new_426
                scripts_narc.files[426] = bytes(assemble(sf_426))
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

    # Mistralton Cargo Service Worker (Script 222 sub63): bypass Flying/Psychic type check (flag 472)
    try:
        if len(scripts_narc.files) > 222 and scripts_narc.files[222]:
            sf_222 = disassemble(scripts_narc.files[222])
            changed_222 = False
            for i in range(len(sf_222.lines) - 1):
                line = sf_222.lines[i]
                if (
                    line.type == "command"
                    and line.parts[:2] == ["VMJumpIf", 255]
                    and sf_222.lines[i + 1].type == "command"
                    and sf_222.lines[i + 1].parts == ["StackPush", 32808]
                ):
                    sf_222.lines[i] = Line("command", ["VMJumpIf", 255, "lbl_worker_any_mon"])
                    sf_222.lines.insert(i + 1, Line("label", ["lbl_worker_any_mon"]))
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
            "We're under strict orders not to[NextLine]let anyone past without the Plasma Card![End]"
        )
        t290[0][1].line = (
            "This is our important task! Nobody[NextLine]enters Giant Chasm without the Plasma Card!"
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
