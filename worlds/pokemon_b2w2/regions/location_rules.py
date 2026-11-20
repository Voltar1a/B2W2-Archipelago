from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from BaseClasses import CollectionState

from .roadblocks import (
    can_use_cut,
    can_use_surf,
    can_use_strength,
    can_use_waterfall,
    can_use_dive,
    can_use_flash,
    has_super_rod,
    can_access_spring,
    can_access_summer,
    can_access_autumn,
    can_access_winter,
    can_access_sunday,
    can_access_wednesday,
    can_access_thursday,
    can_access_saturday,
    has_basic_badge,
    has_toxic_badge,
    has_insect_badge,
    has_bolt_badge,
    has_quake_badge,
    has_jet_badge,
    has_legend_badge,
    has_colress_mchn,
    has_tm_count,
    can_board_plasma_frigate,
    can_enter_marine_tube,
    can_enter_hall_of_fame,
    can_access_legendary_location,
)

if TYPE_CHECKING:
    from .. import PokemonB2W2World


def _is_version(world: "PokemonB2W2World" | None, keys: tuple[str, ...]) -> bool:
    ver = getattr(getattr(world, "options", None), "version", None) if world else None
    return ver is not None and ver.current_key in keys




LOCATION_RULES: dict[str, Callable[[CollectionState, int, PokemonB2W2World], bool]] = {
    # Gym leaders and badges progression prerequisites
    "Castelia Gym - Trainer: Gym Leader Burgh": lambda s, p, w: has_toxic_badge(s, p),
    "Castelia Gym - Gym Leader Burgh Insect Badge": lambda s, p, w: has_toxic_badge(s, p),
    "Nimbasa Gym - Trainer: Gym Leader Elesa": lambda s, p, w: has_insect_badge(s, p),
    "Nimbasa Gym - Gym Leader Elesa Bolt Badge": lambda s, p, w: has_insect_badge(s, p),

    # Route 20 (west is early; east is gated past Hiker Jerome by Basic badge)

    # Route 4 (south is early; north is gated past Colress by Insect badge)

    # Route 20 south (across river, requires Basic Badge, surf and autumn)
    "Route 20 - Hidden: On eastern island (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 20 - Hidden: Between central ledges (Surf, Waterfall)": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 20 - Item: Behind leaf pile north of Youngster (Autumn)": lambda s, p, w: can_access_autumn(s, p, w),

    # Route 19 & Aspertia City & Virbank City
    "Route 19 - Item: Northern grass across water (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Item: Northeast up stairs across water (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Hidden: Below Alder on cliff (Defeat Cheren, Surf)": lambda s, p, w: can_use_surf(s, p, w) and has_basic_badge(s, p),
    "Aspertia City - Item: Across pond southeast (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Aspertia City - Gift: Girl in northeast house after defeating Cheren": lambda s, p, w: True,
    "Aspertia City - Gift: Bianca after defeating Cheren": lambda s, p, w: True,
    # Hall of Fame postgame gifts in s856 are bypassed when living_room_starter is enabled
    # "Aspertia City - Gift from Cedric after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    # "Aspertia City - Gift from Mom after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Floccesy Town - Gift: Bianca after defeating Cheren": lambda s, p, w: True,
    "Virbank City - Item: West of the Pokémon Center accessed from path above the Gym (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Virbank Complex - Item: End of the path behind the cut tree near the inside entrance (Cut)": lambda s, p, w: can_use_cut(s, p, w),

    # Castelia Sewers
    "Castelia Sewers - Item: West of Janitor in east (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Item: Near Worker in west (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Trainer: Worker Scott in west (Autumn/Winter or Spring/Summer, Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),

    # PWT (Plasma Frigate incident)

    # Route 6 & Mistralton Cave & Guidance Chamber
    "Route 6 - Gift: Cheren after PWT Plasma Frigate": lambda s, p, w: has_quake_badge(s, p),
    "Mistralton Cave - Item: 1F, west of Hiker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Mistralton Cave - Item: 1F, east of Hiker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Mistralton Cave - Hidden: 1F, east of the entrance (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Chargestone Cave (1F Full Heal, Yellow Shard, Max Repel, both Hyper Potions + Anna & Ronald are open; rest require Quake Badge)
    # 1F past bridge

    # B1F past bridge

    # B2F past bridge

    # Mistralton City TM Collector
    "Mistralton City - Gift: TM collector in Pokemon Center (10 TMs)": lambda s, p, w: has_tm_count(s, p, 10),
    "Mistralton City - Gift: TM collector in Pokemon Center (20 TMs)": lambda s, p, w: has_tm_count(s, p, 20),
    "Mistralton City - Gift: TM collector in Pokemon Center (35 TMs)": lambda s, p, w: has_tm_count(s, p, 35),
    "Mistralton City - Gift: TM collector in Pokemon Center (50 TMs)": lambda s, p, w: has_tm_count(s, p, 50),
    "Mistralton City - Gift: TM collector in Pokemon Center (70 TMs)": lambda s, p, w: has_tm_count(s, p, 70),
    "Mistralton City - Gift: TM collector in Pokemon Center (95 TMs)": lambda s, p, w: has_tm_count(s, p, 95),

    # Lostlorn Forest

    # Village Bridge
    "Village Bridge - Trainer: Fisherman Dean (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - Item: On the middle patch of land supporting the bridge (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - Item: On the isle on the north part of the river (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Route 11, Route 13, Route 14 & Abundant Shrine
    "Route 11 - Item: At the end of the short land strip west to the bridge, behind the fence (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 13 - Item: South of Ace Trainer (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 13 - Item: On a hill near Parasol Lady (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Hidden: On a hill near Parasol Lady (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Trainer: Fisherman Vince north-east of dark grass island (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - Item: Near Fisherman (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - Item: On the island with dark grass (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 14 - Trainer: Backpacker Reece (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Item: North of Backpacker (Surf)": lambda s, p, w: can_use_surf(s, p, w),


    # Twist Mountain & Icirrus City
    "Icirrus City - Item: West of Pokemon Center (Winter)": lambda s, p, w: can_access_winter(s, p, w),

    # Route 8 & Moor of Icirrus
    "Route 8 - Item: Southwest from the Fisherman (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Route 8 - Hidden: Between Fisherman and Parasol Lady (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - Item: In the gap between trees north-east of the entrance (Spring/Summer/Autumn)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w) or can_access_autumn(s, p, w),
    "Moor of Icirrus - Item: East of Fisherman in the north (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),

    # Clay Tunnel & Seaside Cave

    "Seaside Cave - Item: 1F, on the small island east of Black Belt (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Seaside Cave - Trainer: Battle Girl Maki (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave - Item: B1F, north of Battle Girl (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave - Item: 1F, north of Battle Girl, accessible from B1F (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Route 2, Route 3, Route 22, Route 23, Dragonspiral Tower & Pinwheel Forest
    "Route 2 - Item: To the southwest (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 2 - Item: South of Lass (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 2 - Hidden: Near the Lass past the small tree (Cut)": lambda s, p, w: can_use_cut(s, p, w),


    "Route 22 - Item: West of the pond (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    "Route 23 - Gift: Ace Trainer in house": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - Item: At the end of a stream past the first house (Cut or Surf)": lambda s, p, w: can_use_cut(s, p, w) or can_use_surf(s, p, w),

    "Dragonspiral Tower - Item: Eastern edge of the outside area (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Dragonspiral Tower - Item: On the slope at the exit of Icirrus City (Winter)": lambda s, p, w: can_access_winter(s, p, w),

    # Twist Mountain seasonal items
    "Pinwheel Forest - Item: Outer forest south of Lass (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Route 5
    "Route 5 - Trainer: Motorcyclist Charles on road (Bolt Badge)": lambda s, p, w: has_bolt_badge(s, p),

    # Route 15 & Route 16 & Route 18
    "Route 15 - Item: Southeast of the Black City/White Forest gate (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 15 - Hidden: On the ground by the dark grass (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Item: In the area north of the Strength boulder (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Item: North of Backpacker (Cut)": lambda s, p, w: can_use_cut(s, p, w),
    "Route 16 - Hidden: North of Backpacker (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Trainer: Backpacker Blossom in northeast (Strength)": lambda s, p, w: can_use_strength(s, p, w),

    # Route 1, Route 3, Pinwheel Forest, Striaton City, Dreamyard & Nacrene City
    "Route 3 - Gift: School Kid after Habitat List": lambda s, p, w: has_super_rod(s, p),
    "Pinwheel Forest - Gift: Scientist after Habitat List": lambda s, p, w: can_use_surf(s, p, w) and has_super_rod(s, p),
    "Striaton City - Gift: Fisherman left of Route 3 gate (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Striaton City - Hidden: To the right of the Route 3 entrance (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Nacrene City - Gift: Customer in Cafe Warehouse (Sun/Thu)": lambda s, p, w: can_access_sunday(s, p, w) and can_access_thursday(s, p, w),
    "Nacrene City - Gift: Waitress in Cafe Warehouse (Wed/Sat)": lambda s, p, w: can_access_wednesday(s, p, w) or can_access_saturday(s, p, w),
    "Abyssal Ruins - Gift: 4F, central altar chamber crown": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Undella Town - Gift: Zinzolin in front of gate": lambda s, p, w: can_use_surf(s, p, w) and can_use_dive(s, p, w) and can_use_flash(s, p, w) and can_use_strength(s, p, w),

    # Wellspring Cave
    "Wellspring Cave - Trainer: Veteran Shaun (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Trainer: Battle Girl Xiao (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Trainer: Black Belt Edward (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Trainer: Black Belt Thomas (Surf, Flash)": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave - Item: 1F, West of Battle Girl (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Relic Passage & Relic Castle
    "Relic Passage - Item: Middle section west of Hiker (Surf)": lambda s, p, w: can_use_surf(s, p, w),

    # Giant Chasm & Humilau City & Nature Preserve
    "Giant Chasm - Item: Crater southwest behind Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Item: Northeast of southwest corner, on the other side of a Strength boulder (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Item: At the north end of the pool of water near the Route 22 entrance (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Giant Chasm - Hidden: Behind a Strength boulder near the northeastern corner (Strength)": lambda s, p, w: can_use_strength(s, p, w),
    "Humilau City - Item: North of the Gym (Surf)": lambda s, p, w: can_use_surf(s, p, w),
    "Nature Preserve - Item: On the cliff in the extreme northeast (Waterfall)": lambda s, p, w: can_use_waterfall(s, p, w),

    # Route 1 & Route 18

    # Victory Road


    # Postgame / Hall of Fame locations
    "Floccesy Town - Trainer: PkMn Trainer Alder": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Trainer: Trainer Cynthia": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Gift: Hugh in front of Marine Tube gate": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Driftveil City - Hidden: In the pile of dirt south of the Clay Tunnel entrance, accessible after entering the Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Trainer: Castelia Street - GAME FREAK Morimoto at Game Freak (Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Trainer: Castelia Street - GAME FREAK Nishino at Game Freak (Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower - Trainer: 1F, Waitress Jan after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower - Trainer: 2F, Nursery Aide Ilse after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower - Trainer: 3F, Clerk (F) Lana after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower - Trainer: 4F, Maid Tammy after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Trainer: PkMn Trainer Hugh (Post-Game)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Humilau City - Gift: Couple after Celestial Tower bell": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Village Bridge - Gift: Baker after battle (Post-Game)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Skyarrow Bridge - Gift: Runner after bridge quest": lambda s, p, w: can_enter_hall_of_fame(s, p, w) and has_bolt_badge(s, p) and has_jet_badge(s, p) and can_enter_marine_tube(s, p),
    "Pokemon League - Trainer: Rematch Elite Four Shauntal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Grimsley": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Marshal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Elite Four Caitlin": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokemon League - Trainer: Rematch Champion Iris": lambda s, p, w: can_enter_hall_of_fame(s, p, w),

    # Pokemon Ranger post-battle Berry gifts
}
