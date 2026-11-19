from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from BaseClasses import CollectionState

from .roadblocks import (
    can_use_cut,
    can_use_surf,
    can_use_strength,
    can_use_waterfall,
    can_use_flash,
    can_access_spring,
    can_access_summer,
    can_access_autumn,
    can_access_winter,
    has_basic_badge,
    has_toxic_badge,
    has_insect_badge,
    has_bolt_badge,
    has_quake_badge,
    has_jet_badge,
    has_legend_badge,
    has_colress_mchn,
    can_board_plasma_frigate,
    can_enter_hall_of_fame,
    can_access_legendary_location,
)

if TYPE_CHECKING:
    from .. import PokemonB2W2World


def _is_version(world: "PokemonB2W2World" | None, keys: tuple[str, ...]) -> bool:
    ver = getattr(getattr(world, "options", None), "version", None) if world else None
    return ver is not None and ver.current_key in keys


_VICTORY_ROAD_STRENGTH_LOCATIONS = (
    "Victory Road - Item: 3F, west of Veteran Hugo",
    "Victory Road - Trainer: Ace Trainer Beckett",
    "Victory Road - Trainer: Ace Trainer Caroll",
    "Victory Road - Trainer: Ace Trainer Chandra",
    "Victory Road - Trainer: Ace Trainer Elmer",
    "Victory Road - Trainer: Ace Trainer Pierce",
    "Victory Road - Trainer: Ace Trainer Shanta",
    "Victory Road - Trainer: Ace Trainer Shelly",
    "Victory Road - Trainer: Ace Trainer Webster",
    "Victory Road - Trainer: Backpacker Mae",
    "Victory Road - Trainer: Battle Girl Chalina",
    "Victory Road - Trainer: Black Belt Martell",
    "Victory Road - Item: Castle ruins interior throne hall",
    "Victory Road - Item: Cave 1 central rock ledge",
    "Victory Road - Item: Cave 1 northern ledge",
    "Victory Road - Item: Cave 2 upper terrace",
    "Victory Road - Trainer: Doctor Logan",
    "Victory Road - Item: Eastern cave boulder maze (Strength)",
    "Victory Road - Gift: Hugh",
    "Victory Road - Item: Grove northeastern corner",
    "Victory Road - Hidden: In Castle ruins corner",
    "Victory Road - Hidden: In Cave 2 upper rock",
    "Victory Road - Hidden: In Exterior ridge rock",
    "Victory Road - Hidden: In Grove northern grass",
    "Victory Road - Hidden: In Summit plateau rock",
    "Victory Road - Item: Outside 1 east of Doctor Logan",
    "Victory Road - Item: Outside 1 near Ace Trainer Pierce",
    "Victory Road - Item: Outside 1 south of Veteran Cathy",
    "Victory Road - Trainer: PkMn Trainer Hugh",
    "Victory Road - Trainer: Psychic Al",
    "Victory Road - Trainer: Psychic Alia",
    "Victory Road - Trainer: Ranger Eddie",
    "Victory Road - Trainer: Ranger Elle",
    "Victory Road - Item: Summit plateau before League gate",
    "Victory Road - Trainer: Veteran Abraham",
    "Victory Road - Trainer: Veteran Cathy",
    "Victory Road - Trainer: Veteran Cecile",
    "Victory Road - Trainer: Veteran Claude",
    "Victory Road - Trainer: Veteran Hugo",
    "Victory Road - Trainer: Veteran Portia",
    "Victory Road - Trainer: Veteran Sterling",
)


