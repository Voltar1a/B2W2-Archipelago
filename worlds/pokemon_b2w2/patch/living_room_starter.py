# Living room starter event for Pokémon Black 2 and White 2

from typing import TYPE_CHECKING

try:
    from ..nds_compat import NARC
except (ImportError, ValueError):
    try:
        from worlds.pokemon_b2w2.nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import NARC

try:
    from .script_editing import disassemble, assemble, Line
    from .text import decode, encode, Entry
except (ImportError, ValueError):
    from patch.script_editing import disassemble, assemble, Line
    from patch.text import decode, encode, Entry

if TYPE_CHECKING:
    from ..nds_compat import NintendoDSRom


def replace_between(s, start_lbl: str, end_lbl: str, new_lines: list[Line]) -> None:
    i_start = s.find_label(start_lbl)
    i_end = s.find_label(end_lbl) if end_lbl else len(s.lines)
    if i_start != -1 and i_end != -1:
        s.lines[i_start:i_end] = new_lines


def replace_scr_block(s, scr_name: str, new_lines: list[Line]) -> None:
    idx = s.find_label(scr_name)
    if idx == -1:
        return
    next_idx = -1
    for i in range(idx + 1, len(s.lines)):
        if s.lines[i].type == "label" and not s.lines[i].parts[0].startswith("lbl"):
            next_idx = i
            break
    if next_idx == -1:
        next_idx = len(s.lines)
    s.lines[idx:next_idx] = new_lines


