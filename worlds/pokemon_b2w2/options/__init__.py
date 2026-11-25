from __future__ import annotations

import typing
from dataclasses import dataclass
from Options import Choice, Range, PerGameCommonOptions, OptionError, OptionSet, StartInventoryPool, FreeText, Toggle

from .sanity import (
    # Incomplete: Dexsanity, Dexcountsanity, Seensanity, Seencountsanity, trainersanitybosses,
    # Trainercountsanity, Itemcountsanity, Medalsanity, Medalcountsanity, pokestarstudioschecks,
    # shuffleoverworlditems, shufflenpcgifts, abyssalruins, pokedexchecks, showchecks, Grottosanity
    Trainersanity,
    ShuffleBadgeRewards,
    HiddenItems,
    HabitatListChecks,
)

from .level_cap import (
    # Incomplete: level_cap_type, level_cap_item_value, auto_scale_acquired_pokemon, progressive_level_cap
    # levelcaptype,
    # levelcapitemvalue,
    InfiniteRareCandies,
    # autoscaleacquiredpokemon,
    # progressivelevelcap,
)

from .extra_logic import (
    # Incomplete: fieldrocksmash, hmbadgerequirements, strengthboulders, extracuttrees,
    # randomisestartingtown, startingtownblacklist
    FlashLogic,
    DowsingMachineLogic,
)

from .encounter import (
    RandomiseAbilities,
    RandomiseLevelUpMovesets,
    RandomiseWildPokemon,
    RandomiseTrainerPokemon,
    RandomiseStarterPokemon,
    # Incomplete: randomisestaticpokemon, randomisegiftpokemon, randomisetradepokemon,
    # randomiselegendarypokemon, wildrandomisationblacklist, trainerrandomisationblacklist,
    # weightedbst, adjustlevels, allpokemonseen, modifyitempool, modifylogic, filleritemsblacklist
    CatchRateMultiplier,
)

from .qol import (
    SkipIntro,
    TrainerName,
    SkipIntroGender,
    RivalName,
    InstantText,
    # Incomplete: efficientdialogue
    BlindTrainers,
    # TalkToTrainerWithoutBattling,
    GuaranteedCatch,
    TMHMFullyCompatible,
    BikeEverywhere,
    FastFishing,
    HoldATurbo,
    ExpMultiplier,
    CheckLogFilter,
    RemoveSurfBikeMusic,
    BattleScene,
    BattleStyle,
    AutoRun,
    GuaranteedEscape,
    FastHatch,
    InfiniteRepels,
    SkipPWT,
    SkipJoinAvenue,
    SkipCinematicMovies,
    SkipCatchingTutorial,
    LivingRoomStarter,
    MaxFriendship,
)


class GameVersion(Choice):
    """
    Select your game version.

    - Black 2 - Enforces Pokémon Black 2 logic, encounters, and version specifics.
    - White 2 - Enforces Pokémon White 2 logic, encounters, and version specifics.
    """
    display_name = "Game Version"
    option_black2 = 0
    option_white2 = 1
    default = 0


class Goal(OptionSet):
    """
    Win condition to consider the game beaten. Supports a single goal or a list of multiple goals:
    - champion: Defeat Champion Iris at the Pokémon League
    - legendary_hunt: Clear/encounter a required number of eligible legendary Pokémon locations (configured by legendary_hunt_required and legendary_hunt_allowed)
    - tmhm_hunt: Collect a required number of TMs and HMs (configured by tmhm_hunt)
    - top_trainers: Defeat a required number of eligible top trainers (configured by top_trainers_required and top_trainers_allowed)
    """
    display_name = "Goal"
    valid_keys = [
        "champion",
        "legendary_hunt",
        "tmhm_hunt",
        "top_trainers",
    ]
    default = {"champion"}

    def __init__(self, value: typing.Any = None):
        if isinstance(value, str):
            super().__init__({value.lower()})
        elif isinstance(value, (list, set, tuple)):
            super().__init__({str(v).lower() for v in value})
        else:
            super().__init__(value or self.default)


class TopTrainersRequired(Range):
    """Number of top trainers required to defeat when 'top_trainers' is an active goal (1 to 10)."""
    display_name = "Top Trainers Required"
    range_start = 1
    range_end = 10
    default = 5


class TopTrainersAllowed(OptionSet):
    """Allowed top trainers / superbosses that count towards the 'top_trainers' goal."""
    display_name = "Top Trainers Allowed"
    valid_keys = [
        "ghetsis",
        "cynthia",
        "hugh",
        "alder",
        "gamefreak_morimoto",
        "gamefreak_nishino",
        "n",
        "colress",
        "league_rematch",
        "benga",
    ]
    default = [
        "ghetsis",
        "cynthia",
        "hugh",
        "alder",
        "gamefreak_morimoto",
        "gamefreak_nishino",
        "n",
        "colress",
        "league_rematch",
        "benga",
    ]


class TmhmHuntCount(Range):
    """Number of TMs and HMs required to collect when 'tmhm_hunt' is an active goal (0 to 101; 95 TMs + 6 HMs)."""
    display_name = "TM/HM Hunt Required"
    range_start = 0
    range_end = 101
    default = 60


class LegendaryHuntRequired(Range):
    """Number of legendary encounter locations required to clear when 'legendary_hunt' is an active goal (1 to 13)."""
    display_name = "Legendaries Required"
    range_start = 1
    range_end = 13
    default = 3


