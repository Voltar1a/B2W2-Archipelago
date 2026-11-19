from typing import TYPE_CHECKING, Coroutine, Any, Callable

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonB2W2Client
    from worlds._bizhawk.context import BizHawkClientContext


TM_HM_ITEM_IDS: set[int] = set(range(100328, 100426)) | {100618, 100619, 100620}


def get_method(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> Callable[
    ["PokemonB2W2Client", "BizHawkClientContext"], Coroutine[Any, Any, bool]
]:
    goal_opt = ctx.slot_data.get("options", {}).get("goal", "champion")
    if isinstance(goal_opt, list):
        goals_list = goal_opt
    else:
        goals_list = [goal_opt]

    all_goals: list[Callable[["PokemonB2W2Client", "BizHawkClientContext"], Coroutine[Any, Any, bool]]] = []
    for goal in goals_list:
        match goal:
            case "champion":
                all_goals.append(become_champion)
            case "top_trainers":
                all_goals.append(check_top_trainers)
            case "legendary_hunt":
                all_goals.append(check_legendary_hunt)
            case "tmhm_hunt":
                all_goals.append(tmhm_hunt)
            case _:
                all_goals.append(become_champion)

    if len(all_goals) == 1:
        return all_goals[0]

    async def combined_goals(_client: "PokemonB2W2Client", _ctx: "BizHawkClientContext") -> bool:
        for _g in all_goals:
            if not await _g(_client, _ctx):
                return False
        return True

    return combined_goals


async def become_champion(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    return bool(
        client.get_flag(1861)
        or client.get_flag(2296)
        or client.get_flag(2056)
        or client.get_flag(2301)
        or client.get_flag(0x1D4)
    )


def is_trainer_defeated(trainer: str, client: "PokemonB2W2Client") -> bool:
    match trainer:
        case "cynthia":
            return bool(client.get_flag(1976))
        case "benga":
            return any(client.get_flag(f) for f in (1689, 1690, 2267, 2268, 2269, 2270))
        case "alder":
            return bool(client.get_flag(2102))
        case "colress":
            return bool(client.get_flag(2333))
        case "n":
            return any(client.get_flag(f) for f in (2302, 2303, 2304, 2305))
        case "league_rematch":
            return bool(client.get_flag(2056) or client.get_flag(2301))
        case "gamefreak_morimoto":
            return bool(client.get_flag(1660) or client.get_flag(2112))
        case "gamefreak_nishino":
            return bool(client.get_flag(1877) or client.get_flag(2111))
        case "hugh":
            return any(
                client.get_flag(f)
                for f in (1898, 1899, 1900, 2204, 2205, 2206, 2216, 2217, 2218)
            )
        case "ghetsis":
            return bool(client.get_flag(1865) or client.get_flag(885))
        case _:
            return False


async def check_top_trainers(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    # Defeat of required count of selected top trainers
    opts = ctx.slot_data.get("options", {})
    required = opts.get("top_trainers_required", 5)
    allowed = opts.get("top_trainers_allowed", [
        "cynthia", "benga", "alder", "colress", "n", "league_rematch",
        "gamefreak_morimoto", "gamefreak_nishino", "hugh", "ghetsis"
    ])
    defeated_count = sum(1 for t in allowed if is_trainer_defeated(t, client))
    return defeated_count >= required


def is_legendary_defeated(loc: str, client: "PokemonB2W2Client") -> bool:
    # Stationary encounter at the specified location was defeated or captured
    get_var = getattr(client, "get_var", lambda _v: 0)
    match loc:
        case "cobalion":
            return bool(client.get_flag(802) or client.get_flag(302) or client.get_flag(303))
        case "virizion":
            return bool(client.get_flag(801) or client.get_flag(300) or client.get_flag(301))
        case "terrakion":
            return bool(client.get_flag(330) or (get_var(16611) == 2 and client.get_flag(810)))
        case "zekrom_reshiram":
            return bool(client.get_flag(234) or (get_var(16667) == 2 and client.get_flag(667)))
        case "kyurem":
            return bool(client.get_flag(249) or client.get_flag(481) or (client.get_flag(480) and client.get_flag(1004)))
        case "latios_latias":
            return bool(client.get_flag(374) or (get_var(16652) == 6 and client.get_flag(853)))
        case "uxie":
            return bool(client.get_flag(396) or (get_var(16662) == 3 and client.get_flag(918)))
        case "mesprit":
            return bool(client.get_flag(397) or (get_var(16663) == 3 and client.get_flag(919)))
        case "azelf":
            return bool(client.get_flag(398) or (get_var(16664) == 3 and client.get_flag(920)))
        case "heatran":
            return bool(client.get_flag(380) or (get_var(16500) == 3 and client.get_flag(900)))
        case "cresselia":
            return bool(client.get_flag(379) or (get_var(16499) == 3 and client.get_flag(897)))
        case "regirock":
            return bool(client.get_flag(922) or client.get_flag(400))
        case "registeel_regice":
            return bool(client.get_flag(921) or client.get_flag(399) or client.get_flag(923) or client.get_flag(401))
        case "regice":
            return bool(client.get_flag(921) or client.get_flag(399))
        case "registeel":
            return bool(client.get_flag(923) or client.get_flag(401))
        case "regigigas":
            return bool(client.get_flag(924) or client.get_flag(402))
        case _:
            return False


async def check_legendary_hunt(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    # Defeat or capture of required count of stationary legendaries across Unova
    opts = ctx.slot_data.get("options", {})
    required = opts.get("legendary_hunt_required", 3)
    allowed = opts.get("legendary_hunt_allowed", [
        "cobalion", "virizion", "terrakion", "zekrom_reshiram", "kyurem",
        "latios_latias", "uxie", "mesprit", "azelf", "heatran",
        "cresselia", "regirock", "registeel_regice"
    ])
    cleared = getattr(client, "_cleared_legendaries", None)
    defeated_count = 0
    for loc in allowed:
        if (cleared is not None and loc in cleared) or is_legendary_defeated(loc, client):
            if cleared is not None:
                cleared.add(loc)
            defeated_count += 1
    return defeated_count >= required


TMHM_HUNT_CASHIN_FLAG = 3055


async def tmhm_hunt(client: "PokemonB2W2Client", ctx: "BizHawkClientContext") -> bool:
    opts = ctx.slot_data.get("options", {})
    target = max(0, min(101, int(opts.get("tmhm_hunt", 60))))
    count = sum(1 for item in ctx.items_received if item.item in TM_HM_ITEM_IDS)
    return count >= target and bool(client.get_flag(TMHM_HUNT_CASHIN_FLAG))
