from __future__ import annotations

from typing import NamedTuple, Callable
from BaseClasses import Location, CollectionState

from .items import OVERWORLD_ITEM_LOCATIONS, HIDDEN_ITEM_LOCATIONS
from .gifts import NPC_GIFT_LOCATIONS, BADGE_LOCATIONS, TM_REWARD_LOCATIONS
from .trainers import TRAINER_LOCATIONS
from .sanity import (
    MEDAL_LOCATIONS,
    POKESTAR_LOCATIONS,
    DEXSANITY_LOCATIONS,
    SEENSANITY_LOCATIONS,
    COUNTSANITY_LOCATIONS,
    GROTTO_LOCATIONS,
)

game_name = "Pokemon Black 2 and White 2"


class LocationInfo(NamedTuple):
    id: int
    flag_id: int | None
    region: str | None = None
    rule: Callable[[CollectionState, int], bool] | None = None
    alt_flags: tuple[int, ...] = ()


class PokemonB2W2Location(Location):
    game = game_name


def _build_table(
    raw_dict: dict[str, tuple]
) -> dict[str, LocationInfo]:
    return {
        name: LocationInfo(
            id=entry[0],
            flag_id=entry[1],
            region=entry[2],
            alt_flags=entry[4] if len(entry) > 4 else (),
        )
        for name, entry in raw_dict.items()
    }


# Base locations: overworld item balls, hidden items, gifts, badges, TMs
BASE_LOCATION_TABLE: dict[str, LocationInfo] = {
    **_build_table(OVERWORLD_ITEM_LOCATIONS),
    **_build_table(HIDDEN_ITEM_LOCATIONS),
    **_build_table(NPC_GIFT_LOCATIONS),
    **_build_table(BADGE_LOCATIONS),
    **_build_table(TM_REWARD_LOCATIONS),
}

# Defeatable trainer locations
TRAINER_LOCATION_TABLE: dict[str, LocationInfo] = _build_table(TRAINER_LOCATIONS)

# Sanity locations
SANITY_LOCATION_TABLE: dict[str, LocationInfo] = {
    **_build_table(MEDAL_LOCATIONS),
    **_build_table(POKESTAR_LOCATIONS),
    **_build_table(DEXSANITY_LOCATIONS),
    **_build_table(SEENSANITY_LOCATIONS),
    **_build_table(COUNTSANITY_LOCATIONS),
    **_build_table(GROTTO_LOCATIONS),
}

ALL_LOCATION_TABLE: dict[str, LocationInfo] = {
    **BASE_LOCATION_TABLE,
    **TRAINER_LOCATION_TABLE,
    **SANITY_LOCATION_TABLE,
}


def get_location_lookup_table() -> dict[str, int]:
    return {name: info.id for name, info in ALL_LOCATION_TABLE.items()}


LOCATION_NAME_TO_ID: dict[str, int] = get_location_lookup_table()

LOCATION_ID_TO_FLAG: dict[int, int] = {
    info.id: info.flag_id for info in ALL_LOCATION_TABLE.values()
    if info.flag_id is not None
}

LOCATION_ID_TO_INFO: dict[int, LocationInfo] = {
    info.id: info for info in ALL_LOCATION_TABLE.values()
}

__all__ = [
    "LocationInfo",
    "PokemonB2W2Location",
    "BASE_LOCATION_TABLE",
    "TRAINER_LOCATION_TABLE",
    "SANITY_LOCATION_TABLE",
    "ALL_LOCATION_TABLE",
    "LOCATION_NAME_TO_ID",
    "LOCATION_ID_TO_FLAG",
    "LOCATION_ID_TO_INFO",
    "OVERWORLD_ITEM_LOCATIONS",
    "HIDDEN_ITEM_LOCATIONS",
    "NPC_GIFT_LOCATIONS",
    "BADGE_LOCATIONS",
    "TM_REWARD_LOCATIONS",
    "TRAINER_LOCATIONS",
    "MEDAL_LOCATIONS",
    "POKESTAR_LOCATIONS",
    "DEXSANITY_LOCATIONS",
    "SEENSANITY_LOCATIONS",
    "COUNTSANITY_LOCATIONS",
    "GROTTO_LOCATIONS",
]
