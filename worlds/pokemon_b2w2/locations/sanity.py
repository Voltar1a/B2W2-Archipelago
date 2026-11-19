# Incomplete: Medalsanity, PokestarStudios, Dexsanity, Seensanity, Countsanity and Grottosanity
from __future__ import annotations

# Sanity location tables
# Medalsanity:       600000 + medal_id (0..254)
# Pokéstar Studios:  700000 + movie_id
# Dexsanity:         820000 + national_dex_id (1..649)
# Seensanity:        830000 + national_dex_id (1..649)
# Countsanity:       840000 + count_id

MEDAL_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}
POKESTAR_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}
DEXSANITY_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}
SEENSANITY_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}
COUNTSANITY_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}
GROTTO_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {}

# Incomplete: hidden grotto checks require per-grotto interaction flag hooks before enabling :/
# grotto_locations: dict[str, tuple[int, int | none, str | none, tuple[int, int] | none]] = {
#     "Route 2 - Hidden Grotto": (850001, None, "Route 2", None),
#     "Route 3 - Pond Hidden Grotto": (850002, None, "Route 3", None),
#     "Route 3 - Grass Hidden Grotto": (850003, None, "Route 3", None),
#     "Route 4 - Hidden Grotto": (850004, None, "Route 4", None),
#     "Route 5 - Hidden Grotto": (850005, None, "Route 5", None),
#     "Route 6 - Path Hidden Grotto": (850006, None, "Route 6", None),
#     "Route 6 - Surf Hidden Grotto": (850007, None, "Route 6", None),
#     "Route 7 - Hidden Grotto": (850008, None, "Route 7", None),
#     "Route 9 - Hidden Grotto": (850009, None, "Route 9", None),
#     "Route 13 - Cliff Hidden Grotto": (850010, None, "Route 13", None),
#     "Route 13 - Beach Hidden Grotto": (850011, None, "Route 13", None),
#     "Route 18 - Hidden Grotto": (850012, None, "Route 18", None),
#     "Route 22 - Hidden Grotto": (850013, None, "Route 22", None),
#     "Route 23 - Hidden Grotto": (850014, None, "Route 23", None),
#     "Floccesy Ranch - Hidden Grotto": (850015, None, "Floccesy Ranch", None),
#     "Lostlorn Forest - Hidden Grotto": (850016, None, "Lostlorn Forest", None),
#     "Abundant Shrine - Water Hidden Grotto": (850017, None, "Abundant Shrine", None),
#     "Abundant Shrine - Land Hidden Grotto": (850018, None, "Abundant Shrine", None),
#     "Pinwheel Forest - Exterior Hidden Grotto": (850019, None, "Pinwheel Forest", None),
#     "Pinwheel Forest - Interior Hidden Grotto": (850020, None, "Pinwheel Forest", None),
#     "Giant Chasm - Hidden Grotto": (850021, None, "Giant Chasm", None),
# }
