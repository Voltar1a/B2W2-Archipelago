from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Callable

from .goals import is_legendary_defeated

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonB2W2Client
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# Tracked events bitmap
TRACKED_EVENTS: list[tuple[str, Callable[[PokemonB2W2Client], bool]]] = [
    # Gym leaders (1-8)
    ("event_defeat_cheren", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 1) or c.get_flag(2284) or c.get_flag(1676) or c.get_flag(1891))),
    ("event_defeat_roxie", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 2) or c.get_flag(2287))),
    ("event_defeat_burgh", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 4) or c.get_flag(2286) or c.get_flag(1674))),
    ("event_defeat_elesa", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 8) or c.get_flag(2288))),
    ("event_defeat_clay", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 16) or c.get_flag(2289))),
    ("event_defeat_skyla", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 32) or c.get_flag(2290))),
    ("event_defeat_drayden", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 64) or c.get_flag(2292))),
    ("event_defeat_marlon", lambda c: bool((getattr(c, "_last_badges_byte", 0) & 128) or c.get_flag(2293))),

    # Elite Four & Champion
    ("event_defeat_shauntal", lambda c: bool(c.get_flag(1558) or c.get_flag(2292) or c.get_flag(1663) or c.get_flag(2297))),
    ("event_defeat_grimsley", lambda c: bool(c.get_flag(1560) or c.get_flag(2293) or c.get_flag(1665) or c.get_flag(2298))),
    ("event_defeat_caitlin", lambda c: bool(c.get_flag(1559) or c.get_flag(2294) or c.get_flag(1664) or c.get_flag(2299))),
    ("event_defeat_marshal", lambda c: bool(c.get_flag(1561) or c.get_flag(2295) or c.get_flag(1666) or c.get_flag(2300))),
    ("event_defeat_iris", lambda c: bool(c.get_flag(1861) or c.get_flag(2296) or c.get_flag(2056) or c.get_flag(2301) or c.get_flag(0x1D4))),

    # Story progression events
    ("event_clear_floccesy_ranch", lambda c: bool(c.get_flag(2282) or c.get_flag(1679))),
    ("event_clear_castelia_sewers", lambda c: bool(c.get_flag(2283) or c.get_flag(2114))),
    ("event_win_pwt", lambda c: bool(c.get_flag(2285) or c.get_flag(2100))),
    ("event_clear_chargestone_cave", lambda c: bool(c.get_flag(2294) or c.get_flag(2105))),
    ("event_celestial_tower_bell", lambda c: bool(c.get_flag(2295) or c.get_flag(2106))),
    ("event_clear_reversal_mountain", lambda c: bool(c.get_flag(2297) or c.get_flag(2108))),
    ("event_strange_house", lambda c: bool(c.get_flag(2298) or c.get_flag(2109))),
    ("event_undella_rival", lambda c: bool(c.get_flag(2299) or c.get_flag(2216))),
    ("event_opelucid_frozen", lambda c: bool(c.get_flag(2300) or c.get_flag(2278))),
    ("event_marine_tube_open", lambda c: bool(c.get_flag(2307) or c.get_flag(2279))),
    ("event_plasma_frigate_seaside", lambda c: bool(c.get_flag(2308) or c.get_flag(2319))),
    ("event_plasma_frigate_chasm", lambda c: bool(c.get_flag(2309) or c.get_flag(2320))),
    ("event_defeat_colress", lambda c: bool(c.get_flag(2333) or c.get_flag(1864))),
    ("event_defeat_ghetsis", lambda c: bool(c.get_flag(1865) or c.get_flag(885))),
    ("event_defeat_kyurem_black_white", lambda c: is_legendary_defeated("kyurem", c)),
    ("event_defeat_hugh_victory_road", lambda c: bool(c.get_flag(2204) or c.get_flag(2205) or c.get_flag(2206))),

    # Goals
    ("event_defeat_cynthia", lambda c: bool(c.get_flag(1976))),
    ("event_defeat_benga", lambda c: c.get_var(16708) >= 1),
    ("event_defeat_alder", lambda c: bool(c.get_flag(2102))),
    ("event_defeat_n", lambda c: any(c.get_flag(f) for f in (2302, 2303, 2304, 2305))),
    ("event_defeat_gamefreak_morimoto", lambda c: bool(c.get_flag(1660))),
    ("event_defeat_gamefreak_nishino", lambda c: bool(c.get_flag(2111))),

    # Legendary encounters
    ("event_catch_cobalion", lambda c: is_legendary_defeated("cobalion", c)),
    ("event_catch_virizion", lambda c: is_legendary_defeated("virizion", c)),
    ("event_catch_terrakion", lambda c: is_legendary_defeated("terrakion", c)),
    ("event_catch_zekrom_reshiram", lambda c: is_legendary_defeated("zekrom_reshiram", c)),
    ("event_catch_kyurem", lambda c: is_legendary_defeated("kyurem", c)),
    ("event_catch_latios_latias", lambda c: is_legendary_defeated("latios_latias", c)),
    ("event_catch_uxie", lambda c: is_legendary_defeated("uxie", c)),
    ("event_catch_mesprit", lambda c: is_legendary_defeated("mesprit", c)),
    ("event_catch_azelf", lambda c: is_legendary_defeated("azelf", c)),
    ("event_catch_heatran", lambda c: is_legendary_defeated("heatran", c)),
    ("event_catch_cresselia", lambda c: is_legendary_defeated("cresselia", c)),
    ("event_catch_regirock", lambda c: is_legendary_defeated("regirock", c)),
    ("event_catch_regice", lambda c: is_legendary_defeated("regice", c)),
    ("event_catch_registeel", lambda c: is_legendary_defeated("registeel", c)),
    ("event_catch_regigigas", lambda c: is_legendary_defeated("regigigas", c)),
]


