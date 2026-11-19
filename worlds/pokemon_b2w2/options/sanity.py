# Incomplete: Dexsanity, Dexcountsanity, Seensanity, Seencountsanity,
# Trainercountsanity, Itemcountsanity, Medalsanity, Medalcountsanity, pokestarstudioschecks,
# shuffleoverworlditems, shufflenpcgifts, abyssalruins, pokedexchecks, showchecks, and Grottosanity
# are not yet implemented and are disabled in options/__init__.py
from __future__ import annotations

import random
from typing import Any, Iterable, Self, Dict

from Options import Range, Toggle, DefaultOnToggle, Choice, OptionError
from .common import ExtendedOptionCounter

dex_by_name: dict[str, int] = {}


class DexsanityResolver:

    def resolve_plando_dex(self, value: int | str | list | dict) -> tuple[int, ...]:
        while not isinstance(value, int | range):
            if isinstance(value, str):
                if "," in value:
                    value = value.split(",")
                elif "-" in value and all(a.strip().isnumeric() for a in value.split("-")):
                    res = tuple(int(r) for r in value.split("-"))
                    for r in res:
                        if not 1 <= r <= 649:
                            raise OptionError(
                                f"Option {self.__class__.__name__} contains dex number {r}, which is not in range 1-649"
                            )
                    value = range(res[0], res[1] + 1)
                elif value.strip().isnumeric():
                    value = int(value)
                elif res := dex_by_name.get(value, False):
                    value = res
                else:
                    raise OptionError(f"Option {self.__class__.__name__} contains invalid string value {value}")
            elif isinstance(value, list):
                value = random.choice(value)
            elif isinstance(value, dict):
                for v in value.values():
                    if not isinstance(v, int):
                        raise OptionError(
                            f"Option {self.__class__.__name__} contains a list with a non-integer weight {v} ({type(v)})"
                        )
                value = random.choices(tuple(value), tuple(value.values()))
            else:
                raise OptionError(
                    f"Option {self.__class__.__name__} as a list expects integers, ranges, "
                    f"nested lists, and nested weighted lists, but instead found {type(value)}"
                )
        return tuple(value) if isinstance(value, range) else (value,)


# class Dexsanity(Range, DexsanityResolver):
#     """
#     Adds location checks for catching and registering unique pokemon species in the pokedex
#     """
#     display_name = "Dexsanity"
#     value: int | list[int]
#     Default = 0
#     range_start = 0
#     range_end = 649
#
#     def __init__(self, value: Any):
#         if isinstance(value, Iterable):
#             self.value = sorted(set(vv for v in value for vv in self.resolve_plando_dex(v)))
#         else:
#             super().__init__(value)
#
#     @classmethod
#     def from_any(cls, data: Any) -> Self:
#         if isinstance(data, str):
#             return cls.from_text(str(data))
#         if isinstance(data, (Iterable, int)):
#             return cls(data)
#         raise optionerror(f"unsupported type for {cls.__name__}: {type(data)}")


class Dexcountsanity(ExtendedOptionCounter):
    """
    Adds milestone location checks for catching a total number of species:
    - Maximum (0-649): Total milestone checks to generate (0 to disable).
    - Steps (1-649): Number of caught Pokémon required per check.
    - Leniency: Logic leniency (requires X fewer caught Pokémon).
    """
    display_name = "Dex Countsanity"
    fill_defaults = True
    valid_keys = ["Maximum", "Steps", "Leniency"]
    default = {"Maximum": 0, "Steps": 5, "Leniency": 0}
    individual_min_max = {
        "Maximum": (0, 649),
        "Steps": (1, 649),
        "Leniency": (0, 648),
    }


class Seensanity(Range, DexsanityResolver):
    """
    Adds location checks for seeing unique Pokémon species in the wild or in trainer battles.
    """
    display_name = "Seensanity"
    value: int | list[int]
    default = 0
    range_start = 0
    range_end = 649

    def __init__(self, value: Any):
        if isinstance(value, Iterable):
            self.value = sorted(set(vv for v in value for vv in self.resolve_plando_dex(v)))
        else:
            super().__init__(value)

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, str):
            return cls.from_text(str(data))
        if isinstance(data, (Iterable, int)):
            return cls(data)
        raise OptionError(f"Unsupported type for {cls.__name__}: {type(data)}")


class Seencountsanity(ExtendedOptionCounter):
    """
    Adds milestone location checks for seeing a total number of species:
    - Maximum (0-649): Total milestone checks to generate (0 to disable).
    - Steps (1-649): Number of seen Pokémon required per check.
    - Leniency: Logic leniency.
    """
    display_name = "Seen Countsanity"
    fill_defaults = True
    valid_keys = ["Maximum", "Steps", "Leniency"]
    default = {"Maximum": 0, "Steps": 5, "Leniency": 0}
    individual_min_max = {
        "Maximum": (0, 649),
        "Steps": (1, 649),
        "Leniency": (0, 648),
    }


