from . import PokemonB2W2TestBase, multiply_random_combinations
from ..options import Goal


###################################################
# Goal                                            #
###################################################


class TestGoalChampion(PokemonB2W2TestBase):
    options = {"goal": "champion"}
class TestGoalTopTrainers(PokemonB2W2TestBase):
    options = {"goal": "top_trainers"}
class TestGoalTMHMHunt(PokemonB2W2TestBase):
    options = {"goal": "tmhm_hunt"}
class TestGoalLegendaryHunt(PokemonB2W2TestBase):
    options = {"goal": "legendary_hunt"}
@multiply_random_combinations("goal", tuple(Goal.valid_keys), 8)
class TestCombinedGoals(PokemonB2W2TestBase):
    pass

###################################################
# Shuffle Badges                                  #
###################################################

class TestShuffleBadgesFalse(PokemonB2W2TestBase):
    options = {"shuffle_badges": False}
class TestShuffleBadgesTrue(PokemonB2W2TestBase):
    options = {"shuffle_badges": True}


# class TestModifyItemPoolAll(PokemonB2W2TestBase):
#     Options = {"modify_item_pool": ["Useless key items", "Useful filler", "Ban bad filler"]}
#
# class TestModifyLogicNone(PokemonB2W2TestBase):
#     Options = {"modify_logic": []}
# class TestModifyLogicAll(PokemonB2W2TestBase):
#     Options = {"modify_logic": ["Require Dowsing Machine", "Require flash", "Consider evolutions",
#                                 "Consider static pokemon", "Consider trades", "Consider form change"]}
#
# class TestAdjustLevelsNone(PokemonB2W2TestBase):
#     Options = {"adjust_levels": []}
# class TestAdjustLevelsAll(PokemonB2W2TestBase):
#     Options = {"adjust_levels": ["Trainer by distance", "Wild by distance", "Trainer by sphere", "Wild by sphere"]}
# class TestAdjustLevelsOnlySphere(PokemonB2W2TestBase):
#     Options = {"adjust_levels": ["Trainer by sphere", "Wild by sphere"]}


###################################################
# All Pokémon seen                                #
###################################################


# Incomplete: allpokemonseen is not yet implemented
# class TestAllPokemonSeenTrue(PokemonB2W2TestBase):
#     Options = {"all_pokemon_seen": True}