async def sync_datastorage(client: PokemonB2W2Client, ctx: BizHawkClientContext) -> None:
    # Synchronises seen pokemon, caught pokemon, map ID, and tracked event bitmap flags
    if client.save_data_address == 0 or not client.data_address_confirmed:
        return

    packages: list[dict] = []
    is_battle = getattr(client, "is_battle", False)

    # Map tracking bounce packet from batched playersave.location.zoneid (0x19580)
    if not is_battle:
        map_bytes = getattr(client, "_latest_map_bytes", None)
        if map_bytes and len(map_bytes) >= 2:
            current_map = int.from_bytes(map_bytes[:2], "little")
            if 0 < current_map < 615 and current_map != client.current_map:
                client.current_map = current_map
                packages.append({
                    "cmd": "Bounce",
                    "slots": [ctx.slot],
                    "data": {
                        "time": time.time(),
                        "map": current_map,
                        "map_id": current_map,
                    },
                })

    # Process Pokédex block 54 (0x21400 + 0x08) from batched read
    if not is_battle:
        dex_raw = client.dex_caught_buffer
        if dex_raw and len(dex_raw) >= 420 and dex_raw != getattr(client, "_prev_dex_raw", None):
            client._prev_dex_raw = dex_raw
            caught_bytes = dex_raw[:84]
            seen_bytes = dex_raw[84:420]

            local_caught_pokemon: list[int] = []
            local_seen_pokemon: list[int] = []

            for s in range(1, 650):
                byte_idx = (s - 1) >> 3
                bit_mask = 1 << ((s - 1) & 7)

                if caught_bytes[byte_idx] & bit_mask:
                    local_caught_pokemon.append(s)

                if (
                    (seen_bytes[byte_idx] & bit_mask)
                    or (seen_bytes[84 + byte_idx] & bit_mask)
                    or (seen_bytes[168 + byte_idx] & bit_mask)
                    or (seen_bytes[252 + byte_idx] & bit_mask)
                ):
                    local_seen_pokemon.append(s)

            if local_seen_pokemon != getattr(client, "local_seen_pokemon", None):
                packages.append({
                    "cmd": "Set",
                    "key": f"pokemon_b2w2_seen_pokemon_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": local_seen_pokemon}],
                })
                client.local_seen_pokemon = local_seen_pokemon

            if local_caught_pokemon != getattr(client, "local_caught_pokemon", None):
                packages.append({
                    "cmd": "Set",
                    "key": f"pokemon_b2w2_caught_pokemon_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": local_caught_pokemon}],
                })
                client.local_caught_pokemon = local_caught_pokemon

    # Evaluate tracked events bitmap
    local_tracked_events = 0
    for idx, (_, check_fn) in enumerate(TRACKED_EVENTS):
        if check_fn(client):
            local_tracked_events |= (1 << idx)

    if local_tracked_events != getattr(client, "local_tracked_events", None):
        total_chunks = (len(TRACKED_EVENTS) + 31) // 32
        for chunk in range(total_chunks):
            chunk_val = (local_tracked_events >> (chunk * 32)) & 0xFFFFFFFF
            packages.append({
                "cmd": "Set",
                "key": f"pokemon_b2w2_tracked_events_{ctx.team}_{ctx.slot}_{chunk}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": chunk_val}],
            })
        packages.append({
            "cmd": "Set",
            "key": f"pokemon_b2w2_tracked_events_{ctx.team}_{ctx.slot}",
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": local_tracked_events & 0xFFFFFFFF}],
        })
        client.local_tracked_events = local_tracked_events

    if packages:
        await ctx.send_msgs(packages)
