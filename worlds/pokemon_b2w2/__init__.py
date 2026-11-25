from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, ClassVar

import settings
from BaseClasses import MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World

from . import bizhawk_client, rom
from .groups import get_item_groups, get_location_groups
from .items import ITEM_NAME_TO_ID, ITEM_TABLE, PokemonB2W2Item
from .locations import LOCATION_NAME_TO_ID, LOCATION_ID_TO_FLAG
from .options import PokemonB2W2Options
from .options.groups import option_groups
from .regions import create_regions_and_locations, check_goal_completion
from .rom import PokemonB2W2Patch, PokemonB2Patch, PokemonW2Patch

APWORLD_VERSION = "0.1.1"

bizhawk_client.register_client()


class PokemonB2W2Settings(settings.Group):

    class PokemonBlack2RomFile(settings.UserFilePath):
        # File name of your Pokémon Black 2 version ROM
        description = "Pokemon Black 2 Version ROM"
        copy_to = "PokemonBlack2.nds"

        @classmethod
        def validate(cls, path: str) -> None:
            rom.validate("black2", path)

    class PokemonWhite2RomFile(settings.UserFilePath):
        # File name of your Pokémon White 2 version ROM
        description = "Pokemon White 2 Version ROM"
        copy_to = "PokemonWhite2.nds"

        @classmethod
        def validate(cls, path: str) -> None:
            rom.validate("white2", path)

    black2_rom: PokemonBlack2RomFile = PokemonBlack2RomFile(PokemonBlack2RomFile.copy_to)
    white2_rom: PokemonWhite2RomFile = PokemonWhite2RomFile(PokemonWhite2RomFile.copy_to)


class PokemonB2W2WebWorld(WebWorld):
    theme = "ocean"
    rich_text_options_doc = True
    option_groups = option_groups


