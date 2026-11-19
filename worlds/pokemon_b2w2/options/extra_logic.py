# Incomplete: fieldrocksmash, hmbadgerequirements, strengthboulders, extracuttrees,
# randomisestartingtown, and startingtownblacklist are not yet implemented and are disabled in options/__init__.py
from __future__ import annotations

from typing import Any
from Options import Choice, Toggle


# class FieldRockSmash(Toggle):
#     """
#     makes tm94 rock smash a field move with breakable rocks blocking paths across unova, probably clay tunnel
#     """
#     display_name = "Field Move Rock Smash"
#     Default = True
#
#
# class HMBadgeRequirements(Toggle):
#     """
#     requires specific gym badges to use field moves outside battle
#     """
#     display_name = "HM Badge Requirements"
#     Default = False
#
#
# class StrengthBoulders(Toggle):
#     """
#     repurposes strength boulders to create new physical logic gates across unova
#     """
#     display_name = "Strength Boulders"
#     Default = True
#
#
# class ExtraCutTrees(Toggle):
#     """
#     adds extra cut trees to the overworld to gate progression
#     """
#     display_name = "Extra Cut Trees"
#     Default = True


class FlashLogic(Toggle):
    """
    When enabled, TM70 Flash is logically required to traverse pitch-black areas.
    """
    display_name = "Flash Logic"
    default = True

    @classmethod
    def from_any(cls, data: Any):
        if isinstance(data, (list, set, tuple)):
            return cls(bool(data))
        if isinstance(data, str) and data.lower() in ("default", "standard", "_all", "_random"):
            return cls(True)
        if isinstance(data, str) and data.lower() in ("none", "disabled", "off", "[]"):
            return cls(False)
        return super().from_any(data)


class DowsingMachineLogic(Choice):
    """
    Controls how the Dowsing Machine interacts with hidden items:
    - hard_required: logically required, and hidden items cannot be picked up in-game without the Dowsing Machine.
    - logically_required: logically required to collect hidden items, though they can still be picked up without it.
    - not_required: not required in logic or in-game (Dowsing Machine becomes useful instead of progression).
    """
    display_name = "Dowsing Machine Logic"
    option_hard_required = 0
    option_logically_required = 1
    option_not_required = 2
    default = 1

    @classmethod
    def from_any(cls, data: Any):
        if isinstance(data, bool):
            return cls(cls.option_logically_required if data else cls.option_not_required)
        return super().from_any(data)


# class RandomiseStartingTown(Toggle):
#     """
#     swaps your starting house with a house in another town across unova
#     generation spheres and trainer level scaling adapt to your starting location
#     """
#     display_name = "Randomise Starting Town"
#     Default = False
#
#
# class StartingTownBlacklist(OptionSet):
#     """
#     list of towns prevented from being chosen when randomise starting town is enabled
#     eligible towns:
#     aspertia city, floccesy town, virbank city, castelia city, nimbasa city,
#     driftveil city, mistralton city, lentimas town, undella town, lacunosa town,
#     opelucid city, humilau city, nuvema
#     """
#     display_name = "Starting Town Blacklist"
#     Default = set()
