# Incomplete: efficientdialogue is not yet implemented and is disabled in options/__init__.py
from __future__ import annotations

from Options import Choice, FreeText, Toggle, Range


class SkipIntro(Toggle):
    """Skips Professor Juniper's intro sequence and starts in your house."""
    display_name = "Skip Intro"
    default = True


class TrainerName(FreeText):
    """Custom in-game character name (up to 7 characters). Blank defaults to player name."""
    display_name = "In-Game Character Name"
    default = ""


class SkipIntroGender(Choice):
    """Player gender when the intro is skipped."""
    display_name = "Skip Intro Gender"
    option_male = 0
    option_female = 1
    default = "random"


class RivalName(FreeText):
    """Custom in-game rival name (up to 7 characters). Defaults to Hugh."""
    display_name = "In-Game Rival Name"
    default = "Hugh"


class InstantText(Toggle):
    """All dialogue and textboxes display instantly."""
    display_name = "Instant Text"
    default = True


class BlindTrainers(Toggle):
    """Trainers will not initiate battle on sight (talk to them to battle)."""
    display_name = "Blind Trainers"
    default = True


class GuaranteedCatch(Toggle):
    """Any Poké Ball thrown guarantees 100% catch rate."""
    display_name = "Guaranteed Catch Rate"
    default = True


class TMHMFullyCompatible(Toggle):
    """Allows all Pokémon to learn all TMs and HMs."""
    display_name = "Universal TM/HM Compatibility"
    default = True


class BikeEverywhere(Toggle):
    """Ride bicycle indoors etc."""
    display_name = "Ride Bicycle Everywhere"
    default = True


class FastFishing(Toggle):
    """Immediate bite and 100% bite rate on fishing rods."""
    display_name = "Fast Fishing"
    default = True


class HoldATurbo(Toggle):
    """Holding A advances text rapidly."""
    display_name = "Hold A Turbo"
    default = True


class CheckLogFilter(Choice):
    """Default check log filter in APtransceiver."""
    display_name = "Check Log Filter"
    option_progression = 0
    option_progression_plus_useful = 1
    option_all_checks = 2
    default = 0


class RemoveSurfBikeMusic(Toggle):
    """Keeps area background music playing while surfing or biking."""
    display_name = "Remove Surfing and Bicycle Music"
    default = True


class BattleScene(Choice):
    """Move battle animations."""
    display_name = "Battle Scene Animations"
    option_on = 0
    option_off = 1
    default = 1


class BattleStyle(Choice):
    """In-battle switch prompt when opponent faints."""
    display_name = "Battle Style"
    option_shift = 0
    option_set = 1
    default = 1


class AutoRun(Toggle):
    """Player automatically runs without needing to hold B."""
    display_name = "Auto-Run"
    default = True


class GuaranteedEscape(Toggle):
    """Fleeing from wild Pokémon battles is always 100% successful."""
    display_name = "Guaranteed Escape"
    default = True


class FastHatch(Toggle):
    """Eggs hatch after walking just a few steps (1 egg cycle)."""
    display_name = "Fast Egg Hatching"
    default = True


# class EfficientDialogue(Toggle):
#     """Shortens lengthy dialogue and non-essential cutscenes."""
#     display_name = "Efficient Dialogue"
#     Default = True


class InfiniteRepels(Toggle):
    """Starts you with 999 Max Repels and refills them automatically upon use."""
    display_name = "Infinite Repels"
    default = True


class SkipPokestarStudios(Toggle):
    """Skips mandatory Pokéstar Studios sequence after Roxie."""
    display_name = "Skip Pokéstar Studios"
    default = True


class SkipPWT(Choice):
    """Driftveil PWT Tournament handling."""
    display_name = "Skip Driftveil PWT"
    option_vanilla = 0
    option_faster_cutscenes = 1
    option_skip_entirely = 2
    default = 2


class SkipJoinAvenue(Toggle):
    """Skip Join Avenue via direct warp from Nimbasa City to Route 4."""
    display_name = "Skip Join Avenue"
    default = True


class SkipCinematicMovies(Toggle):
    """Skip 3D full-screen movies (Virbank boat, Mistralton plane, Opelucid freeze, Giant Chasm Kyurem)."""
    display_name = "Skip 3D Cinematic Movies"
    default = True


class SkipCatchingTutorial(Toggle):
    """Skips Bianca's mandatory Route 19 wild Pokémon catching tutorial."""
    display_name = "Skip Route 19 Catching Tutorial"
    default = True


class LivingRoomStarter(Toggle):
    """Puts all Aspertia intro cutscenes into the player's house saving lots of time."""
    display_name = "Living Room Starter Event"
    default = True


class MaxFriendship(Toggle):
    """All obtained Pokémon join with maximum friendship (255)."""
    display_name = "Max Friendship"
    default = True


class ExpMultiplier(Range):
    """
    Multiplier applied to all gained experience points (1x to 10x).
    Can also be dynamically modified in-game at any time via the APtransceiver.
    """
    display_name = "EXP Multiplier"
    range_start = 1
    range_end = 10
    default = 2

