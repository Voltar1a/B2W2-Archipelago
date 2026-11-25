from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable
from BaseClasses import Region

from .roadblocks import (
    has_basic_badge,
    has_toxic_badge,
    has_insect_badge,
    has_bolt_badge,
    has_quake_badge,
    has_jet_badge,
    has_legend_badge,
    has_wave_badge,
    has_all_badges,
    badge_count,
    has_badge_count,
    can_use_cut,
    can_use_fly,
    can_use_surf,
    can_use_strength,
    can_use_waterfall,
    can_use_dive,
    can_use_flash,
    has_dowsing_machine,
    has_bicycle,
    has_super_rod,
    has_colress_mchn,
    has_plasma_card,
    has_dna_splicers,
    has_card_key,
    can_enter_giant_chasm,
    can_access_black_tower,
    can_access_white_treehollow,
    can_battle_benga,
    can_travel_by_ship,
    can_travel_by_plane,
    can_access_top_trainer,
    can_access_legendary_location,
    check_goal_completion,
    can_enter_hall_of_fame,
)
from .location_rules import LOCATION_RULES
from .unova import (
    ConnectionInfo,
    REGION_LIST,
    REGION_CONNECTIONS,
    infer_region_from_name,
)

if TYPE_CHECKING:
    from .. import PokemonB2W2World


