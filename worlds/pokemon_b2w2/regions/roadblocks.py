from __future__ import annotations

from typing import TYPE_CHECKING
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from .. import PokemonB2W2World


# Gym badge logic

def has_basic_badge(state: CollectionState, player: int) -> bool:
    return state.has("Basic Badge", player)


def has_toxic_badge(state: CollectionState, player: int) -> bool:
    return state.has("Toxic Badge", player)


def has_insect_badge(state: CollectionState, player: int) -> bool:
    return state.has("Insect Badge", player)


def has_bolt_badge(state: CollectionState, player: int) -> bool:
    return state.has("Bolt Badge", player)


def has_quake_badge(state: CollectionState, player: int) -> bool:
    return state.has("Quake Badge", player)


def has_jet_badge(state: CollectionState, player: int) -> bool:
    return state.has("Jet Badge", player)


def has_legend_badge(state: CollectionState, player: int) -> bool:
    return state.has("Legend Badge", player)


def has_wave_badge(state: CollectionState, player: int) -> bool:
    return state.has("Wave Badge", player)


def has_tm_count(state: CollectionState, player: int, count: int) -> bool:
    from ..items.tms import TM_ITEM_TABLE
    return sum(1 for item_name in TM_ITEM_TABLE if state.has(item_name, player)) >= count


ALL_BADGES = (
    "Basic Badge",
    "Toxic Badge",
    "Insect Badge",
    "Bolt Badge",
    "Quake Badge",
    "Jet Badge",
    "Legend Badge",
    "Wave Badge",
)


def has_all_badges(state: CollectionState, player: int) -> bool:
    return state.has_all(ALL_BADGES, player)


def badge_count(state: CollectionState, player: int) -> int:
    return sum(1 for badge in ALL_BADGES if state.has(badge, player))


def has_badge_count(state: CollectionState, player: int, count: int) -> bool:
    return badge_count(state, player) >= count


# HM & field move helpers