class LegendaryHuntAllowed(OptionSet):
    """Allowed legendary encounter locations that count towards the 'legendary_hunt' goal."""
    display_name = "Legendaries Allowed"
    valid_keys = [
        "cobalion",
        "virizion",
        "terrakion",
        "kyurem",
        "zekrom_reshiram",
        "mesprit",
        "azelf",
        "uxie",
        "heatran",
        "cresselia",
        "regirock",
        "registeel_regice",
        "latios_latias",
    ]
    default = [
        "cobalion",
        "virizion",
        "terrakion",
        "kyurem",
        "zekrom_reshiram",
        "mesprit",
        "azelf",
        "uxie",
        "heatran",
        "cresselia",
        "regirock",
        "registeel_regice",
        "latios_latias",
    ]





class ExcludePostgameChecks(Toggle):
    """
    Excludes locations that are logically only accessible after completing the selected goal.
    Automatically enabled when the goal is champion-only: all areas and checks that require
    defeating the Champion (entering the Hall of Fame) will be removed from the location pool.
    """
    display_name = "Exclude Postgame Checks"
    default = True


@dataclass
class PokemonB2W2Options(PerGameCommonOptions):
    """Options container for Pokémon Black 2 and White 2 Archipelago randomizer."""
    # Core game and goal options
    version: GameVersion
    goal: Goal
    exclude_postgame_checks: ExcludePostgameChecks
    top_trainers_required: TopTrainersRequired
    top_trainers_allowed: TopTrainersAllowed
    tmhm_hunt: TmhmHuntCount
    legendary_hunt_required: LegendaryHuntRequired
    legendary_hunt_allowed: LegendaryHuntAllowed

    trainersanity: Trainersanity
    # Incomplete: Dexsanity, trainersanity_bosses, Trainercountsanity, Itemcountsanity, Dexcountsanity,
    # Seensanity, Seencountsanity, Medalsanity, Medalcountsanity, pokestar_studios,
    # shuffle_overworld_items, shuffle_npc_gifts, abyssal_ruins, pokedex_checks, show_checks, Grottosanity
    shuffle_badges: ShuffleBadgeRewards
    hidden_items: HiddenItems
    habitat_list_checks: HabitatListChecks

    # Incomplete: level cap options are disabled until enforcement is implemented
    # level_cap_type: LevelCapType
    # level_cap_item_value: LevelCapItemValue
    # progressive_level_cap: ProgressiveLevelCap
    # auto_scale_acquired_pokemon: AutoScaleAcquiredPokemon

    # Incomplete: field_rock_smash, hm_badge_requirements, strength_boulders, extra_cut_trees,
    # randomise_starting_town, starting_town_blacklist
    flash_logic: FlashLogic
    dowsing_machine_logic: DowsingMachineLogic

    randomise_wild_pokemon: RandomiseWildPokemon
    randomise_trainer_pokemon: RandomiseTrainerPokemon
    randomise_starter_pokemon: RandomiseStarterPokemon
    randomise_abilities: RandomiseAbilities
    randomise_level_up_movesets: RandomiseLevelUpMovesets
    # Incomplete: randomise_static_pokemon, randomise_gift_pokemon, randomise_trade_pokemon,
    # randomise_legendary_pokemon, wild_randomisation_blacklist, trainer_randomisation_blacklist,
    # weighted_bst, adjust_levels, all_pokemon_seen, modify_item_pool, modify_logic, filler_items_blacklist

    skip_intro: SkipIntro
    trainer_name: TrainerName
    skip_intro_gender: SkipIntroGender
    rival_name: RivalName

    # Quality of life — APtransceiver (changeable ingame)
    auto_run: AutoRun
    bike_everywhere: BikeEverywhere
    blind_trainers: BlindTrainers
    # talk_to_trainer_without_battling: TalkToTrainerWithoutBattling
    catch_rate_multiplier: CatchRateMultiplier
    check_log_filter: CheckLogFilter
    exp_multiplier: ExpMultiplier
    fast_fishing: FastFishing
    guaranteed_catch: GuaranteedCatch
    guaranteed_escape: GuaranteedEscape
    hold_a_turbo: HoldATurbo

    # Quality of life — Non-APtransceiver (NOT changeable ingame)
    instant_text: InstantText
    fast_hatch: FastHatch
    infinite_rare_candies: InfiniteRareCandies
    infinite_repels: InfiniteRepels
    tmhm_fully_compatible: TMHMFullyCompatible
    remove_surf_bike_music: RemoveSurfBikeMusic
    max_friendship: MaxFriendship
    battle_scene: BattleScene
    battle_style: BattleStyle
    # efficient_dialogue: EfficientDialogue  # INCOMPLETE

    # Cutscene skips
    living_room_starter: LivingRoomStarter
    skip_pwt: SkipPWT
    skip_catching_tutorial: SkipCatchingTutorial
    skip_join_avenue: SkipJoinAvenue
    skip_cinematic_movies: SkipCinematicMovies
    start_inventory_from_pool: StartInventoryPool


# WebHost RestrictedUnpickler requires Option __module__ to end with "options"
from Options import Option as _AP_Option

for _name, _obj in list(locals().items()):
    if isinstance(_obj, type) and issubclass(_obj, _AP_Option) and not _name.startswith("_"):
        if getattr(_obj, "__module__", "").startswith("worlds.pokemon_b2w2"):
            _obj.__module__ = __name__