# Version-exclusive locations
BLACK2_EXCLUSIVE_LOCATIONS: frozenset[str] = frozenset({
    "Route 4 - Near sign in the west",
    "Route 4 - Hill on western side",
    "Route 4 - South of Roughnecks in the west",
    "Route 4 - 2F of second house on right",
    "Route 4 - Ace Trainer in first house on right",
    "Route 4 - Black Belt in 2F of first left house",
    "Route 4 - Maid in third house on right (Guess Pokémon cry)",
    "Route 4 - Fisherman Hubert by water in southwest top",
    "Route 4 - Breeder Irene by Castelia Gate",
    "Route 4 - Hidden western area between stairways southeast of rest house",
    "Route 4 - Hidden in deep sand between two stairways south of Policeman",
    "Route 4 - Hidden deep sand north of fences east of the Roughnecks",
    "Route 4 - Hidden in the middle of a deep sand patch in the west",
    "Route 4 - Hidden western area west of Bikers in deep sand next to barricade",
    "Route 4 - Policeman Braven in south near Castelia Gate",
    "Route 4 - Policeman Dell in north near Nimbasa Gate",
    "Route 4 - Policeman Neagle south of rest house on western side",
    "Route 4 - Roughneck Joey in the west south of the stairs",
    "Route 4 - Roughneck Silvester in northwest fenced area",
    "Route 4 - Biker Stanley in the west",
    "Route 4 - Hooligans Rob & Sal by the south fence in the west",
    "Route 4 - Youngster Sinclair in the west",
    "Reversal Mountain 1F - dead-end tunnel north of Battle Girl",
    "Reversal Mountain 1F - dead-end tunnel east of Doctor in south of main cavern",
    "Reversal Mountain 1F - south of Hiker in north of main cavern",
    "Reversal Mountain 1F - east of Black Belt in west of main cavern",
    "Reversal Mountain 1F - dead-end tunnel east of Backpacker and Hiker in southwest of main cavern",
    "Reversal Mountain B1F - next to the Ranger",
    "Reversal Mountain B1F - Hidden in the stalagmite below the stairs",
    "Reversal Mountain 1F - Hidden in the stalagmite north of Backpacker and Hiker in the west",
    "Reversal Mountain 1F - Hidden in stalagmite south of Scientist in east of main cavern",
    "Reversal Mountain 1F - Hidden in stalagmite in the southeast of main cavern",
    "Reversal Mountain 1F - Hidden dead end south of Ace Trainers in north of main cavern",
    "Reversal Mountain 1F - Hidden dead-end tunnel east of Backpacker and Hiker in south",
    "Reversal Mountain 1F - Backpacker Kiyo in southwest of main cavern",
    "Reversal Mountain 1F - Backpacker Kumiko in north of main cavern",
    "Reversal Mountain - Ranger Lewis B1F to the left",
    "Reversal Mountain - Gift from beating Ranger Lewis B1F to the left",
    "Reversal Mountain - Ranger Eliza 1F in south of the main cavern",
    "Reversal Mountain - Gift from beating Ranger Eliza 1F in south of the main cavern",
    "Reversal Mountain 1F - Ace Trainer Ray in north of main cavern",
    "Reversal Mountain 1F - Ace Trainer Cora in north of main cavern",
    "Reversal Mountain 1F - Hiker Jared in north of main cavern",
    "Reversal Mountain 1F - Hiker Markus in southwest of main cavern",
    "Reversal Mountain 1F - Black Belt Corey in the west of the main cavern",
    "Reversal Mountain 1F - Battle Girl Chan in south of main cavern",
    "Reversal Mountain 1F - Doctor Derek by stairs to B1F in south of main cavern",
    "Plasma Frigate - Near Grunt in southwest of beam puzzle room left ball",
    "Plasma Frigate - Near Grunt in southwest of beam puzzle room right ball",
    "Plasma Frigate - Right of beam puzzle pit",
    "Plasma Frigate - In the northeast room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt by teleporter in southwestern room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt by teleporter in northwest room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt between beds in northwest room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt next to teleporter in centre east room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt between beds in centre east room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt between beds in southwestern room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt southeastern room (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt patrolling western side (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt patrolling eastern side (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt in northeast of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt in southwest of beam puzzle room near two item balls (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt in southeast of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Doctor Julius in southeast of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt northwest of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt northwest of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt northeast of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt in southeast of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt southeast of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt north of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Gift from Team Plasma Password Grunt north of beam puzzle pit (from Giant Chasm)",
    "Mistralton City - South of runway between greenhouses",
    'Victory Road - Section 3: Cave, Gift from beating Ranger Eddie accessed from southeast of League gate',
    'Victory Road - Section 3: Cave, Gift from beating Ranger Elle northwest lower',
    'Victory Road - Section 2: Black Bridge, northwest',
    'Victory Road - Section 4: Mountain, outside Flash cave',
    'Victory Road - Section 2: Black Bridge, southwest',
    'Victory Road - Section 3: Cave, north in Flash section',
    'Victory Road - Bonus: Grove, southwestern corner',
    'Victory Road - Bonus: Grove, northeastern corner',
    'Victory Road - Bonus: White Bridge, southeast of cave entrance',
    'Victory Road - Section 2: Black Bridge, southeast',
    'Victory Road - Section 4: Mountain, far southeast of League exit',
    'Victory Road - Section 3: Cave, southeast across pond in Flash section',
    'Victory Road - Section 4: Mountain, up second set of stairs north in southwest',
    'Victory Road - Hidden section 3: Cave, south in Flash section',
    'Victory Road - Hidden section 3: Cave, east across pond in Flash section',
    'Victory Road - Hidden section 4: Mountain, southwest halfway up stairs east of Battle Girl',
    'Victory Road - Hidden section 4: Mountain, southeast of League gate in rock',
    'Victory Road - Hidden section 3: Cave, southeast',
    'Victory Road - Hidden section 3: Cave, in rock in southwest',
    'Victory Road - Section 1: Ruins, Ace Trainer Billy in southeast',
    'Victory Road - Section 1: Ruins, Psychic Alia in north',
    'Victory Road - Section 2: Black Bridge, Ace Trainer Beckett north',
    'Victory Road - Section 2: Black Bridge, Ace Trainer Shelly centre',
    'Victory Road - Section 2: Black Bridge, Veteran Cathy southwest',
    'Victory Road - Section 2: Black Bridge, Doctor Logan northwest',
    'Victory Road - Section 3: Cave, Ace Trainer Webster in southeast',
    'Victory Road - Section 3: Cave, Ace Trainer Shanta in southeast',
    'Victory Road - Section 4: Mountain, Veteran Sterling outside League gate atop stairs',
    'Victory Road - Section 4: Mountain, Veteran Portia outside League gate below stairs',
    'Victory Road - Section 4: Mountain, Ace Trainer Caroll down stairs southeast of League gate',
    'Victory Road - Section 4: Mountain, Black Belt Martell down stairs far southeast of League gate',
    'Victory Road - Section 4: Mountain, Ace Trainer Elmer southwest up stairs',
    'Victory Road - Section 4: Mountain, Battle Girl Chalina halfway up stairs in southwest',
    'Victory Road - Bonus: White Bridge, Ace Trainer Pierce by water',
    'Victory Road - Bonus: Grove, Ace Trainer Chandra north',
    'Victory Road - Section 3: Cave, Veteran Abraham southwest',
    'Victory Road - Section 1 via Grove, Ace Trainer Jamie centre',
    'Victory Road - Section 1 via Grove, Psychic Al south',
    'Victory Road - Section 3: Cave, Ranger Eddie accessed from southeast of League gate',
    'Victory Road - Section 3: Cave, Ranger Elle northwest lower',
})

