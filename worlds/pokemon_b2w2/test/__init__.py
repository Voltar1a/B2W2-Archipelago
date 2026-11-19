import random
import time
from typing import Iterable, Callable, Type, Any, TYPE_CHECKING

from Options import OptionError
from test.bases import WorldTestBase

if TYPE_CHECKING:
    from .. import PokemonB2W2World


class PokemonB2W2TestBase(WorldTestBase):
    game = "Pokemon Black 2 and White 2"
    world: "PokemonB2W2World"


class ModifierTest(Callable):
    modifier: str
    option: str

    def __call__(self, *args, **kwargs): ...


def requires_modifier(modifier: str, option: str) -> Callable:
    def decorator(c: Callable) -> Callable:
        c.modifier = modifier
        c.option = option
        return c
    return decorator


def multiply_random_combinations(option: str, mods: tuple, count: int, additional: dict[str, Any] = None) -> Callable:
    combs = tuple(random_combination(mods) for _ in range(count))
    additional = additional or {}

    def decorator(cls: Type[WorldTestBase]) -> type:
        def create_test(index: int) -> Callable:
            def _test(self: cls):
                self.options = {option: combs[index]} | additional
                print("Modifiers: " + ", ".join(self.options[option]))
                all_members = tuple(WorldTestBase.__dict__.items()) + tuple(cls.__dict__.items())
                try:
                    for name, value in all_members:
                        if not (isinstance(value, Callable) and name.startswith(("test_", "mod_"))
                                and not name.startswith("test_combination")):
                            continue
                        with self.subTest("World setup", game=self.game):
                            start_time = time.time()
                            self.world_setup()
                            print(f"...took {time.time() - start_time} seconds to generate")
                        name: str
                        value: ModifierTest
                        if name[:5] == "test_" and not name.startswith("test_combination"):
                            with self.subTest(name, game=self.game, seed=self.multiworld.seed):
                                value(self)
                        if name[:4] == "mod_" and value.modifier in self.options[value.option]:
                            with self.subTest(f"Testing {value.modifier}", game=self.game, seed=self.multiworld.seed):
                                value(self)
                except OptionError as err:
                    print("Skipped as a result of an OptionError:\n" + '\n'.join(err.args))

            return _test

        cls.auto_construct = False
        for i in range(count):
            setattr(cls, f"test_combination_{i}", create_test(i))
        return cls

    return decorator


def random_combination(mods: Iterable[str]) -> list[str]:
    ret = []
    for i in mods:
        if random.random() < 0.5:
            ret.append(i)
    return ret

