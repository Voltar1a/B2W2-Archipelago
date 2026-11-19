# Incomplete: randomisestaticpokemon, randomisegiftpokemon, randomisetradepokemon,
# randomiselegendarypokemon, wildrandomisationblacklist, trainerrandomisationblacklist,
# weightedbst, adjustlevels, allpokemonseen, modifyitempool, modifylogic, and filleritemsblacklist
# are not yet implemented and are disabled in options/__init__.py
from __future__ import annotations

import typing
from Options import OptionSet, Range, Toggle
from .common import ToggleSet


class RandomiseWildPokemon(ToggleSet):
    """
    Randomises wild Pokémon encounters.
    Modifiers:
    - Global 1 to 1: Replaces every wild species consistently across all Unova areas.
    - Level appropriate evolutions: Ensures wild encounters have appropriate evolutions.
    - Randomise: Toggles wild Pokémon being randomised.
    - Type themed areas: Tries to give all Pokémon in an area a common type.
    """
    display_name = "Randomise Wild Pokémon"
    valid_keys = [
        "Global 1 to 1",
        "Level appropriate evolutions",
        "Randomise",
        "Type themed areas",
    ]
    auto_add_if_any = "Randomise"
    default = {
        "Global 1 to 1",
        "Level appropriate evolutions",
        "Randomise",
        "Type themed areas",
    }


class RandomiseTrainerPokemon(ToggleSet):
    """
    Randomises trainer Pokémon.
    Modifiers:
    - Consistent enemy teams: Keeps recurring trainer teams (rival, bosses) consistent across encounters.
    - Level appropriate evolutions: Ensures trainer Pokémon have appropriate evolutions.
    - Randomise: Toggles trainer Pokémon being randomised.
    - Type themed: All Pokémon of a trainer share at least one type.
    """
    display_name = "Randomise Trainer Pokémon"
    valid_keys = [
        "Consistent enemy teams",
        "Level appropriate evolutions",
        "Randomise",
        "Type themed",
    ]
    auto_add_if_any = "Randomise"
    default = {
        "Consistent enemy teams",
        "Level appropriate evolutions",
        "Randomise",
        "Type themed",
    }


class RandomiseStarterPokemon(ToggleSet):
    """
    Randomises starter Pokémon choices.
    Modifiers:
    - Base with 2 evolutions: Ensures starters have a 3-stage evolution line.
    - Randomise: Toggles starter Pokémon being randomised.
    """
    display_name = "Randomise Starter Pokémon"
    valid_keys = [
        "Base with 2 evolutions",
        "Randomise",
    ]
    auto_add_if_any = "Randomise"
    default = {
        "Base with 2 evolutions",
        "Randomise",
    }


# class RandomiseStaticPokemon(ToggleSet):
#     """Randomises stationary overworld encounters."""
#     display_name = "Randomise Static Pokémon"
#     valid_keys = [
#         "Randomise",
#         "Match type",
#         "Similar base stats",
#     ]
#     auto_add_if_any = "Randomise"
#
#
# class RandomiseGiftPokemon(ToggleSet):
#     """Randomises gift and fossil Pokémon."""
#     display_name = "Randomise Gift Pokémon"
#     valid_keys = [
#         "Randomise",
#         "Similar base stats",
#     ]
#     auto_add_if_any = "Randomise"
#
#
# class RandomiseTradePokemon(ToggleSet):
#     """Randomises in-game trade Pokémon."""
#     display_name = "Randomise Trade Pokémon"
#     valid_keys = [
#         "Randomise",
#         "Similar base stats",
#     ]
#     auto_add_if_any = "Randomise"
#
#
# class RandomiseLegendaryPokemon(ToggleSet):
#     """Randomises stationary legendary encounters."""
#     display_name = "Randomise Legendary Pokémon"
#     valid_keys = [
#         "Randomise",
#         "Legendary for legendary",
#         "Similar base stats",
#     ]
#     auto_add_if_any = "Randomise"


class RandomiseAbilities(ToggleSet):
    """
    Randomises the abilities of every Pokémon species.
    Modifiers:
    - Include hidden abilities: Randomises hidden abilities as well.
    - One per pokemon: Gives every species only one ability across all slots.
    - Randomise: Toggles abilities being randomised.
    """
    display_name = "Randomise Abilities"
    valid_keys = [
        "Include hidden abilities",
        "One per pokemon",
        "Randomise",
    ]
    auto_add_if_any = "Randomise"


class RandomiseLevelUpMovesets(ToggleSet):
    """
    Randomises level-up learnsets for all Pokémon.
    Modifiers:
    - Randomise: Toggles level-up movesets being randomised.
    """
    display_name = "Randomise Level Up Movesets"
    valid_keys = [
        "Randomise",
    ]
    auto_add_if_any = "Randomise"


# class WildRandomisationBlacklist(OptionSet):
#     """Excludes specific Pokémon from being used in wild randomisation."""
#     display_name = "Wild Randomisation Blacklist"
#     valid_keys: list[str] = []
#
#
# class TrainerRandomisationBlacklist(OptionSet):
#     """Excludes specific Pokémon from being used in trainer randomisation."""
#     display_name = "Trainer Randomisation Blacklist"
#     valid_keys: list[str] = []


class CatchRateMultiplier(Range):
    """Multiplies base catch rates of all Pokémon (1x to 10x)."""
    display_name = "Catch Rate Multiplier"
    range_start = 1
    range_end = 10
    default = 2


class WeightedBST(Range):
    """Adherence to the bimodal BST distribution curve (0 to 100)."""
    display_name = "Weighted Base Stat Totals"
    range_start = 0
    range_end = 100
    default = 0

    @classmethod
    def from_any(cls, data: typing.Any) -> "WeightedBST":
        if isinstance(data, bool):
            return cls(100 if data else 0)
        return super().from_any(data)


class AdjustLevels(OptionSet):
    """Progression sphere scaling for wild and trainer levels."""
    display_name = "Adjust Levels"
    valid_keys = ["wild_by_sphere", "trainer_by_sphere"]
    default = ["wild_by_sphere", "trainer_by_sphere"]


# class AllPokemonSeen(Toggle):
#     """Marks all Pokémon as seen in the Pokédex from the start."""
#     display_name = "All Pokémon Seen"
#     Default = False


class ModifyItemPool(OptionSet):
    """Item pool adjustments (e.g. 'useful_filler', 'ban_bad_filler', 'useless_key_items')."""
    display_name = "Modify Item Pool"
    valid_keys = ["useful_filler", "ban_bad_filler", "useless_key_items"]
    default = ["ban_bad_filler"]


class ModifyLogic(OptionSet):
    """Logical requirement overrides."""
    display_name = "Modify Logic"
    valid_keys = [
        "Require Dowsing Machine",
        "Require flash",
        "Consider evolutions",
        "Consider static pokemon",
        "Consider form change",
        "Consider trainers",
    ]
    default = ["Require Dowsing Machine", "Require flash"]


class FillerItemsBlacklist(OptionSet):
    """Specific item names to never roll as filler (e.g. ['Potion', 'Antidote'])."""
    display_name = "Filler Items Blacklist"
    default = set()
