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
    has_prop_case,
    has_tm_count,
    can_board_plasma_frigate,
    can_enter_marine_tube,
    can_enter_hall_of_fame,
    can_access_legendary_location,
    get_version_key,
)

if TYPE_CHECKING:
    from .. import PokemonB2W2World


def _is_version(world: "PokemonB2W2World" | None, keys: tuple[str, ...]) -> bool:
    ver = getattr(getattr(world, "options", None), "version", None) if world else None
    return ver is not None and ver.current_key in keys




LOCATION_RULES: dict[str, Callable[[CollectionState, int, PokemonB2W2World], bool]] = {
    # Gym leaders and badges progression prerequisites
    "Castelia Gym - Gym Leader Burgh": lambda s, p, w: has_toxic_badge(s, p),
    "Castelia Gym - Gym Leader Burgh Insect Badge": lambda s, p, w: has_toxic_badge(s, p),
    "Nimbasa Gym - Gym Leader Elesa": lambda s, p, w: has_insect_badge(s, p),
    "Nimbasa Gym - Gym Leader Elesa Bolt Badge": lambda s, p, w: has_insect_badge(s, p),

    # Route 20 south (across river, requires Basic Badge, surf and autumn)
    "Route 20 - Hidden on eastern island": lambda s, p, w: can_use_surf(s, p, w),
    "Route 20 - Hidden between central ledges": lambda s, p, w: can_use_surf(s, p, w) and can_use_waterfall(s, p, w),
    "Route 20 - Behind leaf pile north of Youngster (Autumn)": lambda s, p, w: can_access_autumn(s, p, w),

    # Route 19 & Aspertia City & Virbank City
    "Route 19 - Northwest across water": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Northeast up stairs across water": lambda s, p, w: can_use_surf(s, p, w),
    "Route 19 - Hidden below Alder on cliff after beating Cheren": lambda s, p, w: can_use_surf(s, p, w) and has_basic_badge(s, p),
    "Aspertia City - Across pond southeast": lambda s, p, w: can_use_surf(s, p, w),
    "Aspertia City - Girl in northeast house after defeating Cheren": lambda s, p, w: True,
    "Aspertia City - Bianca after defeating Cheren": lambda s, p, w: True,
    # Hall of Fame postgame gifts in s856 are bypassed when living_room_starter is enabled
    # "Aspertia City - Gift from Cedric after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    # "Aspertia City - Gift from Mom after entering Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Floccesy Town - Bianca after defeating Cheren": lambda s, p, w: True,
    "Virbank City - West of the Pokémon Center accessed from path above the Gym": lambda s, p, w: can_use_surf(s, p, w),
    "Virbank Complex - End of the path behind the Cut tree near the inside entrance": lambda s, p, w: can_use_cut(s, p, w),

    # Castelia Sewers
    "Castelia Sewers - West of Janitor in east (Autumn/Winter or Spring/Summer + Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Near Worker in west (Autumn/Winter or Spring/Summer + Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),
    "Castelia Sewers - Worker Scott in west (Autumn/Winter or Spring/Summer + Surf)": lambda s, p, w: can_access_autumn(s, p, w) or can_access_winter(s, p, w) or (can_use_surf(s, p, w) and (can_access_spring(s, p, w) or can_access_summer(s, p, w))),

    # Mistralton City TM Collector
    "Mistralton City - TM collector in house east of Pokémon Center (10 TMs)": lambda s, p, w: has_tm_count(s, p, 10),
    "Mistralton City - TM collector in house east of Pokémon Center (20 TMs)": lambda s, p, w: has_tm_count(s, p, 20),
    "Mistralton City - TM collector in house east of Pokémon Center (35 TMs)": lambda s, p, w: has_tm_count(s, p, 35),
    "Mistralton City - TM collector in house east of Pokémon Center (50 TMs)": lambda s, p, w: has_tm_count(s, p, 50),
    "Mistralton City - TM collector in house east of Pokémon Center (70 TMs)": lambda s, p, w: has_tm_count(s, p, 70),
    "Mistralton City - TM collector in house east of Pokémon Center (95 TMs)": lambda s, p, w: has_tm_count(s, p, 95),

    # Village Bridge
    "Village Bridge - Fisherman in third house from the right after meeting him on Route 8 east": lambda s, p, w: s.can_reach("Route 8", "Region", p),
    "Village Bridge - Fisherman Dean on the central island below the bridge": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - On the central island below the bridge": lambda s, p, w: can_use_surf(s, p, w),
    "Village Bridge - On the isle on the north part of the river": lambda s, p, w: can_use_surf(s, p, w),

    # Route 11, Route 13, Route 14 & Abundant Shrine
    "Route 11 - At the end of the short land strip west of the bridge, behind the fence": lambda s, p, w: can_use_surf(s, p, w),

    "Route 13 - Behind Cut tree in the southwest": lambda s, p, w: can_use_cut(s, p, w),
    "Route 13 - On a hill in the southwest": lambda s, p, w: can_use_strength(s, p, w),
    "Route 13 - Fisherman Vince in shallow water in the centre east across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - In shallow water in the centre east across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Route 13 - On the island with dark grass in the centre east": lambda s, p, w: can_use_surf(s, p, w),

    "Route 14 - Backpacker Reece on the cliffs between waterfalls in the northeast": lambda s, p, w: can_use_surf(s, p, w),
    "Route 14 - Between three waterfalls in the northeast": lambda s, p, w: can_use_surf(s, p, w),


    # Twist Mountain & Icirrus City
    "Icirrus City - West of Pokémon Center (Winter)": lambda s, p, w: can_access_winter(s, p, w),

    # Route 8 & Moor of Icirrus
    "Route 8 - Southwest from the Fisherman in the east": lambda s, p, w: can_use_surf(s, p, w),
    "Route 8 - Hidden between Fisherman and Parasol Lady in north (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),
    "Moor of Icirrus - In the gap between trees northeast of the entrance (Spring/Summer/Autumn)": lambda s, p, w: can_access_spring(s, p, w) or can_access_summer(s, p, w) or can_access_autumn(s, p, w),
    "Moor of Icirrus - East of Fisherman in the north (Surf, Winter)": lambda s, p, w: can_use_surf(s, p, w) or can_access_winter(s, p, w),

    # Clay Tunnel & Seaside Cave
    "Clay Tunnel - Hidden Twist Mountain side rock by Underground Ruins entrance": lambda s, p, w: can_use_surf(s, p, w) and can_use_strength(s, p, w),
    "Clay Tunnel - Hidden Twist Mountain side rock right of pond": lambda s, p, w: can_use_surf(s, p, w) and can_use_strength(s, p, w),

    "Seaside Cave 1F - on the small island east of Black Belt in southeast": lambda s, p, w: can_use_surf(s, p, w),
    "Seaside Cave B1F - Battle Girl Maki southeast": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave B1F - between all the Strength boulders": lambda s, p, w: can_use_strength(s, p, w),
    "Seaside Cave 1F - north accessible from B1F": lambda s, p, w: can_use_strength(s, p, w),

    # Route 2, Route 3, Route 22, Route 23, Dragonspiral Tower & Pinwheel Forest
    "Route 2 - Behind Strength boulder in the south": lambda s, p, w: can_use_strength(s, p, w),
    "Route 2 - South of Lass behind Cut tree in the northwest": lambda s, p, w: can_use_cut(s, p, w),
    "Route 2 - Hidden near the Lass behind Cut tree in the northwest": lambda s, p, w: can_use_cut(s, p, w),
    "Route 2 - Lass Henrietta behind Cut tree in the northwest": lambda s, p, w: can_use_cut(s, p, w),


    "Route 22 - West of the pond in the south": lambda s, p, w: can_use_surf(s, p, w),

    "Route 23 - Old man in house at end of stream across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - At the end of a stream past the first house in the southeast": lambda s, p, w: can_use_cut(s, p, w) or can_use_surf(s, p, w),
    "Route 23 - Near Battle Girl on a mountaintop in the north after the Strength puzzle": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - On a lone mountaintop in the north after the Strength puzzle": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - Hidden in a rock south of the Strength puzzle in the northwest": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - Hidden on a lone mountaintop in the north after the Strength puzzle": lambda s, p, w: can_use_surf(s, p, w),
    "Route 23 - Battle Girl Tiffany in the north after the Strength puzzle": lambda s, p, w: can_use_surf(s, p, w),

    "Dragonspiral Tower - Cedric at tower entrance": lambda s, p, w: s.has("Light Stone", p) if _is_version(w, ("white2", "white_2", "w2")) else s.has("Dark Stone", p),
    "Dragonspiral Tower - Eastern edge of the outside area": lambda s, p, w: can_use_surf(s, p, w),
    "Dragonspiral Tower - On the slope at the exit of Icirrus City (Winter)": lambda s, p, w: can_access_winter(s, p, w),
    "Dragonspiral Tower 2F - on top of a pillar in the southwest": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 3F - northeast corner": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 3F - on a platform in the middle of the floor": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 4F - northeast platform top": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 4F - northeast platform middle": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 4F - northeast platform bottom": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 5F - first ring": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 5F - second ring": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 5F - third ring": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 6F - northeast corner": lambda s, p, w: can_use_strength(s, p, w),
    "Dragonspiral Tower 7F - Hidden northeast corner": lambda s, p, w: can_use_strength(s, p, w),

    # Route 5
    "Route 5 - Motorcyclist Charles on road": lambda s, p, w: has_bolt_badge(s, p),
    "Route 5 - Musician Preston on road": lambda s, p, w: has_prop_case(s, p),

    # Victory Road
    "Victory Road - Section 1 via Black Bridge, Ace Trainer Billy past Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Victory Road - Bonus: Black Bridge, Ace Trainer Chandra across water in southeast": lambda s, p, w: can_use_surf(s, p, w),
    "Victory Road - Bonus: Black Bridge, across water in southeast": lambda s, p, w: can_use_surf(s, p, w),
    "Victory Road - Section 3: Cave, southeast across pond in Flash section": lambda s, p, w: can_use_surf(s, p, w),
    "Victory Road - Section 4: Cave, southeast across pond in Flash section": lambda s, p, w: can_use_surf(s, p, w),
    "Victory Road - Hidden section 3: Cave, east across pond in Flash section": lambda s, p, w: can_use_surf(s, p, w),
    "Victory Road - Hidden section 4: Cave, east across pond in Flash section": lambda s, p, w: can_use_surf(s, p, w),

    # Route 15 & Route 16 & Route 18
    "Route 15 - Southeast past the Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Route 15 - Hidden on the ground by the dark grass in the north past the Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - In the area north of the Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Behind Cut tree in northwest": lambda s, p, w: can_use_cut(s, p, w),
    "Route 16 - Hidden north of Backpacker behind the Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Route 16 - Backpacker Blossom behind the Strength boulder": lambda s, p, w: can_use_strength(s, p, w),

    # Route 1, Route 3, Pinwheel Forest, Striaton City, Dreamyard & Nacrene City
    "Route 3 - School Kid after Habitat List in the north": lambda s, p, w: has_super_rod(s, p),
    "Pinwheel Forest - Inside: Centre inner forest accessed with Surf from the east": lambda s, p, w: can_use_surf(s, p, w),
    "Pinwheel Forest - Inside: Scientist after Habitat List south": lambda s, p, w: can_use_surf(s, p, w) and has_super_rod(s, p),
    "Striaton City - Fisherman left of Route 3 gate across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Striaton City - Hidden to the right of the Route 3 entrance across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Nacrene City - Waitress in lower section of Café Warehouse (Sun)": lambda s, p, w: can_access_sunday(s, p, w),
    "Nacrene City - Waitress in lower section of Café Warehouse (Sun/Thu)": lambda s, p, w: s.has("Grubby Hanky", p) and can_access_sunday(s, p, w) and can_access_thursday(s, p, w),
    "Nacrene City - Waitress by entrance inside of Café Warehouse (Wed/Sat)": lambda s, p, w: can_access_wednesday(s, p, w) or can_access_saturday(s, p, w),
    "Abyssal Ruins 4F - central altar chamber crown": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 2F - southwest quadrant": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - near entrance from 1F": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - northeast quadrant": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - southwest quadrant silver": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - northwest quadrant": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - northeast quadrant gold": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - along east wall": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - northwest corner": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - southeast corner": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - northeast quadrant band": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 2F - southwest corner statue": lambda s, p, w: can_use_flash(s, p, w),
    "Abyssal Ruins 3F - south side": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - southwest corner": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - northeast corner": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - along west wall": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - northeast quadrant band": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - southeast quadrant band": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - center of room": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Abyssal Ruins 3F - northwest corner statue": lambda s, p, w: can_use_flash(s, p, w) and can_use_strength(s, p, w),
    "Undella Town - Zinzolin in front of gate": lambda s, p, w: can_use_surf(s, p, w) and can_use_dive(s, p, w) and can_use_flash(s, p, w) and can_use_strength(s, p, w),

    # Wellspring Cave
    "Wellspring Cave 1F - Battle Girl Maggie west across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Wellspring Cave 1F - West of Battle Girl across the water": lambda s, p, w: can_use_surf(s, p, w),

    # Relic Passage & Relic Castle
    "Relic Passage - Middle section west across the water": lambda s, p, w: can_use_surf(s, p, w),
    "Relic Castle - Easternmost room accessed from Relic Passage": lambda s, p, w: can_use_strength(s, p, w),
    "Relic Castle - Hidden centre of room below Volcarona's room accessed from Relic Passage": lambda s, p, w: can_use_strength(s, p, w),

    # Giant Chasm & Humilau City & Nature Preserve
    "Giant Chasm - Cave, northwest behind Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Cave, northeast of southwest corner, on the other side of a Strength boulder": lambda s, p, w: can_use_strength(s, p, w),
    "Giant Chasm - Cave, at the north end of the pool of water near the Route 22 entrance": lambda s, p, w: can_use_surf(s, p, w),
    "Giant Chasm - Hidden cave, behind a Strength boulder near the northeastern corner": lambda s, p, w: can_use_strength(s, p, w),
    "Humilau City - Northwest behind the Gym": lambda s, p, w: can_use_surf(s, p, w),
    "Nature Preserve - On the cliff in the extreme northeast": lambda s, p, w: can_use_waterfall(s, p, w),

    # Postgame / Hall of Fame locations
    "Floccesy Town - PkMn Trainer Alder": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Driftveil City - PkMn Trainer Hugh (Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Trainer Cynthia": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - Hugh in front of Marine Tube gate": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Driftveil City - Hidden in the pile of dirt south of the Clay Tunnel entrance, accessible after entering the Hall of Fame": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Castelia Street - GAME FREAK Morimoto at Game Freak (Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Castelia City - Castelia Street - GAME FREAK Nishino at Game Freak (Post-HoF)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower 1F - Waitress Jan after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower 2F - Nursery Aide Ilse after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower 3F - Clerk (F) Lana after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Celestial Tower 4F - Maid Tammy after starting quest in Humilau": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Undella Town - PkMn Trainer Hugh (Post-Game)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Humilau City - Couple outside Pokémon Center after ringing Celestial Tower bell": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Humilau City - Nurse in northeastern house": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Village Bridge - Baker after battle (Post-Game)": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Skyarrow Bridge - Runner after bridge quest": lambda s, p, w: can_enter_hall_of_fame(s, p, w) and has_bolt_badge(s, p) and has_jet_badge(s, p) and can_enter_marine_tube(s, p),
    "Pokémon League - Rematch Elite Four Shauntal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokémon League - Rematch Elite Four Grimsley": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokémon League - Rematch Elite Four Marshal": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokémon League - Rematch Elite Four Caitlin": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
    "Pokémon League - Rematch Champion Iris": lambda s, p, w: can_enter_hall_of_fame(s, p, w),
}