def can_use_cut(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM01 Cut", player)


def can_use_fly(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM02 Fly", player)


def can_use_surf(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM03 Surf", player)


def can_use_strength(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM04 Strength", player)


def can_use_waterfall(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM05 Waterfall", player) and can_use_surf(state, player, world)


def can_use_dive(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has("HM06 Dive", player) and can_use_surf(state, player, world)


def get_version_key(world: "PokemonB2W2World" | None, default: str = "black2") -> str:
    ver = getattr(getattr(world, "options", None), "version", None) if world else None
    return ver.current_key if ver is not None else default


def can_use_flash(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    flash_logic = getattr(world.options, "flash_logic", None) if world else None
    if flash_logic is not None and not flash_logic.value:
        return True
    return state.has("TM70 Flash", player)


def has_dowsing_machine(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    dowsing_logic = getattr(world.options, "dowsing_machine_logic", None) if world else None
    if dowsing_logic is not None and int(getattr(dowsing_logic, "value", dowsing_logic)) == 2:
        return True
    return state.has("Dowsing Machine", player)


def has_bicycle(state: CollectionState, player: int) -> bool:
    return state.has("Bicycle", player)


def has_super_rod(state: CollectionState, player: int) -> bool:
    return state.has("Super Rod", player)


def has_colress_mchn(state: CollectionState, player: int) -> bool:
    return state.has("Colress MCHN", player)


def has_plasma_card(state: CollectionState, player: int) -> bool:
    return state.has("Plasma Card", player)


def has_dna_splicers(state: CollectionState, player: int) -> bool:
    return state.has("DNA Splicers", player)


def has_card_key(state: CollectionState, player: int) -> bool:
    return state.has("Card Key", player)


def has_permit(state: CollectionState, player: int) -> bool:
    return state.has("Permit", player)


def can_enter_giant_chasm(state: CollectionState, player: int) -> bool:
    return has_card_key(state, player)


def can_access_black_tower(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    if not has_all_badges(state, player):
        return False
    return get_version_key(world) in ("black2", "black_2", "b2")


def can_access_white_treehollow(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    if not has_all_badges(state, player):
        return False
    return get_version_key(world) in ("white2", "white_2", "w2")


def can_battle_benga(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_enter_hall_of_fame(state, player, world)


def can_enter_marine_tube(state: CollectionState, player: int) -> bool:
    return has_legend_badge(state, player)

# Day of the week access rules

def can_access_day(state: CollectionState, player: int, day_name: str, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has(day_name, player)


def can_access_sunday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Sunday", world)


def can_access_monday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Monday", world)


def can_access_tuesday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Tuesday", world)


def can_access_wednesday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Wednesday", world)


def can_access_thursday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Thursday", world)


def can_access_friday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Friday", world)


def can_access_saturday(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_day(state, player, "Saturday", world)


# Seasons access rules

def can_access_season(state: CollectionState, player: int, season_name: str, world: "PokemonB2W2World" | None = None) -> bool:
    return state.has(season_name, player)


def can_access_spring(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_season(state, player, "Spring", world)


def can_access_summer(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_season(state, player, "Summer", world)


def can_access_autumn(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_season(state, player, "Autumn", world)


def can_access_winter(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return can_access_season(state, player, "Winter", world)


def can_board_plasma_frigate(state: CollectionState, player: int) -> bool:
    return has_plasma_card(state, player)


def can_pass_giant_chasm_to_route_23(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return has_dna_splicers(state, player)


def can_travel_by_ship(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return has_toxic_badge(state, player)


def can_travel_by_plane(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    return has_jet_badge(state, player)


# Goal eval

def can_enter_hall_of_fame(state: CollectionState, player: int, world: "PokemonB2W2World" | None = None) -> bool:
    if world and getattr(world, "_evaluating_pre_goal", False):
        return False
    return (
        has_all_badges(state, player)
        and can_use_strength(state, player, world)
        and can_enter_giant_chasm(state, player)
        and can_pass_giant_chasm_to_route_23(state, player, world)
    )


def can_access_top_trainer(trainer: str, state: CollectionState, player: int, world: "PokemonB2W2World") -> bool:
    champion_ok = can_enter_hall_of_fame(state, player, world)
    if trainer == "cynthia":
        return champion_ok
    elif trainer == "benga":
        return can_battle_benga(state, player, world)
    elif trainer == "alder":
        return champion_ok
    elif trainer == "colress":
        return champion_ok and can_use_surf(state, player, world)
    elif trainer == "n":
        return champion_ok
    elif trainer == "league_rematch":
        return champion_ok
    elif trainer in ("gamefreak_morimoto", "gamefreak_nishino"):
        return champion_ok and has_insect_badge(state, player)
    elif trainer == "hugh":
        return has_quake_badge(state, player)
    elif trainer == "ghetsis":
        return state.can_reach("Plasma Frigate", "Region", player)
    return False


def can_access_legendary_location(loc_key: str, state: CollectionState, player: int, world: "PokemonB2W2World") -> bool:
    champion_ok = can_enter_hall_of_fame(state, player, world)
    east_unova_ok = has_jet_badge(state, player) or can_use_surf(state, player, world)
    humilau_ok = has_legend_badge(state, player) or (can_use_surf(state, player, world) and has_colress_mchn(state, player))
    lake_trio_ok = champion_ok and can_use_surf(state, player, world)
    regi_ok = champion_ok and can_use_surf(state, player, world) and can_use_flash(state, player, world)

    if loc_key == "cobalion":
        return east_unova_ok
    elif loc_key == "virizion":
        return east_unova_ok
    elif loc_key == "terrakion":
        return humilau_ok
    elif loc_key == "zekrom_reshiram":
        return champion_ok
    elif loc_key == "kyurem":
        return champion_ok and can_enter_giant_chasm(state, player) and can_board_plasma_frigate(state, player)
    elif loc_key == "latios_latias":
        return champion_ok and can_use_cut(state, player, world)
    elif loc_key == "uxie":
        return lake_trio_ok
    elif loc_key == "mesprit":
        return lake_trio_ok
    elif loc_key == "azelf":
        return lake_trio_ok and can_use_cut(state, player, world)
    elif loc_key == "heatran":
        return has_jet_badge(state, player) and state.has("Magma Stone", player)
    elif loc_key == "cresselia":
        return champion_ok and state.has("Lunar Wing", player)
    elif loc_key == "regirock":
        return regi_ok
    elif loc_key == "registeel_regice":
        return regi_ok
    return False


def check_goal_completion(state: CollectionState, player: int, world: "PokemonB2W2World") -> bool:
    # Whether all requirements for the world's configured goal(s) are met
    goal_opt = getattr(world.options, "goal", None)
    if goal_opt is None:
        return has_all_badges(state, player)

    if hasattr(goal_opt, "value") and isinstance(goal_opt.value, set):
        active_goals = set(goal_opt.value)
    elif hasattr(goal_opt, "current_key"):
        active_goals = {goal_opt.current_key}
    elif isinstance(goal_opt, (list, set, tuple)):
        active_goals = set(goal_opt)
    else:
        active_goals = {"champion"}

    for key in active_goals:
        if key == "champion":
            if not can_enter_hall_of_fame(state, player, world):
                return False
        elif key == "top_trainers":
            req_opt = getattr(world.options, "top_trainers_required", None)
            needed = req_opt.value if req_opt is not None else 5
            allowed_opt = getattr(world.options, "top_trainers_allowed", None)
            allowed = set(allowed_opt.value) if allowed_opt is not None else {
                "cynthia", "benga", "alder", "colress", "n", "league_rematch",
                "gamefreak_morimoto", "gamefreak_nishino", "hugh", "ghetsis"
            }
            if len(allowed) == 0:
                needed = 0
            else:
                needed = min(needed, len(allowed))
            count = sum(1 for t in allowed if can_access_top_trainer(t, state, player, world))
            if count < needed:
                return False
        elif key == "legendary_hunt":
            req_opt = getattr(world.options, "legendary_hunt_required", None)
            needed = req_opt.value if req_opt is not None else 3
            allowed_opt = getattr(world.options, "legendary_hunt_allowed", None)
            allowed = set(allowed_opt.value) if allowed_opt is not None else {
                "cobalion", "virizion", "terrakion", "zekrom_reshiram", "kyurem",
                "latios_latias", "uxie", "mesprit", "azelf", "heatran",
                "cresselia", "regirock", "registeel_regice"
            }
            if len(allowed) == 0:
                needed = 0
            else:
                needed = min(needed, len(allowed))
            count = sum(1 for loc in allowed if can_access_legendary_location(loc, state, player, world))
            if count < needed:
                return False
        elif key == "tmhm_hunt":
            if not state.can_reach("Mistralton City", "Region", player):
                return False
            cnt_opt = getattr(world.options, "tmhm_hunt", None)
            from ..items.tms import TM_ITEM_TABLE
            from ..items.progression import PROGRESSION_ITEM_TABLE
            tm_hm_names = list(TM_ITEM_TABLE.keys()) + [k for k in PROGRESSION_ITEM_TABLE if k.startswith("HM")]
            target = max(0, min(len(tm_hm_names), int(cnt_opt.value if cnt_opt is not None else 60)))
            tms_found = sum(1 for item_name in tm_hm_names if state.has(item_name, player))
            if tms_found < target:
                return False

    return True
