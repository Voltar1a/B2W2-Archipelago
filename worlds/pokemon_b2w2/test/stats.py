from . import multiply_random_combinations, PokemonB2W2TestBase, requires_modifier
from ..options import RandomiseLevelUpMovesets


class TestRandomiseLevelupMovesSimple(PokemonB2W2TestBase):
    options = {"randomise_level_up_movesets": ["Randomise"]}


@multiply_random_combinations("randomise_level_up_movesets", tuple(RandomiseLevelUpMovesets.valid_keys), 7)
class TestRandomiseLevelupMoves(PokemonB2W2TestBase):

    @requires_modifier("Keep levels and amount", "randomise_level_up_movesets")
    def mod_keep_levels_amount(self):
        from ..data.pokemon.movesets_level_up import table

        correct_amounts = 0
        correct_levels = 0
        last_bad: tuple = None, None
        for name, data in self.world.catchable_species_data.items():
            if len(data.level_up_moves.level_up_moves) == len(table[name].level_up_moves):
                correct_amounts += 1
            else:
                last_bad = name, data
            levels = set(slot[0] for slot in table[name].level_up_moves)
            for slot in data.level_up_moves.level_up_moves:
                if slot[0] not in levels:
                    last_bad = name, data
                    break
            else:
                correct_levels += 1
        c_amount = correct_amounts / len(table)
        c_levels = correct_levels / len(table)
        if c_amount >= 0.9 <= c_levels:
            print(f"Keep levels and amount modifier passed with "
                  f"{c_amount * 100}% correct move counts and {c_levels * 100}% correct levels")
        else:
            self.fail(f"Keep levels and amount modifier failed with "
                      f"{c_amount * 100}% correct move counts and {c_levels * 100}% correct levels.\n"
                      f"Last bad species:\n"
                      f"Original moveset: {table[last_bad[0]].level_up_moves}\n"
                      f"Randomised moveset: {last_bad[1].level_up_moves.level_up_moves}")
