from __future__ import annotations

from Options import OptionGroup

from . import (
    # core game
    GameVersion,
    Goal,
    ExcludePostgameChecks,
    TopTrainersRequired,
    TopTrainersAllowed,
    TmhmHuntCount,
    LegendaryHuntRequired,
    LegendaryHuntAllowed,

    # sanity & logic
    ShuffleBadgeRewards,
    HiddenItems,
    HabitatListChecks,
    Trainersanity,
    FlashLogic,
    DowsingMachineLogic,

    # encounters & randomisation
    RandomiseStarterPokemon,
    RandomiseWildPokemon,
    RandomiseTrainerPokemon,
    RandomiseAbilities,
    RandomiseLevelUpMovesets,

    # character & intro customisation
    TrainerName,
    RivalName,
    SkipIntro,
    SkipIntroGender,

    # qol
    InstantText,
    AutoRun,
    BikeEverywhere,
    GuaranteedCatch,
    CatchRateMultiplier,
    ExpMultiplier,
    HoldATurbo,
    CheckLogFilter,
    GuaranteedEscape,
    FastHatch,
    FastFishing,
    InfiniteRareCandies,
    InfiniteRepels,
    BlindTrainers,
    # TalkToTrainerWithoutBattling,
    TMHMFullyCompatible,
    RemoveSurfBikeMusic,
    MaxFriendship,
    BattleScene,
    BattleStyle,

    # Cutscene skips
    LivingRoomStarter,
    SkipPWT,
    SkipCatchingTutorial,
    SkipJoinAvenue,
    SkipCinematicMovies,
)

option_groups: list[OptionGroup] = [
    OptionGroup("Goal and game version", [
        GameVersion,
        Goal,
        ExcludePostgameChecks,
        TopTrainersRequired,
        TopTrainersAllowed,
        TmhmHuntCount,
        LegendaryHuntRequired,
        LegendaryHuntAllowed,
    ]),
    OptionGroup("Location checks and logic", [
        ShuffleBadgeRewards,
        HiddenItems,
        HabitatListChecks,
        Trainersanity,
        FlashLogic,
        DowsingMachineLogic,
    ]),
    OptionGroup("Pokémon and encounter randomisation", [
        RandomiseStarterPokemon,
        RandomiseWildPokemon,
        RandomiseTrainerPokemon,
        RandomiseAbilities,
        RandomiseLevelUpMovesets,
    ]),
    OptionGroup("Character and intro customisation", [
        TrainerName,
        RivalName,
        SkipIntro,
        SkipIntroGender,
    ]),
    OptionGroup("Quality of life and engine patches", [
        # APtransceiver (changeable ingame)
        AutoRun,
        BikeEverywhere,
        BlindTrainers,
        # TalkToTrainerWithoutBattling,
        CatchRateMultiplier,
        CheckLogFilter,
        ExpMultiplier,
        FastFishing,
        GuaranteedCatch,
        GuaranteedEscape,
        HoldATurbo,
        # Non-APtransceiver (not changeable ingame)
        InstantText,
        FastHatch,
        InfiniteRareCandies,
        InfiniteRepels,
        TMHMFullyCompatible,
        RemoveSurfBikeMusic,
        MaxFriendship,
        BattleScene,
        BattleStyle,
    ]),
    OptionGroup("Cutscene skips", [
        LivingRoomStarter,
        SkipPWT,
        SkipCatchingTutorial,
        SkipJoinAvenue,
        SkipCinematicMovies,
    ]),
]
