from . import multiply_random_combinations, PokemonB2W2TestBase
from ..options import RandomiseWildPokemon, RandomiseTrainerPokemon, RandomiseStarterPokemon


class TestRandomiseWildPokemonSimple(PokemonB2W2TestBase):
    options = {"randomise_wild_pokemon": ["Randomise"]}
@multiply_random_combinations("randomise_wild_pokemon", tuple(RandomiseWildPokemon.valid_keys), 11)
class TestRandomiseWildPokemon(PokemonB2W2TestBase):
    pass


class TestRandomiseTrainerPokemonSimple(PokemonB2W2TestBase):
    options = {"randomise_trainer_pokemon": ["Randomise"]}
@multiply_random_combinations("randomise_trainer_pokemon", tuple(RandomiseTrainerPokemon.valid_keys), 10)
class TestRandomiseTrainerPokemon(PokemonB2W2TestBase):
    pass


class TestRandomiseStarterSimple(PokemonB2W2TestBase):
    options = {"randomise_starter_pokemon": ["Randomise"]}
@multiply_random_combinations("randomise_starter_pokemon", tuple(RandomiseStarterPokemon.valid_keys), 7)
class TestRandomiseStarter(PokemonB2W2TestBase):
    pass


# class TestRandomiseStaticsSimple(PokemonB2W2TestBase):
#     Options = {"randomise_static_pokemon": ["Randomise"]}
# @multiply_random_combinations("randomise_static_pokemon", tuple(randomisestaticpokemon.valid_keys), 5)
# class TestRandomiseStatics(PokemonB2W2TestBase):
#     pass
#
#
# class TestRandomiseGiftSimple(PokemonB2W2TestBase):
#     Options = {"randomise_gift_pokemon": ["Randomise"]}
# @multiply_random_combinations("randomise_gift_pokemon", tuple(randomisegiftpokemon.valid_keys), 5)
# class TestRandomiseGift(PokemonB2W2TestBase):
#     pass
#
#
# class TestRandomiseLegendariesSimple(PokemonB2W2TestBase):
#     Options = {"randomise_legendary_pokemon": ["Randomise"]}
# @multiply_random_combinations("randomise_legendary_pokemon", tuple(randomiselegendarypokemon.valid_keys), 5)
# class TestRandomiseLegendaries(PokemonB2W2TestBase):
#     pass