class Trainersanity(Range):
    """
    Adds location checks for defeating individual trainers throughout Unova.
    - 0 (or false): Disabled (no trainer checks).
    - 1 to 516: Randomly selects that exact number of trainers as location checks.
    - 516 (or true): All trainers throughout Unova are location checks.
    """
    display_name = "Trainersanity"
    range_start = 0
    range_end = 516
    default = 0

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, bool):
            return cls(cls.range_end if data else 0)
        return super().from_any(data)


class Trainercountsanity(ExtendedOptionCounter):
    """
    Adds milestone location checks for defeating a total number of trainers:
    - Maximum (0-650): Total milestone checks to generate (0 to disable).
    - Steps (1-650): Number of defeated trainers required per check.
    - Leniency: Logic leniency.
    """
    display_name = "Trainer Countsanity"
    fill_defaults = True
    valid_keys = ["Maximum", "Steps", "Leniency"]
    default = {"Maximum": 0, "Steps": 10, "Leniency": 0}
    individual_min_max = {
        "Maximum": (0, 650),
        "Steps": (1, 650),
        "Leniency": (0, 649),
    }


class ItemCountsanity(ExtendedOptionCounter):
    """
    Adds milestone location checks for collecting a total number of items:
    - Maximum (0-500): Total milestone checks to generate (0 to disable).
    - Steps (1-500): Number of collected items required per check.
    - Leniency: Logic leniency.
    """
    display_name = "Item Countsanity"
    fill_defaults = True
    valid_keys = ["Maximum", "Steps", "Leniency"]
    default = {"Maximum": 0, "Steps": 5, "Leniency": 0}
    individual_min_max = {
        "Maximum": (0, 500),
        "Steps": (1, 500),
        "Leniency": (0, 499),
    }


class Medalsanity(Toggle):
    """
    Adds location checks for earning individual Medals.
    """
    display_name = "Medalsanity"
    default = False


class Medalcountsanity(ExtendedOptionCounter):
    """
    Adds milestone location checks for earning a total number of Medals:
    - Maximum (0-255): Total milestone checks to generate (0 to disable).
    - Steps (1-255): Number of medals required per check (e.g. Steps 5 generates checks at 5, 10, 15...).
    - Leniency: Logic leniency.
    """
    display_name = "Medal Countsanity"
    fill_defaults = True
    valid_keys = ["Maximum", "Steps", "Leniency"]
    default = {"Maximum": 0, "Steps": 5, "Leniency": 0}
    individual_min_max = {
        "Maximum": (0, 255),
        "Steps": (1, 255),
        "Leniency": (0, 254),
    }


class PokestarStudiosChecks(Toggle):
    """
    Adds location checks for completing movie shoots and achieving Strange Endings at Pokéstar Studios.
    """
    display_name = "Pokéstar Studios Checks"
    default = False


class ShuffleBadgeRewards(DefaultOnToggle):
    """
    Shuffles the 8 Gym Badges into the multiworld item pool.
    - true: Badges are shuffled into the general item pool.
    - false: Badges remain on their vanilla gym leaders.
    """
    display_name = "Shuffle Badge Rewards" 


# class ShuffleOverworldItems(DefaultOnToggle):
#     """
#     shuffles overworld item balls on the ground across unova into pool
#     """
#     display_name = "Shuffle Overworld Items"
#
#
# class ShuffleNPCGifts(DefaultOnToggle):
#     """
#     shuffles items and tms given as gifts by npcs throughout unova into pool
#     """
#     display_name = "Shuffle NPC Gifts"


class HiddenItems(Toggle):
    """
    Include hidden items found with the Dowsing Machine as item locations.
    """
    display_name = "Hidden Items"
    default = True


# class AbyssalRuins(Toggle):
#     """
#     include item checks in the abyssal ruins
#     """
#     display_name = "Abyssal Ruins Checks"
#     Default = False
#
#
# class PokedexChecks(Toggle):
#     """
#     include pokédex milestone checks (e.g. bianca habitat list milestones)
#     """
#     display_name = "Pokédex Milestone Checks"
#     Default = True
#
#
# class ShowChecks(Toggle):
#     """
#     include pokémon showing  item checks (e.g. showing specific pokémon types/forms to npcs)
#     """
#     display_name = "Show Checks"
#     Default = False
#
#
# class Grottosanity(Toggle):
#     """
#     include all 21 hidden grottoes across unova as archipelago location checks
#     """
#     display_name = "Grottosanity (Hidden Grottoes)"
#     Default = False


