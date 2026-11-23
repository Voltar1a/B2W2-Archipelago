from __future__ import annotations

import random
from typing import Any
try:
    from ..nds_compat import NintendoDSRom
    from ..nds_compat import NARC
    from ..patch.lz11 import decomp
except (ImportError, ValueError):
    from nds_compat import NintendoDSRom
    from nds_compat import NARC
    from patch.lz11 import decomp
from .species_data import (
    SPECIES_TABLE,
    ALL_SPECIES,
    get_base_stage,
    get_level_appropriate_species,
    get_3stage_starters,
    get_species_by_type,
)


def _is_enabled(opt: Any) -> bool:
    if isinstance(opt, bool):
        return opt
    if isinstance(opt, (list, set, tuple)):
        opts = [str(x).casefold() for x in opt]
        return "randomise" in opts or "randomize" in opts or len(opts) > 0
    return bool(opt)


def _has_mod(opt: Any, name: str) -> bool:
    if isinstance(opt, (list, set, tuple)):
        target = name.casefold()
        return any(target in str(x).casefold() for x in opt)
    return False


# Gym leader, Elite Four, and boss trainer class type themes (B2W2 class IDs)
SPECIALIST_CLASS_TYPES: dict[int, str] = {
    115: "Normal",     # Cheren (Aspertia Gym)
    116: "Poison",     # Roxie (Virbank Gym)
    113: "Bug",        # Burgh (Castelia Gym)
    112: "Electric",   # Elesa (Nimbasa Gym)
    117: "Ground",     # Clay (Driftveil Gym)
    114: "Flying",     # Skyla (Mistralton Gym)
    118: "Dragon",     # Drayden (Opelucid Gym)
    119: "Water",      # Marlon (Humilau Gym)
    78: "Ghost",       # Shauntal (Elite Four)
    79: "Fighting",    # Marshal (Elite Four)
    80: "Dark",        # Grimsley (Elite Four)
    81: "Psychic",     # Caitlin (Elite Four)
    193: "Dragon",     # Champion Iris
    10: "Fire",        # Chili
    11: "Grass",       # Cilan
    12: "Water",       # Cress
    186: "Steel",      # Colress (Plasma Frigate / P2 Lab)
    195: "Steel",      # Colress (Route 4)
    191: "Ice",        # Zinzolin
    192: "Dark",       # Shadow Triad
    233: "Bug",        # Harlequin (Castelia Gym)
}

ALL_TYPES = [
    "Normal", "Fire", "Water", "Grass", "Electric", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic",
    "Bug", "Rock", "Ghost", "Dragon", "Steel", "Dark",
]


