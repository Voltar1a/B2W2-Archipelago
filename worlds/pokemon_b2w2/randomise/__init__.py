from __future__ import annotations

import random
from typing import Any
try:
    from ..nds_compat import NintendoDSRom
except (ImportError, ValueError):
    from nds_compat import NintendoDSRom
from .stats import randomise_abilities, randomise_level_up_movesets
from .pokemon import (
    ensure_early_damaging_moves,
    randomise_starters,
    randomise_wild_pokemon,
    randomise_trainer_pokemon,
)
try:
    from ..patch.habitat import update_pokedex_habitats
except (ImportError, ValueError):
    from patch.habitat import update_pokedex_habitats


def apply_randomisation(
    rom: NintendoDSRom,
    options: dict[str, Any],
    is_white2: bool = False,
    seed: int = 0,
) -> None:
    rng = random.Random(seed)

    starters = randomise_starters(rom, options, rng)

    randomise_wild_pokemon(rom, options, rng)
    update_pokedex_habitats(rom)

    randomise_trainer_pokemon(rom, options, rng, starters=starters)

    randomise_abilities(rom, options, rng)
    randomise_level_up_movesets(rom, options, rng)

    ensure_early_damaging_moves(rom, starters)