LOCATION_RULES: dict[str, Callable[[CollectionState, int, PokemonB2W2World], bool]] = {
    # Gym leaders and badges progression prerequisites
    "Virbank Gym - Trainer: Guitarist Billy Jo": lambda s, p, w: has_basic_badge(s, p),
    "Virbank Gym - Trainer: Roughneck Nicky": lambda s, p, w: has_basic_badge(s, p),
    "Virbank Gym - Trainer: Gym Leader Roxie": lambda s, p, w: has_basic_badge(s, p),
    "Virbank Gym - Gym Leader Roxie Toxic Badge": lambda s, p, w: has_basic_badge(s, p),
    "Castelia Gym - Trainer: Gym Leader Burgh": lambda s, p, w: has_toxic_badge(s, p),
    "Castelia Gym - Gym Leader Burgh Insect Badge": lambda s, p, w: has_toxic_badge(s, p),
    "Nimbasa Gym - Trainer: Gym Leader Elesa": lambda s, p, w: has_insect_badge(s, p),
    "Nimbasa Gym - Gym Leader Elesa Bolt Badge": lambda s, p, w: has_insect_badge(s, p),
    "Mistralton Gym - Trainer: Gym Leader Skyla": lambda s, p, w: has_quake_badge(s, p),
    "Mistralton Gym - Gym Leader Skyla Jet Badge": lambda s, p, w: has_quake_badge(s, p),
    "Mistralton City - Gift: Skyla after defeating Gym": lambda s, p, w: has_quake_badge(s, p),
    "Opelucid Gym - Trainer: Gym Leader Drayden": lambda s, p, w: has_jet_badge(s, p),
    "Opelucid Gym - Gym Leader Drayden Legend Badge": lambda s, p, w: has_jet_badge(s, p),
    "Opelucid City - Gift: Drayden after defeating Gym": lambda s, p, w: has_jet_badge(s, p),
    "Humilau Gym - Trainer: Gym Leader Marlon": lambda s, p, w: has_legend_badge(s, p) or (can_use_surf(s, p, w) and has_colress_mchn(s, p)),
    "Humilau Gym - Gym Leader Marlon Wave Badge": lambda s, p, w: has_legend_badge(s, p) or (can_use_surf(s, p, w) and has_colress_mchn(s, p)),
    "Humilau City - Gift: Marlon after defeating Gym": lambda s, p, w: has_legend_badge(s, p) or (can_use_surf(s, p, w) and has_colress_mchn(s, p)),

    # Route 20 (west is early; east is gated past Hiker Jerome by Basic badge)
    "Route 20 - Trainer: Hiker Jerome on eastern path": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Trainer: Preschooler Albert east of bridge": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Trainer: Preschooler Lin east of Nursery Aide": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Trainer: Twins Lia & Lily near dark grass": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Trainer: Nursery Aide Kimya in central clearing": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Item: In grass south of Twins": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Item: Ledge east of Nursery Aide": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Gift: Cheren near dark grass": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Trainer: Team Plasma Grunt near dark grass": lambda s, p, w: has_basic_badge(s, p),

    # Route 4 (south is early; north is gated past Colress by Insect badge)
    "Route 4 - Trainer: Trainer Colress blocking north road": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Gift: Colress after battle": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Gift: Ace Trainer in house": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Gift: Black Belt in first left house": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Gift: Waitress in final right house (Guess Pokémon cry)": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Western street": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Central ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: South of Roughneck Silvester": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Northeast hill": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Northwest ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Excavation pit south": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: 2F of Petilil trade house": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Item: Inside Cottonee trade house": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Lady Lina in central ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Backpacker Clifford in southeast": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Roughneck Joey in western fenced area": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Roughneck Silvester in northwest fenced area": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Policeman Dell in north near Nimbasa Gate": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Policeman Neagle on central road": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Biker Stanley in western fenced area": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Hooligans Rob & Sal on western street": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Rich Boy Keenan in west ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Backpacker Roland in north near Nimbasa Gate": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Backpacker Rachel in east ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Pokéfan Norbert in east": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Pokéfan Sachiko in northeast ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Twins Tara & Val in central ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Trainer: Youngster Sinclair in western fenced area": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Northern area between stairways": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Central deep sand north of fenced sand patch": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Eastern deep sand": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: In the middle of a sand patch": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Easternmost hidden item near barricade": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Southwest deep sand": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Northwest deep sand": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Far east deep sand": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Southeast deep sand near ruins": lambda s, p, w: has_insect_badge(s, p),
    "Route 4 - Hidden: Northeast deep sand": lambda s, p, w: has_insect_badge(s, p),

    # Route 20 south (across river, requires Basic Badge, surf and autumn)
    "Route 20 - Trainer: Pokemon Ranger Leaf on southeast island (Basic Badge, Autumn, Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Trainer: Pokemon Ranger Bret on central island (Basic Badge, Autumn, Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Trainer: Pokemon Ranger Malory on eastern island (Basic Badge, Autumn, Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Trainer: Pokemon Ranger Naoko above waterfall (Basic Badge, Autumn, Surf, Waterfall)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w) and can_use_waterfall(s, p, w),
    "Route 20 - Item: Dark grass patch past Hiker Jerome": lambda s, p, w: has_basic_badge(s, p),
    "Route 20 - Item: Island near Rangers northwest (Autumn, Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Item: Island near Rangers southeast (Autumn, Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Item: Cliff southeast of Cave of Being (Autumn, Surf, Waterfall)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_use_waterfall(s, p, w) and can_access_autumn(s, p, w),
    "Route 20 - Hidden: On eastern island (Surf)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w),
    "Route 20 - Hidden: Between central ledges (Surf, Waterfall)": lambda s, p, w: has_basic_badge(s, p) and can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 20 - Item: Behind leaf pile north of Youngster (Autumn)": lambda s, p, w: can_access_autumn(s, p, w),
    "Floccesy Town - Hidden: In dead end from Route 20 (Autumn)": lambda s, p, w: can_access_autumn(s, p, w),

    # Route 19 & Aspertia City & Virbank City
    "Route 19 - Item: Northern grass across water (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Item: Northeast up stairs across water (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Hidden: Below Alder on cliff (Defeat Cheren, Surf)": lambda s, p, w: can_use_surf(s, p, w) and has_basic_badge(s, p),
    "Aspertia City - Item: High grass patch across pond southeast (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Aspertia City - Gift: Girl in northeast house after defeating Cheren": lambda s, p, w: True,
    "Aspertia City - Gift: Bianca after defeating Cheren": lambda s, p, w: True,
    # Hall of Fame postgame gifts in s856 are bypassed when living_room_starter is enabled
    # "Aspertia City - Gift from Cedric after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    # "Aspertia City - Gift from Mom after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Floccesy Town - Gift: Bianca after defeating Cheren": lambda s, p, w: True,
    "Virbank City - Item: West of the Pokémon Center accessed from path above the Gym (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Virbank Complex - Item: End of the path behind the cut tree near the inside entrance (Cut)": lambda s, p, w: can_use_cut(s, p, w),

    # Castelia Sewers
    "Castelia Sewers - Item: North of Worker in west (Spring/Summer)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w),
    "Castelia Sewers - Item: Southwest of Janitor in east (Spring/Summer)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w),
    "Castelia Sewers - Item: West of Janitor in east (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Item: Near Worker in west (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Item: West of Relic Passage entrance (Spring/Summer)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w),
    "Castelia Sewers - Item: Southern canal west end (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Item: West of Scientist in southeast (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Trainer: Worker Scott in west (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Trainer: Scientist Caroline in centre-northeast (Autumn/Winter)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w),
    "Castelia Sewers - Trainer: Scientist Clarke in southeast (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Trainer: Janitor Brady in north (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Gift: Scientist in northern room (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Hidden: Northwest of Worker in west (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Hidden: Northeast of easternmost room (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Hidden: East of Worker in centre (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Hidden: In southern canal southwest of eastern Janitor (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia Sewers - Hidden: In southernmost area (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),

    # PWT (Plasma Frigate incident)
    "PWT - Trainer: Team Plasma Grunt 1 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),
    "PWT - Trainer: Team Plasma Grunt 2 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),
    "PWT - Trainer: Team Plasma Grunt 3 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),
    "PWT - Trainer: Team Plasma Grunt 4 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),
    "PWT - Trainer: Team Plasma Grunt 5 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),
    "PWT - Trainer: Team Plasma Grunt 6 (Plasma Frigate)": lambda s, p, w: has_quake_badge(s, p),

    # Route 6 & Mistralton Cave & Guidance Chamber
    "Route 6 - Gift: Cheren after PWT Plasma Frigate": lambda s, p, w: has_quake_badge(s, p),
    "Route 6 - Item: Behind the Season Research Lab (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 6 - Item: East of Pokemon Breeder (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 6 - Item: East of Season Research Lab (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 6 - Hidden: East of Season Research Lab (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Mistralton Cave - Item: 1F, west of Hiker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Mistralton Cave - Item: 1F, east of Hiker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Mistralton Cave - Hidden: 1F, east of the entrance (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Chargestone Cave (1F Full Heal, Yellow Shard, Max Repel, both Hyper Potions + Anna & Ronald are open; rest require Quake Badge)
    # 1F past bridge
    "Chargestone Cave - Trainer: Ace Trainer Corky (1F, southeast)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: 1F, central floating stones bridge": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Ace Trainer Mary (1F, north)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Hiker Otto (1F, northeast)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: 1F, northeast path near stairs": lambda s, p, w: has_quake_badge(s, p),

    # B1F past bridge
    "Chargestone Cave - Trainer: Ranger Briana (B1F, southeast)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Scientist Lumi (B1F, northeast)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Doctor Kit (B1F, centre-east)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Ranger Louis (1F, south)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: B1F, northwest cavern near Scientist": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: B1F, southeast ledge": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Hidden: B1F, north of Nugget Brothers": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Hidden: 1F, southwest of the cave, arriving from B1F": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Gift: Nugget Brothers on B1F": lambda s, p, w: has_quake_badge(s, p),

    # B2F past bridge
    "Chargestone Cave - Item: B2F, north corner near electric stone": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: B2F, west dead-end": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Item: B2F, south of Ace Trainer": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Hidden: B2F, at the dead end northeast of Ace Trainer": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Hiker Jeremy (B2F, west)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Ace Trainer Vicki (B2F, south)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Guitarist Beverly (B2F, northwest)": lambda s, p, w: has_quake_badge(s, p),
    "Chargestone Cave - Trainer: Ace Trainer Shaye (B2F, north)": lambda s, p, w: has_quake_badge(s, p),

    # Mistralton City gifting
    # "Mistralton City - Gift from TM collector in Pokemon Center 1": lambda s, p, w: has_tm_count(s, p, 35),
    # "Mistralton City - Gift from TM collector in Pokemon Center 2": lambda s, p, w: True,

    # Lostlorn Forest
    "Lostlorn Forest - Trainer: Veteran Murphy on cliff (Surf, Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Lostlorn Forest - Item: In the higher part (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Lostlorn Forest - Hidden: Behind Veteran in northwest corner of cliff (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),

    # Village Bridge
    "Village Bridge - Trainer: Fisherman Dean (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - Trainer: Youngster Karl (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - Item: On the middle patch of land supporting the bridge (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - Item: On the isle on the north part of the river (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Route 11, Route 13, Route 14 & Abundant Shrine
    "Route 11 - Trainer: Ranger Thalia (Waterfall)": lambda s, p, w: can_use_waterfall(s, p, w),
    "Route 11 - Trainer: Ranger Crofton (Waterfall)": lambda s, p, w: can_use_waterfall(s, p, w),
    "Route 11 - Item: Right of Pokemon Ranger Thalia (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 11 - Item: Up the northern waterfall on the western ledge (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 11 - Item: At the end of the short land strip west to the bridge, behind the fence (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 11 - Hidden: Up the northern waterfall on the eastern ledge (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),

    "Route 13 - Item: South of Ace Trainer Miguel (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 13 - Trainer: Parasol Lady Laura (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Item: On a hill near Parasol Lady Laura (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Hidden: On a hill near Parasol Lady Laura": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Trainer: Fisherman Vince (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - Item: Near Fisherman Vince (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - Item: On the island with dark grass (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 14 - Trainer: Ace Trainer Kipp (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Trainer: Ace Trainer Junko (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Trainer: Fisherman Sid (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Item: North of Backpacker Reece (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Trainer: Black Belt Jay (Surf, Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 14 - Trainer: Battle Girl Glinda (Surf, Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 14 - Item: Near Black Belt Jay (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 14 - Hidden: East of Black Belt Jay, near (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 14 - Hidden: On cliff east of Abundant Shrine entrance (Surf and Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),

    "Abundant Shrine - Item: East of the Landorus shrine (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Route 8 & Moor of Icirrus
    "Route 8 - Item: Near water in swamp north of bridge (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 8 - Item: Southwest from the Fisherman (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 8 - Trainer: Fisherman Ryder (Surf or Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Route 8 - Trainer: Parasol Lady Tyra (Surf or Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Route 8 - Hidden: Between Fisherman Ryder and Parasol Lady Tyra (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - Trainer: Fisherman Arnold (Surf or Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - Trainer: Fisherman Eustace (Surf or Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - Item: East of Fisherman Arnold (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - Item: South of Pokemon Ranger Elaine (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Clay Tunnel & Seaside Cave
    "Clay Tunnel - Trainer: Ranger Katie in Room 3 north (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Clay Tunnel - Hidden: Room 2 island rock in middle of pond (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Clay Tunnel - Hidden: Room 3 rock right of pond (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Clay Tunnel - Item: Room 2 southwest chamber upper item (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Clay Tunnel - Item: Room 1 southeast of Full Heal (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Clay Tunnel - Item: Room 2 southwest chamber lower item (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    "Seaside Cave - Item: 1F, on the small island east of the Black Belt Drago": lambda s, p, w: can_use_surf(s, p, w),
    "Seaside Cave - Trainer: Battle Girl Maki (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave - Item: B1F, north of Battle Girl Maki (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave - Item: 1F, north of Battle Girl Tia, accessible from B1F (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Route 2, Route 3, Route 22, Route 23, Dragonspiral Tower & Pinwheel Forest
    "Route 2 - Item: To the southwest (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 2 - Item: South of Lass Henrietta (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 2 - Hidden: Near the Lass past the small tree (Cut)": lambda s, p, w: can_use_cut(s, p, w),

    "Route 3 - Trainer: Fisherman Mack (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 3 - Item: North of Fisherman Mack (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 3 - Item: Northwest of Fisherman Mack (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 3 - Hidden: West of Fisherman Mack (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 22 - Item: West of the pond (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 23 - Trainer: Ranger Lena (Cut, Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Trainer: Ranger Steve (Cut, Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Trainer: Ace Trainer Tom (Cut, Waterfall)": lambda s, p, w: can_use_cut(s, p, w) and can_use_waterfall(s, p, w),
    "Route 23 - Trainer: Ace Trainer Miki (Cut, Waterfall)": lambda s, p, w: can_use_cut(s, p, w) and can_use_waterfall(s, p, w),
    "Route 23 - Item: At the end of a stream past the first house (Cut or Surf)": lambda s, p, w: can_use_cut(s, p, w) or can_use_surf(s, p, w),
    "Route 23 - Item: At a dead end above Ace Trainer Tom (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 23 - Item: At a dead end in the southwestern-most section of the forest, past Hiker Doug (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 23 - Item: On the pedestal where Azelf appears (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 23 - Item: At a dead end west of Black Belt Benjamin (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 23 - Item: Near Battle Girl Tiffany on a mountaintop (Cut and Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Item: On a lone mountaintop (Cut and Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Item: In a grass patch to the northeast of the Strength puzzle (Cut and Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Hidden: In a rock south of the Strength puzzle (Cut and Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),
    "Route 23 - Hidden: At a dead end in the beginning of the forest section (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 23 - Hidden: On a lone mountaintop (Cut and Strength)": lambda s, p, w: can_use_cut(s, p, w) and can_use_strength(s, p, w),

    "Dragonspiral Tower - Item: Eastern edge of the outside area (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Dragonspiral Tower - Item: Entrance, on the slope at the exit of Icirrus City (Winter)": lambda s, p, w: can_access_winter(s, p, w),

    # Twist Mountain seasonal items
    "Twist Mountain - Item: East of Veteran Zach (Winter)": lambda s, p, w: can_access_winter(s, p, w),
    "Twist Mountain - Item: South of Worker Ryan (Winter)": lambda s, p, w: can_access_winter(s, p, w),
    "Twist Mountain - Hidden: Outside, inside the trash can next to the vending machine (Spring/Summer/Autumn)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w) or can_access_autumn(s, p, w),
    "Twist Mountain - Hidden: Inside boulder on worker terrace (Spring/Summer/Autumn)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w) or can_access_autumn(s, p, w),
    "Pinwheel Forest - Item: Outer forest south of Lass Helia (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Route 5
    "Route 5 - Trainer: Motorcyclist Charles on road (Bolt Badge)": lambda s, p, w: has_bolt_badge(s, p),

    # Route 15 & Route 16 & Route 18
    "Route 15 - Item: Southeast of the Black CityB2/White ForestW2 gate (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 15 - Hidden: On the ground by the dark grass (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Item: In the area north of the Strength boulder (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Item: North of Backpacker (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 16 - Hidden: North of Backpacker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Trainer: Backpacker Blossom in northeast (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 18 - Item: South of the house, near Veteran Vincent (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 18 - Item: South of the house, southwest of Black Belt Zachary (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 18 - Hidden: South of the house, southeast of Black Belt Zachary (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Route 1 & Striaton City & Dreamyard & Nacrene City
    "Route 1 - Item: West of the waterfront near the 17 gate (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 1 - Item: In the south (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 1 - Hidden: In the central patch of dark tall grass (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Striaton City - Hidden: To the right of the Route 3 entrance (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Dreamyard - Item: Northern area: south of the stairs to the second floor of the ruins (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Dreamyard - Item: Northern area: on the far south part of the second floor of the ruins (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Dreamyard - Item: Northern area: in the patch of tall grass in the west (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Nacrene City - Gift: Dancer on southern street (Winter)": lambda s, p, w: can_access_winter(s, p, w),

    # Wellspring Cave
    "Wellspring Cave - Trainer: Veteran Shaun (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Trainer: Battle Girl Maggie (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Trainer: Battle Girl Xiao (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Trainer: Black Belt Edward (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Trainer: Black Belt Thomas (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Item: B1F northern pool chamber": lambda s, p, w: can_use_flash(s, p, w),
    "Wellspring Cave - Item: B1F, On cliff, south of Battle Girl Xiao": lambda s, p, w: can_use_flash(s, p, w),
    "Wellspring Cave - Item: 1F, West of Battle Girl Maggie (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Item: B1F, Southeast of Black Belt Thomas, before ledge (Surf)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Item: B1F, Northern end (Surf)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Hidden: B1F, East of Black Belt Thomas": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Hidden: B1F, East of Veteran Shaun (Surf)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),
    "Wellspring Cave - Hidden: B1F, Southwest of Veteran Shaun (Surf)": lambda s, p, w: can_use_surf(s, p, w) and can_use_flash(s, p, w),

    # Relic Passage & Relic Castle
    "Relic Passage - Item: Middle section south room upper item (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Relic Passage - Item: Middle section south room middle item (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Relic Passage - Item: Middle section south room lower item (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Relic Passage - Item: Middle section west of Hiker (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Relic Passage - Hidden: Middle section south room (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Relic Castle - Item: Lowest floor easternmost room (Relic Passage)": lambda s, p, w: s.can_reach("Relic Passage", "Region", p),
    "Relic Castle - Hidden: In Volcarona room (Relic Passage)": lambda s, p, w: s.can_reach("Relic Passage", "Region", p),

    # Giant Chasm & Humilau City & Nature Preserve
    "Giant Chasm - Item: Crater southwest behind Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Item: Northeast of southwest corner, on the other side of a Strength boulder (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Item: At the north end of the pool of water near the 22 entrance (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Giant Chasm - Hidden: Behind a Strength boulder near the northeastern corner (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Trainer: Team Plasma Ghetsis (Plasma Frigate)": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Item: Crater southeast corner path": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Item: Next to a batch of dark tall grass in the northwest, after defeating Ghetsis": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Item: In a dead end north of the center, after defeating Ghetsis": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Item: East of where the Plasma Frigate used to be, after defeating Ghetsis": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Item: West of the spot where the Plasma Frigate used to be, after defeating Ghetsis": lambda s, p, w: can_board_plasma_frigate(s, p),
    "Giant Chasm - Gift: Cheren after defeating Kyurem (Kyurem)": lambda s, p, w: can_access_legendary_location("kyurem", s, p, w),
    "Humilau City - Item: North of the Gym (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Nature Preserve - Item: On the cliff in the extreme northeast (Waterfall)": lambda s, p, w: can_use_waterfall(s, p, w),

    # Victory Road
    "Victory Road - Trainer: Ace Trainer Billy (Black 2 or Strength)": lambda s, p, w: _is_version(w, ("black2", "black_2", "b2")) or can_use_strength(s, p, w),
    "Victory Road - Trainer: Ace Trainer Jamie (White 2 or Strength)": lambda s, p, w: _is_version(w, ("white2", "white_2", "w2")) or can_use_strength(s, p, w),
    "Victory Road - Item: Grove southwestern corner (Cut)": lambda s, p, w: can_use_strength(s, p, w) and can_use_cut(s, p, w),
    "Victory Road - Item: Outside 1 southeastern corner": lambda s, p, w: can_use_strength(s, p, w) and can_use_cut(s, p, w),
    "Victory Road - Item: Northern cave dark chamber (Flash)": lambda s, p, w: can_use_strength(s, p, w) and can_use_flash(s, p, w),
    "Victory Road - Hidden: In Northern dark cave stalagmite": lambda s, p, w: can_use_strength(s, p, w) and can_use_flash(s, p, w),
    **{name: (lambda s, p, w: can_use_strength(s, p, w)) for name in _VICTORY_ROAD_STRENGTH_LOCATIONS},

    # Castelia City back alley requirements
    "Castelia City - Item: Back alley accessible from sewers near trainers (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia City - Item: Back alley accessible from sewers southern corner (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia City - Trainer: Back alley accessible from sewers - Roughneck Ricky (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia City - Trainer: Back alley accessible from sewers - Dancer Jean-Paul (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),
    "Castelia City - Trainer: Back alley accessible from sewers - Guitarist Tina (Spring/Summer, Surf)": lambda s, p, w: can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w)),

    # Postgame / Hall of Fame locations
    "Floccesy Town - Trainer: PkMn Trainer Alder": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Trainer: Trainer Cynthia": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Driftveil City - Hidden: In the pile of dirt south of the Clay Tunnel entrance, accessible after entering the Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Trainer: Castelia Street - GAME FREAK Morimoto (Game Freak, Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Trainer: Castelia Street - GAME FREAK Nishino (Game Freak, Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Trainer: PkMn Trainer Hugh (Post-Game)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Shauntal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Grimsley": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Marshal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Caitlin": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Champion Iris": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
}
