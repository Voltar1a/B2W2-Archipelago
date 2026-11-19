# Dynamic Pokédex habitat list (a/2/9/6) and area town map (a/1/7/6) generator

from __future__ import annotations

import struct
from typing import TYPE_CHECKING

try:
    from ..nds_compat import NARC
except (ImportError, ValueError):
    try:
        from worlds.pokemon_b2w2.nds_compat import NARC
    except (ImportError, ValueError):
        from nds_compat import NARC

if TYPE_CHECKING:
    from ..nds_compat import NintendoDSRom


HABITAT_MAX = 30

# Mapping from each habitat list file index (0..57 in a/2/9/6) to the encounter table indices (0..134 in a/1/2/7)
HABITAT_TO_ENC_FILES: dict[int, list[int]] = {
    0: [104, 105],                                              # Route 4
    1: [124],                                                   # Route 15
    2: [134],                                                   # Route 21
    3: [84, 85, 86, 87, 88, 89, 90, 91, 92],                    # Clay tunnel (+ underground Ruins / chambers)
    4: [23, 24, 25, 26],                                        # Twist mountain
    5: [97],                                                    # Village bridge
    6: [27, 28, 29, 30],                                        # Dragonspiral tower
    7: [81, 82, 83],                                            # Relic passage
    8: [125],                                                   # Route 16
    9: [106],                                                   # Route 5
    10: [98],                                                   # Marvelous bridge
    11: [123],                                                  # Abundant Shrine
    12: [132],                                                  # Undella town
    13: [107],                                                  # Route 6
    14: [43],                                                   # Undella bay
    15: [102, 103],                                             # Wellspring cave
    16: [95],                                                   # Nature Preserve
    17: [127],                                                  # Route 18
    18: [32, 33, 34, 35, 36],                                   # Giant Chasm
    19: [111],                                                  # Route 7
    20: [31, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],           # Victory road
    21: [12, 13, 14, 15, 16, 17, 18, 19],                       # Relic castle
    22: [0],                                                    # Striaton city
    23: [128],                                                  # Route 19
    24: [3],                                                    # Aspertia city
    25: [116],                                                  # Route 8
    26: [44, 45],                                               # Floccesy ranch
    27: [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],               # Strange house
    28: [129],                                                  # Route 20
    29: [4],                                                    # Virbank city
    30: [37, 38, 39, 40, 41],                                   # Castelia Sewers
    31: [118],                                                  # Route 9
    32: [46, 47],                                               # Virbank complex
    33: [42],                                                   # P2 laboratory
    34: [1],                                                    # Castelia city
    35: [8, 9],                                                 # Pinwheel forest
    36: [5],                                                    # Humilau city
    37: [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],   # Reversal mountain
    38: [6, 7],                                                 # Dreamyard
    39: [112, 113, 114, 115],                                   # Celestial tower
    40: [130],                                                  # Route 22
    41: [10, 11],                                               # Desert Resort
    42: [119],                                                  # Route 11
    43: [133],                                                  # Route 17
    44: [99],                                                   # Route 1
    45: [131],                                                  # Route 23
    46: [117],                                                  # Moor of Icirrus
    47: [120],                                                  # Route 12
    48: [100],                                                  # Route 2
    49: [108, 109, 110],                                        # Mistralton cave + Guidance chamber
    50: [121],                                                  # Route 13
    51: [101],                                                  # Route 3
    52: [2],                                                    # Icirrus city
    53: [96],                                                   # Driftveil Drawbridge
    54: [93, 94],                                               # Seaside cave
    55: [126],                                                  # Lostlorn forest
    56: [122],                                                  # Route 14
    57: [20, 21, 22],                                           # Chargestone cave
}

# Mapping from 57 active columns in 85-column town map area table (a/1/7/6) to habitat list file index (0..57)
COL_TO_HAB: dict[int, int] = {
    2: 22, 4: 34, 8: 52, 12: 12, 19: 38, 20: 35, 21: 41, 22: 21,
    24: 57, 25: 4, 26: 6, 27: 18, 29: 33, 30: 15, 31: 49, 32: 39,
    33: 46, 34: 11, 35: 14, 36: 55, 37: 44, 38: 48, 39: 51, 40: 0,
    41: 9, 42: 13, 43: 19, 44: 25, 45: 31, 46: 42, 47: 47, 48: 50,
    49: 56, 50: 1, 51: 8, 52: 43, 53: 17, 55: 53, 57: 5, 58: 10,
    59: 24, 61: 29, 63: 36, 66: 23, 67: 28, 68: 2, 69: 40, 70: 30,
    71: 26, 72: 32, 73: 37, 74: 27, 75: 45, 76: 20, 77: 7, 78: 54,
    79: 3,
}


