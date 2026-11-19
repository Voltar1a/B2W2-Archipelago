from __future__ import annotations

from BaseClasses import Item

from .progression import ItemInfo, PROGRESSION_ITEM_TABLE
from .tms import TM_ITEM_TABLE
from .filler import FILLER_ITEM_TABLE

game_name = "Pokemon Black 2 and White 2"


class PokemonB2W2Item(Item):
    game = game_name


# Unified item table
ITEM_TABLE: dict[str, ItemInfo] = {
    **PROGRESSION_ITEM_TABLE,
    **TM_ITEM_TABLE,
    **FILLER_ITEM_TABLE,
}


def get_item_lookup_table() -> dict[str, int]:
    return {name: info.ap_id for name, info in ITEM_TABLE.items()}


ITEM_NAME_TO_ID: dict[str, int] = get_item_lookup_table()
AP_ID_TO_NAME: dict[int, str] = {info.ap_id: name for name, info in ITEM_TABLE.items()}

__all__ = [
    "ItemInfo",
    "PokemonB2W2Item",
    "ITEM_TABLE",
    "ITEM_NAME_TO_ID",
    "AP_ID_TO_NAME",
    "PROGRESSION_ITEM_TABLE",
    "TM_ITEM_TABLE",
    "FILLER_ITEM_TABLE",
]
