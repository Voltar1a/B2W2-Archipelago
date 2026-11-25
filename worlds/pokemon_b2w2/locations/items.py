from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import LocationInfo

# Overworld item balls (domain: 100000 + N, flag = 1100 + N)
OVERWORLD_ITEM_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Abundant Shrine
    'Abundant Shrine - Across the water near the Breeder in northeast': (100253, 1353, 'Abundant Shrine - Water', None),
    'Abundant Shrine - East of Youngster near shrine in northwest': (100254, 1354, 'Abundant Shrine', None),
    'Abundant Shrine - East of Lass on western side': (100255, 1355, 'Abundant Shrine', None),
    'Abundant Shrine - North of Youngster near house in east': (100256, 1356, 'Abundant Shrine', None),
    'Abundant Shrine - East of the shrine in north': (100257, 1357, 'Abundant Shrine - Water', None),

    # Abyssal Ruins
    'Abyssal Ruins 1F - west of room center': (100324, 1424, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - south of the western entrance': (100325, 1425, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southwest quadrant': (100326, 1426, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast quadrant': (100327, 1427, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southwest corner': (100328, 1428, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast corner': (100329, 1429, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast quadrant vase': (100330, 1430, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - north of the eastern entrance': (100331, 1431, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - north of room center': (100332, 1432, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - near the northeast corner': (100333, 1433, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - near the northern entrance': (100334, 1434, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - south of room center': (100335, 1435, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - north of the western entrance': (100336, 1436, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - northwest quadrant': (100337, 1437, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - inside northern entrance': (100338, 1438, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - inside eastern entrance': (100339, 1439, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - inside southern entrance': (100340, 1440, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast of western entrance': (100341, 1441, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - northwest quadrant silver': (100342, 1442, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - northeast quadrant': (100343, 1443, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast quadrant north pillar': (100344, 1444, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southeast quadrant south pillar': (100345, 1445, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - near northwest corner': (100346, 1446, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - southwest quadrant gold': (100347, 1447, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - east of center': (100348, 1448, 'Abyssal Ruins', None),
    'Abyssal Ruins 1F - north of center statue': (100349, 1449, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - southwest quadrant': (100350, 1450, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - near entrance from 1F': (100351, 1451, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - northeast quadrant': (100352, 1452, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - southwest quadrant silver': (100353, 1453, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - northwest quadrant': (100354, 1454, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - northeast quadrant gold': (100355, 1455, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - along east wall': (100356, 1456, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - northwest corner': (100357, 1457, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - southeast corner': (100358, 1458, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - northeast quadrant band': (100359, 1459, 'Abyssal Ruins', None),
    'Abyssal Ruins 2F - southwest corner statue': (100360, 1460, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - south side': (100361, 1461, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - southwest corner': (100362, 1462, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - northeast corner': (100363, 1463, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - along west wall': (100364, 1464, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - northeast quadrant band': (100365, 1465, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - southeast quadrant band': (100366, 1466, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - center of room': (100367, 1467, 'Abyssal Ruins', None),
    'Abyssal Ruins 3F - northwest corner statue': (100368, 1468, 'Abyssal Ruins', None),

    # Aspertia City
    'Aspertia City - Across pond southeast': (100000, 1100, 'Aspertia City', None),

    # Castelia City
    'Castelia City - Oceanfront Road - In Battle Company 47F': (100023, 1123, 'Castelia City', None),
    'Castelia City - Oceanfront Road - In Battle Company 55F northern desk': (100024, 1124, 'Castelia City', None),
    'Castelia City - Castelia Street - In Game Freak building 22F room': (100025, 1125, 'Castelia City', None),
    'Castelia City - North Street - In top right building 47F southeast corner': (100026, 1126, 'Castelia City', None),
    'Castelia City - Prime Pier south end': (100027, 1127, 'Castelia City', None),
    'Castelia City - Castelia Park from sewers': (100028, 1128, 'Castelia City', None),
    'Castelia City - Back alley accessible from sewers near trainers (Spring/Summer + Surf)': (100029, 1129, 'Castelia City - Back Alley', None),
    'Castelia City - Back alley accessible from sewers southern corner (Spring/Summer + Surf)': (100030, 1130, 'Castelia City - Back Alley', None),

    # Castelia Sewers
    'Castelia Sewers - Near Doctor near centre': (100031, 1131, 'Castelia Sewers', None),
    'Castelia Sewers - Outside Relic Passage entrance': (100032, 1132, 'Castelia Sewers', None),
    'Castelia Sewers - North of Worker in west (Spring/Summer)': (100033, 1133, 'Castelia Sewers - Dry (Spring/Summer)', None),
    'Castelia Sewers - Southwest of Janitor in east (Spring/Summer)': (100034, 1134, 'Castelia Sewers - Dry (Spring/Summer)', None),
    'Castelia Sewers - West of Janitor in east (Autumn/Winter or Spring/Summer + Surf)': (100035, 1135, 'Castelia Sewers', None),
    'Castelia Sewers - Near Worker in west (Autumn/Winter or Spring/Summer + Surf)': (100036, 1136, 'Castelia Sewers', None),
    'Castelia Sewers - West of Relic Passage entrance (Spring/Summer)': (100037, 1137, 'Castelia Sewers - Dry (Spring/Summer)', None),
    'Castelia Sewers - Southern canal west end (Spring/Summer + Surf)': (100038, 1138, 'Castelia Sewers - Water', None),
    'Castelia Sewers - West of Scientist in southeast (Spring/Summer + Surf)': (100039, 1139, 'Castelia Sewers - Water', None),

    # Celestial Tower
    'Celestial Tower 2F - west of Psychic': (100105, 1205, 'Celestial Tower', None),
    'Celestial Tower 2F - east of School Kid': (100106, 1206, 'Celestial Tower', None),
    'Celestial Tower 3F - southwest of Pokéfan': (100107, 1207, 'Celestial Tower', None),
    'Celestial Tower 4F - north of Socialite': (100108, 1208, 'Celestial Tower', None),
    'Celestial Tower 4F - east of Psychic': (100109, 1209, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave 1F - near Route 6 entrance': (100088, 1188, 'Chargestone Cave', None),
    'Chargestone Cave 1F - east of Guitarist': (100089, 1189, 'Chargestone Cave', None),
    'Chargestone Cave 1F - south of Scientist': (100090, 1190, 'Chargestone Cave', None),
    'Chargestone Cave 1F - northeast path near stairs': (100092, 1192, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave 1F - south of bridge': (100093, 1193, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B1F - northwest near Scientist': (100094, 1194, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B1F - in the southeast': (100095, 1195, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B2F - north corner near electric stone': (100096, 1196, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B2F - west dead-end': (100097, 1197, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B2F - south of Ace Trainer': (100098, 1198, 'Chargestone Cave - Past Bridge', None),

    # Clay Tunnel
    'Clay Tunnel - Middle room southwest chamber upper item': (100075, 1175, 'Clay Tunnel - Strength', None),
    'Clay Tunnel - Driftveil side behind central Strength boulder': (100083, 1183, 'Clay Tunnel - Strength', None),
    'Clay Tunnel - Driftveil side behind rock near Strength boulder': (100085, 1185, 'Clay Tunnel - Strength', None),
    'Clay Tunnel - Middle room east side of pond': (100087, 1187, 'Clay Tunnel', None),
    'Clay Tunnel - Middle room southwest chamber lower item': (100319, 1419, 'Clay Tunnel - Strength', None),
    'Clay Tunnel - Twist Mountain side southwest dead end': (100320, 1420, 'Clay Tunnel', None),
    'Clay Tunnel - Twist Mountain side central area': (100321, 1421, 'Clay Tunnel', None),

    # Desert Resort
    'Desert Resort - In the west': (100054, 1154, 'Desert Resort', None),
    'Desert Resort - In a central dip': (100055, 1155, 'Desert Resort', None),
    'Desert Resort - Along the eastern wall': (100056, 1156, 'Desert Resort', None),
    'Desert Resort - In the southwestern corner': (100057, 1157, 'Desert Resort', None),
    'Desert Resort - In a south dead end': (100058, 1158, 'Desert Resort', None),
    'Desert Resort - In a dip west of the entrance': (100059, 1159, 'Desert Resort', None),
    'Desert Resort - North of Relic Castle entrance': (100060, 1160, 'Desert Resort', None),
    'Desert Resort - In the northwest': (100061, 1161, 'Desert Resort', None),

    # Dragonspiral Tower
    'Dragonspiral Tower 4F - northeast platform top': (100180, 1280, 'Dragonspiral Tower', None),
    'Dragonspiral Tower - Eastern edge of the outside area': (100229, 1329, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 5F - third ring': (100230, 1330, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 5F - second ring': (100231, 1331, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 2F - northeast': (100232, 1332, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 3F - northeast corner': (100233, 1333, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 5F - first ring': (100234, 1334, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 3F - on a platform in the middle of the floor': (100235, 1335, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 2F - on top of a pillar in the southwest': (100236, 1336, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 6F - northeast corner': (100237, 1337, 'Dragonspiral Tower', None),
    'Dragonspiral Tower - On the slope at the exit of Icirrus City (Winter)': (100238, 1338, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 4F - northeast platform middle': (100380, 1480, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 4F - northeast platform bottom': (100381, 1481, 'Dragonspiral Tower', None),

    # Dreamyard
    'Dreamyard - Northern area: south of the stairs to the second floor of the ruins': (100291, 1391, 'Dreamyard - Cut Area', None),
    'Dreamyard - Northern area: on the far south part of the second floor of the ruins': (100292, 1392, 'Dreamyard - Cut Area', None),
    'Dreamyard - Northern area: northwest of the eastern patch of tall grass': (100293, 1393, 'Dreamyard', None),
    'Dreamyard - Northern area: in the patch of tall grass in the west': (100295, 1395, 'Dreamyard - Cut Area', None),
    'Dreamyard - Southern area: west of the western stairs, in between the wall and the trees': (100296, 1396, 'Dreamyard', None),
    'Dreamyard - Basement: South of the northeast stairs': (100297, 1397, 'Dreamyard', None),
    'Dreamyard - Northern area: In the northwest corner, accessible from the southwestern stairs in the ruins': (100298, 1398, 'Dreamyard', None),
    'Dreamyard - Basement: In the southwest corner': (100299, 1399, 'Dreamyard', None),

    # Driftveil City
    'Driftveil City - Near the stone bridge': (100070, 1170, 'Driftveil City', None),
    'Driftveil City - In the southwest corner of the market, accessed from the western entrance': (100375, 1475, 'Driftveil City', None),

    # Floccesy Ranch
    'Floccesy Ranch - Northeastern area near Herdier': (100015, 1115, 'Floccesy Ranch', None),
    'Floccesy Ranch - Southern dead end in between fences': (100013, 1113, 'Floccesy Ranch', None),
    'Floccesy Ranch - Northern area south of Youngster': (100014, 1114, 'Floccesy Ranch', None),

    # Floccesy Town
    'Floccesy Town - West side of Alder\'s house': (100011, 1111, 'Floccesy Town', None),

    # Giant Chasm
    'Giant Chasm - Route 13 exit, near the broken bridge outside': (100143, 1243, 'Giant Chasm', None),
    'Giant Chasm - Cave, northwest behind Strength boulder': (100176, 1276, 'Giant Chasm', None),
    'Giant Chasm - Cave, northeast of southwest corner, on the other side of a Strength boulder': (100177, 1277, 'Giant Chasm', None),
    'Giant Chasm - Cave, at the north end of the pool of water near the Route 22 entrance': (100178, 1278, 'Giant Chasm', None),
    'Giant Chasm - Crater, next to a patch of dark tall grass in the northwest after defeating Ghetsis': (100179, 1279, 'Giant Chasm - Post-Frigate', None),
    'Giant Chasm - Crater, in a dead end north of the centre, after defeating Ghetsis': (100181, 1281, 'Giant Chasm - Post-Frigate', None),
    'Giant Chasm - Crater, east of where the Plasma Frigate used to be after defeating Ghetsis': (100182, 1282, 'Giant Chasm - Post-Frigate', None),
    'Giant Chasm - Crater, west of the spot where the Plasma Frigate used to be after defeating Ghetsis': (100183, 1283, 'Giant Chasm - Post-Frigate', None),
    'Giant Chasm - Crater, north of the southwest corner along the western wall': (100184, 1284, 'Giant Chasm', None),
    'Giant Chasm - Crater, in the southwest corner': (100185, 1285, 'Giant Chasm', None),
    'Giant Chasm - Crater, southeast corner path after beating Ghetsis': (100186, 1286, 'Giant Chasm - Post-Frigate', None),

    # Guidance Chamber
    'Guidance Chamber 3F - northeast corner': (100081, 1181, 'Guidance Chamber', None),
    'Guidance Chamber 3F - northeast of entrance': (100082, 1182, 'Guidance Chamber', None),

    # Humilau City
    'Humilau City - Northwest at end of planks': (100164, 1264, 'Humilau City', None),
    'Humilau City - Northwest behind the Gym': (100171, 1271, 'Humilau City', None),
    'Humilau City - Northeast in the shallow water': (100304, 1404, 'Humilau City', None),

    # Icirrus City
    'Icirrus City - East of the Pokémon Center across bridge guarded by Shadow Triad': (100223, 1323, 'Icirrus City', None),
    'Icirrus City - West of Pokémon Center (Winter)': (100239, 1339, 'Icirrus City', None),

    # Lacunosa Town
    'Lacunosa Town - Inside northeast raised house': (100141, 1241, 'Lacunosa Town', None),
    'Lacunosa Town - On the raised part in the southwest': (100142, 1242, 'Lacunosa Town', None),
    'Route 12 - In northeast': (100144, 1244, 'Route 12', None),

    # Lentimas Town
    'Lentimas Town - On the hill north of the Pokémon Center': (100110, 1210, 'Lentimas Town', None),

    # Lostlorn Forest
    'Lostlorn Forest - Inside a tree stump in the lower part': (100065, 1165, 'Lostlorn Forest', None),
    'Lostlorn Forest - In the higher part accessed with Waterfall': (100066, 1166, 'Lostlorn Forest - Waterfall', None),
    'Lostlorn Forest - Northeastern stump': (100067, 1167, 'Lostlorn Forest', None),

    # Mistralton Cave
    'Mistralton Cave 1F - north': (100079, 1179, 'Mistralton Cave', None),
    'Mistralton Cave 1F - northeast': (100080, 1180, 'Mistralton Cave', None),
    'Mistralton Cave 2F - south after wrapping around from east': (100084, 1184, 'Mistralton Cave', None),
    'Mistralton Cave 2F - northwest after wrapping around from northeast': (100086, 1186, 'Mistralton Cave', None),

    # Mistralton City
    'Mistralton City - Near the plane south of the Cargo Service building': (100099, 1199, 'Mistralton City', None),
    'Mistralton City - South of runway between greenhouses': (100100, 1200, 'Mistralton City', None),
    'Mistralton City - South of runway between fields': (100393, 1200, 'Mistralton City', None),

    # Moor of Icirrus
    'Moor of Icirrus - In the gap between trees northeast of the entrance (Spring/Summer/Autumn)': (100224, 1324, 'Moor of Icirrus', None),
    'Moor of Icirrus - South behind the Strength boulder in the west': (100225, 1325, 'Moor of Icirrus - Strength', None),

    'Moor of Icirrus - East of Fisherman in the north (Surf, Winter)': (100226, 1326, 'Moor of Icirrus', None),
    'Moor of Icirrus - In the far northeast': (100227, 1327, 'Moor of Icirrus', None),
    'Moor of Icirrus - Southeast of the entrance': (100228, 1328, 'Moor of Icirrus', None),

    # N's Castle
    'N\'s Castle 4F - inside N\'s room': (100216, 1316, 'N\'s Castle', None),
    'N\'s Castle 4F - south of N\'s room': (100217, 1317, 'N\'s Castle', None),
    'N\'s Castle 4F - in the southeast corner': (100219, 1319, 'N\'s Castle', None),

    # Nature Preserve
    'Nature Preserve - Northwest of the plane': (100272, 1372, 'Nature Preserve', None),
    'Nature Preserve - In the dark grass above the Haxorus': (100273, 1373, 'Nature Preserve', None),
    'Nature Preserve - On the cliff in the extreme northeast': (100286, 1386, 'Nature Preserve', None),

    # Nimbasa City
    'Nimbasa City - Near the large Audino figure in the amusement park': (100062, 1162, 'Nimbasa City', None),

    # Nuvema Town
    'Nuvema Town - In BW player\'s bedroom on 2F, middle house': (100309, 1409, 'Nuvema Town', None),

    # P2 Laboratory
    'P2 Laboratory - Inside the laboratory': (100377, 1477, 'P2 Laboratory', None),

    # PWT
    'PWT - At the end of the western pier': (100071, 1171, 'PWT', None),

    # Pinwheel Forest
    'Pinwheel Forest - Inside: Centre inner forest accessed with Surf from the east': (100258, 1358, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: North inner forest northeast of Veterans': (100259, 1359, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: South inner forest': (100260, 1360, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Eastern edge of area': (100262, 1362, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Northeast west of Rumination Field': (100263, 1363, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Northeast inner forest next to leaf pile': (100264, 1364, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Southwest inner forest': (100265, 1365, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: West inner forest northwest of Youngster': (100266, 1366, 'Pinwheel Forest', None),
    'Pinwheel Forest - Outside: North behind southern fence': (100267, 1367, 'Pinwheel Forest', None),
    'Pinwheel Forest - Outside: Southwest north of Ace Trainer': (100268, 1368, 'Pinwheel Forest', None),
    'Pinwheel Forest - Outside: Southwest by the dark grass': (100269, 1369, 'Pinwheel Forest', None),
    'Pinwheel Forest - Outside: North near the railroad tracks': (100270, 1370, 'Pinwheel Forest', None),
    'Pinwheel Forest - Outside: Southwest, south of Challenge Rock': (100271, 1371, 'Pinwheel Forest', None),

    # Plasma Frigate
    'Plasma Frigate - Top of the beam puzzle maze': (100187, 1287, 'Plasma Frigate', None),
    'Plasma Frigate - Near Grunt in southwest of beam puzzle room left ball': (100188, 1288, 'Plasma Frigate', None),
    'Plasma Frigate - Near Grunt in southeast of beam puzzle room right ball': (100391, 1288, 'Plasma Frigate', None),
    'Plasma Frigate B1F - left big room (from Route 21)': (100189, 1289, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Near Grunt in southwest of beam puzzle room right ball': (100190, 1290, 'Plasma Frigate', None),
    'Plasma Frigate - Near Grunt in southeast of beam puzzle room left ball': (100392, 1290, 'Plasma Frigate', None),
    'Plasma Frigate - In the northeast room (from Route 21)': (100191, 1291, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Right of beam puzzle pit': (100192, 1292, 'Plasma Frigate', None),
    'Plasma Frigate B2F - in the yellow warp panel to left of the puzzle pit': (100193, 1293, 'Plasma Frigate', None),
    'Plasma Frigate - North on deck (from Route 21)': (100378, 1478, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Southeast on deck (from Route 21)': (100379, 1479, 'Plasma Frigate (Route 21)', None),

    # Relic Castle
    'Relic Castle - Easternmost room accessed from Relic Passage': (100261, 1361, 'Relic Castle - Volcarona', None),
    'Relic Castle B1F - from going down stairs': (100318, 1418, 'Relic Castle', None),

    # Relic Passage
    'Relic Passage - Castelia section west of female Scientist accessed from the east': (100040, 1140, 'Relic Passage (Castelia)', None),
    'Relic Passage - Castelia section north of male Scientist in the middle': (100383, 1483, 'Relic Passage (Castelia)', None),
    'Relic Passage - Castelia section near ledges (from Driftveil)': (100041, 1141, 'Relic Passage', None),
    'Relic Passage - Middle section eastern separate room upper item': (100042, 1142, 'Relic Passage - Strength', None),
    'Relic Passage - Middle section eastern separate room middle item': (100043, 1143, 'Relic Passage - Strength', None),
    'Relic Passage - Middle section eastern separate room lower item': (100044, 1144, 'Relic Passage - Strength', None),
    'Relic Passage - Middle section west across the water': (100045, 1145, 'Relic Passage', None),
    'Relic Passage - East of Driftveil exit near Backpacker': (100046, 1146, 'Relic Passage', None),

    # Reversal Mountain
    'Reversal Mountain - Exterior, behind the Strange House': (100115, 1215, 'Reversal Mountain', None),
    'Reversal Mountain - Exterior, eastern valley path': (100116, 1216, 'Reversal Mountain', None),
    'Reversal Mountain - Exterior, on the hill, accessed from inside the mountain in the southwest': (100117, 1217, 'Reversal Mountain', None),
    'Reversal Mountain - Exterior, on the hill, accessed from inside the mountain in the northeast': (100382, 1482, 'Reversal Mountain', None),
    'Reversal Mountain 1F - near exit to Lentimas Town': (100118, 1218, 'Reversal Mountain', None),
    'Reversal Mountain 1F - dead-end tunnel north of Battle Girl': (100119, 1219, 'Reversal Mountain', None),
    'Reversal Mountain 1F - above Hiker in the southeast': (100386, 1219, 'Reversal Mountain', None),
    'Reversal Mountain 1F - dead-end tunnel east of Doctor in south of main cavern': (100120, 1220, 'Reversal Mountain', None),
    'Reversal Mountain 1F - in the west southeast of male Backpacker and Hiker': (100387, 1220, 'Reversal Mountain', None),
    'Reversal Mountain 1F - south of Hiker in north of main cavern': (100121, 1221, 'Reversal Mountain', None),
    'Reversal Mountain 1F - northwest of Black Belt southwest of Ace Trainers': (100388, 1221, 'Reversal Mountain', None),
    'Reversal Mountain 1F - east of Black Belt in west of main cavern': (100122, 1222, 'Reversal Mountain', None),
    'Reversal Mountain 1F - south of Scientist in northeast': (100389, 1222, 'Reversal Mountain', None),
    'Reversal Mountain 1F - dead-end tunnel east of Backpacker and Hiker in southwest of main cavern': (100123, 1223, 'Reversal Mountain', None),
    'Reversal Mountain 1F - in the west east of the entrance': (100390, 1223, 'Reversal Mountain', None),
    'Reversal Mountain B1F - next to the Ranger': (100124, 1224, 'Reversal Mountain', None),
    'Reversal Mountain B1F - near the entrance to 1F': (100125, 1225, 'Reversal Mountain', None),

    # Route 1
    'Route 1 - West of the waterfront after surfing to the western section': (100307, 1407, 'Route 1 - Water', None),
    'Route 1 - In the southeast of the western section': (100308, 1408, 'Route 1 - Water', None),

    # Route 2
    'Route 2 - Northeast elevated plateau west': (100300, 1400, 'Route 2', None),
    'Route 2 - In the tall grass near Youngster in the east': (100301, 1401, 'Route 2', None),
    'Route 2 - Behind Strength boulder in the south': (100302, 1402, 'Route 2', None),
    'Route 2 - South of Lass behind Cut tree in the northwest': (100303, 1403, 'Route 2', None),
    'Route 2 - Northeast elevated plateau east': (100305, 1405, 'Route 2', None),
    'Route 2 - In tall grass in the southwest': (100306, 1406, 'Route 2', None),

    # Route 3
    'Route 3 - Near School Kid in the dark grass in the southeast': (100274, 1374, 'Route 3', None),
    'Route 3 - Near School Kid in the southwest': (100275, 1375, 'Route 3', None),
    'Route 3 - North of Fisherman in the west across the pond': (100276, 1376, 'Route 3 - Water', None),
    'Route 3 - Northwest of Fisherman in the west across the pond': (100277, 1377, 'Route 3 - Water', None),
    'Route 3 - South of the pond, near Fisherman': (100278, 1378, 'Route 3', None),
    'Route 3 - North of the T-intersection': (100279, 1379, 'Route 3', None),
    'Route 3 - Inside the nursery in the northeast': (100280, 1380, 'Route 3', None),

    # Route 4
    'Route 4 - Near sign in the west': (100047, 1147, 'Route 4 - North', None),
    'Route 4 - Hill on western side': (100048, 1148, 'Route 4 - North', None),
    'Route 4 - Between two houses in central ruins': (100384, 1147, 'Route 4 - North', None),
    'Route 4 - Northwest ruins': (100385, 1148, 'Route 4 - North', None),
    'Route 4 - South of Roughnecks in the west': (100049, 1149, 'Route 4 - North', None),
    'Route 4 - Hidden behind Pokéfan in northeast of ruins': (100050, 1150, 'Route 4 - North', None),
    'Route 4 - 2F of second house on right': (100051, 1151, 'Route 4 - North', None),
    'Route 4 - Inside Cottonee trade house': (100052, 1152, 'Route 4 - North', None),
    'Route 4 - Near water in southwest': (100053, 1153, 'Route 4', None),

    # Route 5
    'Route 5 - Near patch of dark grass': (100068, 1168, 'Route 5', None),
    'Route 5 - Southern side of the fence by the Driftveil Drawbridge': (100069, 1169, 'Route 5', None),

    # Route 6
    'Route 6 - Near the Season Research Lab': (100072, 1172, 'Route 6', None),
    'Route 6 - East of School Kid in east': (100073, 1173, 'Route 6', None),
    'Route 6 - Between Parasol Lady and School Kid west of Season Research Lab': (100074, 1174, 'Route 6', None),
    'Route 6 - Behind the Season Research Lab': (100076, 1176, 'Route 6 - Water', None),
    'Route 6 - Between bridges in south': (100077, 1177, 'Route 6 - Water', None),
    'Route 6 - East of Season Research Lab': (100078, 1178, 'Route 6 - Water', None),

    # Route 7
    'Route 7 - In the empty spot of the southern field of grass, southwest ball': (100101, 1201, 'Route 7', None),
    'Route 7 - In the east, past the easternmost raised walkway': (100102, 1202, 'Route 7', None),
    'Route 7 - In the empty spot in the northwestern field of grass': (100103, 1203, 'Route 7', None),
    'Route 7 - Southeast of Celestial Tower': (100104, 1204, 'Route 7', None),

    # Route 8
    'Route 8 - North of Youngster in northwest': (100220, 1320, 'Route 8', None),
    'Route 8 - Southwest from the Fisherman in the east': (100221, 1321, 'Route 8', None),
    'Route 8 - East of Youngster in north': (100222, 1322, 'Route 8', None),

    # Route 9
    'Route 9 - Northeast of the Tubeline Bridge gate': (100157, 1257, 'Route 9', None),
    'Route 9 - South of the Opelucid City gate': (100158, 1258, 'Route 9', None),
    'Route 9 - Where Challenger\'s Cave entrance used to be': (100159, 1259, 'Route 9', None),
    'Route 9 - On the road, north of the dark grass': (100160, 1260, 'Route 9', None),
    'Route 9 - Behind the fence southeast of the Tubeline Bridge gate': (100161, 1261, 'Route 9', None),

    # Route 11
    'Route 11 - Right of Pokémon Ranger in northeast down waterfall': (100154, 1254, 'Route 11 - Waterfall', None),
    'Route 11 - Up the northern waterfall on the western ledge': (100155, 1255, 'Route 11 - Waterfall', None),
    'Route 11 - At the end of the short land strip west of the bridge, behind the fence': (100156, 1256, 'Route 11', None),

    # Route 12
    'Route 12 - Dark grass north patch east': (100145, 1245, 'Route 12', None),
    'Route 12 - South of fence near Village Bridge Gate': (100146, 1246, 'Route 12', None),
    'Route 12 - Centre in the grass': (100147, 1247, 'Route 12', None),
    'Route 12 - Dark grass north patch west': (100374, 1474, 'Route 12', None),

    # Route 13
    'Route 13 - Behind Cut tree in the southwest': (100133, 1233, 'Route 13', None),
    'Route 13 - On a hill in the southwest': (100134, 1234, 'Route 13', None),
    'Route 13 - Across the two bridges in the centre of the route': (100135, 1235, 'Route 13', None),
    'Route 13 - In the northeast of the grass patch in the north near Cobalion': (100136, 1236, 'Route 13', None),
    'Route 13 - On a shore south of the Giant Chasm entrance': (100137, 1237, 'Giant Chasm', None),
    'Route 13 - On beach above ledge near Undella gate': (100138, 1238, 'Route 13', None),
    'Route 13 - In shallow water in the centre east across the water': (100139, 1239, 'Route 13', None),
    'Route 13 - On the island with dark grass in the centre east': (100140, 1240, 'Route 13', None),
    'Route 13 - In the southwest of the grass patch in the north near Cobalion': (100373, 1473, 'Route 13', None),

    # Route 14
    'Route 14 - In the north on the beach': (100129, 1229, 'Route 14', None),
    'Route 14 - Between three waterfalls in the northeast': (100130, 1230, 'Route 14', None),
    'Route 14 - In dark grass in the west': (100131, 1231, 'Route 14', None),
    'Route 14 - Near Black Belt on the highest section in the north': (100132, 1232, 'Route 14 - Waterfall', None),

    # Route 15
    'Route 15 - Southeast past the Strength boulder': (100251, 1351, 'Route 15', None),
    'Route 15 - On the rock wall in the northwest of the Poké Transfer Lab': (100252, 1352, 'Route 15', None),

    # Route 16
    'Route 16 - In the area north of the Strength boulder': (100063, 1163, 'Route 16', None),
    'Route 16 - Behind Cut tree in northwest': (100064, 1164, 'Route 16', None),

    # Route 17
    'Route 17 - Northwest of Fisherman in the southeast next to the gate': (100310, 1410, 'Route 17', None),
    'Route 17 - On the island of shallow water the Fisherman is standing on in the southwest': (100311, 1411, 'Route 17', None),
    'Route 17 - Shallow water southwest of the P2 Laboratory in the north': (100312, 1412, 'Route 17', None),

    # Route 18
    'Route 18 - In northeast of dark grass accessible from northern Route 17 entrance': (100313, 1413, 'Route 18', None),
    'Route 18 - Behind western Strength boulder, near Veteran': (100314, 1414, 'Route 18 - Strength Area', None),
    'Route 18 - On south of cliff southwest of Black Belt, behind Strength boulder': (100315, 1415, 'Route 18 - Strength Area', None),
    'Route 18 - Southwest, south of Veteran': (100316, 1416, 'Route 18', None),
    'Route 18 - South of the beach accessible from northern Route 17 entrance': (100317, 1417, 'Route 18', None),

    # Route 19
    'Route 19 - Near Youngster shortcut ledges': (100323, 1423, 'Route 19', None),
    'Route 19 - Northwest across water': (100001, 1101, 'Route 19', None),
    'Route 19 - Northeast up stairs across water': (100002, 1102, 'Route 19', None),

    # Route 20
    'Route 20 - North of Lass in grass patch': (100003, 1103, 'Route 20', None),
    'Route 20 - Behind leaf pile north of Youngster (Autumn)': (100004, 1104, 'Route 20', None),
    'Route 20 - Dark grass patch on eastern path': (100009, 1109, 'Route 20 - North', None),
    'Route 20 - In grass south of Twins in east': (100005, 1105, 'Route 20 - North', None),
    'Route 20 - East of Nursery Aide in east': (100006, 1106, 'Route 20 - North', None),
    'Route 20 - Land in the middle of leaves southeast ball (Autumn)': (100008, 1108, 'Route 20 - Autumn Islands', None),
    'Route 20 - Land in the middle of leaves northwest ball (Autumn)': (100007, 1107, 'Route 20 - Autumn Islands', None),
    'Route 20 - Cliff southeast of Cave of Being (Autumn)': (100010, 1110, 'Route 20 - Waterfall', None),

    # Route 21
    'Route 21 - In shallow water in the middle of the route': (100169, 1269, 'Route 21', None),
    'Route 21 - West of the northern Seaside Cave entrance': (100170, 1270, 'Route 21', None),

    # Route 22
    'Route 22 - On a cliff east of the Giant Chasm entrance accessed from the walkway': (100172, 1272, 'Route 22', None),
    'Route 22 - West of the pond in the south': (100173, 1273, 'Route 22', None),
    'Route 22 - In the dark grass in the middle of the route accessed from jumping off the walkway': (100174, 1274, 'Route 22', None),
    'Route 22 - At the end of the ridge in the middle of the route': (100175, 1275, 'Route 22', None),
    'Route 22 - Northwest corner of the northern dark grass': (100370, 1470, 'Route 22', None),
    'Route 22 - Southeast of the Giant Chasm entrance, southwest ball': (100371, 1471, 'Route 22', None),

    # Route 23
    'Route 23 - Southern cliff behind ledge': (100194, 1294, 'Route 23', None),
    'Route 23 - Behind the house on the cliff in the southeast': (100195, 1295, 'Route 23', None),
    'Route 23 - Next to Pokémon Ranger in leaf pile on cliff in east': (100196, 1296, 'Route 23', None),
    'Route 23 - At the end of a stream past the first house in the southeast': (100197, 1297, 'Route 23', None),
    'Route 23 - At a dead end above Ace Trainer in the north of the forest section in the northwest': (100198, 1298, 'Route 23 - Cut Area', None),
    'Route 23 - At a dead end in the southwesternmost section of the forest in the northwest': (100199, 1299, 'Route 23 - Cut Area', None),
    'Route 23 - On the pedestal where Azelf appears in the northwest': (100200, 1300, 'Route 23 - Cut Area', None),
    'Route 23 - At a dead end in the northwest of the forest section in the northwest': (100201, 1301, 'Route 23 - Cut Area', None),
    'Route 23 - Near Battle Girl on a mountaintop in the north after the Strength puzzle': (100202, 1302, 'Route 23 - Strength Area', None),
    'Route 23 - On a lone mountaintop in the north after the Strength puzzle': (100203, 1303, 'Route 23 - Strength Area', None),
    'Route 23 - In a grass patch to the northeast of the Strength puzzle in the northwest': (100372, 1472, 'Route 23 - Strength Area', None),    

    # Seaside Cave
    'Seaside Cave B1F - between all the Strength boulders': (100162, 1262, 'Seaside Cave', None),
    'Seaside Cave 1F - between the two Pokémon Rangers between two ledges in the southwest': (100163, 1263, 'Seaside Cave', None),
    'Seaside Cave 1F - centre, southeast of Route 21 exit': (100165, 1265, 'Seaside Cave', None),
    'Seaside Cave 1F - on the small island east of Black Belt in southeast': (100166, 1266, 'Seaside Cave', None),
    'Seaside Cave 1F - north accessible from B1F': (100167, 1267, 'Seaside Cave', None),
    'Seaside Cave B1F - in the south': (100168, 1268, 'Seaside Cave', None),

    # Shopping Mall
    'Shopping Mall - Bottom section, inside the storage room': (100376, 1476, 'Shopping Mall', None),

    # Strange House
    'Strange House - Basement, between the rows of bookshelves on first basement traverse': (100111, 1211, 'Strange House', None),
    'Strange House 2F - in the eastern room after second basement traverse': (100112, 1212, 'Strange House', None),
    'Strange House - Basement, northwest of the eastern stairs on second basement traverse': (100113, 1213, 'Strange House', None),
    'Strange House 1F - in the western room after first basement traverse': (100114, 1214, 'Strange House', None),

    # Striaton City
    'Striaton City - South of the fountain, right of the running girl': (100288, 1388, 'Striaton City', None),
    'Striaton City - Behind the fence on the southern edge of town': (100289, 1389, 'Striaton City', None),
    'Striaton City - 2F of upper east apartment': (100290, 1390, 'Striaton City', None),
    'Striaton City - Left of the fountain': (100294, 1394, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - South of 3F walkway': (100240, 1340, 'Twist Mountain', None),
    'Twist Mountain - Northeast cave 3F in east': (100241, 1341, 'Twist Mountain', None),
    'Twist Mountain - 2F western cave northwest': (100242, 1342, 'Twist Mountain', None),
    'Twist Mountain - East of southern walkway 2F': (100243, 1343, 'Twist Mountain', None),
    'Twist Mountain - Eastern lower cave (Winter)': (100244, 1344, 'Twist Mountain - Winter', None),
    'Twist Mountain - Lowest cave, east of Ice Rock': (100245, 1345, 'Twist Mountain', None),
    'Twist Mountain - 2F on west of southern walkway': (100246, 1346, 'Twist Mountain', None),
    'Twist Mountain - Southwest of Veteran west cave 2F': (100247, 1347, 'Twist Mountain', None),
    'Twist Mountain - Middle cave northeast in south (Winter)': (100248, 1348, 'Twist Mountain - Winter', None),
    "Twist Mountain - Cave north of the Worker's shed in the northwest (Spring/Summer/Autumn)": (100249, 1349, 'Twist Mountain - Non-Winter', None),
    'Twist Mountain - North of 3F walkway': (100250, 1350, 'Twist Mountain', None),

    # Undella Bay
    'Undella Bay - In southern shallow water': (100127, 1227, 'Undella Bay', None),
    'Undella Bay - Northeast of the Undella Town Pokémon Center': (100128, 1228, 'Undella Bay', None),

    # Undella Town
    'Undella Town - South of the Reversal Mountain entrance': (100126, 1226, 'Undella Town', None),

    # Victory road
    'Victory Road - Entrance exterior east of Pokémon Center': (100012, 1112, 'Victory Road', None),
    'Victory Road - Entrance, past ledge east of Pokémon Center': (100018, 1118, 'Victory Road', None),
    'Victory Road - Entrance, southeast of Pokémon Center': (100091, 1191, 'Victory Road', None),
    'Victory Road - Bonus: Black Bridge, east of entrance': (100204, 1304, 'Victory Road - Strength', None),
    'Victory Road - Section 2: Black Bridge, northwest': (100395, 1304, 'Victory Road - Strength', None),
    'Victory Road - Section 5: Mountain, outside Flash cave': (100205, 1305, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Mountain, outside Flash cave': (100396, 1305, 'Victory Road - Strength', None),
    'Victory Road - Bonus: Black Bridge, near Ace Trainer by water': (100206, 1306, 'Victory Road - Strength', None),
    'Victory Road - Section 2: Black Bridge, southwest': (100397, 1306, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Cave, north in Flash section': (100207, 1307, 'Victory Road - Dark Cave', None),
    'Victory Road - Section 3: Cave, north in Flash section': (100398, 1307, 'Victory Road - Dark Cave', None),
    'Victory Road - Section 2: Grove, southwestern corner': (100208, 1308, 'Victory Road - Grove', None),
    'Victory Road - Bonus: Grove, southwestern corner': (100399, 1308, 'Victory Road - Grove', None),
    'Victory Road - Bonus: Waterfall, across water': (100209, 1309, 'Victory Road - Waterfall', None),
    'Victory Road - Section 2: Grove, northeastern corner': (100210, 1310, 'Victory Road - Strength', None),
    'Victory Road - Bonus: Grove, northeastern corner': (100400, 1310, 'Victory Road - Strength', None),
    'Victory Road - Section 3: White Bridge, southeast of cave entrance': (100211, 1311, 'Victory Road - Strength', None),
    'Victory Road - Bonus: White Bridge, southeast of cave entrance': (100401, 1311, 'Victory Road - Strength', None),
    'Victory Road - Bonus: Black Bridge, across water in southeast': (100212, 1312, 'Victory Road - Strength', None),
    'Victory Road - Section 2: Black Bridge, southeast': (100402, 1312, 'Victory Road - Strength', None),
    'Victory Road - Section 5: Mountain, far southeast of League exit': (100213, 1313, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Mountain, far southeast of League exit': (100403, 1313, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Cave, southeast across pond in Flash section': (100214, 1314, 'Victory Road - Dark Cave', None),
    'Victory Road - Section 3: Cave, southeast across pond in Flash section': (100404, 1314, 'Victory Road - Dark Cave', None),
    'Victory Road - Section 5: Mountain, up second set of stairs north in southwest': (100215, 1315, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Mountain, up second set of stairs north in southwest': (100405, 1315, 'Victory Road - Strength', None),
    'Victory Road - Section 1 via waterfall, south by Veterans': (100218, 1318, 'Victory Road - Waterfall', None),
    'Victory Road - Approach to N\'s Castle, centre': (100322, 1422, 'Victory Road - Strength', None),

    # Village Bridge
    'Village Bridge - In the southwest grass': (100148, 1248, 'Village Bridge', None),
    'Village Bridge - On the central island below the bridge': (100149, 1249, 'Village Bridge', None),
    'Village Bridge - On the isle on the north part of the river': (100150, 1250, 'Village Bridge', None),
    'Village Bridge - On the tennis court in the southeast': (100151, 1251, 'Village Bridge', None),
    'Village Bridge - In the northeast corner': (100152, 1252, 'Village Bridge', None),
    'Village Bridge - East of the basketball court in the northwest': (100153, 1253, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Inside house near Pokéstar Studios entrance': (100022, 1122, 'Virbank City', None),
    'Virbank City - West of the Pokémon Center accessed from path above the Gym': (100016, 1116, 'Virbank City', None),

    # Virbank Complex Entrance
    'Virbank Complex - Waterside dead end past Roughneck in entrance': (100017, 1117, 'Virbank Complex Entrance', None),
    'Virbank Complex - Grass patch south of complex sign in entrance': (100019, 1119, 'Virbank Complex Entrance', None),

    # Virbank Complex Inside
    'Virbank Complex - In the southeast near the water accessed via the beams': (100021, 1121, 'Virbank Complex Inside', None),
    'Virbank Complex - End of the path behind the Cut tree near the inside entrance': (100020, 1120, 'Virbank Complex Inside', None),

    # Wellspring Cave
    'Wellspring Cave 1F - West of Battle Girl across the water': (100281, 1381, 'Wellspring Cave', None),
    'Wellspring Cave B1F - centre east down stairs': (100282, 1382, 'Wellspring Cave - B1F', None),
    'Wellspring Cave B1F - Southeast of Black Belt, before ledge in the southeast': (100283, 1383, 'Wellspring Cave - B1F', None),
    'Wellspring Cave B1F - Northern end': (100284, 1384, 'Wellspring Cave - B1F', None),
    'Wellspring Cave 1F - East of Hiker in the east': (100285, 1385, 'Wellspring Cave', None),
    'Wellspring Cave B1F - On cliff, south of Battle Girl in centre': (100287, 1387, 'Wellspring Cave - B1F', None),
}

# Hidden items (domain: 200000 + N, flag = 2820 + N)
HIDDEN_ITEM_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Abundant Shrine
    'Abundant Shrine - Hidden west of Youngster near shrine in northwest': (200177, 2997, 'Abundant Shrine', None),
    'Abundant Shrine - Hidden east of ledge near pond in the south': (200178, 2998, 'Abundant Shrine', None),
    'Abundant Shrine - Hidden southeast of Youngster in east': (200179, 2999, 'Abundant Shrine', None),
    'Abundant Shrine - Hidden eastern part of fence near Breeder in northeast': (200180, 3000, 'Abundant Shrine - Water', None),

    # Accumula Town
    'Accumula Town - Hidden in the trash can near the benches': (200200, 3020, 'Accumula Town', None),

    # Castelia Sewers
    'Castelia Sewers - Hidden northwest of Worker in west (Spring/Summer + Surf)': (200078, 2898, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Hidden northeast of easternmost room (Spring/Summer + Surf)': (200079, 2899, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Hidden east of Worker in centre (Spring/Summer + Surf)': (200080, 2900, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Hidden in southern canal southwest of eastern Janitor (Spring/Summer + Surf)': (200081, 2901, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Hidden in southernmost area (Spring/Summer + Surf)': (200082, 2902, 'Castelia Sewers - Water', None),

    # Celestial Tower
    'Celestial Tower 5F - Hidden west of the bell platform': (200158, 2978, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave 1F - Hidden north of Guitarist, under the crystal': (200061, 2881, 'Chargestone Cave', None),
    'Chargestone Cave 1F - Hidden north of the bridge': (200062, 2882, 'Chargestone Cave', None),
    'Chargestone Cave 1F - Hidden southwest of the cave, arriving from B1F': (200063, 2883, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B1F - Hidden north of Nugget Brothers': (200064, 2884, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B2F - Hidden at the dead end northeast of Ace Trainer': (200065, 2885, 'Chargestone Cave - Past Bridge', None),

    # Clay Tunnel
    'Clay Tunnel - Hidden Driftveil side northwest corner rock': (200117, 2937, 'Clay Tunnel', None),
    'Clay Tunnel - Hidden Driftveil side down stairs near Strength boulder': (200118, 2938, 'Clay Tunnel', None),
    'Clay Tunnel - Hidden middle room rock on southwest side of pond': (200119, 2939, 'Clay Tunnel', None),
    'Clay Tunnel - Hidden middle room island rock in middle of pond': (200120, 2940, 'Clay Tunnel - Surf', None),
    'Clay Tunnel - Hidden Twist Mountain side rock by Underground Ruins entrance': (200121, 2941, 'Clay Tunnel', None),
    'Clay Tunnel - Hidden Twist Mountain side rock right of pond': (200122, 2942, 'Clay Tunnel - Surf', None),

    # Desert Resort
    'Desert Resort - Hidden southwest of Relic Castle entrance': (200051, 2871, 'Desert Resort', None),
    'Desert Resort - Hidden on central raised part encircled by a male Backpacker': (200052, 2872, 'Desert Resort', None),
    'Desert Resort - Hidden in raised deep sand near the centre by a female Backpacker': (200053, 2873, 'Desert Resort', None),
    'Desert Resort - Hidden in deep sand near the entrance to the northwest of the deep sand plus': (200054, 2874, 'Desert Resort', None),
    'Desert Resort - Hidden in the southwest in a dead end': (200055, 2875, 'Desert Resort', None),
    'Desert Resort - Hidden in the northeast': (200056, 2876, 'Desert Resort', None),

    # Dragonspiral Tower
    'Dragonspiral Tower 2F - Hidden on a lone rock in the north': (200071, 2891, 'Dragonspiral Tower', None),
    'Dragonspiral Tower 7F - Hidden northeast corner': (200072, 2892, 'Dragonspiral Tower', None),

    # Dreamyard
    'Dreamyard - Hidden southern area: northwest of the eastern stairs, in front of the furnace': (200041, 2861, 'Dreamyard', None),
    'Dreamyard - Hidden northern area: In the eastern patch of tall grass in the north, accessible from the southwestern stairs in the ruins': (200042, 2862, 'Dreamyard', None),

    # Driftveil City
    'Driftveil City - Hidden southwest of the statue by the Driftveil Drawbridge': (200004, 2824, 'Driftveil City', None),
    'Driftveil City - Hidden in the pile of dirt south of the Clay Tunnel entrance, accessible after entering the Hall of Fame': (200005, 2825, 'Driftveil City', None),

    # Floccesy Town
    'Floccesy Town - Hidden in dead end from northwest of Route 20 (Autumn)': (200212, 3032, 'Floccesy Town - Autumn Ledge', None),

    # Giant Chasm
    'Giant Chasm - Hidden Route 13 exit, in the southern patch of grass': (200073, 2893, 'Giant Chasm', None),
    'Giant Chasm - Hidden Route 13 exit, on the broken bridge': (200074, 2894, 'Giant Chasm', None),
    'Giant Chasm - Hidden cave, behind a Strength boulder near the northeastern corner': (200075, 2895, 'Giant Chasm', None),
    'Giant Chasm - Hidden cave, on a rock near the southern exit': (200076, 2896, 'Giant Chasm', None),
    'Giant Chasm - Hidden cave, in the small indent near the northwest corner': (200077, 2897, 'Giant Chasm', None),

    # Guidance Chamber
    'Guidance Chamber 3F - Hidden west of entrance': (200154, 2974, 'Guidance Chamber', None),
    'Guidance Chamber 3F - Hidden at the dead end right above the old man': (200155, 2975, 'Guidance Chamber', None),

    # Humilau City
    'Humilau City - Hidden in the trash can of the hut in the south': (200008, 2828, 'Humilau City', None),
    'Humilau City - Hidden in the shallow water in the centre': (200208, 3028, 'Humilau City', None),

    # Lostlorn Forest
    'Lostlorn Forest - Hidden southwest of main clearing': (200184, 3004, 'Lostlorn Forest', None),
    'Lostlorn Forest - Hidden behind Veteran in northwest corner of cliff': (200185, 3005, 'Lostlorn Forest - Waterfall', None),

    # Mistralton Cave
    'Mistralton Cave 1F - Hidden southeast of the entrance after wrapping around': (200151, 2971, 'Mistralton Cave', None),
    'Mistralton Cave 2F - Hidden south': (200152, 2972, 'Mistralton Cave', None),
    'Mistralton Cave 2F - Hidden northwest': (200153, 2973, 'Mistralton Cave', None),

    # Mistralton City
    'Mistralton City - Hidden middle of runway between two planes': (200006, 2826, 'Mistralton City', None),
    'Mistralton City - Hidden in the house east of the Pokémon Center, in a trash can': (200007, 2827, 'Mistralton City', None),

    # Moor of Icirrus
    'Moor of Icirrus - Hidden on the ground beside trees southwest of Fisherman in the east': (200161, 2981, 'Moor of Icirrus', None),
    'Moor of Icirrus - Hidden in the gap between trees west of Fisherman in the north': (200162, 2982, 'Moor of Icirrus', None),
    'Moor of Icirrus - Hidden in the gap between trees on the left at the entrance': (200163, 2983, 'Moor of Icirrus', None),

    # Nacrene City
    'Nacrene City - Hidden at the western end of the railroad tracks': (200001, 2821, 'Nacrene City', None),

    # Nimbasa City
    'Nimbasa City - Hidden narrow path west of the Pokémon Center above the sign': (200002, 2822, 'Nimbasa City', None),
    'Nimbasa City - Hidden in the trash can near the Rondez-View Ferris Wheel': (200003, 2823, 'Nimbasa City', None),

    # Nuvema Town
    'Nuvema Town - Hidden southwest of central house on the path': (200199, 3019, 'Nuvema Town', None),

    # PWT
    'PWT - Hidden in the trash can north of the fountain': (200059, 2879, 'PWT', None),
    'PWT - Hidden southeast of the Relic Passage entrance': (200060, 2880, 'PWT', None),

    # Pinwheel Forest
    'Pinwheel Forest - Hidden outside: In a puddle in the south': (200043, 2863, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden outside: Outer forest northeast behind northern fence': (200044, 2864, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden outside: On the eastern part of ledge in southeast': (200045, 2865, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden inside: Northeast east of Rumination Field': (200046, 2866, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden inside: Centre inner forest west of Lass and Youngster': (200047, 2867, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden inside: East of the bridge near Surf section': (200048, 2868, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden inside: East near the bridge in southwest of dark grass': (200049, 2869, 'Pinwheel Forest', None),
    'Pinwheel Forest - Hidden inside: Southwest inner forest west of Youngster': (200050, 2870, 'Pinwheel Forest', None),

    # Relic Castle
    'Relic Castle B1F - Hidden in westernmost sand pile after falling through quicksand': (200057, 2877, 'Relic Castle', None),
    'Relic Castle - Hidden centre of room below Volcarona\'s room accessed from Relic Passage': (200058, 2878, 'Relic Castle - Volcarona', None),

    # Relic Passage
    'Relic Passage - Hidden Castelia section south of female Scientist in east': (200110, 2930, 'Relic Passage (Castelia)', None),
    'Relic Passage - Hidden middle section dead end in the southwest': (200111, 2931, 'Relic Passage', None),
    'Relic Passage - Hidden middle section rock in the southwest': (200112, 2932, 'Relic Passage', None),
    'Relic Passage - Hidden middle section rock near central Psychic': (200113, 2933, 'Relic Passage', None),
    'Relic Passage - Hidden middle section rock near northeastern Psychic': (200114, 2934, 'Relic Passage', None),
    'Relic Passage - Hidden middle section rock near Backpacker in southeast': (200115, 2935, 'Relic Passage', None),
    'Relic Passage - Hidden middle section eastern separate room': (200116, 2936, 'Relic Passage - Strength', None),

    # Reversal Mountain
    'Reversal Mountain B1F - Hidden in the stalagmite below the stairs': (200087, 2907, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden in the stalagmite north of Backpacker and Hiker in the west': (200088, 2908, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden in stalagmite south of Scientist in east of main cavern': (200089, 2909, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden in stalagmite in the southeast of main cavern': (200090, 2910, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden dead end south of Ace Trainers in north of main cavern': (200091, 2911, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden dead-end tunnel east of Backpacker and Hiker in south': (200092, 2912, 'Reversal Mountain', None),
    'Reversal Mountain B1F - Hidden in a rock near the big rock': (200093, 2913, 'Reversal Mountain', None),
    'Reversal Mountain - Hidden rock centre-east by B1F stairs': (200094, 2914, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden north in southern dead end west of Ace Trainers, in a rock': (200095, 2915, 'Reversal Mountain', None),
    'Reversal Mountain - Hidden north in rock west of Ace Trainers': (200096, 2916, 'Reversal Mountain', None),
    'Reversal Mountain - Hidden in central west, northeast of Battle Girl': (200097, 2917, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Hidden far southeast in a rock': (200098, 2918, 'Reversal Mountain', None),

    # Route 1
    'Route 1 - Hidden in the middle of the central patch of tall grass': (200128, 2948, 'Route 1', None),
    'Route 1 - Hidden atop the southern hill in the western section': (200129, 2949, 'Route 1 - Water', None),

    # Route 2
    'Route 2 - Hidden on the road between two ledges in the north': (200130, 2950, 'Route 2', None),
    'Route 2 - Hidden near the Lass behind Cut tree in the northwest': (200131, 2951, 'Route 2', None),

    # Route 3
    'Route 3 - Hidden in the sandbox west of the daycare in the northeast': (200132, 2952, 'Route 3', None),
    'Route 3 - Hidden west of Fisherman in the west across the pond': (200133, 2953, 'Route 3 - Water', None),
    'Route 3 - Hidden on the ledge near Lass in the northwest': (200210, 3030, 'Route 3', None),

    # Route 4
    'Route 4 - Hidden western area between stairways southeast of rest house': (200137, 2957, 'Route 4 - North', None),
    'Route 4 - Hidden in deep sand between two stairways south of Policeman': (200138, 2958, 'Route 4 - North', None),
    'Route 4 - Hidden deep sand north of fences east of the Roughnecks': (200139, 2959, 'Route 4 - North', None),
    'Route 4 - Hidden in the middle of a deep sand patch in the west': (200140, 2960, 'Route 4 - North', None),
    'Route 4 - Hidden western area west of Bikers in deep sand next to barricade': (200141, 2961, 'Route 4 - North', None),
    'Route 4 - Hidden in deep sand in southwest of ruins': (200142, 2962, 'Route 4 - North', None),
    'Route 4 - Hidden northwest of crossroads along ruins road': (200143, 2963, 'Route 4 - North', None),
    'Route 4 - Hidden far east deep sand in ruins': (200144, 2964, 'Route 4 - North', None),
    'Route 4 - Hidden southeast of ruins between two houses': (200145, 2965, 'Route 4 - North', None),
    'Route 4 - Hidden west of Pokéfan in east of ruins': (200146, 2966, 'Route 4 - North', None),

    # Route 5
    'Route 5 - Hidden in middle of road below Trainer Tips sign': (200147, 2967, 'Route 5', None),

    # Route 6
    'Route 6 - Hidden south of the Season Research Lab, empty spot in patch of grass': (200148, 2968, 'Route 6', None),
    'Route 6 - Hidden east of Season Research Lab': (200149, 2969, 'Route 6 - Water', None),
    'Route 6 - Hidden in a patch of grass, west of the Hiker in the north': (200150, 2970, 'Route 6', None),

    # Route 7
    'Route 7 - Hidden behind the Celestial Tower': (200156, 2976, 'Route 7', None),
    'Route 7 - Hidden on a rock southwest of the northern house': (200157, 2977, 'Route 7', None),

    # Route 8
    'Route 8 - Hidden between Fisherman and Parasol Lady in north (Surf, Winter)': (200159, 2979, 'Route 8', None),
    'Route 8 - Hidden northwest of Icirrus City entrance in southwest': (200160, 2980, 'Route 8', None),

    # Route 9
    'Route 9 - Hidden east of where Challenger\'s Cave entrance used to be': (200164, 2984, 'Route 9', None),

    # Route 11
    'Route 11 - Hidden up the northern waterfall on the eastern ledge': (200165, 2985, 'Route 11 - Waterfall', None),
    'Route 11 - Hidden far northwest corner of the grass patch in the west': (200166, 2986, 'Route 11', None),

    # Route 12
    'Route 12 - Hidden east of the tallest hill': (200167, 2987, 'Route 12', None),
    'Route 12 - Hidden northwest near the dark grass': (200168, 2988, 'Route 12', None),
    'Route 12 - Hidden northeast corner of the dark grass': (200169, 2989, 'Route 12', None),

    # Route 13
    'Route 13 - Hidden on beach south of the sand bar': (200170, 2990, 'Route 13', None),
    'Route 13 - Hidden on a hill in the southwest in the grass': (200171, 2991, 'Route 13', None),
    'Route 13 - Hidden northern beach east of the stairs': (200172, 2992, 'Route 13', None),
    'Route 13 - Hidden next to rock above ledge near Undella gate': (200173, 2993, 'Route 13', None),
    'Route 13 - Hidden in rock accessed from Giant Chasm entrance': (200174, 2994, 'Giant Chasm', None),

    # Route 14
    'Route 14 - Hidden northeast corner on the highest section': (200175, 2995, 'Route 14 - Waterfall', None),
    'Route 14 - Hidden east of Abundant Shrine entrance next to ledge': (200176, 2996, 'Route 14 - Waterfall', None),

    # Route 15
    'Route 15 - Hidden on the ground by the dark grass in the north past the Strength boulder': (200181, 3001, 'Route 15', None),
    'Route 15 - Hidden behind a rock east of Backpacker in southwest': (200182, 3002, 'Route 15', None),

    # Route 16
    'Route 16 - Hidden north of Backpacker behind the Strength boulder': (200183, 3003, 'Route 16', None),

    # Route 17
    'Route 17 - Hidden southwest of Fisherman in the southeast next to the gate': (200205, 3025, 'Route 17', None),
    'Route 17 - Hidden on the L-shaped island of shallow water in the north': (200206, 3026, 'Route 17', None),
    'Route 17 - Hidden in shallow water southwest of the P2 Laboratory in the north': (200207, 3027, 'Route 17', None),

    # Route 18
    'Route 18 - Hidden in northwest of dark grass accessible from northern Route 17 entrance': (200186, 3006, 'Route 18', None),
    'Route 18 - Hidden on south of cliff southeast of Black Belt, behind Strength boulder': (200187, 3007, 'Route 18 - Strength Area', None),
    'Route 18 - Hidden south of the beach in a rock accessible from northern Route 17 entrance': (200188, 3008, 'Route 18', None),
    'Route 18 - Hidden northeast down the stairs': (200189, 3009, 'Route 18', None),
    'Route 18 - Hidden in stone in southwest on beach': (200190, 3010, 'Route 18', None),
    'Route 18 - Hidden on south of beach accessible from northern Route 17 entrance': (200191, 3011, 'Route 18', None),

    # Route 19
    'Route 19 - Hidden below Alder on cliff after beating Cheren': (200192, 3012, 'Route 19', None),

    # Route 20
    'Route 20 - Hidden in rock northwest of Hiker': (200211, 3031, 'Route 20', None),
    'Route 20 - Hidden on eastern island': (200193, 3013, 'Route 20 - North', None),
    'Route 20 - Hidden between central ledges': (200194, 3014, 'Route 20 - North', None),

    # Route 22
    'Route 22 - Hidden on the northwestern cliff': (200195, 3015, 'Route 22', None),
    'Route 22 - Hidden on the isolated cliff in the middle of the route between two walkways': (200196, 3016, 'Route 22', None),

    # Route 23
    'Route 23 - Hidden in a rock south of the Strength puzzle in the northwest': (200099, 2919, 'Route 23 - Strength Area', None),
    'Route 23 - Hidden at a dead end in the northeast of the forest section in the northwest': (200100, 2920, 'Route 23 - Cut Area', None),
    'Route 23 - Hidden on a lone mountaintop in the north after the Strength puzzle': (200101, 2921, 'Route 23 - Strength Area', None),
    'Route 23 - Hidden in rock south of Black Belt on the cliff in the southeast': (200197, 3017, 'Route 23', None),
    'Route 23 - Hidden east of Ace Trainer in the northeast': (200198, 3018, 'Route 23', None),    

    # Seaside Cave
    'Seaside Cave 1F - Hidden in the rock at the northeast corner': (200123, 2943, 'Seaside Cave', None),
    'Seaside Cave 1F - Hidden in between three ledges in the west': (200124, 2944, 'Seaside Cave', None),

    # Striaton City
    'Striaton City - Hidden to the right of the Route 3 entrance across the water': (200000, 2820, 'Striaton City', None),
    'Striaton City - Hidden south of the fountain, to the left of the running girl': (200209, 3029, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - Hidden outside, inside the trash can next to the vending machine (Spring/Summer/Autumn)': (200066, 2886, 'Twist Mountain - Non-Winter', None),
    'Twist Mountain - Hidden inside a boulder east cave 2F': (200067, 2887, 'Twist Mountain', None),
    'Twist Mountain - Hidden middle cave northeast in northeast (Winter)': (200068, 2888, 'Twist Mountain - Winter', None),
    'Twist Mountain 2F - Hidden southwest of western cave': (200069, 2889, 'Twist Mountain', None),
    "Twist Mountain - Hidden cave north of the Worker's shed in the northwest inside boulder (Spring/Summer/Autumn)": (200070, 2890, 'Twist Mountain - Non-Winter', None),

    # Undella Bay
    'Undella Bay - Hidden east of the Undella Town Pokémon Center, on the sand': (200083, 2903, 'Undella Town', None),

    # Undella Town
    'Undella Town - Hidden west of the bulldozer near Reversal Mountain': (200201, 3021, 'Undella Town', None),
    'Undella Town - Hidden on the beach, southwest of the Pokémon Center': (200202, 3022, 'Undella Town', None),
    'Undella Town - Hidden on the beach, south of the gate': (200203, 3023, 'Undella Town', None),
    'Undella Town - Hidden on the beach, southeast of Reversal Mountain entrance': (200204, 3024, 'Undella Town', None),

    # Victory road
    'Victory Road - Hidden entrance, south of Pokémon Center': (200102, 2922, 'Victory Road', None),
    'Victory Road - Hidden entrance, southeast of Pokémon Center': (200103, 2923, 'Victory Road', None),
    'Victory Road - Hidden section 4: Cave, in rock in southwest': (200104, 2924, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 3: Cave, in rock in southwest': (200218, 2924, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 4: Cave, southeast': (200105, 2925, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 3: Cave, southeast': (200217, 2925, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 4: Cave, south in Flash section': (200106, 2926, 'Victory Road - Dark Cave', None),
    'Victory Road - Hidden section 3: Cave, south in Flash section': (200213, 2926, 'Victory Road - Dark Cave', None),
    'Victory Road - Hidden section 4: Cave, east across pond in Flash section': (200107, 2927, 'Victory Road - Dark Cave', None),
    'Victory Road - Hidden section 3: Cave, east across pond in Flash section': (200214, 2927, 'Victory Road - Dark Cave', None),
    'Victory Road - Hidden section 5: Mountain, southwest halfway up stairs east of Battle Girl': (200108, 2928, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 4: Mountain, southwest halfway up stairs east of Battle Girl': (200215, 2928, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 5: Mountain, southeast of League gate in rock': (200109, 2929, 'Victory Road - Strength', None),
    'Victory Road - Hidden section 4: Mountain, southeast of League gate in rock': (200216, 2929, 'Victory Road - Strength', None),

    # Village Bridge
    'Village Bridge - Hidden in the trash can in the northwest corner': (200125, 2945, 'Village Bridge', None),
    'Village Bridge - Hidden in the southwest grass': (200126, 2946, 'Village Bridge', None),
    'Village Bridge - Hidden in the northwest of the dark grass in the northeast': (200127, 2947, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Hidden in trash can west of nursery': (200040, 2860, 'Virbank City', None),

    # Virbank Complex Entrance
    'Virbank City - Hidden at dead end accessed from path above the Gym': (200084, 2904, 'Virbank Complex Entrance', None),

    # Virbank Complex Inside
    'Virbank Complex - Hidden in grass southeast of Youngster': (200085, 2905, 'Virbank Complex Inside', None),
    'Virbank Complex - Hidden at end of dark grass': (200086, 2906, 'Virbank Complex Inside', None),

    # Wellspring Cave
    'Wellspring Cave B1F - Hidden centre east in dead end': (200134, 2954, 'Wellspring Cave - B1F', None),
    'Wellspring Cave B1F - Hidden east of Veteran in the north': (200135, 2955, 'Wellspring Cave - B1F', None),
    'Wellspring Cave B1F - Hidden southwest of Veteran in north': (200136, 2956, 'Wellspring Cave - B1F', None),
}

