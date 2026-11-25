from __future__ import annotations

from typing import TYPE_CHECKING, Any

try:
    from ..nds_compat import NARC
except (ImportError, ValueError):
    try:
        from worlds.pokemon_b2w2.nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import NARC

if TYPE_CHECKING:
    from .. import PokemonB2W2World
    from ..nds_compat import NintendoDSRom


# B2W2 script NARC: a/0/5/6

def patch_scripts(world: "PokemonB2W2World", rom: "NintendoDSRom") -> None:
    slot_data = world.fill_slot_data() if world else {}
    patch_scripts_from_rom(rom, slot_data)


def patch_scripts_from_rom(rom: "NintendoDSRom", slot_data: dict[str, Any] | None = None) -> None:
    # Patches a/0/5/6 item ball, hidden item, NPC gift, badge, battle, and roadblock scripts
    if slot_data is None:
        slot_data = {}

    script_narc_data = rom.getFileByName("a/0/5/6")
    script_narc = NARC(script_narc_data)

    loc_check_info = slot_data.get("loc_check_info", {})
    all_flags = sorted(int(k) for k in loc_check_info.keys())
    flag_to_text_id: dict[int, int] = {f_id: 21 + i for i, f_id in enumerate(all_flags)}

    hard_required_dowsing = int(slot_data.get("options", {}).get("dowsing_machine_logic", 1)) == 0
    no_trainer_battles = bool(slot_data.get("options", {}).get("talk_to_trainer_without_battling", False))
    patch_gift_flag_injections(script_narc)
    patch_gym_leader_badges(script_narc)
    patch_scripted_trainer_battles(script_narc, no_battle=no_trainer_battles)
    if no_trainer_battles:
        patch_overworld_trainer_no_battle(script_narc)
    patch_item_ball_scripts(script_narc, flag_to_text_id)
    patch_hidden_item_scripts(script_narc, flag_to_text_id, hard_required_dowsing=hard_required_dowsing)
    patch_npc_gift_scripts(script_narc, flag_to_text_id)
    patch_gym_clyde_autocollect(script_narc)
    patch_special_gift_requirements(script_narc, flag_to_text_id)
    patch_roadblock_scripts(script_narc, rom)

    rom.setFileByName("a/0/5/6", script_narc.save())


def patch_special_gift_requirements(script_narc: NARC, flag_to_text_id: dict[int, int] | None = None) -> None:
    # Patches NPC gift scripts whose vanilla conditions would otherwise cause softlocks
    from .script_editing import disassemble, assemble, Line

    if len(script_narc.files) > 938:
        try:
            s938 = disassemble(script_narc.files[938])
            for i, line in enumerate(s938.lines):
                if line.type == "command" and line.parts[0] == "StorePartyCountMore":
                    s938.lines.insert(i + 1, Line(type="command", parts=["WorkSetConst", 32803, 1]))
                    s938.lines.insert(i + 2, Line(type="command", parts=["VMJump", "lbl1_4"]))
                    script_narc.files[938] = assemble(s938)
                    break
        except Exception:
            pass

    if len(script_narc.files) > 752:
        try:
            s752 = disassemble(script_narc.files[752])
            for i, line in enumerate(s752.lines):
                if line.type == "command" and line.parts == ["VMJumpIf", 255, "lbl2_4"]:
                    s752.lines[i] = Line(type="command", parts=["VMJump", "lbl2_4"])
                    script_narc.files[752] = assemble(s752)
                    break
        except Exception:
            pass

    if len(script_narc.files) > 878:
        try:
            s878 = disassemble(script_narc.files[878])
            for i, line in enumerate(s878.lines):
                if line.type == "command" and line.parts == ["***HABITATLISTENABLE***"]:
                    gift_lines = [
                        Line("command", ["StackPush", 32768]),
                        Line("command", ["StackPush", 32769]),
                    ]
                    if flag_to_text_id and 2345 in flag_to_text_id:
                        gift_lines.extend([
                            Line("command", ["WorkSetConst", 16798, flag_to_text_id[2345]]),
                            Line("command", ["WorkSetConst", 32768, 639]),
                            Line("command", ["WorkSetConst", 32769, 1]),
                        ])
                    else:
                        gift_lines.extend([
                            Line("command", ["WorkSet", 32768, 4]),
                            Line("command", ["WorkSet", 32769, 5]),
                        ])
                    gift_lines.extend([
                        Line("command", ["RTCallGlobal", 2805]),
                        Line("command", ["StackPop", 32769]),
                        Line("command", ["StackPop", 32768]),
                        Line("command", ["FlagSet", 2345]),
                    ])
                    start_i = i - 5 if i >= 5 and s878.lines[i - 5].parts == ["PlaySound", 2176] else i
                    s878.lines[start_i : i + 1] = gift_lines
                    break
            for i, line in enumerate(s878.lines):
                if line.type == "command" and line.parts == ["WorkSetConst", 16723, 2]:
                    s878.lines.insert(i + 1, Line("command", ["FlagSet", 2345]))
                    break
            script_narc.files[878] = bytes(assemble(s878))
        except Exception:
            pass

    if len(script_narc.files) > 254:
        try:
            s254 = disassemble(script_narc.files[254])
            for i, line in enumerate(s254.lines):
                if line.type == "command" and line.parts == ["CheckItemBagNumber", 578, 1, 32784]:
                    s254.lines.insert(i + 1, Line(type="command", parts=["WorkSetConst", 32784, 1]))
                    script_narc.files[254] = bytes(assemble(s254))
                    break
        except Exception:
            pass

    # Driftveil Luxury Suites 1F Lady (204): bypass random owned-TM move check
    if len(script_narc.files) > 204:
        try:
            s204 = disassemble(script_narc.files[204])
            sub5_idx = s204.find_label("sub5")
            if sub5_idx != -1 and s204.find_label("lbl2_9") != -1:
                s204.lines[sub5_idx + 1 : sub5_idx + 1] = [
                    Line("command", ["WorkSetConst", 32802, 0]),
                    Line("command", ["VMJump", "lbl2_9"]),
                ]
                script_narc.files[204] = bytes(assemble(s204))
        except Exception:
            pass


