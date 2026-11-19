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
        "Route 4 - Item: Western street",
        "Route 4 - Item: Northeast hill",
        "Route 4 - Item: South of Roughneck Silvester",
        "Route 4 - Item: 2F of Petilil trade house",
        "Route 4 - Hidden: Northern area between stairways",
        "Route 4 - Hidden: Central deep sand north of fenced sand patch",
        "Route 4 - Hidden: Eastern deep sand",
        "Route 4 - Hidden: In the middle of a sand patch",
        "Route 4 - Hidden: Easternmost hidden item near barricade",
        "Route 4 - Trainer: Policeman Braven in south near Castelia Gate",
        "Route 4 - Trainer: Policeman Dell in north near Nimbasa Gate",
        "Route 4 - Trainer: Policeman Neagle on central road",
        "Route 4 - Trainer: Roughneck Joey in western fenced area",
        "Route 4 - Trainer: Roughneck Silvester in northwest fenced area",
        "Route 4 - Trainer: Biker Stanley in western fenced area",
        "Route 4 - Trainer: Hooligans Rob & Sal on western street",
        "Route 4 - Trainer: Youngster Sinclair in western fenced area",
    }

    WHITE2_EXCLUSIVE_LOCATIONS = {
        "Route 4 - Item: Central ruins",
        "Route 4 - Item: Northwest ruins",
        "Route 4 - Item: Excavation pit south",
        "Route 4 - Item: Inside Cottonee trade house",
        "Route 4 - Hidden: Southwest deep sand",
        "Route 4 - Hidden: Northwest deep sand",
        "Route 4 - Hidden: Far east deep sand",
        "Route 4 - Hidden: Southeast deep sand near ruins",
        "Route 4 - Hidden: Northeast deep sand",
        "Route 4 - Trainer: Rich Boy Keenan in west ruins",
        "Route 4 - Trainer: Backpacker Roland in north near Nimbasa Gate",
        "Route 4 - Trainer: Backpacker Rachel in east ruins",
        "Route 4 - Trainer: Pokéfan Norbert in east",
        "Route 4 - Trainer: Pokéfan Sachiko in northeast ruins",
        "Route 4 - Trainer: Twins Tara & Val in central ruins",
        "Route 4 - Trainer: Backpacker Clifford in southeast",
        "Route 4 - Trainer: Lady Lina in central ruins",
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

    world.multiworld.regions.extend(regions.values())
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