WHITE2_EXCLUSIVE_LOCATIONS: frozenset[str] = frozenset({
    "Route 4 - Between two houses in central ruins",
    "Route 4 - Northwest ruins",
    "Route 4 - Hidden behind Pokéfan in northeast of ruins",
    "Route 4 - Inside Cottonee trade house",
    "Route 4 - Ace Trainer in first house east of ruins crossroads",
    "Route 4 - Black Belt in house in the far southeast of ruins",
    "Route 4 - Maid in southwest house (Guess Pokémon cry)",
    "Route 4 - Fisherman Hubert at south water top",
    "Route 4 - Breeder Irene along road in the south",
    "Route 4 - Hidden in deep sand in southwest of ruins",
    "Route 4 - Hidden northwest of crossroads along ruins road",
    "Route 4 - Hidden far east deep sand in ruins",
    "Route 4 - Hidden southeast of ruins between two houses",
    "Route 4 - Hidden west of Pokéfan in east of ruins",
    "Route 4 - Rich Boy Keenan along ruins road to the west",
    "Route 4 - Backpacker Roland along road north of ruins",
    "Route 4 - Backpacker Rachel east along ruins road",
    "Route 4 - Pokéfan Norbert in far southeast of ruins",
    "Route 4 - Pokéfan Sachiko in northeast ruins",
    "Route 4 - Twins Tara & Val at start of ruins road",
    "Route 4 - Backpacker Clifford in southeast on road",
    "Route 4 - Lady Lina in central ruins",
    "Reversal Mountain 1F - above Hiker in the southeast",
    "Reversal Mountain 1F - in the west southeast of male Backpacker and Hiker",
    "Reversal Mountain 1F - northwest of Black Belt southwest of Ace Trainers",
    "Reversal Mountain 1F - south of Scientist in northeast",
    "Reversal Mountain 1F - in the west east of the entrance",
    "Reversal Mountain B1F - near the entrance to 1F",
    "Reversal Mountain B1F - Hidden in a rock near the big rock",
    "Reversal Mountain - Hidden rock centre-east by B1F stairs",
    "Reversal Mountain 1F - Hidden north in southern dead end west of Ace Trainers, in a rock",
    "Reversal Mountain - Hidden north in rock west of Ace Trainers",
    "Reversal Mountain - Hidden in central west, northeast of Battle Girl",
    "Reversal Mountain 1F - Hidden far southeast in a rock",
    "Reversal Mountain 1F - Backpacker Kiyo in west",
    "Reversal Mountain 1F - Backpacker Kumiko southeast",
    "Reversal Mountain 1F - Ranger Lewis in the southwest",
    "Reversal Mountain 1F - Gift from beating Ranger Lewis in the southwest",
    "Reversal Mountain B1F - Ranger Eliza in the northwest",
    "Reversal Mountain B1F - Gift from beating Ranger Eliza in the northwest",
    "Reversal Mountain 1F - Ace Trainer Ray in north",
    "Reversal Mountain 1F - Ace Trainer Cora in north",
    "Reversal Mountain 1F - Hiker Jared southeast",
    "Reversal Mountain 1F - Hiker Markus in west",
    "Reversal Mountain 1F - Black Belt Corey centre east",
    "Reversal Mountain 1F - Battle Girl Chan central west",
    "Reversal Mountain 1F - Doctor Derek in south",
    "Plasma Frigate - Near Grunt in southeast of beam puzzle room right ball",
    "Plasma Frigate - Near Grunt in southeast of beam puzzle room left ball",
    "Plasma Frigate B1F - left big room (from Route 21)",
    "Plasma Frigate B2F - in the yellow warp panel to left of the puzzle pit",
    "Plasma Frigate - Team Plasma Grunt patrolling on right (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt patrolling on left (from Route 21)",
    "Plasma Frigate - Team Plasma Grunt northwest of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt northeast of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt top left of puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt northeast of beam puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt centre left of puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt in southwest of beam puzzle room near Doctor (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt in southeast of beam puzzle room near two item balls (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Grunt centre right of puzzle pit (from Giant Chasm)",
    "Plasma Frigate - Doctor Julius in southwest of beam puzzle room (from Giant Chasm)",
    "Plasma Frigate - Team Plasma Password Grunt in bottom right room between beds (from Route 21)",
    "Plasma Frigate - Team Plasma Password Grunt at bottom of left big room (from Route 21)",
    "Plasma Frigate - Team Plasma Password Grunt in top left room (from Route 21)",
    "Plasma Frigate - Team Plasma Password Grunt on right of bottom right room (from Route 21)",
    "Plasma Frigate - Team Plasma Password Grunt in top right room (from Route 21)",
    "Plasma Frigate - Team Plasma Password Grunt in left big room middle (from Route 21)",
    "Plasma Frigate - Gift from Team Plasma Password Grunt in left big room middle (from Route 21)",
    "Mistralton City - South of runway between fields",
    'Victory Road - Section 4: Cave, Gift from beating Ranger Eddie accessed from southeast of League gate',
    'Victory Road - Section 4: Cave, Gift from beating Ranger Elle northwest lower',
    'Victory Road - Bonus: Black Bridge, east of entrance',
    'Victory Road - Section 5: Mountain, outside Flash cave',
    'Victory Road - Bonus: Black Bridge, near Ace Trainer by water',
    'Victory Road - Section 4: Cave, north in Flash section',
    'Victory Road - Section 2: Grove, southwestern corner',
    'Victory Road - Section 2: Grove, northeastern corner',
    'Victory Road - Section 3: White Bridge, southeast of cave entrance',
    'Victory Road - Bonus: Black Bridge, across water in southeast',
    'Victory Road - Section 5: Mountain, far southeast of League exit',
    'Victory Road - Section 4: Cave, southeast across pond in Flash section',
    'Victory Road - Section 5: Mountain, up second set of stairs north in southwest',
    'Victory Road - Hidden section 4: Cave, south in Flash section',
    'Victory Road - Hidden section 4: Cave, east across pond in Flash section',
    'Victory Road - Hidden section 5: Mountain, southwest halfway up stairs east of Battle Girl',
    'Victory Road - Hidden section 5: Mountain, southeast of League gate in rock',
    'Victory Road - Hidden section 4: Cave, southeast',
    'Victory Road - Hidden section 4: Cave, in rock in southwest',
    'Victory Road - Section 1, Ace Trainer Jamie centre',
    'Victory Road - Section 1, Psychic Al northwest',
    'Victory Road - Section 1 via Black Bridge, Ace Trainer Billy past Strength boulder',
    'Victory Road - Bonus: Black Bridge, Psychic Alia north',
    'Victory Road - Section 2: Grove, Ace Trainer Beckett north',
    'Victory Road - Section 2: Grove, Ace Trainer Shelly south',
    'Victory Road - Section 3: White Bridge, Veteran Cathy by entrance',
    'Victory Road - Section 3: White Bridge, Doctor Logan north',
    'Victory Road - Section 4: Cave, Ace Trainer Webster in southeast',
    'Victory Road - Section 4: Cave, Ace Trainer Shanta in southeast',
    'Victory Road - Section 5: Mountain, Veteran Sterling outside League gate atop stairs',
    'Victory Road - Section 5: Mountain, Veteran Portia outside League gate below stairs',
    'Victory Road - Section 5: Mountain, Ace Trainer Caroll down stairs southeast of League gate',
    'Victory Road - Section 5: Mountain, Black Belt Martell down stairs far southeast of League gate',
    'Victory Road - Section 5: Mountain, Ace Trainer Elmer southwest up stairs',
    'Victory Road - Section 5: Mountain, Battle Girl Chalina halfway up stairs in southwest',
    'Victory Road - Bonus: Black Bridge, Ace Trainer Pierce by water',
    'Victory Road - Bonus: Black Bridge, Ace Trainer Chandra across water in southeast',
    'Victory Road - Section 4: Cave, Veteran Abraham southwest',
    'Victory Road - Section 4: Cave, Ranger Eddie accessed from southeast of League gate',
    'Victory Road - Section 4: Cave, Ranger Elle northwest lower',
})

