# Incomplete
from __future__ import annotations

from Options import Toggle


class InfiniteRareCandies(Toggle):
    """
    Starts the player with 999 Rare Candies and automatically replenishes them upon use.
    NOT changeable ingame.
    """
    display_name = "Infinite Rare Candies"
    default = False


# from typing import Any
# from Options import OptionList, Choice, Range, OptionError
#
# class LevelCapType(Choice):
#     """
#     how the progressive level cap is increased:
#     - none: level caps are disabled
#     - badges: gym badges increase the level cap at each gym milestone: [13, 18, 24, 30, 33, 39, 48, 51, 59]
#     - items: collectible 'level cap upgrade' items are shuffled into the multiworld pool
#     - items_badge_gated (default): 'level cap upgrade' items raise the cap, gated by the upcoming gym badge
#     """
#     display_name = "Level Cap Type"
#     option_none = 0
#     option_badges = 1
#     option_items = 2
#     option_items_badge_gated = 3
#     alias_disabled = 0
#     alias_off = 0
#     alias_false = 0
#     alias_badge = 1
#     alias_item = 2
#     alias_upgrades = 2
#     alias_both = 3
#     alias_items_with_badges = 3
#     alias_items_with_badge_gating = 3
#     alias_items_w_badge_gating = 3
#     alias_badge_gated = 3
#     alias_gated = 3
#     Default = 3
#
#     @classmethod
#     def from_any(cls, data: Any):
#         if isinstance(data, str):
#             S = data.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
#             if s in (
#                 "items_w__badge_gating",
#                 "items_w_badge_gating",
#                 "items_with_badge_gating",
#                 "items_badge_gated",
#                 "items_and_badges",
#                 "both",
#                 "gated",
#             ):
#                 return cls(cls.option_items_badge_gated)
#         return super().from_any(data)
#
#
# class LevelCapItemValue(Range):
#     """
#     how many levels each 'level cap upgrade' item increases your level cap by (1 to 5)
#     """
#     display_name = "Level Cap Item Value"
#     range_start = 1
#     range_end = 5
#     Default = 2
#
#
# class AutoScaleAcquiredPokemon(Toggle):
#     """
#     when active, all newly acquired pokémon are scaled to your current level cap
#     """
#     display_name = "Auto-Scale Acquired Pokémon to Level Cap"
#     Default = True
#
#
# class ProgressiveLevelCap(OptionList):
#     """
#     defines the level cap curve across 0 to 8 gym badges:
#     - normal: [13, 18, 24, 30, 33, 39, 48, 51, 59]
#     - hard: [12, 16, 22, 28, 31, 37, 45, 48, 56]
#     - custom: a custom list of 9 levels (0 to 8 badges)
#     """
#     display_name = "Progressive Level Cap"
#     Default = [13, 18, 24, 30, 33, 39, 48, 51, 59]
#     value: list[int]
#
#     @classmethod
#     def from_any(cls, data: Any):
#         standard_caps = [13, 18, 24, 30, 33, 39, 48, 51, 59]
#         hard_caps = [12, 16, 22, 28, 31, 37, 45, 48, 56]
#         if data in (0, "disabled", "off", False, "false", "none", []):
#             return cls([])
#         if data in (1, "normal", "standard", "on", True, "true", "default"):
#             return cls(list(standard_caps))
#         if data in (2, "hard"):
#             return cls(list(hard_caps))
#         if isinstance(data, (list, tuple)):
#             if len(data) == 0:
#                 return cls([])
#             if len(data) != 9:
#                 raise optionerror(
#                     f"progressive level cap list must contain exactly 9 values (0 to 8 badges), got {len(data)}: {data}"
#                 )
#             Vals = [int(x) for x in data]
#             for i in range(len(vals)):
#                 if not (1 <= vals[i] <= 100):
#                     raise optionerror(f"level cap at badge {i} ({vals[i]}) must be between 1 and 100.")
#                 if i > 0 and vals[i] < vals[i - 1]:
#                     raise optionerror(
#                         f"level cap for {i} badges ({vals[i]}) cannot be lower than for {i - 1} badges ({vals[i - 1]})."
#                     )
#             return cls(vals)
#         if isinstance(data, dict):
#             if len(data) != 9:
#                 raise optionerror(
#                     f"progressive level cap mapping must contain keys 0 through 8, got: {list(data.keys())}"
#                 )
#             Vals = []
#             for b in range(9):
#                 Key = b if b in data else str(b)
#                 if key not in data:
#                     raise optionerror(f"progressive level cap mapping missing key for badge count {b}")
#                 vals.append(int(data[key]))
#             for i in range(len(vals)):
#                 if not (1 <= vals[i] <= 100):
#                     raise optionerror(f"level cap at badge {i} ({vals[i]}) must be between 1 and 100.")
#                 if i > 0 and vals[i] < vals[i - 1]:
#                     raise optionerror(
#                         f"level cap for {i} badges ({vals[i]}) cannot be lower than for {i - 1} badges ({vals[i - 1]})."
#                     )
#             return cls(vals)
#         raise optionerror(f"invalid progressive level cap option: {data}")
