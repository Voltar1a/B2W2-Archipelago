from __future__ import annotations

# NPC gift checks (domain: 300000 + idx)
NPC_GIFT_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Abundant Shrine
    'Abundant Shrine - Gift: Elder near Landorus shrine': (300215, 1710, 'Abundant Shrine', None),

    # Abyssal Ruins
    'Abyssal Ruins - Gift: 4F, central altar chamber crown': (300164, 1469, 'Abyssal Ruins', None),

    # Accumula Town
    'Accumula Town - Gift: Youngster in southwest': (300220, 2766, 'Accumula Town', None),
    'Accumula Town - Gift: Lass in northeast': (300221, 2767, 'Accumula Town', None),
    'Accumula Town - Gift: Man in northern building 2F': (300223, 335, 'Accumula Town', None),
    'Accumula Town - Gift: Girl in northwest building 2F after quiz': (300225, 337, 'Accumula Town', None),
    'Accumula Town - Gift: Pianist in northeastern house': (300228, 2335, 'Accumula Town', None),
    'Accumula Town - Gift: Man in northwest building 2F': (300322, 103, 'Accumula Town', None),

    # Anville Town
    'Anville Town - Gift: Railwayman in southeast house': (300311, 239, 'Anville Town', None),
    'Anville Town - Gift: Girl on platform after talking, finding Pansage outside Musical Theatre, then talking again': (300321, 365, 'Anville Town', None),

    # Aspertia City
    'Aspertia City - Gift: Bianca at lookout': (300001, 2802, 'Aspertia City', None),
    'Aspertia City - Gift: Woman at Route 19 gate': (300002, 1703, 'Aspertia City', None),
    'Aspertia City - Gift: School Kid in Trainers\' School': (300003, 269, 'Aspertia City', None),
    'Aspertia City - Gift: Girl in northeast house after defeating Cheren': (300004, 277, 'Aspertia City', None),
    # HoF postgame gifts in s856 are bypassed when living_room_starter is enabled - issues so excluded

    # Aspertia Gym
    'Aspertia Gym - Gift: Clyde': (300007, 115, 'Aspertia Gym', None),

    # Castelia City
    'Castelia City - Gift: Clerk at Bridge Gate': (300167, 442, 'Castelia City', None),
    'Castelia City - Gift: Oceanfront Road - Harlequin near Prime Pier': (300047, 2338, 'Castelia City', None),
    'Castelia City - Gift: Oceanfront Road - Harlequin after finding clowns': (300074, 2339, 'Castelia City', None),
    'Castelia City - Gift: Mode Street - Casteliacone stand lady': (300050, 2752, 'Castelia City', None),
    'Castelia City - Gift: Unity Pier - Girl': (300051, 443, 'Castelia City', None),
    'Castelia City - Gift: Gym Street - Man in Studio Castelia 1F': (300063, 2732, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Woman in Battle Company 1F': (300065, 361, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Battle Company president on 1F': (300068, 852, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Scientist in Battle Company 47F': (300069, 143, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Clerk in middle of Battle Company 47F': (300070, 362, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Clerk in Battle Company 47F': (300071, 210, 'Castelia City', None),
    'Castelia City - Gift: North Street - Man in left building 1F': (300072, 382, 'Castelia City', None),
    'Castelia City - Gift: Narrow Street - Waiter in cafe': (300075, 133, 'Castelia City', None),
    'Castelia City - Gift: North Street - Pokédex Scientist on 1F of right building': (300076, 244, 'Castelia City', None),

    # Castelia Gate
    'Castelia Gate - Gift: Bianca at Route 4 gate': (300073, 1706, 'Castelia Gate', None),

    # Castelia Gym
    'Castelia Gym - Gift: Clyde': (300049, 109, 'Castelia Gym', None),

    # Castelia Sewers
    'Castelia Sewers - Gift: Scientist in northern room (Spring/Summer, Surf)': (300281, 2781, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Gift: Scientist in room near Doctor': (300284, 2782, 'Castelia Sewers', None),

    # Celestial Tower
    'Celestial Tower - Gift: 1F, Professor Juniper': (300192, 1711, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave - Gift: B1F, Nugget Brothers 1': (300153, 296, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave - Gift: B1F, Nugget Brothers 2': (300359, 2585, 'Chargestone Cave - Past Bridge', None),

    # Desert Resort
    'Desert Resort - Gift: Man in black in sand pit in the east': (300149, 216, 'Desert Resort', None),

    # Dragonspiral Tower
    'Dragonspiral Tower - Gift: Cedric at tower entrance': (300162, 2341, 'Dragonspiral Tower', None),

    # Dreamyard
    'Dreamyard - Gift: Northern area: Soul Dew after battling Latios/Latias on 2F southeastern ruins after chase (Cut)': (300365, 497, 'Dreamyard - Cut Area', None),

    # Driftveil City
    'Driftveil City - Gift: Clyde': (300108, 111, 'Driftveil City', None),
    'Driftveil City - Gift: Girl on upper floor of Pokemon Center': (300109, 122, 'Driftveil City', None),
    'Driftveil City - Gift: Old man on 1F of Grand Hotel Driftveil': (300112, 319, 'Driftveil City', None),
    'Driftveil City - Gift: Lady on 1F of Driftveil Luxury Suites (TM move)': (300113, 2759, 'Driftveil City', None),
    'Driftveil City - Gift: Man in black at market': (300117, 324, 'Driftveil City', None),
    'Driftveil City - Gift: Gentleman on 25F of Driftveil Chateau Hotel': (300301, 318, 'Driftveil City', None),
    'Driftveil City - Gift: Axew on 19F of Grand Hotel Driftveil': (300302, 320, 'Driftveil City', None),
    'Driftveil City - Gift: Waiter on 23F of Driftveil Luxury Suites': (300303, 322, 'Driftveil City', None),
    'Driftveil City - Gift: Veteran on 25F of Driftveil Continental Hotel': (300304, 323, 'Driftveil City', None),

    # Driftveil Drawbridge
    'Driftveil Drawbridge - Gift: Youngster on west of bridge': (300169, 282, 'Driftveil Drawbridge', None),

    # Floccesy Ranch
    'Floccesy Ranch - Gift: After battling Hugh': (300017, 2343, 'Floccesy Ranch', None),
    'Floccesy Ranch - Gift: Hugh in northwest': (300018, 2344, 'Floccesy Ranch', None),

    # Floccesy Town
    'Floccesy Town - Gift: Old man in house east of Pokemon Center': (300009, 278, 'Floccesy Town', None),
    'Floccesy Town - Gift: Mr Medal after defeating School Kids': (300010, 267, 'Floccesy Town', None),
    'Floccesy Town - Gift: Bianca after defeating Cheren': (300011, 2345, 'Floccesy Town', None),

    # Giant Chasm
    'Giant Chasm - Gift: Rood after defeating Plasma Grunt in crater': (300163, 2346, 'Giant Chasm', None),
    'Giant Chasm - Gift: DNA Splicers after defeating Ghetsis': (300310, 481, 'Giant Chasm - Post-Frigate', None),

    # Humilau City
    'Humilau City - Gift: Couple outside Pokémon Center after ringing Celestial Tower bell': (300271, 2347, 'Humilau City', None),
    'Humilau City - Gift: Nurse in northeastern house': (300272, 342, 'Humilau City', None),
    'Humilau City - Gift: Socialite in northwestern house near Route 22 after walking Mienfoo': (300274, 2768, 'Humilau City', None),

    # Humilau Gym
    'Humilau Gym - Gift: Clyde': (300278, 117, 'Humilau Gym', None),

    # Icirrus City
    'Icirrus City - Gift: Battle Girl in Pokemon Center': (300123, 120, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman in western house 1': (300126, 201, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman in western house 2': (300366, 202, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman in western house 3': (300367, 203, 'Icirrus City', None),

    # Lacunosa Town
    'Lacunosa Town - Gift: Executive in northeast raised house': (300232, 2784, 'Lacunosa Town', None),

    # Lentimas Town
    'Lentimas Town - Gift: Old woman in Pokemon Center': (300268, 294, 'Lentimas Town', None),

    # Marine Tube
    'Marine Tube - Gift: Female Ace Trainer in middle': (300270, 389, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Gift: Professor Juniper on runway': (300118, 1707, 'Mistralton City', None),
    'Mistralton City - Gift: Veteran in Cargo Service building': (300358, 121, 'Mistralton City', None),
    'Mistralton City - Gift: Pilot in Cargo Service building': (300120, 472, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (10 TMs)': (300313, 450, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (20 TMs)': (300314, 451, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (35 TMs)': (300121, 452, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (50 TMs)': (300315, 453, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (70 TMs)': (300316, 454, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in house east of Pokemon Center (95 TMs)': (300317, 455, 'Mistralton City', None),

    # Mistralton Gym
    'Mistralton Gym - Gift: Clyde': (300357, 112, 'Mistralton Gym', None),

    # Musical Theater
    'Musical Theater - Gift: Owner at theater entrance': (300099, 2350, 'Musical Theater', None),

    # N's Castle
    'N\'s Castle - Gift: 5F, N after the first battle': (300175, 1708, 'N\'s Castle', None),

    # Nacrene City
    'Nacrene City - Gift: Lenora in museum': (300036, 445, 'Nacrene City', None),
    'Nacrene City - Gift: Waitress by entrance inside of Cafe Warehouse (Wed/Sat)': (300043, 2735, 'Nacrene City', None),
    'Nacrene City - Gift: Waitress in lower section of Cafe Warehouse (Sun)': (300372, 2553, 'Nacrene City', None),
    'Nacrene City - Gift: Waitress in lower section of Cafe Warehouse (Sun/Thu)': (300046, 2353, 'Nacrene City', None),

    # Nimbasa City
    'Nimbasa City - Gift: Rosa/Nate at Battle Subway entrance': (300077, 764, 'Nimbasa City', None),
    'Nimbasa City - Gift: Clyde': (300078, 110, 'Nimbasa City', None),
    'Nimbasa City - Gift: Gentleman in the Pokemon Center': (300081, 305, 'Nimbasa City', None),
    'Nimbasa City - Gift: Madame in 2F of northwest building': (300105, 262, 'Nimbasa City', None),
    'Nimbasa City - Gift: Ace Trainer in 2F of northwestern building': (300107, 213, 'Nimbasa City', None),
    'Nimbasa City - Gift: Beauty at end of old gym': (300364, 459, 'Nimbasa City', None),

    # Nuvema Town
    'Nuvema Town - Gift: Cheren\'s father in bottom right house': (300218, 413, 'Nuvema Town', None),
    'Nuvema Town - Gift: Cedric Juniper in northwest Juniper Pokémon Lab': (300363, 2437, 'Nuvema Town', None),

    # Opelucid City
    'Opelucid City - Gift: Clyde': (300129, 114, 'Opelucid City', None),
    'Opelucid City - Gift: Linebacker on 2F of Drayden\'s house': (300132, 240, 'Opelucid City', None),
    'Opelucid City - Gift: Woman on 2F of Drayden\'s house': (300133, 241, 'Opelucid City', None),
    'Opelucid City - Gift: Woman in house east of Gym': (300138, 236, 'Opelucid City', None),

    # P2 Laboratory
    'P2 Laboratory - Gift: Scientist Dudley 1': (300319, 2443, 'P2 Laboratory', None),
    'P2 Laboratory - Gift: Scientist Dudley 2': (300320, 2461, 'P2 Laboratory', None),

    # Pinwheel Forest
    'Pinwheel Forest - Gift: Outside: Challenge Rock (Fighting-type)': (300142, 2760, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Inside: Cheren in northeast inner forest after meeting Gorm': (300144, 908, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Inside: Scientist after Habitat List south': (300148, 470, 'Pinwheel Forest', None),

    # Plasma Frigate
    'Plasma Frigate - Gift: Colress in bridge chamber': (300306, 429, 'Plasma Frigate (P2 Laboratory)', None),

    # Pokémon League

    # PWT
    'PWT - Gift: Worker southeast of fountain': (300312, 448, 'PWT', None),

    # Reversal Mountain

    # Route 1
    'Route 1 - Gift: Woman in the central patch of tall grass': (300362, 425, 'Route 1', None),

    # Route 11
    'Route 11 - Gift: Ranger inside trailer': (300207, 384, 'Route 11', None),

    # Route 13
    'Route 13 - Gift: Ace trainer on beach near southern house': (300208, 2738, 'Route 13', None),
    'Route 13 - Gift: Girl in house in the west accessed from tree path': (300213, 304, 'Route 13', None),

    # Route 16
    'Route 16 - Gift: Man in Nimbasa Gate': (300106, 263, 'Route 16', None),
    'Marvelous Bridge - Gift: Roughneck at Route 16 gate': (300216, 385, 'Route 16', None),

    # Route 18
    'Route 18 - Item: Northern cliff east of Veteran': (300368, 943, 'Route 18', None),

    # Route 19
    'Route 19 - Gift: Alder after Floccesy events': (300008, 2361, 'Route 19', None),

    # Route 2
    'Route 2 - Gift: Lady in the northeast': (300179, 2362, 'Route 2', None),

    # Route 20
    'Route 20 - Gift: Cheren near dark grass': (300012, 2363, 'Route 20 - North', None),

    # Route 22
    'Route 22 - Gift: Colress at Terrakion plateau in the northwest after beating Marlon': (300279, 2364, 'Route 22', None),

    # Route 3
    'Route 3 - Gift: School Kid after Habitat List in the north': (300180, 471, 'Route 3 - Water', None),

    # Route 4
    'Route 4 - Gift: Colress after battle': (300181, 1705, 'Route 4 - North', None),
    'Route 4 - Gift: Ace Trainer in first house on right': (300182, 2772, 'Route 4 - North', None),
    'Route 4 - Gift: Ace Trainer in first house east of ruins crossroads': (300369, 2772, 'Route 4 - North', None),
    'Route 4 - Gift: Black Belt in 2F of first left house': (300288, 386, 'Route 4 - North', None),
    'Route 4 - Gift: Black Belt in house in the far southeast of ruins': (300370, 386, 'Route 4 - North', None),
    'Route 4 - Gift: Maid in third house on right (Guess Pokémon cry)': (300289, 363, 'Route 4 - North', None),
    'Route 4 - Gift: Maid in southwest house (Guess Pokémon cry)': (300371, 363, 'Route 4 - North', None),

    # Route 5
    'Route 5 - Gift: Item bought from Breeder': (300186, 2751, 'Route 5', None),

    # Route 6
    'Route 6 - Gift: Girl in house southeast of Chargestone Cave': (300190, 383, 'Route 6', None),

    # Route 8
    'Route 8 - Gift: Parasol lady by Tubeline Bridge in east': (300195, 2749, 'Route 8', None),
    'Tubeline Bridge - Gift: Scientist at Route 8 gate': (300197, 346, 'Route 8', None),

    # Shopping Mall
    'Shopping Mall - Gift: Lady in bottom section': (300200, 2765, 'Shopping Mall', None),

    # Skyarrow Bridge
    'Skyarrow Bridge - Gift: Runner after bridge quest': (300166, 2586, 'Skyarrow Bridge', None),

    # Strange House
    'Strange House - Gift: 2F, Ghost girl in bedroom after second basement traverse': (300287, 899, 'Strange House', None),

    # Striaton City
    'Striaton City - Gift: Fisherman left of Route 3 gate across the water (Surf)': (300028, 140, 'Striaton City', None),
    'Striaton City - Gift: Roughneck in eastmost alley': (300361, 142, 'Striaton City', None),
    'Striaton City - Gift: Pansage show in restaurant': (300030, 2777, 'Striaton City', None),
    'Striaton City - Gift: Girl in Pokemon Center': (300033, 381, 'Striaton City', None),
    'Striaton City - Gift: Man on 1F of lower east apartment': (300034, 104, 'Striaton City', None),
    'Striaton City - Gift: Schoolboy quiz in Trainers\' School': (300035, 355, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - Gift: Fossil worker': (300159, 2747, 'Twist Mountain', None),

    # Undella Town
    'Undella Town - Gift: Man in west of Pokemon Center': (300235, 295, 'Undella Town', None),
    'Undella Town - Gift: Zinzolin in front of gate': (300360, 2803, 'Undella Town', None),

    # Victory road

    # Village Bridge
    'Village Bridge - Gift: Girl on bridge after checking out the noise in the room below her': (300170, 468, 'Village Bridge', None),
    'Village Bridge - Gift: Baker after battle (Post-Game)': (300171, 457, 'Village Bridge', None),
    'Village Bridge - Gift: Fisherman in third house from the right after meeting him on Route 8 east': (300318, 299, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Gift: Attendant in Route 20 gate': (300019, 2367, 'Virbank City', None),
    'Virbank City - Gift: Nursery Aide in the nursery': (300020, 279, 'Virbank City', None),
    'Virbank City - Gift: Roughneck in front of Gym': (300021, 492, 'Virbank City', None),

    # Virbank Complex
    'Virbank Complex - Gift: Roughneck trading Poke Ball for Great Ball in entrance by waterside': (300023, 2763, 'Virbank Complex', None),

    # Virbank Complex Inside
    'Virbank Complex - Gift: Scientist after talking to him three times': (300024, 310, 'Virbank Complex Inside', None),
    'Virbank Complex - Gift: Girl at southernmost end after filling Habitat List': (300025, 467, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Gift: Clyde': (300022, 116, 'Virbank Gym', None),

    # Pokemon Ranger post-battle Berry gifts (unused persistent flags 1500..1519 & 2385..2398)
    'Chargestone Cave - Gift: B1F, Ranger Briana': (300323, 1500, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave - Gift: 1F, Ranger Louis': (300324, 1501, 'Chargestone Cave - Past Bridge', None),
    'Clay Tunnel - Gift: Ranger Katie in Twist Mountain side north': (300325, 1502, 'Clay Tunnel', None),
    'Clay Tunnel - Gift: Ranger Maxwell in Twist Mountain side south': (300326, 1503, 'Clay Tunnel', None),
    'Desert Resort - Gift: Ranger Anja in east': (300327, 1504, 'Desert Resort', None),
    'Desert Resort - Gift: Ranger Jaden near entrance': (300328, 1505, 'Desert Resort', None),
    'Lostlorn Forest - Gift: Ranger Forrest in north': (300329, 1506, 'Lostlorn Forest', None),
    'Lostlorn Forest - Gift: Ranger Serenity inside leaf pile': (300330, 1507, 'Lostlorn Forest', None),
    'Moor of Icirrus - Gift: Ranger Elaine in west behind strength boulder (Strength)': (300331, 1508, 'Moor of Icirrus - Strength', None),
    'Moor of Icirrus - Gift: Ranger Parker in southeast': (300332, 1509, 'Moor of Icirrus', None),
    'Pinwheel Forest - Gift: Inside: Ranger Dwayne south inner forest in leaf pile': (300333, 1510, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Inside: Ranger Hillary south inner forest': (300334, 1511, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Inside: Ranger Melita northeast inner forest': (300335, 1512, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Inside: Ranger Ralph northwest inner forest': (300336, 1513, 'Pinwheel Forest', None),
    'Reversal Mountain - Gift: Ranger Eliza (1F B2 / 2F W2)': (300337, 1514, 'Reversal Mountain', None),
    'Reversal Mountain - Gift: Ranger Lewis (2F B2 / 1F W2)': (300338, 1515, 'Reversal Mountain', None),
    'Route 1 - Gift: Ranger Audra next to the gate in the western section': (300339, 1516, 'Route 1 - Water', None),
    'Route 1 - Gift: Ranger Rick east of the gate in the western section': (300340, 1517, 'Route 1 - Water', None),
    'Route 11 - Gift: Ranger Crofton south of trailer': (300341, 1518, 'Route 11', None),
    'Route 11 - Gift: Ranger Thalia northeast down waterfall (Surf, Waterfall)': (300342, 1519, 'Route 11 - Waterfall', None),
    'Route 13 - Gift: Ranger Daryl east of northern house': (300343, 2385, 'Route 13', None),
    'Route 13 - Gift: Ranger Dianne east of Cobalion in north': (300344, 2386, 'Route 13', None),
    'Route 20 - Gift: Pokemon Ranger Bret in west of leaves (Autumn)': (300345, 2387, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift: Pokemon Ranger Leaf north of land in leaves (Autumn)': (300346, 2388, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift: Pokemon Ranger Malory west of land in leaves (Autumn)': (300347, 2389, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift: Pokemon Ranger Naoko above waterfall in south (Autumn)': (300348, 2390, 'Route 20 - Waterfall', None),
    'Route 23 - Gift: Ranger Lena north along main path at bottom of stairs': (300349, 2391, 'Route 23', None),
    'Route 23 - Gift: Ranger Steve east on cliff in leaf pile': (300350, 2392, 'Route 23', None),
    'Route 5 - Gift: Ranger Lois above road': (300351, 2393, 'Route 5', None),
    'Route 6 - Gift: Ranger Richard north of Season Research Lab across the water': (300352, 2394, 'Route 6', None),
    'Seaside Cave - Gift: 1F, Ranger Johan southwest': (300353, 2395, 'Seaside Cave', None),
    'Seaside Cave - Gift: 1F, Ranger Mikiko west': (300354, 2396, 'Seaside Cave', None),
    'Victory Road - Gift: 2F, Ranger Eddie': (300355, 2397, 'Victory Road - Strength', None),
    'Victory Road - Gift: 2F, Ranger Elle': (300356, 2398, 'Victory Road - Strength', None),
}

# Gym badges (domain: 400001..400008, flag = 2414 + badge_idx)
BADGE_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Aspertia Gym
    'Aspertia Gym - Gym Leader Cheren Basic Badge': (400001, 1676, 'Aspertia Gym', None, (2284,)),

    # Castelia City
    'Castelia Gym - Gym Leader Burgh Insect Badge': (400003, 1674, 'Castelia City', None, (2286,)),

    # Driftveil City
    'Driftveil Gym - Gym Leader Clay Quake Badge': (400005, 1678, 'Driftveil City', None, (2288,)),

    # Humilau City
    'Humilau Gym - Gym Leader Marlon Wave Badge': (400008, 1680, 'Humilau City', None, (2291,)),

    # Mistralton City
    'Mistralton Gym - Gym Leader Skyla Jet Badge': (400006, 1675, 'Mistralton City', None, (2289,)),

    # Nimbasa City
    'Nimbasa Gym - Gym Leader Elesa Bolt Badge': (400004, 1673, 'Nimbasa City', None, (2287,)),

    # Opelucid City
    'Opelucid Gym - Gym Leader Drayden Legend Badge': (400007, 1679, 'Opelucid City', None, (2290,)),

    # Virbank Gym
    'Virbank Gym - Gym Leader Roxie Toxic Badge': (400002, 1677, 'Virbank Gym', None, (2285,)),
}

# Story / gym TM & HM rewards (domain: 500000 + TM/HM num)
TM_REWARD_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Aspertia City
    'Aspertia City - Gift: Bianca after defeating Cheren': (500027, 2368, 'Aspertia City', None),

    # Aspertia Gym
    'Aspertia Gym - Gift: Cheren after defeating Gym': (500083, 2377, 'Aspertia Gym', None),

    # Castelia City
    'Castelia City - Gift: Castelia Street - Guitarist in building on left 11F': (500044, 209, 'Castelia City', None),
    'Castelia City - Gift: North Street - Girl on the left in lower right building 47F': (500045, 416, 'Castelia City', None),
    'Castelia City - Gift: Narrow Street - From man behind dumpster': (500070, 2369, 'Castelia City', None),
    'Castelia City - Gift: Burgh after defeating Gym': (500076, 2379, 'Castelia City', None),

    # Castelia Sewers
    'Castelia Sewers - Gift: Hugh after defeating Team Plasma near Relic Passage': (500004, 2370, 'Castelia Sewers', None),

    # Driftveil City
    'Driftveil City - Gift: Clay after defeating Gym': (500078, 2381, 'Driftveil City', None),

    # Floccesy Ranch
    'Floccesy Ranch - Gift: Team Plasma Grunt at the end of forest': (500021, 2371, 'Floccesy Ranch', None),

    # Humilau City
    'Humilau Gym - Gift: Marlon after defeating Gym': (500055, 2384, 'Humilau Gym', None),

    # Lentimas Town
    'Lentimas Town - Gift: Woman in house near girl with Krokorok': (500057, 118, 'Lentimas Town', None),

    # Lostlorn Forest
    'Lostlorn Forest - Gift: Backpacker in northern clearing': (500095, 967, 'Lostlorn Forest', None),

    # Marine Tube
    'Marine Tube - Gift: Parasol Lady at Humilau City entrance': (500042, 343, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Gift: Skyla after defeating Gym': (500062, 2382, 'Mistralton City', None),

    # Musical Theater
    'Musical Theater - Gift: Lady to the right of the reception counter': (500049, 211, 'Musical Theater', None),

    # Nimbasa City
    'Nimbasa City - Gift: Elesa after defeating Gym': (500072, 2380, 'Nimbasa City', None),

    # Opelucid City
    'Opelucid City - Gift: Drayden after defeating Gym': (500082, 2383, 'Opelucid City', None),

    # Reversal Mountain
    'Reversal Mountain - Gift: Scientist after Habitat List in northeast of main cavern': (500054, 469, 'Reversal Mountain', None),

    # Route 23
    'Route 23 - Gift: Old man in house at end of stream across the water (Surf)': (500035, 473, 'Route 23', None),

    # Route 5
    'Route 5 - Gift: Bianca near Nimbasa Gate': (500002, 2373, 'Route 5', None),

    # Route 6
    'Route 6 - Gift: Cheren after PWT Plasma Frigate in Season Research Lab': (500003, 2439, 'Route 6', None),

    # Tubeline Bridge
    'Tubeline Bridge - Gift: Battle Girl on middle of bridge': (500043, 345, 'Tubeline Bridge', None),

    # Undella Town
    'Undella Town - Gift: Hugh in front of Marine Tube gate': (500006, 414, 'Undella Town', None),

    # Victory road
    'Victory Road - Gift: N at badge check gates': (500005, 2374, 'Victory Road', None),
    'Victory Road - Gift: Hugh': (500024, 2375, 'Victory Road - Strength', None),

    # Virbank City
    'Virbank City - Gift: Roxie after defeating Team Plasma Grunt at harbour after Gym': (500001, 1704, 'Virbank City', None),

    # Virbank Complex Inside
    'Virbank Complex - Gift: Man at entrance after defeating all three Workers': (500094, 465, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Gift: Roxie after defeating Gym': (500009, 2378, 'Virbank Gym', None),
}