def apply_living_room_starter(rom: "NintendoDSRom", options: dict) -> None:
    a003_data = rom.getFileByName("a/0/0/3")
    if a003_data is not None:
        a003 = NARC(a003_data)
        entries = decode(a003.files[173])
        rival = (str(options.get("rival_name", "Hugh")).strip() or "Hugh")[:7]
        if entries:
            while len(entries[0]) < 77:
                entries[0].append(Entry("", key=None))
            entries[0][55].line = "Mom: [c_100_#1_0]![NextLine]Come over here for a second!"
            entries[0][56].line = "Bianca: Hi, [c_100_#1_0]![NextLine]It's so wonderful to meet you![End][NextLine]I have a present for you[NextLine]from Professor Juniper!"
            entries[0][57].line = "Bianca: Go on, open the case[NextLine]and choose your partner Pokémon!"
            entries[0][58].line = "[c_100_#1_0] received[NextLine]the [c_101_#1_1]!"
            entries[0][59].line = "Would you like to give a nickname[NextLine]to your partner [c_101_#1_1]?"
            entries[0][60].line = "Bianca: That is such a great name![NextLine]It suits your partner perfectly!"
            entries[0][61].line = "Bianca: Gotcha! Keeping the[NextLine]original name is cool too!"
            entries[0][62].line = "Bianca: Now you've got your Pokémon,[NextLine]so I'll give you this, too - a Pokédex!"
            entries[0][63].line = "[c_100_#1_0] received[NextLine]the [c_ff00_#1_2]Pokédex[c_ff00_#1_0]!"
            entries[0][64].line = "Bianca: That Pokédex will record[NextLine]all the Pokémon you meet in Unova!"
            entries[0][65].line = f"{rival}: Alright, [c_100_#1_0]![NextLine]We both have Pokémon now![End][NextLine]There's only one thing to do![NextLine]Let's see what you're made of!"
            entries[0][66].line = "Bianca: Wait, don't battle in here![NextLine]At least take it outside first!"
            entries[0][67].line = f"{rival}: Tch... You're pretty good,[NextLine][c_100_#1_0]! Don't you dare fall behind!"
            entries[0][68].line = f"Mom: Wait a moment, [c_100_#1_0]![NextLine]{rival} dashed out of here so fast...[End][NextLine]I couldn't give him his Town Map![NextLine]Take two, and give one to him later!"
            entries[0][69].line = "[c_100_#1_0] received[NextLine]the [c_ff00_#1_2]Town Map[c_ff00_#1_0]!"
            entries[0][70].line = "Mom: And take these Running Shoes[NextLine]for your adventure, too!"
            entries[0][71].line = "[c_100_#1_0] received a pair of[NextLine][c_ff00_#1_2]Running Shoes[c_ff00_#1_0]!"
            entries[0][72].line = "Mom: Hold the B Button to run fast![NextLine]Put them on and race around![End][NextLine]And remember, you can always come[NextLine]home to rest your Pokémon!"
            entries[0][73].line = "Bianca: Oh, and before I head out![NextLine]Professor Juniper sent these too!"
            entries[0][74].line = "Bianca: Have fun on your journey[NextLine]with your partner Pokémon!"
            entries[0][75].line = "Mom: Welcome home, [c_100_#1_0]![NextLine]Let me rest your Pokémon!"
            entries[0][76].line = (
                "Mom: One more thing - the dev[NextLine]wanted me to tell you this:[End][NextLine]"
                "“Press START to open the APtransceiver,[NextLine]which contains useful features!\""
            )
            a003.files[173] = encode(entries)
            rom.setFileByName("a/0/0/3", a003.save())

    # Add Bianca and Hugh NPCs to player's house
    a126_data = rom.getFileByName("a/1/2/6")
    if a126_data is not None:
        a126 = NARC(a126_data)
        f167 = bytearray(a126.files[167])
        n_20 = f167[4]
        base = 8 + 20 * n_20

        # NPC 0 (Mom): sprite=251, flag=0 (always spawn), script=4 (scr3), dir=3 (east), x=4, y=4
        f167[base + 0 : base + 2] = (0).to_bytes(2, "little")
        f167[base + 2 : base + 4] = (251).to_bytes(2, "little")
        f167[base + 8 : base + 10] = (0).to_bytes(2, "little")
        f167[base + 10 : base + 12] = (4).to_bytes(2, "little")
        f167[base + 12 : base + 14] = (3).to_bytes(2, "little")
        f167[base + 28 : base + 30] = (4).to_bytes(2, "little")
        f167[base + 30 : base + 32] = (4).to_bytes(2, "little")

        # NPC 1 (Bianca): sprite=249 (green hat), flag=2401 (despawn after starter event), script=3 (scr2), dir=1 (south), x=5, y=3 (top-middle)
        b1 = base + 36
        f167[b1 + 0 : b1 + 2] = (1).to_bytes(2, "little")
        f167[b1 + 2 : b1 + 4] = (249).to_bytes(2, "little")
        f167[b1 + 8 : b1 + 10] = (2401).to_bytes(2, "little")
        f167[b1 + 10 : b1 + 12] = (3).to_bytes(2, "little")
        f167[b1 + 12 : b1 + 14] = (1).to_bytes(2, "little")
        f167[b1 + 28 : b1 + 30] = (5).to_bytes(2, "little")
        f167[b1 + 30 : b1 + 32] = (3).to_bytes(2, "little")

        # NPC 2 (Hugh): sprite=291 (canonical Hugh sprite), flag=2401 (despawn after starter event), script=5 (scr4), dir=2 (west), x=6, y=4
        b2 = base + 72
        f167[b2 + 0 : b2 + 2] = (2).to_bytes(2, "little")
        f167[b2 + 2 : b2 + 4] = (291).to_bytes(2, "little")
        f167[b2 + 8 : b2 + 10] = (2401).to_bytes(2, "little")
        f167[b2 + 10 : b2 + 12] = (5).to_bytes(2, "little")
        f167[b2 + 12 : b2 + 14] = (2).to_bytes(2, "little")
        f167[b2 + 28 : b2 + 30] = (6).to_bytes(2, "little")
        f167[b2 + 30 : b2 + 32] = (4).to_bytes(2, "little")

        # Configure coordinate trigger 0 at bedroom doorway (x=10, y=8):
        # (10, 7) Is solid wall (0x0081) and (10, 8) is a 1-tile bottleneck
        # keep vanilla trigger 1 at (10, 8) (scr15, var 16544 == 2) untouched so the post-credits scene runs
        # warp entries are 20 bytes each (not 24), so triggers start at offset 460:
        p_trig = base + 36 * f167[5] + 20 * f167[6]

        # Trigger 0: doorway tile (10, 8) -> script_id = 3 (scr2) when var 16544 == 0
        tb0 = p_trig
        f167[tb0 + 0 : tb0 + 2] = (3).to_bytes(2, "little")
        f167[tb0 + 2 : tb0 + 4] = (0).to_bytes(2, "little")
        f167[tb0 + 4 : tb0 + 6] = (16544).to_bytes(2, "little")
        f167[tb0 + 6 : tb0 + 8] = (0).to_bytes(2, "little")
        f167[tb0 + 8 : tb0 + 10] = (0).to_bytes(2, "little")
        f167[tb0 + 10 : tb0 + 12] = (10).to_bytes(2, "little")
        f167[tb0 + 12 : tb0 + 14] = (8).to_bytes(2, "little")
        f167[tb0 + 14 : tb0 + 16] = (1).to_bytes(2, "little")
        f167[tb0 + 16 : tb0 + 18] = (1).to_bytes(2, "little")
        f167[tb0 + 18 : tb0 + 20] = (0).to_bytes(2, "little")
        f167[tb0 + 20 : tb0 + 22] = (0).to_bytes(2, "little")

        a126.files[167] = bytes(f167)
        rom.setFileByName("a/1/2/6", a126.save())

    # Patch level scripts and event scripts in a/0/5/6
    a056_data = rom.getFileByName("a/0/5/6")
    if a056_data is not None:
        a056 = NARC(a056_data)

        a056.files[857] = bytes([
            2, 0, 1, 0, 0, 0,
            4, 0, 2, 0, 0, 0,
            3, 0, 18, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
        ])

        s854 = disassemble(a056.files[854])
        for nop_scr in ("scr1", "scr2", "scr3", "scr6", "scr7", "scr8", "scr21", "scr31", "scr32"):
            replace_scr_block(s854, nop_scr, [
                Line("label", [nop_scr]),
                Line("command", ["RTFinishSubEvents"]),
                Line("command", ["ActorUnlockAll"]),
                Line("command", ["VMHalt"]),
            ])
        replace_scr_block(s854, "scr29", [
            Line("label", ["scr29"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["FadeIntoBlack"]),
            Line("command", ["FlagReset", 739]),
            Line("command", ["FlagReset", 740]),
            Line("command", ["RTReserveScript", 17]),
            Line("command", ["Xtransciever7 (0x1A7)"]),
            Line("command", ["CMD_0c4", 428, 14, 0, 3, 0]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
        ])
        a056.files[854] = bytes(assemble(s854))

        s = disassemble(a056.files[856])

        replace_between(s, "scr1", "scr17", [
            Line("label", ["scr1"]),
            Line("command", ["StackPushFlag", 2401]),
            Line("command", ["StackPushConst", 1]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_scr1_end"]),
            Line("command", ["ActorSetGPos", 0, 5, 0, 3, 1]),
            Line("label", ["lbl_scr1_end"]),
            Line("command", ["VMHalt"]),
        ])

        replace_between(s, "scr17", "scr16", [
            Line("label", ["scr17"]),
            Line("command", ["VMHalt"]),
        ])

        starting_day = options.get("starting_day", 0)
        starting_season = options.get("starting_season", 0)
        hold_a_turbo = 1 if options.get("hold_a_turbo", True) else 2
        blind_trainers = 1 if options.get("blind_trainers", False) else 2
        auto_run = 1 if options.get("auto_run", False) else 2
        guaranteed_escape = 1 if options.get("guaranteed_escape", False) else 2
        fast_fishing = 1 if options.get("fast_fishing", True) else 2
        bike_everywhere = 1 if options.get("bike_everywhere", True) else 2
        catch_mult = 255 if bool(options.get("guaranteed_catch", False)) else int(options.get("catch_rate_multiplier", 1))
        if catch_mult == 0:
            catch_mult = 1
        exp_mult = int(options.get("exp_multiplier", 1))
        log_filter = int(options.get("check_log_filter", 0))

        scr16_cmds = [
            Line("label", ["scr16"]),
            Line("command", ["CMD_2e9", 1, 1]),
            Line("command", ["WorkSetConst", 16796, 428]),
            Line("command", ["FlagSet", 2801]),
            Line("command", ["FlagSet", 2488]),
            Line("command", ["WorkSetConst", 16791, log_filter]),
            Line("command", ["WorkSetConst", 16792, catch_mult]),
            Line("command", ["WorkSetConst", 16793, exp_mult]),
            Line("command", ["WorkSetConst", 16794, blind_trainers]),
            Line("command", ["WorkSetConst", 16795, hold_a_turbo]),
            Line("command", ["WorkSetConst", 16801, auto_run]),
            Line("command", ["WorkSetConst", 16802, guaranteed_escape]),
            Line("command", ["WorkSetConst", 16803, fast_fishing]),
            Line("command", ["WorkSetConst", 16804, bike_everywhere]),
            Line("command", ["WorkSetConst", 16799, starting_day]),
            Line("command", ["WorkSetConst", 16800, starting_season]),
            Line("command", ["FlagSet", 3040]),
            Line("command", ["FlagSet", 3041 + starting_season]),
            Line("command", ["FlagSet", 3045 + starting_day]),
        ]
        scr16_cmds.extend([
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
        ])
        replace_between(s, "scr16", "scr2", scr16_cmds)

        s_grass = options.get("starter_grass", 495)
        s_fire = options.get("starter_fire", 498)
        s_water = options.get("starter_water", 501)
        loc_check_info = options.get("slot_data", {}).get("loc_check_info", {})
        all_flags = sorted(int(k) for k in loc_check_info.keys())
        flag_to_text_id = {f_id: 21 + i for i, f_id in enumerate(all_flags)}

        scr2_lines = [
            Line("label", ["scr2"]),
            # Initialise APTransceiver flag and archi options unconditionally on first step
            Line("command", ["FlagSet", 2488]),
            Line("command", ["WorkSetConst", 16794, blind_trainers]),
            Line("command", ["WorkSetConst", 16795, hold_a_turbo]),
            Line("command", ["WorkSetConst", 16801, auto_run]),
            Line("command", ["WorkSetConst", 16802, guaranteed_escape]),
            Line("command", ["WorkSetConst", 16803, fast_fishing]),
            Line("command", ["WorkSetConst", 16804, bike_everywhere]),
            Line("command", ["WorkSetConst", 16799, starting_day]),
            Line("command", ["WorkSetConst", 16800, starting_season]),
            Line("command", ["WorkSetConst", 16791, log_filter]),
            Line("command", ["WorkSetConst", 16792, catch_mult]),
            Line("command", ["WorkSetConst", 16793, exp_mult]),
            Line("command", ["StackPushFlag", 2401]),
            Line("command", ["StackPushConst", 0]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_scr2_done"]),

            Line("label", ["lbl_start_cutscene"]),
            Line("command", ["ActorPauseAll"]),

            Line("command", ["WorkSetConst", 16544, 1]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 55, 0, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["ChangeMusic", 1088]),
            Line("command", ["CMD_24f", 255, 5, 5, 0, 8, 0]),
            Line("command", ["ActorCmdWait"]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 56, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["MsgActorEx", 1024, 57, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["WorkSetConst", 32804, 0]),
            Line("command", ["WorkSetConst", 32805, 0]),
            Line("command", ["Xtransciever4 (0x1A4)"]),
            Line("command", ["Xtransciever7 (0x1A7)"]),
            Line("command", ["CMD_14b"]),
            Line("command", ["CallPoke3Select", 32804]),
            Line("command", ["CMD_14a"]),
            Line("command", ["Xtransciever5 (0x1A5)"]),
            Line("command", ["Xtransciever7 (0x1A7)"]),

            Line("command", ["WorkCmpConst", 32804, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_starter_snivy"]),

            Line("command", ["WorkCmpConst", 32804, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_starter_tepig"]),

            Line("command", ["WorkSetConst", 16432, 2]),
            Line("command", ["CMD_209", 8, 2]),
            Line("command", ["WorkSetConst", 32805, s_water]),
            Line("command", ["WordSetPokeSpecies", 1, s_water]),
            Line("command", ["WordSetPokeSpecies", 2, s_water]),
            Line("command", ["VMJump", "lbl_starter_received"]),

            Line("label", ["lbl_starter_snivy"]),
            Line("command", ["WorkSetConst", 16432, 0]),
            Line("command", ["CMD_209", 8, 3]),
            Line("command", ["WorkSetConst", 32805, s_grass]),
            Line("command", ["WordSetPokeSpecies", 1, s_grass]),
            Line("command", ["WordSetPokeSpecies", 2, s_grass]),
            Line("command", ["VMJump", "lbl_starter_received"]),

            Line("label", ["lbl_starter_tepig"]),
            Line("command", ["WorkSetConst", 16432, 1]),
            Line("command", ["CMD_209", 8, 1]),
            Line("command", ["WorkSetConst", 32805, s_fire]),
            Line("command", ["WordSetPokeSpecies", 1, s_fire]),
            Line("command", ["WordSetPokeSpecies", 2, s_fire]),

            Line("label", ["lbl_starter_received"]),
            Line("command", ["PlayFanfare", 1304]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgSystem", 58, 2]),
            Line("command", ["WaitFanfare"]),
            Line("command", ["MsgWaitAdvance"]),
            Line("command", ["MsgSystemClose"]),

            Line("command", ["CMD_10c", 32784, 32805, 0, 5]),
            Line("command", ["FlagSet", 2401]),

            Line("command", ["MsgActorEx", 1024, 59, 1, 2, 0]),
            Line("command", ["YesNoWin", 32784]),
            Line("command", ["WorkCmpConst", 32784, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_skip_nickname"]),

            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["Xtransciever4 (0x1A4)"]),
            Line("command", ["Xtransciever7 (0x1A7)"]),
            Line("command", ["CMD_105", 32784, 0, 0]),
            Line("command", ["FlashBlackInstant"]),
            Line("command", ["Xtransciever7 (0x1A7)"]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 60, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["VMJump", "lbl_after_nickname"]),

            Line("label", ["lbl_skip_nickname"]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 61, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("label", ["lbl_after_nickname"]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 62, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["FlagSet", 2402]),
            Line("command", ["PlayFanfare", 1303]),
            Line("command", ["StoreHeroGender", 32784]),
            Line("command", ["StackPush", 32784]),
            Line("command", ["StackPushConst", 0]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_dex_male"]),
            Line("command", ["Animate19B", 63]),
            Line("command", ["VMJump", "lbl_dex_done"]),
            Line("label", ["lbl_dex_male"]),
            Line("command", ["Animate19B", 64]),
            Line("label", ["lbl_dex_done"]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgSystem", 63, 2]),
            Line("command", ["WaitFanfare"]),
            Line("command", ["MsgWaitAdvance"]),
            Line("command", ["MsgSystemClose"]),
            Line("command", ["StorePokemonCaughtWF"]),
            Line("command", ["WorkSetConst", 16547, 2]),
            Line("command", ["FlagSet", 738]),
            Line("command", ["FlagSet", 987]),
            Line("command", ["FlagSet", 744]),
            Line("command", ["FlagSet", 743]),

            Line("command", ["MsgActorEx", 1024, 64, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["ChangeMusic", 1237]),
            Line("command", ["CMD_24f", 2, 5, 4, 1, 8, 0]),
            Line("command", ["ActorCmdWait"]),
            Line("command", ["ActorCmdExec", 2, "act3_12"]),
            Line("command", ["ActorCmdWait"]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 65, 2, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["MsgActorEx", 1024, 66, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["WorkCmpConst", 16432, 0]),
            Line("command", ["VMJumpIf", 1, "lbl_fight_hugh_161"]),

            Line("command", ["WorkCmpConst", 16432, 1]),
            Line("command", ["VMJumpIf", 1, "lbl_fight_hugh_162"]),

            Line("command", ["SingleTrainerBattle", 163, 0, 1]),
            Line("command", ["VMJump", "lbl_fight_done"]),

            Line("label", ["lbl_fight_hugh_161"]),
            Line("command", ["SingleTrainerBattle", 161, 0, 1]),
            Line("command", ["VMJump", "lbl_fight_done"]),

            Line("label", ["lbl_fight_hugh_162"]),
            Line("command", ["SingleTrainerBattle", 162, 0, 1]),

            Line("label", ["lbl_fight_done"]),
            Line("command", ["DisableTrainer"]),
            Line("command", ["CMD_290", 1]),
            Line("command", ["StoreBattleResult", 32784]),
            Line("command", ["WorkSetConst", 16545, 5]),
            Line("command", ["DeactiveTrainerId", 161]),
            Line("command", ["DeactiveTrainerId", 162]),
            Line("command", ["DeactiveTrainerId", 163]),
            Line("command", ["FlagSet", 1681]),
            Line("command", ["FlagSet", 1682]),
            Line("command", ["FlagSet", 1683]),
            Line("command", ["CMD_104"]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 67, 2, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["FadeToDefaultMusic"]),
            Line("command", ["ActorCmdExec", 2, "act_hugh_exit"]),
            Line("command", ["ActorCmdWait"]),
            Line("command", ["PlaySound", 1369]),
            Line("command", ["ActorDelete", 2]),
            Line("command", ["WaitSound"]),
            Line("command", ["VMSleep", 20]),
            Line("command", ["FlagSet", 739]),

            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActorEx", 1024, 68, 0, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["StackPush", 32768]),
            Line("command", ["StackPush", 32769]),
            Line("command", ["WorkSet", 32768, 442]),
            Line("command", ["WorkSet", 32769, 1]),
            Line("command", ["RTCallGlobal", 2805]),
            Line("command", ["StackPop", 32769]),
            Line("command", ["StackPop", 32768]),

            Line("command", ["MsgActorEx", 1024, 70, 0, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["PlayerEnableRunningShoes"]),
            Line("command", ["PlayFanfare", 1303]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgSystem", 71, 2]),
            Line("command", ["WaitFanfare"]),
            Line("command", ["MsgWaitAdvance"]),
            Line("command", ["MsgSystemClose"]),

            Line("command", ["MsgActorEx", 1024, 72, 0, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["MsgActorEx", 1024, 73, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["StackPush", 32768]),
            Line("command", ["StackPush", 32769]),
            *(
                [
                    Line("command", ["WorkSetConst", 16798, flag_to_text_id[2802]]),
                    Line("command", ["WorkSetConst", 32768, 639]),
                    Line("command", ["WorkSetConst", 32769, 1]),
                ]
                if 2802 in flag_to_text_id
                else [
                    Line("command", ["WorkSet", 32768, 4]),
                    Line("command", ["WorkSet", 32769, 5]),
                ]
            ),
            Line("command", ["RTCallGlobal", 2805]),
            Line("command", ["StackPop", 32769]),
            Line("command", ["StackPop", 32768]),
            Line("command", ["FlagSet", 2802]),

            Line("command", ["MsgActorEx", 1024, 74, 1, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),
            Line("command", ["ActorCmdExec", 1, "act_bianca_exit"]),
            Line("command", ["ActorCmdWait"]),
            Line("command", ["PlaySound", 1369]),
            Line("command", ["ActorDelete", 1]),
            Line("command", ["WaitSound"]),
            Line("command", ["FlagSet", 740]),

            Line("command", ["MsgActorEx", 1024, 76, 0, 2, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["MsgWinCloseAll"]),

            Line("command", ["CMD_24f", 0, 5, 3, 1, 8, 0]),
            Line("command", ["ActorCmdWait"]),
            Line("command", ["ActorCmdExec", 0, "act3_12"]),
            Line("command", ["ActorCmdWait"]),

            Line("command", ["WorkSetConst", 16545, 7]),
            Line("command", ["WorkSetConst", 16549, 2]),
            Line("command", ["WorkSetConst", 16544, 1]),
            Line("command", ["WorkSetConst", 16661, 4]),
            Line("command", ["FlagReset", 2430]),
            Line("command", ["FlagSet", 732]),
            Line("command", ["FlagSet", 742]),
            Line("command", ["FlagSet", 743]),
            Line("command", ["FlagSet", 744]),
            Line("command", ["FlagSet", 745]),
            Line("command", ["FlagSet", 747]),
            Line("command", ["FlagSet", 748]),
            Line("command", ["WorkSetConst", 16547, 2]),
            Line("command", ["FlagSet", 738]),
            Line("command", ["WorkSetConst", 16610, 1]),
            Line("command", ["FlagSet", 499]),
            Line("command", ["FlagSet", 2488]),
            Line("command", ["WorkSetConst", 16794, blind_trainers]),
            Line("command", ["WorkSetConst", 16795, hold_a_turbo]),
            Line("command", ["WorkSetConst", 16801, auto_run]),
            Line("command", ["WorkSetConst", 16802, guaranteed_escape]),
            Line("command", ["WorkSetConst", 16803, fast_fishing]),
            Line("command", ["WorkSetConst", 16804, bike_everywhere]),
            Line("command", ["WorkSetConst", 16799, starting_day]),
            Line("command", ["WorkSetConst", 16800, starting_season]),
            Line("command", ["CMD_262", 4, 1]),

            Line("label", ["lbl_scr2_done"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),

            Line("label", ["act_hugh_exit"]),
            Line("action", ["WalkE4F", 1]),
            Line("action", ["WalkS4F", 2]),
            Line("action", ["WalkW4F", 1]),
            Line("action", ["WalkS4F", 4]),
            Line("action", ["EndAction", 0]),

            Line("label", ["act_bianca_exit"]),
            Line("action", ["WalkS8F", 1]),
            Line("action", ["WalkE8F", 1]),
            Line("action", ["WalkS8F", 2]),
            Line("action", ["WalkW8F", 1]),
            Line("action", ["WalkS8F", 4]),
            Line("action", ["EndAction", 0]),
        ]
        replace_between(s, "scr2", "scr15", scr2_lines)

        new_scr3 = [
            Line("label", ["scr3"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["ActorSetEyeToEye"]),

            Line("command", ["StackPushFlag", 2401]),
            Line("command", ["StackPushConst", 0]),
            Line("command", ["StackCmp", 1]),
            Line("command", ["VMJumpIf", 255, "lbl_mom_heal"]),

            Line("command", ["PlaySound", 1351]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActor", 1024, 55, 0, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgActorClose"]),
            Line("command", ["VMJump", "lbl_mom_done"]),

            Line("label", ["lbl_mom_heal"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActor", 1024, 75, 0, 0]),
            Line("command", ["PlayFanfare", 1300]),
            Line("command", ["CMD_104"]),
            Line("command", ["WaitFanfare"]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgActorClose"]),

            Line("label", ["lbl_mom_done"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
        ]
        replace_between(s, "scr3", "scr4", new_scr3)

        new_scr4 = [
            Line("label", ["scr4"]),
            Line("command", ["ActorPauseAll"]),
            Line("command", ["ActorSetEyeToEye"]),
            Line("command", ["PlaySound", 1351]),
            Line("command", ["WordSetPlayerName", 0]),
            Line("command", ["MsgActor", 1024, 55, 0, 0]),
            Line("command", ["InputWaitLast"]),
            Line("command", ["MsgActorClose"]),
            Line("command", ["RTFinishSubEvents"]),
            Line("command", ["ActorUnlockAll"]),
            Line("command", ["VMHalt"]),
        ]
        replace_between(s, "scr4", "scr5", new_scr4)

        a056.files[856] = bytes(assemble(s))
        rom.setFileByName("a/0/5/6", a056.save())