def patch_roadblock_scripts(script_narc: NARC, rom: Any | None = None) -> None:
    # Patches roadblock scripts so that in-game passage rules align with archi logic items
    from .script_editing import disassemble, assemble, Line

    if len(script_narc.files) > 892:
        try:
            s892 = disassemble(script_narc.files[892])
            idx6 = s892.find_label("scr6")
            if idx6 != -1:
                for k in range(idx6 + 1, min(idx6 + 40, len(s892.lines))):
                    if s892.lines[k].type == "command" and s892.lines[k].parts == ["ObjInitNPCGPos", 0, 1, 160, 2, 643]:
                        s892.lines[k:k] = [
                            Line("command", ["StackPushFlag", 1726]),
                            Line("command", ["StackPushConst", 0]),
                            Line("command", ["StackCmp", 1]),
                            Line("command", ["VMJumpIf", 255, "lbl7_38"]),
                        ]
                        break
            idx0 = s892.find_label("scr0")
            if idx0 != -1:
                s892.lines[idx0 + 1 : idx0 + 1] = [
                    Line("command", ["StoreBadge", 32776, 0]),
                    Line("command", ["WorkCmpConst", 32776, 1]),
                    Line("command", ["VMJumpIf", 1, "scr1"]),
                ]
            idx1 = s892.find_label("scr1")
            if idx1 != -1:
                s892.lines[idx1 + 1 : idx1 + 1] = [
                    Line("command", ["StoreBadge", 32776, 0]),
                    Line("command", ["WorkCmpConst", 32776, 0]),
                    Line("command", ["VMJumpIf", 1, "scr0"]),
                    Line("command", ["FlagGet", 1726, 32776]),
                    Line("command", ["WorkCmpConst", 32776, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_jerome_pass"]),
                ]
            for i, line in enumerate(s892.lines):
                if line.type == "command" and line.parts == ["WorkSetConst", 16555, 2]:
                    s892.lines.insert(i + 1, Line("command", ["FlagSet", 1726]))
                    break
            idx3 = s892.find_label("scr3")
            if idx3 != -1:
                s892.lines[idx3 + 1 : idx3 + 1] = [
                    Line("command", ["StoreBadge", 32776, 0]),
                    Line("command", ["WorkCmpConst", 32776, 0]),
                    Line("command", ["VMJumpIf", 1, "scr0"]),
                    Line("command", ["FlagGet", 1726, 32776]),
                    Line("command", ["WorkCmpConst", 32776, 0]),
                    Line("command", ["VMJumpIf", 1, "scr1"]),
                    Line("label", ["lbl_jerome_pass"]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ]
            idx2 = s892.find_label("scr2")
            if idx2 != -1:
                s892.lines[idx2 + 1 : idx2 + 1] = [
                    Line("command", ["FlagGet", 701, 32776]),
                    Line("command", ["WorkCmpConst", 32776, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_scr2_skip"]),
                    Line("command", ["FlagGet", 703, 32776]),
                    Line("command", ["WorkCmpConst", 32776, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_scr2_skip"]),
                    Line("command", ["FlagGet", 2363, 32776]),
                    Line("command", ["WorkCmpConst", 32776, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_scr2_skip"]),
                ]
                s892.lines.extend([
                    Line("label", ["lbl_scr2_skip"]),
                    Line("command", ["WorkSetConst", 16555, 6]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
            scr1_pos = s892.find_label("scr1")
            if scr1_pos != -1:
                act_up = None
                act_down = None
                for k in range(scr1_pos, min(scr1_pos + 45, len(s892.lines))):
                    if s892.lines[k].type == "command" and s892.lines[k].parts == ["StackPushConst", 644]:
                        for m in range(k + 1, min(k + 8, len(s892.lines))):
                            if s892.lines[m].type == "command" and s892.lines[m].parts[0] == "ActorCmdExec" and s892.lines[m].parts[1] == 0:
                                act_up = s892.lines[m].parts[2]
                                break
                    elif s892.lines[k].type == "command" and s892.lines[k].parts == ["StackPushConst", 646]:
                        for m in range(k + 1, min(k + 8, len(s892.lines))):
                            if s892.lines[m].type == "command" and s892.lines[m].parts[0] == "ActorCmdExec" and s892.lines[m].parts[1] == 0:
                                act_down = s892.lines[m].parts[2]
                                break
                for lbl_name, turn_cmd in ((act_up, "TurnN8F"), (act_down, "TurnS8F")):
                    if lbl_name:
                        a_idx = s892.find_label(lbl_name)
                        if a_idx != -1:
                            end_idx = a_idx + 1
                            while end_idx < len(s892.lines) and s892.lines[end_idx].type == "action" and s892.lines[end_idx].parts[0] != "EndAction":
                                end_idx += 1
                            s892.lines[a_idx + 1 : end_idx] = [Line("action", [turn_cmd, 1])]
            script_narc.files[892] = bytes(assemble(s892))

            if rom is not None:
                a003_data = rom.getFileByName("a/0/0/3")
                if a003_data is not None:
                    a003 = NARC(a003_data)
                    from .text import decode, encode
                    texts = decode(a003.files[603])
                    jerome_msg = "C'mon... A kid without the Basic[NextLine]Badge can't pass here![End][NextLine]Battle with the Trainers and Pokémon[NextLine]in this area, then battle some more!"
                    texts[0][1].line = jerome_msg
                    texts[0][2].line = jerome_msg + "[End]"
                    a003.files[603] = encode(texts)
                    rom.setFileByName("a/0/0/3", a003.save())

                a126_data = rom.getFileByName("a/1/2/6")
                if a126_data is not None:
                    a126 = NARC(a126_data)
                    if len(a126.files) > 560:
                        import struct
                        f560 = bytearray(a126.files[560])
                        _, nf, nn, nw, nt = struct.unpack_from("<IBBBB", f560, 0)
                        off_trig = 8 + nf * 20 + nn * 36 + nw * 20
                        modified_560 = False
                        for t_idx in range(nt):
                            t_off = off_trig + t_idx * 22
                            if t_off + 22 > len(f560):
                                break
                            scr_f, val_f, var_f = struct.unpack_from("<3H", f560, t_off)
                            x_f = struct.unpack_from("<H", f560, t_off + 10)[0]
                            if scr_f == 2 and val_f == 1 and var_f == 16555 and x_f == 158:
                                f560[t_off + 10 : t_off + 12] = (159).to_bytes(2, "little")
                                modified_560 = True
                        if modified_560:
                            a126.files[560] = bytes(f560)
                            rom.setFileByName("a/1/2/6", a126.save())
        except Exception:
            pass

    if len(script_narc.files) > 504:
        try:
            s504 = disassemble(script_narc.files[504])
            idx4 = s504.find_label("scr4")
            if idx4 != -1:
                s504.lines[idx4 + 1 : idx4 + 1] = [
                    Line("command", ["FlagGet", 2400, 32800]),
                    Line("command", ["WorkCmpConst", 32800, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_skyarrow_pass"]),
                ]
                s504.lines.extend([
                    Line("label", ["lbl_skyarrow_pass"]),
                    Line("command", ["WorkSetConst", 16609, 1]),
                    Line("command", ["FlagSet", 809]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
            script_narc.files[504] = bytes(assemble(s504))
        except Exception:
            pass

    if len(script_narc.files) > 698:
        try:
            s698 = disassemble(script_narc.files[698])
            idx4 = s698.find_label("scr4")
            if idx4 != -1:
                s698.lines[idx4 + 1 : idx4 + 1] = [
                    Line("command", ["FlagGet", 2400, 32800]),
                    Line("command", ["WorkCmpConst", 32800, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_tubeline_pass"]),
                ]
                s698.lines.extend([
                    Line("label", ["lbl_tubeline_pass"]),
                    Line("command", ["ActorSetGPos", 2, 3, 0, 8, 3]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
            script_narc.files[698] = bytes(assemble(s698))
        except Exception:
            pass


    if len(script_narc.files) > 192:
        try:
            s192 = disassemble(script_narc.files[192])
            idx29 = s192.find_label("scr29")
            if idx29 != -1:
                s192.lines[idx29 + 1 : idx29 + 1] = [
                    Line("command", ["FlagGet", 2400, 32800]),
                    Line("command", ["WorkCmpConst", 32800, 1]),
                    Line("command", ["VMJumpIf", 1, "lbl_clay_pass"]),
                ]
                s192.lines.extend([
                    Line("label", ["lbl_clay_pass"]),
                    Line("command", ["WorkSetConst", 16580, 1]),
                    Line("command", ["FlagSet", 718]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ])
            script_narc.files[192] = bytes(assemble(s192))
        except Exception:
            pass

    if len(script_narc.files) > 768:
        try:
            s768 = disassemble(script_narc.files[768])
            idx0 = s768.find_label("scr0")
            if idx0 != -1:
                for i in range(idx0, min(idx0 + 6, len(s768.lines))):
                    if s768.lines[i].type == "command" and s768.lines[i].parts == ["StackPushFlag", 2400]:
                        s768.lines[i : i + 3] = [
                            Line("command", ["StoreBadgeNumber", 32800]),
                            Line("command", ["StackPush", 32800]),
                            Line("command", ["StackPushConst", 8]),
                            Line("command", ["StackCmp", 0]),
                        ]
                        break
            idx1 = s768.find_label("scr1")
            if idx1 != -1:
                for i in range(idx1, min(idx1 + 6, len(s768.lines))):
                    if s768.lines[i].type == "command" and s768.lines[i].parts == ["StackPushFlag", 2400]:
                        s768.lines[i : i + 3] = [
                            Line("command", ["StoreBadgeNumber", 32800]),
                            Line("command", ["StackPush", 32800]),
                            Line("command", ["StackPushConst", 8]),
                            Line("command", ["StackCmp", 4]),
                        ]
                        break
            script_narc.files[768] = bytes(assemble(s768))
        except Exception:
            pass

    # Route 19 (874): remove Alder's first cutscene (scr1) while preserving his post-Floccesy gift (scr6)
    if len(script_narc.files) > 874:
        try:
            s874 = disassemble(script_narc.files[874])
            modified_874 = False
            i = 0
            while i < len(s874.lines):
                line = s874.lines[i]
                if line.type == "command" and line.parts == ["WorkSetConst", 16547, 1]:
                    s874.lines[i] = Line("command", ["WorkSetConst", 16547, 2])
                    if not (
                        i + 1 < len(s874.lines)
                        and s874.lines[i + 1].type == "command"
                        and s874.lines[i + 1].parts == ["FlagSet", 738]
                    ):
                        s874.lines.insert(i + 1, Line("command", ["FlagSet", 738]))
                    modified_874 = True
                i += 1
            idx1 = s874.find_label("scr1")
            if idx1 != -1 and not (
                idx1 + 1 < len(s874.lines)
                and s874.lines[idx1 + 1].type == "command"
                and s874.lines[idx1 + 1].parts == ["WorkSetConst", 16547, 2]
            ):
                s874.lines[idx1 + 1 : idx1 + 1] = [
                    Line("command", ["WorkSetConst", 16547, 2]),
                    Line("command", ["FlagSet", 738]),
                    Line("command", ["RTFinishSubEvents"]),
                    Line("command", ["ActorUnlockAll"]),
                    Line("command", ["VMHalt"]),
                ]
                modified_874 = True
            if modified_874:
                script_narc.files[874] = bytes(assemble(s874))
        except Exception:
            pass

    # Virbank City (896): skip both start cutscenes
    if len(script_narc.files) > 896:
        try:
            s896 = disassemble(script_narc.files[896])
            modified_896 = False
            for lbl_name in ("scr8", "scr0"):
                idx = s896.find_label(lbl_name)
                if idx != -1 and not (
                    idx + 1 < len(s896.lines)
                    and s896.lines[idx + 1].type == "command"
                    and s896.lines[idx + 1].parts == ["WorkSetConst", 16556, 2]
                ):
                    s896.lines[idx + 1 : idx + 1] = [
                        Line("command", ["WorkSetConst", 16556, 2]),
                        Line("command", ["FlagSet", 726]),
                        Line("command", ["FlagSet", 2489]),
                        Line("command", ["RTFinishSubEvents"]),
                        Line("command", ["ActorUnlockAll"]),
                        Line("command", ["VMHalt"]),
                    ]
                    modified_896 = True
            idx23 = s896.find_label("scr23")
            if idx23 != -1 and s896.find_label("lbl_virbank_init_done") == -1:
                s896.lines[idx23 + 1 : idx23 + 1] = [
                    Line("command", ["StackPush", 16556]),
                    Line("command", ["StackPushConst", 2]),
                    Line("command", ["StackCmp", 0]),
                    Line("command", ["VMJumpIf", 255, "lbl_virbank_init_done"]),
                    Line("command", ["WorkSetConst", 16556, 2]),
                    Line("command", ["FlagSet", 726]),
                    Line("command", ["FlagSet", 2489]),
                    Line("label", ["lbl_virbank_init_done"]),
                ]
                modified_896 = True
            if modified_896:
                script_narc.files[896] = bytes(assemble(s896))
        except Exception:
            pass

    # Virbank Gym (1004): skip pokestar and enable grunt at harbour
    if len(script_narc.files) > 1004:
        try:
            s1004 = disassemble(script_narc.files[1004])
            modified_1004 = False
            for i, l in enumerate(s1004.lines):
                if (
                    l.type == "command"
                    and l.parts == ["WorkSetConst", 16557, 1]
                    and i + 3 < len(s1004.lines)
                    and s1004.lines[i + 1].parts == ["WorkSetConst", 16650, 1]
                    and s1004.lines[i + 2].parts == ["WorkSetConst", 16556, 3]
                ):
                    s1004.lines[i : i + 3] = [
                        Line("command", ["WorkSetConst", 16557, 2]),
                        Line("command", ["WorkSetConst", 16650, 3]),
                        Line("command", ["WorkSetConst", 16556, 5]),
                        Line("command", ["FlagSet", 720]),
                        Line("command", ["FlagSet", 721]),
                        Line("command", ["FlagSet", 2440]),
                        Line("command", ["FlagReset", 724]),
                    ]
                    modified_1004 = True
                    break
            if modified_1004:
                script_narc.files[1004] = bytes(assemble(s1004))
        except Exception:
            pass

    # Castelia Gym (976): keep Colress hidden at Castelia fountain (flag 756) after beating Burgh
    if len(script_narc.files) > 976:
        try:
            s976 = disassemble(script_narc.files[976])
            modified_976 = False
            for i, l in enumerate(s976.lines):
                if l.type == "command" and l.parts == ["FlagReset", 756]:
                    s976.lines[i] = Line("command", ["FlagSet", 756])
                    modified_976 = True
            if modified_976:
                script_narc.files[976] = bytes(assemble(s976))
        except Exception:
            pass

    # Virbank Harbor (904): ensure Harlequin counter (16610) is initialised if story_roadblocks was disabled
    if len(script_narc.files) > 904:
        try:
            s904 = disassemble(script_narc.files[904])
            if s904.find_label("lbl3_harlequin_ok") == -1:
                modified_904 = False
                i = 0
                while i < len(s904.lines):
                    if (
                        s904.lines[i].type == "command"
                        and s904.lines[i].parts == ["MapChangeCore", 38, 12, 0, 10, 2]
                    ):
                        init_lines = [
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
                        ]
                        s904.lines[i:i] = init_lines
                        modified_904 = True
                        break
                    i += 1
                if modified_904:
                    script_narc.files[904] = bytes(assemble(s904))
        except Exception:
            pass

    # Castelia City Harlequin (56, 102, 504): preserve clowns found before scr19 & sync 16610 before prize check
    if len(script_narc.files) > 56:
        try:
            s56 = disassemble(script_narc.files[56])
            modified_56 = False
            i = 0
            while i < len(s56.lines):
                if s56.lines[i].type == "command" and s56.lines[i].parts == ["WorkSetConst", 16610, 2]:
                    preserve_lines = [
                        Line("command", ["WorkSetConst", 16610, 2]),
                        Line("command", ["FlagGet", 312, 32804]),
                        Line("command", ["WorkAdd", 16610, 32804]),
                        Line("command", ["FlagGet", 313, 32804]),
                        Line("command", ["WorkAdd", 16610, 32804]),
                        Line("command", ["FlagGet", 314, 32804]),
                        Line("command", ["WorkAdd", 16610, 32804]),
                        Line("command", ["FlagSet", 2338]),
                    ]
                    s56.lines[i : i + 1] = preserve_lines
                    modified_56 = True
                    i += len(preserve_lines)
                    continue
                i += 1
            if modified_56:
                script_narc.files[56] = bytes(assemble(s56))
        except Exception:
            pass

    for h_idx, h_lbl in ((56, "scr20"), (102, "scr6"), (504, "scr6")):
        if len(script_narc.files) > h_idx:
            try:
                sh = disassemble(script_narc.files[h_idx])
                skip_lbl = f"lbl_sync_harlequin_{h_idx}"
                if sh.find_label(skip_lbl) == -1:
                    h_pos = sh.find_label(h_lbl)
                    if h_pos != -1:
                        # Insert right before StackPush 16610 inside this Harlequin check block
                        for k in range(h_pos + 1, min(len(sh.lines), h_pos + 12)):
                            if sh.lines[k].type == "command" and sh.lines[k].parts == ["StackPush", 16610]:
                                sh.lines[k:k] = [
                                    Line("command", ["FlagGet", 2476, 32804]),
                                    Line("command", ["StackPush", 32804]),
                                    Line("command", ["StackPushConst", 1]),
                                    Line("command", ["StackCmp", 1]),
                                    Line("command", ["VMJumpIf", 255, skip_lbl]),
                                    Line("command", ["StackPush", 16610]),
                                    Line("command", ["StackPushConst", 6]),
                                    Line("command", ["StackCmp", 0]),
                                    Line("command", ["VMJumpIf", 255, skip_lbl]),
                                    Line("command", ["WorkSetConst", 16610, 2]),
                                    Line("command", ["FlagGet", 312, 32804]),
                                    Line("command", ["WorkAdd", 16610, 32804]),
                                    Line("command", ["FlagGet", 313, 32804]),
                                    Line("command", ["WorkAdd", 16610, 32804]),
                                    Line("command", ["FlagGet", 314, 32804]),
                                    Line("command", ["WorkAdd", 16610, 32804]),
                                    Line("command", ["WorkSetConst", 32804, 0]),
                                    Line("label", [skip_lbl]),
                                ]
                                script_narc.files[h_idx] = bytes(assemble(sh))
                                break
            except Exception:
                pass


def patch_item_ball_scripts(script_narc: NARC, flag_to_text_id: dict[int, int]) -> None:
    # Patches overworld item balls in a/0/5/6 file 1240
    from .script_editing import disassemble, assemble, Line

    s1240 = disassemble(script_narc.files[1240])
    new_lines: list[Line] = []
    skip_until_label = False
    for line in s1240.lines:
        if line.type == "label":
            skip_until_label = False
            if line.parts[0].startswith("scr"):
                try:
                    cur_scr = int(line.parts[0][3:])
                except ValueError:
                    cur_scr = -1
                flag_id = 1100 + cur_scr if cur_scr != -1 else -1
                if flag_id in flag_to_text_id:
                    text_id = flag_to_text_id[flag_id]
                    new_lines.extend([
                        Line("label", [f"scr{cur_scr}"]),
                        Line("command", ["ActorPauseAll"]),
                        Line("command", ["ActorSetEyeToEye"]),
                        Line("command", ["ActorGetSpawnFlag", 32785, 32784]),
                        Line("command", ["FlagSet", 32784]),
                        Line("command", ["ActorDelete", 32785]),
                        Line("command", ["WorkSetConst", 16798, text_id]),
                        Line("command", ["WorkSetConst", 32768, 639]),
                        Line("command", ["WorkSetConst", 32769, 1]),
                        Line("command", ["RTCallGlobal", 2811]),
                        Line("command", ["RTFinishSubEvents"]),
                        Line("command", ["ActorUnlockAll"]),
                        Line("command", ["VMHalt"]),
                    ])
                    skip_until_label = True
                    continue
        if not skip_until_label:
            new_lines.append(line)

    s1240.lines = new_lines
    script_narc.files[1240] = bytes(assemble(s1240))


def patch_hidden_item_scripts(
    script_narc: NARC,
    flag_to_text_id: dict[int, int],
    hard_required_dowsing: bool = False,
) -> None:
    # Patches hidden items in a/0/5/6 file 1241
    from .script_editing import disassemble, assemble, Line

    s1241 = disassemble(script_narc.files[1241])
    new_lines: list[Line] = []
    skip_until_label = False
    for line in s1241.lines:
        if line.type == "label":
            skip_until_label = False
            if line.parts[0].startswith("scr"):
                try:
                    cur_scr = int(line.parts[0][3:])
                except ValueError:
                    cur_scr = -1
                flag_id = 2820 + cur_scr if cur_scr != -1 else -1
                if flag_id in flag_to_text_id:
                    text_id = flag_to_text_id[flag_id]
                    new_lines.extend([
                        Line("label", [f"scr{cur_scr}"]),
                        Line("command", ["ActorPauseAll"]),
                    ])
                    if hard_required_dowsing:
                        new_lines.extend([
                            Line("command", ["CheckItemBagNumber", 471, 1, 32784]),
                            Line("command", ["StackPush", 32784]),
                            Line("command", ["StackPushConst", 1]),
                            Line("command", ["StackCmp", 1]),
                            Line("command", ["VMJumpIf", 255, f"lbl_no_dowsing_{cur_scr}"]),
                        ])
                    new_lines.extend([
                        Line("command", ["WorkSetConst", 16798, text_id]),
                        Line("command", ["WorkSetConst", 32768, 639]),
                        Line("command", ["WorkSetConst", 32769, 1]),
                        Line("command", ["WorkSetConst", 32770, 2820 + cur_scr]),
                        Line("command", ["RTCallGlobal", 2811]),
                        Line("command", ["FlagSet", 2820 + cur_scr]),
                        Line("command", ["RTFinishSubEvents"]),
                        Line("command", ["ActorUnlockAll"]),
                        Line("command", ["VMHalt"]),
                    ])
                    if hard_required_dowsing:
                        new_lines.extend([
                            Line("label", [f"lbl_no_dowsing_{cur_scr}"]),
                            Line("command", ["RTFinishSubEvents"]),
                            Line("command", ["ActorUnlockAll"]),
                            Line("command", ["VMHalt"]),
                        ])
                    skip_until_label = True
                    continue
        if not skip_until_label:
            new_lines.append(line)

    s1241.lines = new_lines
    script_narc.files[1241] = bytes(assemble(s1241))

    s1238 = disassemble(script_narc.files[1238])

    lbl1_1_idx = s1238.find_label("lbl1_1")
    if lbl1_1_idx != -1:
        close_idx = -1
        for k in range(lbl1_1_idx + 1, min(len(s1238.lines), lbl1_1_idx + 10)):
            if s1238.lines[k].type == "command" and s1238.lines[k].parts == ["MsgActorClose"]:
                close_idx = k
                break
        target_idx = close_idx if close_idx != -1 else lbl1_1_idx
        s1238.lines[target_idx + 1 : target_idx + 1] = [
            Line("command", ["WorkCmpConst", 32768, 639]),
            Line("command", ["VMJumpIf", 1, "lbl1_2"]),
        ]

    scr5_idx = s1238.find_label("scr5")
    if scr5_idx != -1:
        s1238.lines[scr5_idx + 1 : scr5_idx + 1] = [
            Line("command", ["WorkCmpConst", 32768, 639]),
            Line("command", ["VMJumpIf", 1, "lbl6_30"]),
        ]

    sub33_idx = s1238.find_label("sub33")
    if sub33_idx != -1:
        s1238.lines[sub33_idx + 1 : sub33_idx + 1] = [
            Line("command", ["WorkCmpConst", 32768, 639]),
            Line("command", ["VMJumpIf", 1, "lbl7_34"]),
        ]

    for sub_name in ("sub37", "sub62"):
        sub_idx = s1238.find_label(sub_name)
        if sub_idx != -1:
            s1238.lines[sub_idx + 1 : sub_idx + 1] = [
                Line("command", ["WorkCmpConst", 32768, 639]),
                Line("command", ["VMJumpIf", 1, "lbl_sub37_remote"]),
            ]

    for sub_name in ("sub3", "sub24"):
        sub_idx = s1238.find_label(sub_name)
        if sub_idx != -1:
            s1238.lines[sub_idx + 1 : sub_idx + 1] = [
                Line("command", ["WorkCmpConst", 32776, 639]),
                Line("command", ["VMJumpIf", 1, "lbl_npc_remote"]),
            ]

    # Append remote NPC gift check handlers
    s1238.lines.extend([
        Line("label", ["lbl_sub37_remote"]),
        Line("command", ["VMCall", "lbl_npc_remote"]),
        Line("command", ["WorkSetConst", 32784, 0]),
        Line("command", ["VMReturn"]),

        Line("label", ["lbl_npc_remote"]),
        Line("command", ["PlayFanfare", 1302]),
        Line("command", ["WordSetPlayerName", 0]),
        Line("command", ["WorkCmpConst", 16798, 0]),
        Line("command", ["VMJumpIf", 1, "lbl_npc_default_msg"]),
        Line("command", ["VMJump", "lbl_npc_has_msg"]),
        Line("label", ["lbl_npc_default_msg"]),
        Line("command", ["WorkSetConst", 16798, 20]),
        Line("label", ["lbl_npc_has_msg"]),
        Line("command", ["MsgSystem", 16798, 0]),
        Line("command", ["WaitFanfare"]),
        Line("command", ["MsgWaitAdvance"]),
        Line("command", ["MsgSystemClose"]),
        Line("command", ["WorkSetConst", 16798, 0]),
        Line("command", ["WorkSetConst", 32784, 1]),
        Line("command", ["VMReturn"]),
    ])

    script_narc.files[1238] = bytes(assemble(s1238))


VAR_TO_GIFT_FLAG: dict[tuple[int, int], int] = {
    (16608, 1): 1703,   # Route 19 gate woman
    (16547, 4): 2361,   # Route 19 Alder
    (16723, 2): 2345,   # Floccesy town Bianca C-Gear
    (16555, 3): 2363,   # Route 20 Cheren
    (16551, 1): 2343,   # Floccesy rancher's wife potion
    (16551, 3): 2344,   # Floccesy Hugh northwest
    (16721, 1): 2367,   # Virbank Route 20 gate
    (16551, 5): 2371,   # Floccesy Plasma grunt TM21 frustration
    (16552, 3): 2368,   # Aspertia Bianca TM27 return
    (16695, 1): 2369,   # Castelia alley flash TM70
    (16676, 1): 2375,   # Victory road Hugh TM24
    (16647, 2): 2335,   # Accumula pianist
    (16610, 6): 2339,   # Castelia Harlequin after finding clowns
    (16622, 7): 2347,   # Humilau walkway
    (16519, 2): 2350,   # musical owner
    (16604, 1): 2561,   # Nacrene Cafe Warehouse Grubby Hanky (Sun)
    (16604, 3): 2353,   # Nacrene Cafe Warehouse Fluffy Tail (Sun/Thu)
    (16648, 7): 2586,   # Skyarrow Bridge Marathon Runner
}

CUSTOM_GIFT_INJECTIONS: list[tuple[int, list[Any], int]] = [
    (638, ["WorkSet", 32768, 109], 2362),    # Route 2 Dawn Stone lady
    (896, ["WorkSet", 32768, 420], 1704),    # Virbank Roxie outside gym (HM01 cut)
    (652, ["WorkSet", 32768, 46], 1705),     # Route 4 (B2) Colress after battle
    (1102, ["WorkSet", 32768, 46], 1705),    # Route 4 (W2) Colress after battle
    (102, ["WorkSet", 32768, 471], 1706),    # Castelia gate Bianca
    (214, ["WorkSet", 32768, 1], 1707),      # Mistralton Juniper on runway
    (676, ["WorkSet", 32768, 231], 1711),    # Celestial Tower 1F Juniper (Lucky Egg)
    (556, ["WorkSet", 32768, 617], 1708),    # N's castle N in throne room (B2 dark stone)
    (556, ["WorkSet", 32768, 616], 1708),    # N's castle N in throne room (W2 light stone)
    (824, ["WorkSet", 32768, 425], 414),     # Undella Town Hugh outside villa (HM06 dive)
    (824, ["WorkSet", 32768, 89], 2803),      # Undella Town Zinzolin in front of gate (Big Pearl)
    (824, ["WorkSetConst", 32768, 89], 2803),
    (752, ["WorkSet", 32768, 638], 1710),    # Abundant Shrine elder
    (56, ["WorkSet", 32768, 450], 2338),     # Castelia harlequin (bicycle)
    (56, ["WorkSet", 32768, 50], 2339),      # Castelia harlequin after finding clowns
    (102, ["WorkSet", 32768, 50], 2339),     # Castelia gate harlequin after finding clowns
    (504, ["WorkSet", 32768, 50], 2339),     # Skyarrow gate harlequin after finding clowns
    (90, ["WorkSet", 32768, 15], 210),       # Castelia Battle Company 47F Clerk (shares scr1 with trainer 501)
    (154, ["WorkSet", 32768, 578], 2350),    # Musical Theater owner (Prop Case)
    (1276, ["WorkSet", 32768, 627], 267),    # Floccesy Town Mr Medal (Medal Box)
    (740, ["WorkSet", 32768, 65], 2738),     # Route 13 Flute gentleman
    (740, ["WorkSet", 32768, 66], 2738),
    (740, ["WorkSet", 32768, 67], 2738),
    (740, ["WorkSet", 32768, 68], 2738),
    (740, ["WorkSet", 32768, 69], 2738),
    (412, ["WorkSet", 32768, 54], 2341),     # Dragonspiral tower Cedric
    (466, ["WorkSet", 32768, 29], 2346),     # Giant Chasm rood (max revive x3)
    (948, ["WorkSet", 32768, 635], 2364),    # Route 22 Colress (Colress MCHN)
    (870, ["WorkSet", 32768, 4], 2802),     # Aspertia Pokemon Center Bianca (Poké Ball x10)
    (658, ["WorkSet", 32768, 421], 2373),    # Route 5 Bianca (fly)
    (990, ["WorkSet", 32768, 423], 2370),    # Castelia Sewers Iris (strength)
    (1146, ["WorkSet", 32768, 424], 2374),   # Victory road N (waterfall)
    (978, ["WorkSet", 32768, 410], 2377),    # Aspertia gym Cheren (TM83 work up)
    (1004, ["WorkSet", 32768, 336], 2378),   # Virbank gym Roxie (TM09 venoshock)
    (976, ["WorkSet", 32768, 403], 2379),    # Castelia gym Burgh (TM76 struggle bug)
    (126, ["WorkSet", 32768, 399], 2380),    # Nimbasa gym Elesa (TM72 volt switch)
    (194, ["WorkSet", 32768, 405], 2381),    # Driftveil gym Clay (TM78 bulldoze)
    (216, ["WorkSet", 32768, 389], 2382),    # Mistralton gym Skyla (TM62 acrobatics)
    (242, ["WorkSet", 32768, 409], 2383),    # Opelucid gym Drayden (TM82 dragon tail)
    (946, ["WorkSet", 32768, 382], 2384),    # Humilau gym Marlon (TM55 scald)
    (854, ["WorkSet", 32768, 354], 2368),    # Aspertia city Bianca outside gym (TM27 return)
    (890, ["WorkSet", 32768, 348], 2371),    # Floccesy ranch Plasma grunt (TM21 frustration)
    (516, ["WorkSet", 32768, 7], 299),       # Village Bridge fisherman (Dive Ball x5)
    (204, ["WorkSet", 32768, 93], 2759),     # Driftveil Luxury Suites 1F lady (Heart Scale)
]

# Gym leader & interior helper/Clyde scripts -> badge index (0..7)
GYM_BADGE_MAP: dict[int, int] = {
    978: 0, 1004: 1, 976: 2, 126: 3, 194: 4, 216: 5, 242: 6, 946: 7,
    58: 2, 910: 1, 220: 5,
}
GYM_LEADER_SCRIPTS: list[int] = [978, 1004, 976, 126, 194, 216, 242, 946]
GYM_CLYDE_FLAGS: dict[int, int] = {
    978: 115,   # Aspertia Gym - Clyde
    1004: 116,  # Virbank Gym - Clyde
    976: 109,   # Castelia Gym - Clyde
    126: 110,   # Nimbasa Gym - Clyde
    194: 111,   # Driftveil Gym - Clyde
    216: 112,   # Mistralton Gym - Clyde
    242: 114,   # Opelucid Gym - Clyde
    946: 117,   # Humilau Gym - Clyde
}
GYM_TRAINERS_BY_LEADER_SCRIPT: dict[int, tuple[int, list[int]]] = {
    978: (0, [171, 172]),
    1004: (1, [178, 179]),
    976: (2, [734, 735, 736, 737]),
    126: (3, [207, 208, 209]),
    194: (4, [319, 320, 321, 322, 323, 324, 325]),
    216: (5, [149, 150, 151, 152, 332]),
    242: (6, [381, 382, 383, 384, 385]),
    946: (7, [350, 351, 352, 353, 354, 355]),
}


def patch_gym_leader_badges(script_narc: NARC) -> None:
    # Decouples gym leader defeat state (Flag 2414 + idx) from AP badge item ownership (StoreBadge)
    # and ensures defeating any gym leader also marks/deactivates all gym trainers in that gym
    from .script_editing import disassemble, assemble, Line

    for s_idx, expected_badge in GYM_BADGE_MAP.items():
        if len(script_narc.files) > s_idx:
            try:
                scr = disassemble(script_narc.files[s_idx])
                modified = False
                for i, line in enumerate(scr.lines):
                    if line.type != "command" or len(line.parts) <= 1:
                        continue
                    if line.parts[0] == "SetBadge":
                        scr.lines[i] = Line(type="command", parts=["WorkSetConst", 32800, 0])
                        modified = True
                    elif line.parts[0] == "StoreBadge" and len(line.parts) > 2:
                        dest_var, badge_idx = line.parts[1], line.parts[2]
                        if isinstance(badge_idx, int) and 0 <= badge_idx < 8:
                            scr.lines[i] = Line(type="command", parts=["FlagGet", 2414 + badge_idx, dest_var])
                            modified = True

                if s_idx in GYM_TRAINERS_BY_LEADER_SCRIPT:
                    badge_idx, tids = GYM_TRAINERS_BY_LEADER_SCRIPT[s_idx]
                    clear_flag = 2414 + badge_idx
                    existing_deactive = {
                        l.parts[1]
                        for l in scr.lines
                        if l.type == "command" and l.parts[0] == "DeactiveTrainerId" and len(l.parts) > 1
                    }
                    # Look inside the leader defeat block (prefer the FlagSet 2414+idx line)
                    i = 0
                    while i < len(scr.lines):
                        if scr.lines[i].type == "command" and scr.lines[i].parts == ["FlagSet", clear_flag]:
                            nearby_flags = {
                                scr.lines[k].parts[1]
                                for k in range(max(0, i - 10), min(len(scr.lines), i + 25))
                                if scr.lines[k].type == "command" and scr.lines[k].parts[0] == "FlagSet"
                            }
                            inject = []
                            for tid in tids:
                                if tid not in existing_deactive:
                                    inject.append(Line(type="command", parts=["DeactiveTrainerId", tid]))
                                t_flag = 1520 + tid
                                if t_flag not in nearby_flags:
                                    inject.append(Line(type="command", parts=["FlagSet", t_flag]))
                            if inject:
                                scr.lines[i + 1 : i + 1] = inject
                                modified = True
                                i += len(inject)
                        i += 1

                if modified:
                    script_narc.files[s_idx] = bytes(assemble(scr))
            except Exception:
                pass


def patch_gift_flag_injections(script_narc: NARC) -> None:
    # Injects physical FlagSet <flag_id> into cutscenes and story scripts that award gifts
    from .script_editing import disassemble, assemble, Line

    for s_idx, target_parts, flag_id in CUSTOM_GIFT_INJECTIONS:
        if len(script_narc.files) > s_idx:
            try:
                scr = disassemble(script_narc.files[s_idx])
                modified = False
                for i, line in enumerate(list(scr.lines)):
                    if line.type == "command" and line.parts == target_parts:
                        if i + 1 < len(scr.lines) and scr.lines[i + 1].type == "command" and scr.lines[i + 1].parts == ["FlagSet", flag_id]:
                            continue
                        scr.lines.insert(i + 1, Line("command", ["FlagSet", flag_id]))
                        modified = True
                if modified:
                    script_narc.files[s_idx] = bytes(assemble(scr))
            except Exception:
                pass


_VAR_GIFT_BYTE_PATTERNS: tuple[bytes, ...] = tuple(
    op + k[0].to_bytes(2, "little") + k[1].to_bytes(2, "little")
    for k in VAR_TO_GIFT_FLAG
    for op in (b"\x28\x00", b"\x2a\x00")
)


def patch_gym_clyde_autocollect(script_narc: NARC) -> None:
    """Set Clyde's gift flag when defeating each gym leader so missed Clyde checks auto-collect."""
    from .script_editing import disassemble, assemble, Line

    for s_idx, clyde_flag in GYM_CLYDE_FLAGS.items():
        if len(script_narc.files) <= s_idx or s_idx not in GYM_BADGE_MAP:
            continue
        clear_flag = 2414 + GYM_BADGE_MAP[s_idx]
        try:
            scr = disassemble(script_narc.files[s_idx])
            modified = False
            i = 0
            while i < len(scr.lines):
                if scr.lines[i].type == "command" and scr.lines[i].parts == ["FlagSet", clear_flag]:
                    nearby_flags = {
                        scr.lines[k].parts[1]
                        for k in range(max(0, i - 10), min(len(scr.lines), i + 25))
                        if scr.lines[k].type == "command" and scr.lines[k].parts[0] == "FlagSet"
                    }
                    if clyde_flag not in nearby_flags:
                        scr.lines.insert(i + 1, Line(type="command", parts=["FlagSet", clyde_flag]))
                        modified = True
                        i += 1
                i += 1
            if modified:
                script_narc.files[s_idx] = bytes(assemble(scr))
        except Exception:
            pass

    for s_idx in range(len(script_narc.files)):
        if s_idx in (856, 1238, 1239, 1240, 1241, 1242, 1243):
            continue
        raw = script_narc.files[s_idx]
        if not any(p in raw for p in _VAR_GIFT_BYTE_PATTERNS):
            continue
        try:
            scr = disassemble(raw)
            modified = False
            for i, line in enumerate(list(scr.lines)):
                if (
                    line.type == "command"
                    and line.parts[0] in ("WorkSet", "WorkSetConst")
                    and len(line.parts) > 2
                ):
                    pair = (line.parts[1], line.parts[2])
                    if pair in VAR_TO_GIFT_FLAG:
                        flag_id = VAR_TO_GIFT_FLAG[pair]
                        if i + 1 < len(scr.lines) and scr.lines[i + 1].type == "command" and scr.lines[i + 1].parts == ["FlagSet", flag_id]:
                            continue
                        scr.lines.insert(i + 1, Line("command", ["FlagSet", flag_id]))
                        modified = True
            if modified:
                script_narc.files[s_idx] = bytes(assemble(scr))
        except Exception:
            pass


def patch_overworld_trainer_no_battle(script_narc: NARC) -> None:
    # Skips overworld trainer battles in s1239 so talking to a trainer marks them defeated immediately
    from .script_editing import disassemble, assemble, Line

    if len(script_narc.files) <= 1239 or not script_narc.files[1239]:
        return
    try:
        sf = disassemble(script_narc.files[1239])
        modified = False
        for i, line in enumerate(sf.lines):
            if line.type == "command" and line.parts:
                if line.parts[0] == "StorePartyCountMore":
                    sf.lines[i] = Line("command", ["WorkSetConst", line.parts[1], 6])
                    modified = True
                elif line.parts[0] in ("SingleTrainerBattle", "DoubleTrainerBattle", "MultiTrainerBattle"):
                    sf.lines[i] = Line("command", ["WorkSetConst", 32784, 1])
                    modified = True
                elif line.parts[0] == "StoreBattleResult" and len(line.parts) > 1:
                    sf.lines[i] = Line("command", ["WorkSetConst", line.parts[1], 1])
                    modified = True
        if modified:
            script_narc.files[1239] = bytes(assemble(sf))
    except Exception:
        pass


def patch_scripted_trainer_battles(script_narc: NARC, no_battle: bool = False) -> None:
    # Injects FlagSet (1520 + tid) right after scripted trainer battles
    from .script_editing import disassemble, assemble, Line

    for s_idx in range(len(script_narc.files)):
        if s_idx in (856, 1238, 1239, 1240, 1241, 1242, 1243):
            continue
        raw = script_narc.files[s_idx]
        if not no_battle and b"\x85\x00" not in raw and b"\x86\x00" not in raw:
            continue
        try:
            scr = disassemble(raw)
            modified = False
            i = 0
            inject_count = 0
            last_was_trainer = False
            while i < len(scr.lines):
                line = scr.lines[i]
                if line.type == "command":
                    to_inject = []
                    is_losable = False
                    if line.parts[0] == "StartWildBattle":
                        last_was_trainer = False
                    elif no_battle and last_was_trainer and line.parts[0] == "StoreBattleResult" and len(line.parts) > 1:
                        scr.lines[i] = Line("command", ["WorkSetConst", line.parts[1], 1])
                        modified = True
                    elif line.parts[0] == "SingleTrainerBattle" and len(line.parts) > 1:
                        tid = line.parts[1]
                        flags = line.parts[3] if len(line.parts) > 3 else 0
                        if isinstance(tid, int) and 0 < tid < 1000:
                            to_inject.append(1520 + tid)
                            if flags == 1 or tid in (161, 162, 163):
                                is_losable = True
                    elif line.parts[0] == "DoubleTrainerBattle" and len(line.parts) > 3:
                        tid1 = line.parts[2]
                        tid2 = line.parts[3]
                        flags = line.parts[4] if len(line.parts) > 4 else 0
                        if s_idx == 14 and tid1 in (494, 495, 496) and tid2 in (494, 495, 496):
                            to_inject.extend([2014, 2015])
                        else:
                            if isinstance(tid1, int) and 0 < tid1 < 1000:
                                to_inject.append(1520 + tid1)
                            if isinstance(tid2, int) and 0 < tid2 < 1000 and tid2 != tid1:
                                to_inject.append(1520 + tid2)
                        if flags == 1:
                            is_losable = True

                    if no_battle and line.parts[0] in ("SingleTrainerBattle", "DoubleTrainerBattle", "MultiTrainerBattle"):
                        scr.lines[i] = Line("command", ["WorkSetConst", 32784, 1])
                        last_was_trainer = True
                        modified = True

                    if to_inject:
                        already_patched = any(
                            scr.lines[k].type == "command" and scr.lines[k].parts == ["FlagSet", to_inject[0]]
                            for k in range(i + 1, min(len(scr.lines), i + 10))
                        )

                        if not already_patched:
                            inject_count += 1
                            skip_lbl = f"lbl_skip_win_{s_idx}_{inject_count}"
                            injected_lines = []
                            if is_losable:
                                for f_id in to_inject:
                                    injected_lines.append(Line("command", ["FlagSet", f_id]))
                            else:
                                injected_lines.append(Line("command", ["WorkSetConst", 32784, 1] if no_battle else ["StoreBattleResult", 32784]))
                                injected_lines.append(Line("command", ["StackPush", 32784]))
                                injected_lines.append(Line("command", ["StackPushConst", 1]))
                                injected_lines.append(Line("command", ["StackCmp", 1]))
                                injected_lines.append(Line("command", ["VMJumpIf", 255, skip_lbl]))
                                for f_id in to_inject:
                                    injected_lines.append(Line("command", ["FlagSet", f_id]))
                                injected_lines.append(Line("label", [skip_lbl]))

                            for offset, inj_l in enumerate(injected_lines):
                                scr.lines.insert(i + 1 + offset, inj_l)
                            modified = True
                            i += len(injected_lines)
                i += 1
            if modified:
                script_narc.files[s_idx] = bytes(assemble(scr))
        except Exception:
            pass

    _inject_missable_trainer_flags(script_narc)


_GIANT_CHASM_FRIGATE_TIDS: list[int] = [
    344, 348,
    430, 431, 432, 434, 435, 438, 439,
    445, 446, 447, 448, 449, 452, 453, 454,
    497, 498, 499,
    807, 808, 809, 810, 811,
]

_ROUTE_21_FRIGATE_TIDS: list[int] = [
    343, 347, 426, 427, 428, 429, 436, 437,
    441, 442, 443, 444, 450, 451,
    500, 797, 798, 799, 800, 801, 802, 812,
]

_GIANT_CHASM_FRIGATE_ITEM_FLAGS: list[int] = [
    356, 1287, 1288, 1290, 1292, 1293,
]

_ROUTE_21_FRIGATE_ITEM_FLAGS: list[int] = [
    356, 1289, 1291, 1478, 1479,
]

_MISSABLE_TRAINER_TRIGGERS: list[tuple[int, list[Any], list[int]]] = [
    # Opelucid City Plasma assault cleared -> Grunts 1..3
    (240, ["FlagSet", 796], [585, 586, 587]),
    # Route 21 / Seaside Cave Plasma Frigate departure
    (1112, ["WorkSetConst", 16646, 4], _ROUTE_21_FRIGATE_TIDS),
    # Giant Chasm Plasma Frigate completed (Ghetsis beaten) or skipped (1242 unlock)
    (1208, ["FlagSet", 885], _GIANT_CHASM_FRIGATE_TIDS),
    (1242, ["FlagSet", 976], _GIANT_CHASM_FRIGATE_TIDS),
]

_MISSABLE_ITEM_TRIGGERS: list[tuple[int, list[Any], list[int]]] = [
    (1112, ["WorkSetConst", 16646, 4], _ROUTE_21_FRIGATE_ITEM_FLAGS),
    (1208, ["FlagSet", 885], _GIANT_CHASM_FRIGATE_ITEM_FLAGS),
    (1242, ["FlagSet", 976], _GIANT_CHASM_FRIGATE_ITEM_FLAGS),
]


def _inject_missable_trainer_flags(script_narc: NARC) -> None:
    # Auto-flags mutually exclusive or story-locked trainers and items when their area clears
    from .script_editing import disassemble, assemble, Line

    by_script: dict[int, list[tuple[list[Any], list[int]]]] = {}
    for s_idx, trigger_parts, tids in _MISSABLE_TRAINER_TRIGGERS:
        by_script.setdefault(s_idx, []).append((trigger_parts, [1520 + tid for tid in tids]))
    for s_idx, trigger_parts, flags in _MISSABLE_ITEM_TRIGGERS:
        by_script.setdefault(s_idx, []).append((trigger_parts, flags))

    for s_idx, rules in by_script.items():
        if len(script_narc.files) <= s_idx:
            continue
        try:
            scr = disassemble(script_narc.files[s_idx])
            modified = False
            for trigger_parts, flags in rules:
                i = 0
                while i < len(scr.lines):
                    if scr.lines[i].type == "command" and scr.lines[i].parts == trigger_parts:
                        nearby = {
                            scr.lines[k].parts[1]
                            for k in range(i + 1, min(len(scr.lines), i + len(flags) + 10))
                            if scr.lines[k].type == "command" and scr.lines[k].parts[0] == "FlagSet"
                        }
                        inject = [
                            Line("command", ["FlagSet", flg])
                            for flg in flags
                            if flg not in nearby
                        ]
                        if inject:
                            scr.lines[i + 1 : i + 1] = inject
                            modified = True
                            i += len(inject)
                    i += 1
            if modified:
                script_narc.files[s_idx] = bytes(assemble(scr))
        except Exception:
            pass


def patch_npc_gift_scripts(script_narc: NARC, flag_to_text_id: dict[int, int]) -> None:
    # Scans zone scripts in a/0/5/6 for NPC gift routines that set WorkSet 32768, <item_id>
    from .script_editing import disassemble, assemble, Line

    gift_rtcall_ids = {2800, 2801, 2802, 2805, 2806, 2807, 2814}

    def _is_block_boundary(line: Line) -> bool:
        return (
            line.type == "label"
            and bool(line.parts)
            and str(line.parts[0]).startswith(("scr", "sub", "act"))
        )

    for s_idx in range(len(script_narc.files)):
        if s_idx in (856, 1238, 1239, 1240, 1241, 1242, 1243):
            continue
        raw = script_narc.files[s_idx]
        if b"\x28\x00\x00\x80" not in raw and b"\x2a\x00\x00\x80" not in raw:
            continue
        try:
            scr = disassemble(raw)
            modified = False
            new_lines: list[Line] = []
            lines = scr.lines
            for l_idx, l in enumerate(lines):
                if (
                    l.type == "command"
                    and l.parts[0] in ("WorkSet", "WorkSetConst")
                    and len(l.parts) > 2
                    and l.parts[1] == 32768
                ):
                    # if this item was already set to 639 or register 16798 was already assigned,
                    # a custom patch routine already handles it
                    if l.parts[2] == 639 or (
                        new_lines
                        and new_lines[-1].type == "command"
                        and new_lines[-1].parts[0] == "WorkSetConst"
                        and len(new_lines[-1].parts) > 1
                        and new_lines[-1].parts[1] == 16798
                    ):
                        new_lines.append(l)
                        continue

                    block_start = l_idx
                    while block_start > 0 and not _is_block_boundary(lines[block_start]):
                        block_start -= 1
                    block_end = l_idx + 1
                    while block_end < len(lines) and not _is_block_boundary(lines[block_end]):
                        block_end += 1

                    rtcall_id: int | None = None
                    for k in range(l_idx + 1, min(block_end, l_idx + 25)):
                        nxt = lines[k]
                        if nxt.type == "command":
                            if nxt.parts[0] in ("VMHalt", "VMReturn"):
                                break
                            if nxt.parts[0] == "RTCallGlobal" and len(nxt.parts) > 1:
                                rtcall_id = nxt.parts[1]
                                break

                    if rtcall_id not in gift_rtcall_ids:
                        new_lines.append(l)
                        continue

                    candidates: list[tuple[int, int]] = []
                    for k in range(block_start, block_end):
                        cand = lines[k]
                        if cand.type == "command":
                            f: int | None = None
                            if (
                                cand.parts[0] in ("WorkSet", "WorkSetConst")
                                and len(cand.parts) > 2
                                and cand.parts[1] == 32770
                                and cand.parts[2] in flag_to_text_id
                            ):
                                f = cand.parts[2]
                            elif (
                                cand.parts[0] == "FlagSet"
                                and len(cand.parts) > 1
                                and cand.parts[1] in flag_to_text_id
                            ):
                                f = cand.parts[1]
                            elif (
                                cand.parts[0] in ("WorkSet", "WorkSetConst")
                                and len(cand.parts) > 2
                                and (cand.parts[1], cand.parts[2]) in VAR_TO_GIFT_FLAG
                                and VAR_TO_GIFT_FLAG[(cand.parts[1], cand.parts[2])] in flag_to_text_id
                            ):
                                f = VAR_TO_GIFT_FLAG[(cand.parts[1], cand.parts[2])]
                            if f is not None:
                                candidates.append((abs(k - l_idx), f))

                    if candidates:
                        candidates.sort(key=lambda c: c[0])
                        closest_flag = candidates[0][1]
                        new_lines.append(Line("command", ["WorkSetConst", 16798, flag_to_text_id[closest_flag]]))
                        new_lines.append(Line("command", ["WorkSetConst", 32768, 639]))
                        modified = True
                        continue

                new_lines.append(l)

            if modified:
                scr.lines = new_lines
                script_narc.files[s_idx] = bytes(assemble(scr))
        except Exception:
            pass

    tm_collector_flags = [f for f in (450, 451, 452, 453, 454) if f in flag_to_text_id]
    if tm_collector_flags:
        try:
            sc224 = disassemble(script_narc.files[224])
            lines224 = sc224.lines
            modified224 = False
            for tm_flag in tm_collector_flags:
                for i, l in enumerate(lines224):
                    if l.type == "command" and l.parts == ["FlagSet", tm_flag]:
                        if i > 0 and lines224[i - 1].type == "command" and lines224[i - 1].parts == ["VMCall", "sub21"]:
                            lines224[i - 1 : i] = [
                                Line("command", ["StackPush", 32768]),
                                Line("command", ["StackPush", 32769]),
                                Line("command", ["WorkSetConst", 16798, flag_to_text_id[tm_flag]]),
                                Line("command", ["WorkSetConst", 32768, 639]),
                                Line("command", ["WorkSet", 32769, 1]),
                                Line("command", ["RTCallGlobal", 2805]),
                                Line("command", ["StackPop", 32769]),
                                Line("command", ["StackPop", 32768]),
                                Line("command", ["MsgActor", 1024, 6, 0, 0]),
                                Line("command", ["InputWaitLast"]),
                                Line("command", ["MsgWinCloseAll"]),
                            ]
                            modified224 = True
                        break
            if modified224:
                script_narc.files[224] = bytes(assemble(sc224))
        except Exception:
            pass

    ranger_trainer_to_gift_flag = {
        543: 1500, 544: 1501, 509: 1502, 508: 1503, 667: 1504, 666: 1505,
        298: 1506, 297: 1507, 579: 1508, 578: 1509, 640: 1510, 642: 1511,
        641: 1512, 639: 1513, 517: 1514, 518: 1514, 515: 1515, 516: 1515,
        410: 1516, 409: 1517, 305: 1518, 304: 1519, 294: 2385, 295: 2386,
        388: 2387, 386: 2388, 389: 2389, 387: 2390, 483: 2391, 484: 2392,
        293: 2393, 292: 2394, 473: 2395, 474: 2396, 658: 2397, 659: 2398,
    }
    try:
        sc1239 = disassemble(script_narc.files[1239])
        lines1239 = sc1239.lines
        for i, l in enumerate(lines1239):
            if l.type == "label" and l.parts == ["sub31"]:
                for j in range(i + 1, min(len(lines1239), i + 12)):
                    if lines1239[j].type == "command" and lines1239[j].parts == ["TrainerGetPrizeItem", 32800, 32768]:
                        if (
                            j + 2 < len(lines1239)
                            and lines1239[j + 1].parts == ["WorkSetConst", 32769, 1]
                            and lines1239[j + 2].parts == ["RTCallGlobal", 2805]
                        ):
                            dispatch: list[Line] = []
                            branches: list[Line] = []
                            for tid, gflag in ranger_trainer_to_gift_flag.items():
                                if gflag in flag_to_text_id:
                                    lbl = f"lbl_ranger_gift_{tid}"
                                    dispatch.append(Line("command", ["WorkCmpConst", 32800, tid]))
                                    dispatch.append(Line("command", ["VMJumpIf", 1, lbl]))
                                    branches.extend([
                                        Line("label", [lbl]),
                                        Line("command", ["WorkSetConst", 16798, flag_to_text_id[gflag]]),
                                        Line("command", ["WorkSetConst", 32768, 639]),
                                        Line("command", ["WorkSetConst", 32769, 1]),
                                        Line("command", ["RTCallGlobal", 2805]),
                                        Line("command", ["FlagSet", gflag]),
                                        Line("command", ["VMJump", "lbl_ranger_gift_done"]),
                                    ])
                            if dispatch:
                                fallback = [
                                    Line("command", ["TrainerGetPrizeItem", 32800, 32768]),
                                    Line("command", ["WorkSetConst", 32769, 1]),
                                    Line("command", ["RTCallGlobal", 2805]),
                                    Line("command", ["VMJump", "lbl_ranger_gift_done"]),
                                ]
                                lines1239[j : j + 3] = dispatch + fallback + branches + [Line("label", ["lbl_ranger_gift_done"])]
                                sc1239.lines = lines1239
                                script_narc.files[1239] = bytes(assemble(sc1239))
                        break
                break
    except Exception:
        pass

    if 2763 in flag_to_text_id:
        try:
            sc912 = disassemble(script_narc.files[912])
            lines912 = sc912.lines
            mod912 = False
            i = 0
            while i < len(lines912):
                if lines912[i].type == "command" and lines912[i].parts == ["Screen0xB5", 3, 1, 32784]:
                    lines912.pop(i)
                    mod912 = True
                    continue
                if (
                    lines912[i].type == "command"
                    and lines912[i].parts == ["WordSetItemName", 0, 4]
                    and i + 6 < len(lines912)
                    and lines912[i + 6].type == "command"
                    and lines912[i + 6].parts == ["MsgWinCloseAll"]
                ):
                    lines912[i : i + 7] = [
                        Line("command", ["StackPush", 32768]),
                        Line("command", ["StackPush", 32769]),
                        Line("command", ["WorkSetConst", 16798, flag_to_text_id[2763]]),
                        Line("command", ["WorkSetConst", 32768, 639]),
                        Line("command", ["WorkSet", 32769, 1]),
                        Line("command", ["RTCallGlobal", 2805]),
                        Line("command", ["StackPop", 32769]),
                        Line("command", ["StackPop", 32768]),
                    ]
                    mod912 = True
                    i += 8
                    continue
                i += 1
            if mod912:
                script_narc.files[912] = bytes(assemble(sc912))
        except Exception:
            pass

    if 239 in flag_to_text_id:
        try:
            sc842 = disassemble(script_narc.files[842])
            lines842 = sc842.lines
            for i in range(len(lines842) - 2):
                if (
                    lines842[i].type == "command"
                    and lines842[i].parts == ["FlagSet", 239]
                    and lines842[i + 1].type == "command"
                    and lines842[i + 1].parts == ["WorkSetConst", 16740, 50]
                    and lines842[i + 2].type == "command"
                    and lines842[i + 2].parts == ["VMCall", "sub4"]
                ):
                    lines842[i : i + 3] = [
                        Line("command", ["MsgWinCloseAll"]),
                        Line("command", ["StackPush", 32768]),
                        Line("command", ["StackPush", 32769]),
                        Line("command", ["WorkSetConst", 16798, flag_to_text_id[239]]),
                        Line("command", ["WorkSetConst", 32768, 639]),
                        Line("command", ["WorkSet", 32769, 1]),
                        Line("command", ["RTCallGlobal", 2801]),
                        Line("command", ["StackPop", 32769]),
                        Line("command", ["StackPop", 32768]),
                        Line("command", ["FlagSet", 239]),
                        Line("command", ["WorkSetConst", 16741, 0]),
                        Line("command", ["MsgActor", 1024, 3, 0, 0]),
                        Line("command", ["InputWaitLast"]),
                        Line("command", ["MsgWinCloseAll"]),
                    ]
                    script_narc.files[842] = bytes(assemble(sc842))
                    break
        except Exception:
            pass

    if 2732 in flag_to_text_id:
        try:
            sc86 = disassemble(script_narc.files[86])
            lines86 = sc86.lines
            for i in range(len(lines86) - 3):
                if (
                    lines86[i].type == "command"
                    and lines86[i].parts == ["StackPushFlag", 2732]
                    and lines86[i + 3].type == "command"
                    and lines86[i + 3].parts == ["VMJumpIf", 255, "lbl7_8"]
                ):
                    lines86[i + 4 : i + 4] = [
                        Line("command", ["StackPush", 32768]),
                        Line("command", ["StackPush", 32769]),
                        Line("command", ["WorkSetConst", 16798, flag_to_text_id[2732]]),
                        Line("command", ["WorkSetConst", 32768, 639]),
                        Line("command", ["WorkSet", 32769, 1]),
                        Line("command", ["RTCallGlobal", 2805]),
                        Line("command", ["StackPop", 32769]),
                        Line("command", ["StackPop", 32768]),
                        Line("command", ["FlagSet", 2732]),
                        Line("command", ["VMJump", "lbl7_8"]),
                    ]
                    script_narc.files[86] = bytes(assemble(sc86))
                    break
        except Exception:
            pass

    if 244 in flag_to_text_id:
        try:
            sc116 = disassemble(script_narc.files[116])
            for i, ln in enumerate(sc116.lines):
                if ln.type == "command" and ln.parts == ["StackPushConst", 40]:
                    sc116.lines[i] = Line("command", ["StackPushConst", 0])
                    script_narc.files[116] = bytes(assemble(sc116))
                    break
        except Exception:
            pass