def update_pokedex_habitats(rom: "NintendoDSRom") -> None:
    # Rebuilds the Pokédex habitat list NARC (a/2/9/6) and Pokédex area NARC (a/1/7/6)
    enc_data = rom.getFileByName("a/1/2/7")
    hab_data = rom.getFileByName("a/2/9/6")
    if enc_data is None or hab_data is None:
        return

    enc_narc = NARC(enc_data)
    hab_narc = NARC(hab_data)

    for h_idx in range(min(58, len(hab_narc.files))):
        land_kind = int.from_bytes(hab_narc.files[h_idx][6:8], "little")
        sp_map: dict[int, tuple[list[list[int]], list[list[int]]]] = {}

        for e_idx in HABITAT_TO_ENC_FILES.get(h_idx, ()):
            if e_idx >= len(enc_narc.files):
                continue
            fdata = enc_narc.files[e_idx]
            season_count = len(fdata) // 232
            if season_count == 0:
                continue

            for s in range(4):
                s_idx = s if s < season_count else 0
                off = s_idx * 232 + 8
                for slot in range(56):
                    raw = int.from_bytes(fdata[off + slot * 4 : off + slot * 4 + 2], "little")
                    sp = raw & 0x7FF
                    form = raw >> 11
                    if not (1 <= sp <= 649):
                        continue
                    kind = 0 if slot < 36 else (1 if slot < 46 else 2)
                    if sp not in sp_map:
                        sp_map[sp] = ([[0] * 3 for _ in range(4)], [[0] * 3 for _ in range(4)])
                    sp_map[sp][0][s][kind] = 1
                    if sp in (585, 586):
                        sp_map[sp][1][s][kind] = s
                    elif sp in (550, 422, 423) and sp_map[sp][1][s][kind] == 0:
                        sp_map[sp][1][s][kind] = form

        entries = sorted(sp_map.keys())[:HABITAT_MAX]
        kinds = [
            1 if any(sp_map[sp][0][s][k] for sp in entries for s in range(4)) else 0
            for k in range(3)
        ]
        by_season = [
            1 if any(len(set(sp_map[sp][0][s][k] for s in range(4))) > 1 for sp in entries) else 0
            for k in range(3)
        ]

        out = bytearray(struct.pack("<3B3BHH", *by_season, *kinds, land_kind, len(entries)))
        for sp in entries:
            pres, frms = sp_map[sp]
            out += struct.pack(
                "<H12B12BH",
                sp,
                *(pres[s][k] for s in range(4) for k in range(3)),
                *(frms[s][k] for s in range(4) for k in range(3)),
                0,
            )
        hab_narc.files[h_idx] = bytes(out)

    rom.setFileByName("a/2/9/6", hab_narc.save())

    a176_data = rom.getFileByName("a/1/7/6")
    if a176_data is not None:
        a176 = NARC(a176_data)
        built = [[[0] * 85 for _ in range(4)] for _ in range(650)]
        sub_ranges = [
            (0, range(0, 12)),
            (1, range(12, 24)),
            (2, range(24, 36)),
            (3, range(36, 41)),
            (4, range(41, 46)),
            (5, range(46, 51)),
            (6, range(51, 56)),
        ]
        for col, h_idx in COL_TO_HAB.items():
            for e_idx in HABITAT_TO_ENC_FILES.get(h_idx, ()):
                if e_idx >= len(enc_narc.files):
                    continue
                fdata = enc_narc.files[e_idx]
                season_count = len(fdata) // 232
                if season_count == 0:
                    continue
                for s in range(4):
                    s_idx = s if s < season_count else 0
                    off = s_idx * 232 + 8
                    for bit, r in sub_ranges:
                        for slot in r:
                            sp = int.from_bytes(fdata[off + slot * 4 : off + slot * 4 + 2], "little") & 0x7FF
                            if 1 <= sp <= 649:
                                built[sp][s][col] |= 1 << bit

        for sp in range(1, min(650, len(a176.files) + 1)):
            seasons = built[sp]
            all_year = int(all(seasons[s] == seasons[0] for s in range(4)))
            adata = bytearray([all_year])
            for s in range(4):
                row = seasons[s]
                adata += bytes([int(not any(row))] + row)
            a176.files[sp - 1] = bytes(adata)

        rom.setFileByName("a/1/7/6", a176.save())
