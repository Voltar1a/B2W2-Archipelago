from . import PokemonB2W2TestBase


###################################################
# Dexsanity                                       #
###################################################


# class TestDexsanityPartial(PokemonB2W2TestBase):
#     Options = {"dexsanity": 100}
# class TestDexsanityFull(PokemonB2W2TestBase):
#     Options = {
#         "dexsanity": 649,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexsanityPlandoVanilla(PokemonB2W2TestBase):
#     Options = {
#         "dexsanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#     }
# class TestDexsanityPlandoRandomised(PokemonB2W2TestBase):
#     Options = {
#         "dexsanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexsanityPlandoAllObtainable(PokemonB2W2TestBase):
#     Options = {
#         "dexsanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#         "randomise_wild_pokemon": ["Randomise"],
#     }


###################################################
# Dexcountsanity                                  #
###################################################


# class TestDexcountsanityPartialVanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 100}}
# class TestDexcountsanityPartialRando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityPartialEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityFullVanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 649}}
# class TestDexcountsanityFullRando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityFullEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityPartial10StepsVanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 100, "Steps": 10}}
# class TestDexcountsanityPartial10StepsRando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Steps": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityPartial10StepsEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Steps": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityFull10StepsVanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 649, "Steps": 10}}
# class TestDexcountsanityFull10StepsRando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Steps": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityFull10StepsEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Steps": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityPartialLeniency10Vanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 100, "Leniency": 10}}
# class TestDexcountsanityPartialLeniency10Rando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Leniency": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityPartialLeniency10EnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Leniency": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityFullLeniency10Vanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 649, "Leniency": 10}}
# class TestDexcountsanityFullLeniency10Rando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Leniency": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityFullLeniency10EnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Leniency": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityPartial10StepsLeniency10Vanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10}}
# class TestDexcountsanityPartial10StepsLeniency10Rando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityPartial10StepsLeniency10EnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestDexcountsanityFull10StepsLeniency10Vanilla(PokemonB2W2TestBase):
#     Options = {"dexcountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10}}
# class TestDexcountsanityFull10StepsLeniency10Rando(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10},
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestDexcountsanityFull10StepsLeniency10EnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "dexcountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10},
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }


###################################################
# Seensanity                                      #
###################################################


# class TestSeensanityPartialVanilla(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 100,
#         "all_pokemon_seen": True,
#     }
# class TestSeensanityPartialRando(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 100,
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestSeensanityPartialEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 100,
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestSeensanityFullVanilla(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 649,
#         "all_pokemon_seen": True,
#     }
# class TestSeensanityFullRando(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 649,
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestSeensanityFullEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": 649,
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestSeensanityPlandoVanilla(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#         "all_pokemon_seen": True,
#     }
# class TestSeensanityPlandoRando(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestSeensanityPlandoEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "seensanity": [random.randint(1, 649) for _ in range(98)] + ["10-20", "450-500"],
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }


###################################################
# Seencountsanity                                 #
###################################################


# class TestSeencountsanityPartialVanilla(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#     }
# class TestSeencountsanityPartialRando(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestSeencountsanityPartialEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 100, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }
# class TestSeencountsanityFullVanilla(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#     }
# class TestSeencountsanityFullRando(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Randomise"],
#     }
# class TestSeencountsanityFullEnsureAll(PokemonB2W2TestBase):
#     Options = {
#         "seencountsanity": {"Maximum": 649, "Steps": 10, "Leniency": 10},
#         "all_pokemon_seen": True,
#         "randomise_wild_pokemon": ["Ensure all obtainable"],
#     }


###################################################
# Trainersanity                                   #
###################################################


class TestTrainersanityVanilla(PokemonB2W2TestBase):
    options = {"trainersanity": True}


class TestTrainersanityWithRandomWild(PokemonB2W2TestBase):
    options = {
        "trainersanity": True,
        "randomise_wild_pokemon": ["Randomise"],
    }


###################################################
# Trainercountsanity                              #
###################################################


# class TestTrainercountsanityPartial(PokemonB2W2TestBase):
#     Options = {"trainercountsanity": {"Maximum": 50, "Steps": 5, "Leniency": 2}}


# class TestTrainercountsanityFull(PokemonB2W2TestBase):
#     Options = {"trainercountsanity": {"Maximum": 300, "Steps": 10, "Leniency": 10}}


# class TestProgressiveLevelCapStandard(PokemonB2W2TestBase):
#     Options = {
#         "progressive_level_cap": "standard",
#         "infinite_rare_candies": True,
#     }
#
#
# class TestProgressiveLevelCapHard(PokemonB2W2TestBase):
#     Options = {
#         "progressive_level_cap": "hard",
#         "infinite_rare_candies": True,
#     }
