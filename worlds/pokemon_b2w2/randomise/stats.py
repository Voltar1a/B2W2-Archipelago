from __future__ import annotations

import random
from typing import Any
try:
    from ..nds_compat import NintendoDSRom
    from ..nds_compat import NARC
except (ImportError, ValueError):
    from nds_compat import NintendoDSRom
    from nds_compat import NARC


def randomise_abilities(rom: NintendoDSRom, options: dict[str, Any], rng: random.Random) -> None:
    # Randomises abilities in personal NARC a/0/1/6 across species 1 to 649 (and form variants)
    opt_val = options.get("randomise_abilities", False)
    if not opt_val:
        return

    all_abilities = list(range(1, 165))

    is_one_per_pokemon = False
    is_include_hidden = False
    if isinstance(opt_val, (set, list)):
        is_one_per_pokemon = "One per pokemon" in opt_val
        is_include_hidden = "Include hidden abilities" in opt_val

    a016 = NARC(rom.getFileByName("a/0/1/6"))
    # File 709 is personal_file_regional_dex (1370 bytes)
    for i in range(1, min(709, len(a016.files))):
        pdata = bytearray(a016.files[i])
        if len(pdata) == 76:
            ab1 = rng.choice(all_abilities)
            ab2 = ab1 if is_one_per_pokemon else rng.choice(all_abilities)
            pdata[0x18] = ab1
            pdata[0x19] = ab2
            if is_include_hidden:
                pdata[0x1A] = rng.choice(all_abilities)
            a016.files[i] = bytes(pdata)

    rom.setFileByName("a/0/1/6", a016.save())


def randomise_level_up_movesets(rom: NintendoDSRom, options: dict[str, Any], rng: random.Random) -> None:
    # Randomises level-up learnset moves in NARC a/0/1/8 across all species
    if not options.get("randomise_level_up_movesets", False):
        return

    all_moves = list(range(1, 560))

    # Identify all damaging moves (power > 0) from move data archive a/0/2/1
    a021_data = rom.getFileByName("a/0/2/1")
    damaging_moves = []
    if a021_data is not None:
        moves_narc = NARC(a021_data)
        damaging_moves = [i for i in range(1, len(moves_narc.files)) if moves_narc.files[i][3] > 0]
    if not damaging_moves:
        damaging_moves = [1, 33]  # Fallback to pound, tackle

    a018 = NARC(rom.getFileByName("a/0/1/8"))
    for i in range(1, len(a018.files)):
        ldata = bytearray(a018.files[i])
        if len(ldata) < 4:
            continue

        num_slots = len(ldata) // 4
        for slot_idx in range(num_slots):
            offset = slot_idx * 4
            move_id = int.from_bytes(ldata[offset:offset + 2], "little")
            level = int.from_bytes(ldata[offset + 2:offset + 4], "little")
            if move_id == 0xFFFF and level == 0xFFFF:
                break
            # The first move (slot 0) must always be a damaging move
            if slot_idx == 0:
                new_move = rng.choice(damaging_moves)
            else:
                new_move = rng.choice(all_moves)
            ldata[offset:offset + 2] = new_move.to_bytes(2, "little")

        a018.files[i] = bytes(ldata)

    rom.setFileByName("a/0/1/8", a018.save())
