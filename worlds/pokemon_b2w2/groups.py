from __future__ import annotations

from .items import (
    TM_ITEM_TABLE,
    ITEM_TABLE,
)
from .locations import (
    OVERWORLD_ITEM_LOCATIONS,
    HIDDEN_ITEM_LOCATIONS,
    NPC_GIFT_LOCATIONS,
    BADGE_LOCATIONS,
    TM_REWARD_LOCATIONS,
    TRAINER_LOCATIONS,
    MEDAL_LOCATIONS,
    POKESTAR_LOCATIONS,
    DEXSANITY_LOCATIONS,
    SEENSANITY_LOCATIONS,
)


def get_item_groups() -> dict[str, set[str]]:
    return {
        "Badges": {
            "Basic Badge", "Toxic Badge", "Insect Badge", "Bolt Badge",
            "Quake Badge", "Jet Badge", "Legend Badge", "Wave Badge",
        },
        "HMs": {
            "HM01 Cut", "HM02 Fly", "HM03 Surf", "HM04 Strength", "HM05 Waterfall", "HM06 Dive",
        },
        "TMs": set(TM_ITEM_TABLE.keys()),
        "TMs and HMs": {*TM_ITEM_TABLE.keys(), "HM01 Cut", "HM02 Fly", "HM03 Surf", "HM04 Strength", "HM05 Waterfall", "HM06 Dive"},
        "Key Items": {name for name, info in ITEM_TABLE.items() if info.pocket == "key_items"},
        "Medicine": {name for name, info in ITEM_TABLE.items() if info.pocket == "medicine"},
        "Berries": {name for name, info in ITEM_TABLE.items() if info.pocket == "berries"},
        "Poké Balls": {name for name in ITEM_TABLE.keys() if "Ball" in name},
        "Evolution Stones": {
            "Sun Stone", "Moon Stone", "Fire Stone", "Thunderstone",
            "Water Stone", "Leaf Stone", "Shiny Stone", "Dusk Stone",
            "Dawn Stone", "Oval Stone",
        },
        "Seasons": {"Spring", "Summer", "Autumn", "Winter"},
    }


def get_location_groups() -> dict[str, set[str]]:
    raw_groups = {
        "Overworld items": set(OVERWORLD_ITEM_LOCATIONS.keys()),
        "Hidden items": set(HIDDEN_ITEM_LOCATIONS.keys()),
        "NPC gifts": set(NPC_GIFT_LOCATIONS.keys()),
        "Badge rewards": set(BADGE_LOCATIONS.keys()),
        "TM rewards": set(TM_REWARD_LOCATIONS.keys()),
        "Trainersanity": set(TRAINER_LOCATIONS.keys()),
        "Medalsanity": set(MEDAL_LOCATIONS.keys()),
        "Pokéstar Studios": set(POKESTAR_LOCATIONS.keys()),
        "Dexsanity": set(DEXSANITY_LOCATIONS.keys()),
        "Seensanity": set(SEENSANITY_LOCATIONS.keys()),
    }
    return {k: v for k, v in raw_groups.items() if len(v) > 0}
