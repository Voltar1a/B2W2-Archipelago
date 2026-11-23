from __future__ import annotations

from typing import TYPE_CHECKING
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


def create_regions_and_locations(world: "PokemonB2W2World") -> dict[str, Region]:
    from ..locations import (
        PokemonB2W2Location,
        BASE_LOCATION_TABLE,
        TRAINER_LOCATION_TABLE,
        SANITY_LOCATION_TABLE,
    )
    from ..locations.items import HIDDEN_ITEM_LOCATIONS

    # Version-exclusive locations
    BLACK2_EXCLUSIVE_LOCATIONS = {
        "Route 4 - Item: Near sign in the west",
        "Route 4 - Item: Hill on western side",
        "Route 4 - Item: South of Roughnecks in the west",
        "Route 4 - Item: 2F of second house on right",
        "Route 4 - Gift: Ace Trainer in first house on right",
        "Route 4 - Gift: Black Belt in 2F of first left house",
        "Route 4 - Gift: Maid in third house on right (Guess Pokémon cry)",
        "Route 4 - Trainer: Fisherman Hubert by water in southwest top",
        "Route 4 - Trainer: Breeder Irene by Castelia Gate",
        "Route 4 - Hidden: Western area between stairways southeast of rest house",
        "Route 4 - Hidden: In deep sand between two stairways south of Policeman",
        "Route 4 - Hidden: Deep sand north of fences east of the Roughnecks",
        "Route 4 - Hidden: In the middle of a deep sand patch in the west",
        "Route 4 - Hidden: Western area west of bikers in deep sand next to barricade",
        "Route 4 - Trainer: Policeman Braven in south near Castelia Gate",
        "Route 4 - Trainer: Policeman Dell in north near Nimbasa Gate",
        "Route 4 - Trainer: Policeman Neagle south of rest house on western side",
        "Route 4 - Trainer: Roughneck Joey in the west south of the stairs",
        "Route 4 - Trainer: Roughneck Silvester in northwest fenced area",
        "Route 4 - Trainer: Biker Stanley in the west",
        "Route 4 - Trainer: Hooligans Rob & Sal by the south fence in the west",
        "Route 4 - Trainer: Youngster Sinclair in the west",
        "Reversal Mountain - Item: 1F, dead-end tunnel north of Battle Girl",
        "Reversal Mountain - Item: 1F, dead-end tunnel east of Doctor in south of main cavern",
        "Reversal Mountain - Item: 1F, south of Hiker in north of main cavern",
        "Reversal Mountain - Item: 1F, east of Black Belt in west of main cavern",
        "Reversal Mountain - Item: 1F, dead-end tunnel east of Backpacker and Hiker in southwest of main cavern",
        "Reversal Mountain - Hidden: B1F, in the stalagmite below the stairs",
        "Reversal Mountain - Hidden: 1F, in the stalagmite north of Backpacker and Hiker in the west",
        "Reversal Mountain - Hidden: 1F, in stalagmite south of Scientist in east of main cavern",
        "Reversal Mountain - Hidden: 1F, in stalagmite in the southeast of main cavern",
        "Reversal Mountain - Hidden: 1F, dead end south of Ace Trainers in north of main cavern",
        "Reversal Mountain - Hidden: 1F, dead-end tunnel east of Backpacker and Hiker in south",
        "Reversal Mountain - Trainer: 1F, Backpacker Kiyo in southwest of main cavern",
        "Reversal Mountain - Trainer: 1F, Backpacker Kumiko in north of main cavern",
        "Reversal Mountain - Trainer: Ranger Lewis B1F to the left",
        "Reversal Mountain - Trainer: Ranger Eliza 1F in south of the main cavern",
        "Reversal Mountain - Trainer: 1F, Ace Trainer Ray in north of main cavern",
        "Reversal Mountain - Trainer: 1F, Ace Trainer Cora in north of main cavern",
        "Reversal Mountain - Trainer: 1F, Hiker Jared in north of main cavern",
        "Reversal Mountain - Trainer: 1F, Hiker Markus in southwest of main cavern",
        "Reversal Mountain - Trainer: 1F, Black Belt Corey in the west of the main cavern",
        "Reversal Mountain - Trainer: 1F, Battle Girl Chan in south of main cavern",
        "Reversal Mountain - Trainer: 1F, Doctor Derek by stairs to B1F in south of main cavern",
        "Plasma Frigate - Item: B2F, bow side of the maze",
        "Plasma Frigate - Item: B2F, near Grunt with Krokorok and Krookodile (Max Revive)",
        "Plasma Frigate - Item: B2F, near Grunt with Krokorok and Krookodile (Max Elixir)",
        "Plasma Frigate - Item: In the northeast room",
        "Plasma Frigate - Item: B2F, bow side from Grunt with Drapion",
        "Plasma Frigate - Trainer: Team Plasma Grunt 1 by teleporter in southwestern room (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 6 next to teleporter in centre east room (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 7 between beds in centre east room (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 8 (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 9 between beds in southwestern room (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 10 southeastern room (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt at entrance (from Route 21)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 22 (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 27 (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 24 (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 26 (from Giant Chasm)",
        "Plasma Frigate - Trainer: Doctor Julius (from Giant Chasm)",
        "Mistralton City - Item: South of runway between greenhouses",
    }

    WHITE2_EXCLUSIVE_LOCATIONS = {
        "Route 4 - Item: Between two houses in central ruins",
        "Route 4 - Item: Northwest ruins",
        "Route 4 - Item: Hidden behind Pokéfan in northeast of ruins",
        "Route 4 - Item: Inside Cottonee trade house",
        "Route 4 - Gift: Ace Trainer in first house east of ruins crossroads",
        "Route 4 - Gift: Black Belt in house in the far southeast of ruins",
        "Route 4 - Gift: Maid in southwest house (Guess Pokémon cry)",
        "Route 4 - Trainer: Fisherman Hubert at south water top",
        "Route 4 - Trainer: Breeder Irene along road in the south",
        "Route 4 - Hidden: In deep sand in southwest of ruins",
        "Route 4 - Hidden: Northwest of crossroads along ruins road",
        "Route 4 - Hidden: Far east deep sand in ruins",
        "Route 4 - Hidden: Southeast of ruins between two houses",
        "Route 4 - Hidden: West of Pokéfan in east of ruins",
        "Route 4 - Trainer: Rich Boy Keenan along ruins road to the west",
        "Route 4 - Trainer: Backpacker Roland along road north of ruins",
        "Route 4 - Trainer: Backpacker Rachel east along ruins road",
        "Route 4 - Trainer: Pokéfan Norbert in far southeast of ruins",
        "Route 4 - Trainer: Pokéfan Sachiko in northeast ruins",
        "Route 4 - Trainer: Twins Tara & Val at start of ruins road",
        "Route 4 - Trainer: Backpacker Clifford in southeast on road",
        "Route 4 - Trainer: Lady Lina in central ruins",
        "Reversal Mountain - Item: 1F, above Hiker in the southeast",
        "Reversal Mountain - Item: 1F, in the west southeast of male Backpacker and Hiker",
        "Reversal Mountain - Item: 1F, northwest of Black Belt southwest of Ace Trainers",
        "Reversal Mountain - Item: 1F, south of Scientist in northeast",
        "Reversal Mountain - Item: 1F, in the west east of the entrance",
        "Reversal Mountain - Item: B1F, near the entrance to 1F",
        "Reversal Mountain - Hidden: B1F, in a rock near the big rock",
        "Reversal Mountain - Hidden: Rock centre-east by B1F stairs",
        "Reversal Mountain - Hidden: 1F, north in southern dead end west of Ace Trainers, in a rock",
        "Reversal Mountain - Hidden: North in rock west of Ace Trainers",
        "Reversal Mountain - Hidden: In central west, northeast of Battle Girl",
        "Reversal Mountain - Hidden: 1F, far southeast in a rock",
        "Reversal Mountain - Trainer: 1F, Backpacker Kiyo in west",
        "Reversal Mountain - Trainer: 1F, Backpacker Kumiko southeast",
        "Reversal Mountain - Trainer: 1F, Ranger Lewis in the southwest",
        "Reversal Mountain - Trainer: B1F, Ranger Eliza in the northwest",
        "Reversal Mountain - Trainer: 1F, Ace Trainer Ray in north",
        "Reversal Mountain - Trainer: 1F, Ace Trainer Cora in north",
        "Reversal Mountain - Trainer: 1F, Hiker Jared southeast",
        "Reversal Mountain - Trainer: 1F, Hiker Markus in west",
        "Reversal Mountain - Trainer: 1F, Black Belt Corey centre east",
        "Reversal Mountain - Trainer: 1F, Battle Girl Chan central west",
        "Reversal Mountain - Trainer: 1F, Doctor Derek in south",
        "Plasma Frigate - Item: B2F, top of the beam puzzle maze bow side of the maze",
        "Plasma Frigate - Item: Near Grunt in southeast of beam puzzle room right ball",
        "Plasma Frigate - Item: Near Grunt in southeast of beam puzzle room left ball",
        "Plasma Frigate - Item: B1F, bigger room on the left",
        "Plasma Frigate - Item: B2F, in the yellow warp panel to left of the puzzle pit",
        "Plasma Frigate - Trainer: Team Plasma Grunt 11 northwest of beam puzzle room (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 12 northeast of beam puzzle room (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 13 top left of puzzle pit (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 14 northeast of beam puzzle pit (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 15 centre left of puzzle pit (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 16 in southwest of beam puzzle room near doctor (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 17 in southeast of beam puzzle room near two item balls (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 18 centre right of puzzle pit (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 23 left ambushing double battling grunt guarding southern door (from Giant Chasm)",
        "Plasma Frigate - Trainer: Team Plasma Grunt 25 right ambushing double battling grunt guarding southern door (from Giant Chasm)",
        "Plasma Frigate - Trainer: Doctor Julius in southwest of beam puzzle room (from Giant Chasm)",
        "Mistralton City - Item: South of runway between fields",
    }

    v_opt = getattr(world.options, "version", None)
    v_key = v_opt.current_key if v_opt is not None else "black2"

    regions: dict[str, Region] = {
        name: Region(name, world.player, world.multiworld)
        for name in REGION_LIST
    }

    # Connect regions
    import inspect
    for conn in REGION_CONNECTIONS:
        src = regions[conn.source]
        dst = regions[conn.destination]
        conn_name = conn.name or f"{conn.source} -> {conn.destination}"
        if conn.rule is not None:
            rule_fn = conn.rule
            sig = inspect.signature(rule_fn)
            if len(sig.parameters) >= 3:
                src.connect(dst, conn_name, lambda state, fn=rule_fn: fn(state, world.player, world))
            else:
                src.connect(dst, conn_name, lambda state, fn=rule_fn: fn(state, world.player))
        else:
            src.connect(dst, conn_name)

    world.multiworld.regions.extend(regions.values())

    def make_access_rule(loc_name: str, base_rule):
        tags = []
        if base_rule is not None:
            tags.append(base_rule)
        if loc_name in HIDDEN_ITEM_LOCATIONS:
            tags.append(lambda state, p: has_dowsing_machine(state, p, world))
        if loc_name in LOCATION_RULES:
            rule_cb = LOCATION_RULES[loc_name]
            tags.append(lambda state, p, cb=rule_cb: cb(state, p, world))
        if not tags:
            return None
        return lambda state: all(t(state, world.player) for t in tags)

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

            for loc_name, loc_info in {**BASE_LOCATION_TABLE, **TRAINER_LOCATION_TABLE}.items():
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
        if name in excluded_postgame_locations:
            return False
        if v_key in ("black2", "black_2", "b2"):
            return name not in WHITE2_EXCLUSIVE_LOCATIONS
        elif v_key in ("white2", "white_2", "w2"):
            return name not in BLACK2_EXCLUSIVE_LOCATIONS
        return True

    # Place base item/gift/badge/tm locations
    hidden_enabled = getattr(world.options, "hidden_items", None) is None or bool(world.options.hidden_items.value)
    for loc_name, loc_info in BASE_LOCATION_TABLE.items():
        if not is_loc_allowed(loc_name):
            continue
        if loc_name in HIDDEN_ITEM_LOCATIONS and not hidden_enabled:
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
                "Floccesy Town - Trainer: PkMn Trainer Alder",
                "Undella Town - Trainer: Trainer Cynthia",
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