class PokemonB2W2World(World):
    """
    Explore the Unova region two years after the events of Black and White!
    New areas, new story, new characters!
    """
    game = "Pokemon Black 2 and White 2"
    options_dataclass = PokemonB2W2Options
    options: PokemonB2W2Options
    topology_present = True
    ut_can_gen_without_yaml: ClassVar[bool] = True
    web = PokemonB2W2WebWorld()

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID
    item_name_groups = get_item_groups()
    location_name_groups = get_location_groups()
    settings_key = "pokemon_b2w2_settings"
    settings: ClassVar[PokemonB2W2Settings]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game)
        if isinstance(passthrough, dict):
            if "starting_day" in passthrough:
                self.starting_day = int(passthrough["starting_day"])
            if "starting_season" in passthrough:
                self.starting_season = int(passthrough["starting_season"])
            pt_opts = passthrough.get("options", {})
            if isinstance(pt_opts, dict):
                for opt_name in (
                    "version",
                    "goal",
                    "exclude_postgame_checks",
                    "top_trainers_required",
                    "top_trainers_allowed",
                    "tmhm_hunt",
                    "legendary_hunt_required",
                    "legendary_hunt_allowed",
                    "shuffle_badges",
                    "hidden_items",
                    "habitat_list_checks",
                    "trainersanity",
                    "flash_logic",
                    "dowsing_machine_logic",
                    "infinite_rare_candies",
                ):
                    if opt_name in pt_opts and hasattr(self.options, opt_name):
                        cur_opt = getattr(self.options, opt_name)
                        val = pt_opts[opt_name]
                        if hasattr(cur_opt, "range_start") and hasattr(cur_opt, "range_end") and isinstance(val, int):
                            val = max(cur_opt.range_start, min(cur_opt.range_end, val))
                        setattr(self.options, opt_name, type(cur_opt).from_any(val))

        if not hasattr(self, "starting_day"):
            self.starting_day = self.random.choice(range(7))
        if not hasattr(self, "starting_season"):
            self.starting_season = self.random.choice(range(4))

        # Validate non-empty goals and allowed target sets
        goal_opt = getattr(self.options, "goal", None)
        active_goals = (
            set(goal_opt.value)
            if (goal_opt is not None and hasattr(goal_opt, "value") and isinstance(goal_opt.value, set))
            else set()
        )
        if goal_opt is not None and not active_goals:
            goal_opt.value = {"champion"}
            active_goals = {"champion"}

        excl_post = getattr(self.options, "exclude_postgame_checks", None)
        if excl_post is not None and active_goals.issubset({"champion", "iris"}):
            excl_post.value = 1

        # Clamp goal requirement counts and fill empty allowed sets with a random target
        top_allowed = getattr(self.options, "top_trainers_allowed", None)
        top_req = getattr(self.options, "top_trainers_required", None)
        if top_allowed is not None and top_req is not None:
            if not top_allowed.value and "top_trainers" in active_goals:
                top_allowed.value = {self.random.choice(sorted(top_allowed.valid_keys))}
            allowed_count = len(top_allowed.value)
            if allowed_count > 0 and top_req.value > allowed_count:
                top_req.value = allowed_count

        leg_allowed = getattr(self.options, "legendary_hunt_allowed", None)
        leg_req = getattr(self.options, "legendary_hunt_required", None)
        if leg_allowed is not None and leg_req is not None:
            if not leg_allowed.value and "legendary_hunt" in active_goals:
                leg_allowed.value = {self.random.choice(sorted(leg_allowed.valid_keys))}
            allowed_count = len(leg_allowed.value)
            if allowed_count > 0 and leg_req.value > allowed_count:
                leg_req.value = allowed_count

        # Pull starting inventory from the pool
        start_inv = getattr(self.options, "start_inventory", None)
        start_inv_pool = getattr(self.options, "start_inventory_from_pool", None)
        if start_inv and getattr(start_inv, "value", None) and start_inv_pool is not None:
            for item_name, count in list(start_inv.value.items()):
                start_inv_pool.value[item_name] = start_inv_pool.value.get(item_name, 0) + count
            start_inv.value.clear()

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data

    def create_regions(self) -> None:
        create_regions_and_locations(self)
        self.multiworld.completion_condition[self.player] = lambda state: check_goal_completion(state, self.player, self)

    def create_item(self, name: str) -> PokemonB2W2Item:
        info = ITEM_TABLE[name]
        classification = info.classification
        goal_val = getattr(self.options, "goal", None)
        active_goals = goal_val.value if (goal_val is not None and hasattr(goal_val, "value") and isinstance(goal_val.value, set)) else set()
        if name.startswith("TM") and classification == ItemClassification.useful:
            classification = ItemClassification.progression_skip_balancing
        elif name == "Rare Candy":
            inf_candy = getattr(self.options, "infinite_rare_candies", None)
            if inf_candy is not None and inf_candy.value:
                classification = ItemClassification.filler
        elif name == "Dowsing Machine":
            hidden_opt = getattr(self.options, "hidden_items", None)
            dowsing_opt = getattr(self.options, "dowsing_machine_logic", None)
            if (hidden_opt is not None and not hidden_opt.value) or (
                dowsing_opt is not None and int(dowsing_opt.value) == 2
            ):
                classification = ItemClassification.useful
        elif name == "Prop Case":
            ts_opt = getattr(self.options, "trainersanity", None)
            if ts_opt is not None and ts_opt.value:
                classification = ItemClassification.progression
        return PokemonB2W2Item(name, classification, info.ap_id, self.player)

    _FILLER_ITEMS: tuple[str, ...] = (
        "Potion",
        "Super Potion",
        "Hyper Potion",
        "Full Restore",
        "Revive",
        "Full Heal",
        "Parlyz Heal",
        "Antidote",
        "Awakening",
        "Burn Heal",
        "Ether",
        "Max Ether",
        "Elixir",
        "HP Up",
        "Protein",
        "Iron",
        "Carbos",
        "Calcium",
        "Zinc",
        "Poké Ball",
        "Great Ball",
        "Ultra Ball",
        "Net Ball",
        "Dusk Ball",
        "Quick Ball",
        "Timer Ball",
        "Repel",
        "Super Repel",
        "Max Repel",
        "Escape Rope",
        "Rare Candy",
        "PP Up",
        "Heart Scale",
        "Nugget",
        "Big Pearl",
        "Star Piece",
        "Oran Berry",
        "Cheri Berry",
        "Pecha Berry",
        "Sitrus Berry",
        "Lum Berry",
    )

    def get_filler_item_name(self) -> str:
        return self.random.choice(self._FILLER_ITEMS)

    def create_items(self) -> None:
        item_pool: list[PokemonB2W2Item] = []

        # Core progression badges and key items
        badge_names = [
            "Basic Badge",
            "Toxic Badge",
            "Insect Badge",
            "Bolt Badge",
            "Quake Badge",
            "Jet Badge",
            "Legend Badge",
            "Wave Badge",
        ]
        gym_loc_names = [
            "Aspertia Gym - Gym Leader Cheren Basic Badge",
            "Virbank Gym - Gym Leader Roxie Toxic Badge",
            "Castelia Gym - Gym Leader Burgh Insect Badge",
            "Nimbasa Gym - Gym Leader Elesa Bolt Badge",
            "Driftveil Gym - Gym Leader Clay Quake Badge",
            "Mistralton Gym - Gym Leader Skyla Jet Badge",
            "Opelucid Gym - Gym Leader Drayden Legend Badge",
            "Humilau Gym - Gym Leader Marlon Wave Badge",
        ]
        badge_opt = getattr(self.options, "shuffle_badges", None)
        shuffle_badges = bool(badge_opt.value) if badge_opt is not None else True

        if not shuffle_badges:  # Vanilla
            for loc_name, badge_name in zip(gym_loc_names, badge_names):
                loc = self.get_location(loc_name)
                loc.place_locked_item(self.create_item(badge_name))
        else:  # Shuffled into pool (default)
            for b in badge_names:
                item_pool.append(self.create_item(b))

        other_progression_items = [
            "Dowsing Machine",
            "Bicycle",
            "Super Rod",
            "HM01 Cut",
            "HM02 Fly",
            "HM03 Surf",
            "HM04 Strength",
            "HM05 Waterfall",
            "HM06 Dive",
            "Colress MCHN",
            "Plasma Card",
            "Card Key",
            "DNA Splicers",
            "Lunar Wing",
            "Magma Stone",
            "Permit",
            "TM70 Flash",
            "Grubby Hanky",
        ]
        v_opt = getattr(self.options, "version", None)
        v_key = v_opt.current_key if v_opt is not None else "black2"
        other_progression_items.append("Light Stone" if v_key in ("white2", "white_2", "w2") else "Dark Stone")
        ts_opt = getattr(self.options, "trainersanity", None)
        if ts_opt is not None and ts_opt.value:
            other_progression_items.append("Prop Case")
        for item_name in other_progression_items:
            item_pool.append(self.create_item(item_name))

        # Day of the week progression handling
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if not hasattr(self, "starting_day"):
            self.starting_day = self.random.choice(range(7))
        starting_day_name = days[self.starting_day]

        self.multiworld.push_precollected(self.create_item(starting_day_name))
        for day_idx, d_name in enumerate(days):
            if day_idx != self.starting_day:
                item_pool.append(self.create_item(d_name))

        # Seasons progression handling
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        if not hasattr(self, "starting_season"):
            self.starting_season = self.random.choice(range(4))
        starting_season_name = seasons[self.starting_season]

        self.multiworld.push_precollected(self.create_item(starting_season_name))
        for s_idx, s_name in enumerate(seasons):
            if s_idx != self.starting_season:
                item_pool.append(self.create_item(s_name))

        # Useful items: training/EV gear, evolution stones & items, held battle items
        useful_items = [
            "Medal Box",
            "Exp. Share",
            "Lucky Egg",
            "Amulet Coin",
            "Soothe Bell",
            "Macho Brace",
            "Power Bracer",
            "Power Belt",
            "Power Lens",
            "Power Band",
            "Power Anklet",
            "Power Weight",
            "Sun Stone",
            "Moon Stone",
            "Fire Stone",
            "Thunderstone",
            "Water Stone",
            "Leaf Stone",
            "Shiny Stone",
            "Dusk Stone",
            "Dawn Stone",
            "Oval Stone",
            "King's Rock",
            "Metal Coat",
            "Dragon Scale",
            "Up-Grade",
            "DeepSeaTooth",
            "DeepSeaScale",
            "Protector",
            "Electirizer",
            "Magmarizer",
            "Dubious Disc",
            "Reaper Cloth",
            "Razor Claw",
            "Razor Fang",
            "Prism Scale",
            "Leftovers",
            "Choice Band",
            "Choice Specs",
            "Choice Scarf",
            "Life Orb",
            "Focus Sash",
            "Eviolite",
            "Rocky Helmet",
            "Expert Belt",
            "Muscle Band",
            "Wise Glasses",
            "Scope Lens",
            "Quick Claw",
            "Shell Bell",
            "Light Clay",
            "Black Sludge",
            "Toxic Orb",
            "Flame Orb",
            "Air Balloon",
        ]
        unfilled_count = len(self.multiworld.get_unfilled_locations(self.player))
        for item_name in useful_items:
            if len(item_pool) < unfilled_count:
                item_pool.append(self.create_item(item_name))

        # TMs (skip any already added to progression)
        from .items.tms import TM_ITEM_TABLE
        prog_set = set(other_progression_items)
        for tm_name in TM_ITEM_TABLE:
            if tm_name not in prog_set and len(item_pool) < unfilled_count:
                item_pool.append(self.create_item(tm_name))

        # Fill remaining locations with repeating filler items
        idx = 0
        while len(item_pool) < unfilled_count:
            item_pool.append(self.create_item(self._FILLER_ITEMS[idx % len(self._FILLER_ITEMS)]))
            idx += 1

        self.multiworld.itempool.extend(item_pool[:unfilled_count])

    def set_rules(self) -> None:
        pass

    def generate_output(self, output_directory: str) -> None:
        server = ""
        if getattr(self.multiworld, "server_address", None):
            server = str(self.multiworld.server_address).strip()

        ver = getattr(self.options, "version", 0)
        ver_val = ver.value if hasattr(ver, "value") else ver
        if ver_val == 0:
            patch_cls = PokemonB2Patch
        elif ver_val == 1:
            patch_cls = PokemonW2Patch
        else:
            patch_cls = PokemonB2W2Patch

        patch = patch_cls(
            os.path.join(
                output_directory,
                f"{self.multiworld.get_out_file_name_base(self.player)}{patch_cls.patch_file_ending}",
            ),
            player=self.player,
            player_name=self.player_name,
            world=self,
            server=server,
        )
        patch.write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        cached = getattr(self, "_cached_slot_data", None)
        if cached is not None:
            return cached

        remote_flags: list[int] = []
        remote_recipients: set[str] = set()
        loc_check_info: dict[str, list[Any]] = {}
        trainer_checks: list[int] = []

        for loc in self.multiworld.get_locations(self.player):
            addr = loc.address
            if addr is None:
                continue
            if 810000 <= addr < 820000:
                trainer_checks.append(addr)
            if addr in LOCATION_ID_TO_FLAG and loc.item is not None:
                f_id = LOCATION_ID_TO_FLAG[addr]
                if f_id is not None:
                    is_local = bool(loc.item.player == self.player)
                    recipient_name = self.multiworld.get_player_name(loc.item.player)
                    if not is_local:
                        remote_flags.append(f_id)
                        remote_recipients.add(recipient_name)
                    classification = loc.item.classification
                    class_val = int(classification.value if hasattr(classification, "value") else classification)
                    f_str = str(f_id)
                    if f_str not in loc_check_info:
                        loc_check_info[f_str] = [
                            loc.item.name,
                            recipient_name,
                            class_val,
                            is_local,
                        ]

        remote_flags.sort()
        trainer_checks.sort()
        recipient_label = (
            next(iter(remote_recipients))
            if len(remote_recipients) == 1
            else ("another world" if not remote_recipients else "their ally")
        )

        # Generate Pokemon locations mapping (encounter areas + statics)
        from .randomise.wild_tables import get_pokemon_locations
        is_w2 = (getattr(self.options.version, "current_key", "black2") == "white2")
        rand_wild = bool(self.options.randomise_wild_pokemon.value) if hasattr(self.options.randomise_wild_pokemon, "value") else False
        seed = getattr(self.multiworld, "seed", 0)
        poke_locs = get_pokemon_locations(
            is_white2=is_w2,
            randomise_wild=rand_wild,
            randomise_statics=False,
            seed=seed,
        )

        # Load map ID mapping
        map_id_to_name = {}
        try:
            from .zones import ZONES
            map_id_to_name = {str(k): v for k, v in ZONES.items()}
        except Exception:
            pass

        self._cached_slot_data = {
            "apworld_version": APWORLD_VERSION,
            "version": self.options.version.current_key,
            "starting_day": getattr(self, "starting_day", 0),
            "starting_season": getattr(self, "starting_season", 0),
            "trainersanity": int(self.options.trainersanity.value),
            "trainer_checks": trainer_checks,
            "region_encounters": poke_locs,
            "pokemon_locations": poke_locs,
            "map_id_to_name": map_id_to_name,
            "infinite_rare_candies": int(self.options.infinite_rare_candies.value),
            "infinite_repels": int(self.options.infinite_repels.value),
            "remote_flags": remote_flags,
            "loc_check_info": loc_check_info,
            "recipient_label": recipient_label,
            "options": {
                "check_log_filter": int(self.options.check_log_filter.value),
                "starting_day": getattr(self, "starting_day", 0),
                "starting_season": getattr(self, "starting_season", 0),
                "version": getattr(self.options.version, "current_key", "black2"),
                "goal": list(self.options.goal.value) if hasattr(self.options.goal, "value") and isinstance(self.options.goal.value, set) else [getattr(self.options.goal, "current_key", "champion")],
                "tmhm_hunt": getattr(self.options.tmhm_hunt, "value", 60),
                "top_trainers_required": getattr(self.options.top_trainers_required, "value", 5),
                "top_trainers_allowed": list(self.options.top_trainers_allowed.value) if hasattr(self.options, "top_trainers_allowed") and hasattr(self.options.top_trainers_allowed, "value") else [],
                "legendary_hunt_required": getattr(self.options.legendary_hunt_required, "value", 3),
                "legendary_hunt_allowed": list(self.options.legendary_hunt_allowed.value) if hasattr(self.options, "legendary_hunt_allowed") and hasattr(self.options.legendary_hunt_allowed, "value") else [],
                "exclude_postgame_checks": bool(self.options.exclude_postgame_checks.value),
                "shuffle_badges": bool(self.options.shuffle_badges.value),
                "hidden_items": bool(self.options.hidden_items.value),
                "habitat_list_checks": bool(self.options.habitat_list_checks.value),
                "flash_logic": bool(self.options.flash_logic.value),
                "dowsing_machine_logic": int(self.options.dowsing_machine_logic.value),
                "trainersanity": int(self.options.trainersanity.value),
                "skip_intro": bool(self.options.skip_intro.value),
                "trainer_name": str(self.options.trainer_name.value),
                "skip_intro_gender": self.options.skip_intro_gender.current_key,
                "rival_name": str(self.options.rival_name.value),
                "instant_text": bool(self.options.instant_text.value),
                "battle_scene": self.options.battle_scene.current_key,
                "battle_style": self.options.battle_style.current_key,
                "auto_run": bool(self.options.auto_run.value),
                "guaranteed_escape": bool(self.options.guaranteed_escape.value),
                "guaranteed_catch": bool(self.options.guaranteed_catch.value),
                "catch_rate_multiplier": int(self.options.catch_rate_multiplier.value),
                "exp_multiplier": int(self.options.exp_multiplier.value),
                "blind_trainers": bool(self.options.blind_trainers.value),
                "talk_to_trainer_without_battling": bool(self.options.talk_to_trainer_without_battling.value),
                "hold_a_turbo": bool(self.options.hold_a_turbo.value),
                "fast_hatch": bool(self.options.fast_hatch.value),
                "fast_fishing": bool(self.options.fast_fishing.value),
                "tmhm_fully_compatible": bool(self.options.tmhm_fully_compatible.value),
                "max_friendship": bool(self.options.max_friendship.value),
                "bike_everywhere": bool(self.options.bike_everywhere.value),
                "remove_surf_bike_music": bool(self.options.remove_surf_bike_music.value),
                "infinite_repels": bool(self.options.infinite_repels.value),
                "infinite_rare_candies": bool(self.options.infinite_rare_candies.value),
                "skip_pwt": bool(self.options.skip_pwt.value),
                "skip_catching_tutorial": bool(self.options.skip_catching_tutorial.value),
                "skip_join_avenue": bool(self.options.skip_join_avenue.value),
                "skip_cinematic_movies": bool(self.options.skip_cinematic_movies.value),
                "living_room_starter": bool(self.options.living_room_starter.value),
                "randomise_wild_pokemon": list(self.options.randomise_wild_pokemon.value) if isinstance(self.options.randomise_wild_pokemon.value, (set, list)) else bool(self.options.randomise_wild_pokemon.value),
                "randomise_trainer_pokemon": list(self.options.randomise_trainer_pokemon.value) if isinstance(self.options.randomise_trainer_pokemon.value, (set, list)) else bool(self.options.randomise_trainer_pokemon.value),
                "randomise_starter_pokemon": list(self.options.randomise_starter_pokemon.value) if isinstance(self.options.randomise_starter_pokemon.value, (set, list)) else bool(self.options.randomise_starter_pokemon.value),
                "randomise_abilities": list(self.options.randomise_abilities.value) if isinstance(self.options.randomise_abilities.value, (set, list)) else bool(self.options.randomise_abilities.value),
                "randomise_level_up_movesets": list(self.options.randomise_level_up_movesets.value) if isinstance(self.options.randomise_level_up_movesets.value, (set, list)) else bool(self.options.randomise_level_up_movesets.value),
            },
        }
        return self._cached_slot_data

try:
    from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

    def run_client(*args):
        from worlds._bizhawk.context import launch
        launch_subprocess(launch, name="BizHawkClient", args=args)

    components.append(
        Component(
            "Pokemon Black 2 and White 2 Client",
            func=run_client,
            component_type=Type.CLIENT,
            file_identifier=SuffixIdentifier(".apb2w2", ".apb2", ".apw2"),
            description="Open BizHawk Client with a Pokemon Black 2 or White 2 patch file.",
        )
    )
except (ImportError, ModuleNotFoundError):
    pass