def ensure_early_damaging_moves(
    rom: NintendoDSRom,
    species_list: tuple[int, ...] | list[int] | None = None,
) -> None:
    # Ensures starter Pokémon (and any early encounter species) have a damaging move
    a021_data = rom.getFileByName("a/0/2/1")
    a018_data = rom.getFileByName("a/0/1/8")
    if a021_data is None or a018_data is None:
        return

    moves_narc = NARC(a021_data)
    learnsets = NARC(a018_data)

    def is_damaging(m_id: int) -> bool:
        if 1 <= m_id < len(moves_narc.files):
            return moves_narc.files[m_id][3] > 0
        return False

    targets = list(species_list) if species_list is not None else list(range(1, len(learnsets.files)))
    modified = False

    for sp in targets:
        if not (1 <= sp < len(learnsets.files)):
            continue
        ldata = bytearray(learnsets.files[sp])
        if len(ldata) < 4:
            continue

        slots: list[tuple[int, int]] = []
        has_damaging = False
        earliest_damaging_idx = -1

        for s_idx in range(len(ldata) // 4):
            off = s_idx * 4
            m = int.from_bytes(ldata[off:off + 2], "little")
            lvl = int.from_bytes(ldata[off + 2:off + 4], "little")
            if m == 0xFFFF and lvl == 0xFFFF:
                break
            slots.append((m, lvl))
            if lvl <= 5 and is_damaging(m):
                has_damaging = True
            elif earliest_damaging_idx == -1 and is_damaging(m):
                earliest_damaging_idx = s_idx

        if not has_damaging:
            # Need to ensure a damaging move at level 1 in the very first slot
            if earliest_damaging_idx != -1:
                # move earliest damaging move to level 1 and place it in slot 0
                dmg_move, _ = slots[earliest_damaging_idx]
                slots.pop(earliest_damaging_idx)
                slots.insert(0, (dmg_move, 1))
            else:
                # Species has no damaging moves in its learnset at all - ABRAAAAAA bringer of crashes
                # assign a basic move: confusion for psychic, tackle for others
                dmg_move = 93 if sp in (63, 64, 65) else 33
                slots.insert(0, (dmg_move, 1))

            new_ldata = bytearray()
            for m, lvl in slots:
                new_ldata += m.to_bytes(2, "little") + lvl.to_bytes(2, "little")
            new_ldata += b"\xFF\xFF\xFF\xFF"
            learnsets.files[sp] = bytes(new_ldata)
            modified = True

    if modified:
        rom.setFileByName("a/0/1/8", learnsets.save())


def randomise_starters(rom: NintendoDSRom, options: dict[str, Any], rng: random.Random) -> tuple[int, int, int]:
    # Randomises starter Pokémon choices for Bianca's gift
    opt = options.get("randomise_starter_pokemon", False)
    if not _is_enabled(opt):
        return (495, 498, 501)

    use_3stage = _has_mod(opt, "Base with 2 evolutions")
    if use_3stage:
        cand_pool = get_3stage_starters()
    else:
        cand_pool = [dex for dex, info in SPECIES_TABLE.items() if info.stage == 1]

    if len(cand_pool) < 3:
        cand_pool = get_3stage_starters()

    starters = rng.sample(cand_pool, 3)
    s_grass, s_fire, s_water = starters[0], starters[1], starters[2]

    # Store in options dict for living_room_starter patch
    options["starter_grass"] = s_grass
    options["starter_fire"] = s_fire
    options["starter_water"] = s_water

    # Also patch Aspertia lookout vanilla script (file 854 in a/0/5/6) in case living room starter is off
    try:
        scripts_narc = NARC(rom.getFileByName("a/0/5/6"))
        s854 = bytearray(scripts_narc.files[854])

        def replace_u16(data: bytearray, old_val: int, new_val: int) -> None:
            old_b = old_val.to_bytes(2, "little")
            new_b = new_val.to_bytes(2, "little")
            idx = 0
            while True:
                idx = data.find(old_b, idx)
                if idx == -1:
                    break
                data[idx:idx + 2] = new_b
                idx += 2

        replace_u16(s854, 495, s_grass)
        replace_u16(s854, 498, s_fire)
        replace_u16(s854, 501, s_water)
        scripts_narc.files[854] = bytes(s854)
        rom.setFileByName("a/0/5/6", scripts_narc.save())
    except Exception:
        pass

    # Patch starter selection screen graphics (NARC a/2/0/2 = arcid_psel) and species table (overlay 316)
    try:
        src_narc = NARC(rom.getFileByName("a/0/0/4"))
        dest_narc = NARC(rom.getFileByName("a/2/0/2"))

        def _darken_rgb555(pltt_bytes: bytes) -> bytes:
            out = bytearray(len(pltt_bytes))
            for off in range(0, len(pltt_bytes) - 1, 2):
                c = int.from_bytes(pltt_bytes[off : off + 2], "little")
                r = (c & 0x1F) >> 1
                g = ((c >> 5) & 0x1F) >> 1
                b = ((c >> 10) & 0x1F) >> 1
                dark_c = (c & 0x8000) | (b << 10) | (g << 5) | r
                out[off : off + 2] = dark_c.to_bytes(2, "little")
            return bytes(out)

        for i, s in enumerate((s_grass, s_fire, s_water)):
            # Preserve 40-byte RLCN header in PLTT (files 0, 2, 4) and PLTTDark (files 1, 3, 5)
            src_pltt_colors = src_narc.files[s * 20 + 18][40:72]
            orig_pltt = dest_narc.files[i * 2]
            dest_narc.files[i * 2] = orig_pltt[:40] + src_pltt_colors + orig_pltt[72:]

            orig_pltt_dark = dest_narc.files[i * 2 + 1]
            dest_narc.files[i * 2 + 1] = orig_pltt_dark[:40] + _darken_rgb555(src_pltt_colors) + orig_pltt_dark[72:]

            # Preserve 48-byte RGCN header in NCGR (files 12, 13, 14) so 1D mapping mode stays intact
            src_ncgr = decomp(src_narc.files[s * 20], 0)
            orig_ncgr = dest_narc.files[12 + i]
            dest_narc.files[12 + i] = orig_ncgr[:48] + src_ncgr[48:]

        rom.setFileByName("a/2/0/2", dest_narc.save())
    except Exception:
        pass

    try:
        try:
            from ..nds_compat import saveOverlayTable
        except (ImportError, ValueError):
            from nds_compat import saveOverlayTable
        overlay_table = rom.loadArm9Overlays()
        if 316 in overlay_table:
            ov316 = overlay_table[316]
            ov316_data = bytearray(ov316.data)
            ov316_data[0x2c14:0x2c16] = s_grass.to_bytes(2, "little")
            ov316_data[0x2c16:0x2c18] = s_fire.to_bytes(2, "little")
            ov316_data[0x2c18:0x2c1a] = s_water.to_bytes(2, "little")
            ov316.data = bytes(ov316_data)
            rom.files[ov316.fileID] = ov316.save(compress=ov316.compressed)
            rom.arm9OverlayTable = saveOverlayTable(overlay_table)
    except Exception:
        pass

    ensure_early_damaging_moves(rom, (s_grass, s_fire, s_water))
    return (s_grass, s_fire, s_water)


def randomise_wild_pokemon(rom: NintendoDSRom, options: dict[str, Any], rng: random.Random) -> None:
    # Randomises wild encounters across all 135 zone tables in NARC a/1/2/7
    opt = options.get("randomise_wild_pokemon", False)
    if not _is_enabled(opt):
        return

    try:
        from ..patch.habitat import HABITAT_TO_ENC_FILES
    except (ImportError, ValueError):
        from patch.habitat import HABITAT_TO_ENC_FILES

    level_appropriate = _has_mod(opt, "Level appropriate evolutions")
    type_themed = _has_mod(opt, "Type themed areas")
    global_1_to_1 = _has_mod(opt, "Global 1 to 1")
    global_map: dict[int, int] = {}

    narc = NARC(rom.getFileByName("a/1/2/7"))
    for h_idx in range(58):
        enc_indices = HABITAT_TO_ENC_FILES[h_idx]
        # Pick theme type once per habitat area if enabled
        theme_type = rng.choice(ALL_TYPES) if type_themed else None
        type_cands = get_species_by_type(theme_type) if theme_type else ALL_SPECIES
        area_map: dict[int, int] = global_map if global_1_to_1 else {}

        for file_idx in enc_indices:
            if file_idx >= len(narc.files):
                continue
            fdata = bytearray(narc.files[file_idx])
            if len(fdata) < 232:
                continue

            season_count = len(fdata) // 232
            for season in range(season_count):
                season_offset = season * 232 + 8
                for slot in range(56):
                    slot_offset = season_offset + slot * 4
                    raw_species = int.from_bytes(fdata[slot_offset:slot_offset + 2], "little")
                    dex_num = raw_species & 0x7FF
                    if dex_num == 0:
                        continue

                    if dex_num not in area_map:
                        used = set(area_map.values())
                        if level_appropriate:
                            avail = [c for c in type_cands if get_base_stage(c) not in used] or type_cands
                            chosen_base = get_base_stage(rng.choice(avail))
                        else:
                            avail = [c for c in type_cands if c not in used] or type_cands
                            chosen_base = rng.choice(avail)
                        area_map[dex_num] = chosen_base

                    min_lvl = fdata[slot_offset + 2]
                    max_lvl = fdata[slot_offset + 3]
                    avg_lvl = (min_lvl + max_lvl) // 2
                    base_species = area_map[dex_num]
                    final_species = get_level_appropriate_species(base_species, avg_lvl, rng) if level_appropriate else base_species
                    form = (season if season < 4 else 0) if final_species in (585, 586) else 0
                    new_raw = (form << 11) | (final_species & 0x7FF)
                    fdata[slot_offset:slot_offset + 2] = new_raw.to_bytes(2, "little")

            narc.files[file_idx] = bytes(fdata)

    rom.setFileByName("a/1/2/7", narc.save())


def randomise_trainer_pokemon(
    rom: NintendoDSRom,
    options: dict[str, Any],
    rng: random.Random,
    starters: tuple[int, int, int] = (495, 498, 501),
) -> None:
    # Randomises trainer parties in a/0/9/2 with headers in a/0/9/1
    opt = options.get("randomise_trainer_pokemon", False)
    if not _is_enabled(opt):
        return

    level_appropriate = _has_mod(opt, "Level appropriate evolutions")
    consistent_rival = _has_mod(opt, "Consistent enemy teams") or _has_mod(opt, "Consistent rival party")
    type_themed = _has_mod(opt, "Type themed")

    n1 = NARC(rom.getFileByName("a/0/9/1"))
    n2 = NARC(rom.getFileByName("a/0/9/2"))

    s_grass, s_fire, s_water = starters

    hugh_rosters: dict[int, list[int]] = {
        1: [s_fire, rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES)],
        2: [s_water, rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES)],
        0: [s_grass, rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES), rng.choice(ALL_SPECIES)],
    }

    colress_type = "Steel" if type_themed else None
    colress_cands = get_species_by_type(colress_type) if colress_type else ALL_SPECIES
    colress_roster = [rng.choice(colress_cands) for _ in range(6)]

    zinzolin_type = "Ice" if type_themed else None
    zinzolin_cands = get_species_by_type(zinzolin_type) if zinzolin_type else ALL_SPECIES
    zinzolin_roster = [rng.choice(zinzolin_cands) for _ in range(3)]

    triad_type = "Dark" if type_themed else None
    triad_cands = get_species_by_type(triad_type) if triad_type else ALL_SPECIES
    triad_rosters: dict[str, list[int]] = {
        "m1": [rng.choice(triad_cands) for _ in range(3)],
        "m2": [rng.choice(triad_cands) for _ in range(3)],
        "m3": [rng.choice(triad_cands) for _ in range(3)],
    }

    cheren_type = "Normal" if type_themed else None
    cheren_cands = get_species_by_type(cheren_type) if cheren_type else ALL_SPECIES
    cheren_roster = [rng.choice(cheren_cands) for _ in range(6)]

    for tid in range(1, len(n1.files)):
        tdata = bytearray(n1.files[tid])
        pdata = bytearray(n2.files[tid])
        num_pokemon = tdata[3]
        if num_pokemon == 0 or len(pdata) == 0:
            continue

        trainer_class = tdata[1]
        has_custom_moves = bool(tdata[0] & 1)
        has_custom_item = bool(tdata[0] & 2)
        entry_len = 8 + (8 if has_custom_moves else 0) + (2 if has_custom_item else 0)
        kept_len = 10 if has_custom_item else 8

        is_hugh = (trainer_class == 145)

        vanilla_species = [
            int.from_bytes(pdata[i * entry_len + 4 : i * entry_len + 6], "little")
            for i in range(num_pokemon)
            if i * entry_len + 6 <= len(pdata)
        ]

        hugh_branch = 1
        if is_hugh:
            if any(sp in (501, 502, 503) for sp in vanilla_species):
                hugh_branch = 2
            elif any(sp in (495, 496, 497) for sp in vanilla_species):
                hugh_branch = 0
            else:
                hugh_branch = 1

        theme_type: str | None = None
        if type_themed and not is_hugh:
            theme_type = SPECIALIST_CLASS_TYPES.get(trainer_class)
            if not theme_type:
                theme_type = rng.choice(ALL_TYPES)
        type_cands = get_species_by_type(theme_type) if theme_type else ALL_SPECIES

        new_pdata = bytearray()
        for poke_idx in range(num_pokemon):
            off = poke_idx * entry_len
            if off + kept_len > len(pdata):
                break

            level = int.from_bytes(pdata[off + 2:off + 4], "little")
            orig_sp = vanilla_species[poke_idx] if poke_idx < len(vanilla_species) else 0

            if is_hugh and consistent_rival:
                if orig_sp in (495, 496, 497, 498, 499, 500, 501, 502, 503):
                    base_mon = hugh_rosters[hugh_branch][0]
                elif orig_sp in (519, 520, 521):
                    base_mon = hugh_rosters[hugh_branch][1]
                elif orig_sp in (512, 514, 516):
                    base_mon = hugh_rosters[hugh_branch][2]
                elif orig_sp == 626:
                    base_mon = hugh_rosters[hugh_branch][3]
                elif orig_sp in (328, 329, 330):
                    base_mon = hugh_rosters[hugh_branch][4]
                elif orig_sp in (602, 603, 604):
                    base_mon = hugh_rosters[hugh_branch][5]
                else:
                    base_mon = hugh_rosters[hugh_branch][poke_idx % 6]

            elif tid in (358, 344, 813) and consistent_rival:
                base_mon = colress_roster[poke_idx % 6]

            elif tid in (704, 584, 347, 497) and consistent_rival:
                base_mon = zinzolin_roster[poke_idx % 3]

            elif tid in (583, 348, 687) and consistent_rival:
                base_mon = triad_rosters["m1"][poke_idx % 3]

            elif tid in (498, 688) and consistent_rival:
                base_mon = triad_rosters["m2"][poke_idx % 3]

            elif tid in (499, 689) and consistent_rival:
                base_mon = triad_rosters["m3"][poke_idx % 3]

            elif tid in (156, 700, 706, 707, 708) and consistent_rival:
                base_mon = cheren_roster[poke_idx % 6]

            else:
                base_mon = rng.choice(type_cands)

            if level_appropriate:
                new_species = get_level_appropriate_species(base_mon, level, rng)
            else:
                new_species = base_mon

            # Clear custom moveset flag & strip move bytes so randomized species use their own learnset
            entry = bytearray(pdata[off : off + kept_len])
            entry[4:6] = new_species.to_bytes(2, "little")
            if new_species != orig_sp:
                entry[6:8] = b"\x00\x00"
            new_pdata.extend(entry)

        if has_custom_moves and len(new_pdata) == num_pokemon * kept_len:
            tdata[0] &= ~1
            n1.files[tid] = bytes(tdata)
            n2.files[tid] = bytes(new_pdata)
        else:
            # Fallback if truncated vanilla entry
            n2.files[tid] = bytes(new_pdata) if len(new_pdata) == num_pokemon * kept_len else bytes(pdata)

    rom.setFileByName("a/0/9/1", n1.save())
    rom.setFileByName("a/0/9/2", n2.save())