_RULE_PARAM_COUNTS: dict[Any, int] = {}

HABITAT_LIST_LOCATIONS: frozenset[str] = frozenset({
    "Pinwheel Forest - Inside: Scientist after Habitat List south",
    "Route 3 - School Kid after Habitat List in the north",
    "Virbank Complex - Girl at southernmost end after filling Habitat List",
    "Reversal Mountain - Scientist after Habitat List in northeast of main cavern",
})


def create_regions_and_locations(world: "PokemonB2W2World") -> dict[str, Region]:
    from ..locations import (
        PokemonB2W2Location,
        BASE_LOCATION_TABLE,
        TRAINER_LOCATION_TABLE,
        SANITY_LOCATION_TABLE,
    )
    from ..locations.items import HIDDEN_ITEM_LOCATIONS
    from itertools import chain

    v_opt = getattr(world.options, "version", None)
    v_key = v_opt.current_key if v_opt is not None else "black2"
    player = world.player

    regions: dict[str, Region] = {
        name: Region(name, player, world.multiworld)
        for name in REGION_LIST
    }

    # Connect regions
    for conn in REGION_CONNECTIONS:
        src = regions[conn.source]
        dst = regions[conn.destination]
        conn_name = conn.name or f"{conn.source} -> {conn.destination}"
        if conn.rule is not None:
            rule_fn = conn.rule
            param_count = _RULE_PARAM_COUNTS.get(rule_fn)
            if param_count is None:
                param_count = len(inspect.signature(rule_fn).parameters)
                _RULE_PARAM_COUNTS[rule_fn] = param_count
            if param_count >= 3:
                src.connect(dst, conn_name, lambda state, fn=rule_fn, p=player, w=world: fn(state, p, w))
            else:
                src.connect(dst, conn_name, lambda state, fn=rule_fn, p=player: fn(state, p))
        else:
            src.connect(dst, conn_name)

    world.multiworld.regions.extend(regions.values())

    dowsing_opt = getattr(world.options, "dowsing_machine_logic", None)
    dowsing_required = dowsing_opt is None or int(getattr(dowsing_opt, "value", dowsing_opt)) != 2
    rule_cache: dict[str, Callable[[Any], bool] | None] = {}

    def make_access_rule(loc_name: str, base_rule):
        if loc_name in rule_cache:
            return rule_cache[loc_name]
        tags = []
        if base_rule is not None:
            tags.append(base_rule)
        if dowsing_required and loc_name in HIDDEN_ITEM_LOCATIONS:
            tags.append(lambda state, p: state.has("Dowsing Machine", p))
        if loc_name in LOCATION_RULES:
            rule_cb = LOCATION_RULES[loc_name]
            tags.append(lambda state, p, cb=rule_cb, w=world: cb(state, p, w))
        if not tags:
            compiled = None
        elif len(tags) == 1:
            t0 = tags[0]
            compiled = lambda state, fn0=t0, p=player: fn0(state, p)
        elif len(tags) == 2:
            t0, t1 = tags
            compiled = lambda state, fn0=t0, fn1=t1, p=player: fn0(state, p) and fn1(state, p)
        else:
            tag_tuple = tuple(tags)
            compiled = lambda state, fns=tag_tuple, p=player: all(fn(state, p) for fn in fns)
        rule_cache[loc_name] = compiled
        return compiled

    is_b2 = v_key in ("black2", "black_2", "b2")
    is_w2 = v_key in ("white2", "white_2", "w2")
    excluded_by_version = WHITE2_EXCLUSIVE_LOCATIONS if is_b2 else (BLACK2_EXCLUSIVE_LOCATIONS if is_w2 else frozenset())

    rem_opt = getattr(world.options, "exclude_postgame_checks", None)
    remove_postgame = rem_opt is not None and bool(rem_opt.value)
    excluded_postgame_locations: set[str] = set()

    if remove_postgame:
        # Determine locations that are logically only accessible after the goal is completed
        world._evaluating_pre_goal = True
        try:
            from BaseClasses import CollectionState
            from ..items import PROGRESSION_ITEM_TABLE, TM_ITEM_TABLE
            test_state = CollectionState(world.multiworld)
            for item_name in PROGRESSION_ITEM_TABLE:
                test_state.collect(world.create_item(item_name))
            for item_name in TM_ITEM_TABLE:
                test_state.collect(world.create_item(item_name))
            test_state.collect(world.create_item("Prop Case"))

            # BFS reachability of regions starting from Aspertia city
            reachable_regions: set[str] = set()
            start_reg = regions.get("Aspertia City")
            if start_reg:
                queue = [start_reg]
                reachable_regions.add(start_reg.name)
                while queue:
                    curr = queue.pop(0)
                    for exit_conn in curr.exits:
                        if exit_conn.connected_region and exit_conn.connected_region.name not in reachable_regions:
                            if exit_conn.access_rule(test_state):
                                reachable_regions.add(exit_conn.connected_region.name)
                                queue.append(exit_conn.connected_region)

            for loc_name, loc_info in chain(BASE_LOCATION_TABLE.items(), TRAINER_LOCATION_TABLE.items()):
                if loc_name in excluded_by_version:
                    continue
                reg_name = loc_info.region or infer_region_from_name(loc_name)
                if reg_name not in reachable_regions:
                    excluded_postgame_locations.add(loc_name)
                else:
                    rule_fn = make_access_rule(loc_name, loc_info.rule)
                    if rule_fn and not rule_fn(test_state):
                        excluded_postgame_locations.add(loc_name)
        finally:
            world._evaluating_pre_goal = False

    def is_loc_allowed(name: str) -> bool:
        return name not in excluded_postgame_locations and name not in excluded_by_version

    # Place base item/gift/badge/tm locations
    hidden_enabled = getattr(world.options, "hidden_items", None) is None or bool(world.options.hidden_items.value)
    habitat_enabled = getattr(world.options, "habitat_list_checks", None) is None or bool(world.options.habitat_list_checks.value)
    for loc_name, loc_info in BASE_LOCATION_TABLE.items():
        if not is_loc_allowed(loc_name):
            continue
        if loc_name in HIDDEN_ITEM_LOCATIONS and not hidden_enabled:
            continue
        if loc_name in HABITAT_LIST_LOCATIONS and not habitat_enabled:
            continue
        reg_name = loc_info.region or infer_region_from_name(loc_name)
        region = regions.get(reg_name, regions["Aspertia City"])
        loc = PokemonB2W2Location(world.player, loc_name, loc_info.id, region)
        rule_fn = make_access_rule(loc_name, loc_info.rule)
        if rule_fn is not None:
            loc.access_rule = rule_fn
        region.locations.append(loc)

    # Place trainer locations if Trainersanity is enabled (full/partial)
    trainersanity_val = getattr(world.options, "trainersanity", None)
    if trainersanity_val is not None and trainersanity_val.value:
        count = int(trainersanity_val.value)
        allowed_trainers = [
            (loc_name, loc_info)
            for loc_name, loc_info in TRAINER_LOCATION_TABLE.items()
            if is_loc_allowed(loc_name)
        ]
        allowed_trainers.sort(key=lambda t: t[0])
        passthrough = getattr(world.multiworld, "re_gen_passthrough", {}).get(world.game)
        if isinstance(passthrough, dict) and "trainer_checks" in passthrough:
            trainer_id_set = set(passthrough["trainer_checks"])
            chosen_trainers = [t for t in allowed_trainers if t[1].id in trainer_id_set]
        elif count < len(allowed_trainers):
            chosen_trainers = world.random.sample(allowed_trainers, count)
        else:
            chosen_trainers = allowed_trainers

        for loc_name, loc_info in chosen_trainers:
            reg_name = loc_info.region or infer_region_from_name(loc_name)
            region = regions.get(reg_name, regions["Aspertia City"])
            loc = PokemonB2W2Location(world.player, loc_name, loc_info.id, region)
            rule_fn = make_access_rule(loc_name, loc_info.rule)
            if rule_fn is not None:
                loc.access_rule = rule_fn
            region.locations.append(loc)

    # Place sanity locations when implemented
    for loc_name, loc_info in SANITY_LOCATION_TABLE.items():
        if not is_loc_allowed(loc_name):
            continue
        reg_name = loc_info.region or infer_region_from_name(loc_name)
        region = regions.get(reg_name, regions["Aspertia City"])
        loc = PokemonB2W2Location(world.player, loc_name, loc_info.id, region)
        rule_fn = make_access_rule(loc_name, loc_info.rule)
        if rule_fn is not None:
            loc.access_rule = rule_fn
        region.locations.append(loc)

    # Exclude locations that only unlock strictly postgame if the goal is only Champion
    goal_opt = getattr(world.options, "goal", None)
    if hasattr(goal_opt, "value") and isinstance(goal_opt.value, set):
        active_goals = set(goal_opt.value)
    elif hasattr(goal_opt, "current_key"):
        active_goals = {goal_opt.current_key}
    elif isinstance(goal_opt, (list, set, tuple)):
        active_goals = set(goal_opt)
    else:
        active_goals = {"champion"}

    if active_goals.issubset({"champion", "iris"}):
        try:
            from BaseClasses import LocationProgressType
            post_game_regions = {
                "Route 1", "Route 2", "Route 3", "Nuvema Town", "Accumula Town", "Striaton City",
                "Dreamyard", "Pinwheel Forest", "Nacrene City",
                "Route 17", "Route 18", "P2 Laboratory", "Nature Preserve",
                "N's Castle",
            }
            post_game_locs = {
                "Floccesy Town - PkMn Trainer Alder",
                "Undella Town - Trainer Cynthia",
            }
            for region in regions.values():
                is_post_game_reg = region.name in post_game_regions
                for loc in region.locations:
                    if is_post_game_reg or loc.name in post_game_locs or "Rematch" in loc.name or "Post-Game" in loc.name or "Hall of Fame" in loc.name:
                        loc.progress_type = LocationProgressType.EXCLUDED
        except Exception:
            pass

    return regions


__all__ = [
    "ConnectionInfo",
    "REGION_LIST",
    "REGION_CONNECTIONS",
    "infer_region_from_name",
    "create_regions_and_locations",
    "has_basic_badge",
    "has_toxic_badge",
    "has_insect_badge",
    "has_bolt_badge",
    "has_quake_badge",
    "has_jet_badge",
    "has_legend_badge",
    "has_wave_badge",
    "has_all_badges",
    "badge_count",
    "has_badge_count",
    "can_use_cut",
    "can_use_fly",
    "can_use_surf",
    "can_use_strength",
    "can_use_waterfall",
    "can_use_dive",
    "can_use_flash",
    "has_dowsing_machine",
    "has_bicycle",
    "has_super_rod",
    "has_colress_mchn",
    "has_plasma_card",
    "has_dna_splicers",
    "has_card_key",
    "can_enter_giant_chasm",
    "can_access_black_tower",
    "can_access_white_treehollow",
    "can_battle_benga",
    "can_travel_by_ship",
    "can_travel_by_plane",
    "can_access_top_trainer",
    "can_access_legendary_location",
    "check_goal_completion",
    "can_enter_hall_of_fame",
]
