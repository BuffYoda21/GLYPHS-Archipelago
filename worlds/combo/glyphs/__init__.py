from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict, TextIO

from .Shop import get_shop_prices
from .Types import ButtonData, ButtonColor, ItemData
from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table, hats
from .Options import GlyphsOptions
from .Regions import create_regions
from .Rules import set_rules, connect_entrances
from .Buttons import randomize_buttons, get_raw_button_color_data, get_button_color_spoiler_data, get_broken_button_spoiler_data

class GlyphsWeb(WebWorld):
    theme = "stone"
    
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up (the game you are randomizing) for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["BuffYoda21"]
    )]

class GlyphsWorld(World):
    """
    Traverse the depths of the Tomb of Forbidden Knowledge; a sentient labyrinth
    containing traces of the past in the form of glyphs. Formidable bosses, platforming,
    and puzzles stand in the way of discovery - GLYPHS fulfills the extent that one
    willingly searches for true knowledge. Your determination dictates where this story will unfold.
    """

    # game = "GLYPHS"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items() if data.ap_code is not None}
    location_name_to_id = get_location_names()
    options: GlyphsOptions
    options_dataclass = GlyphsOptions
    web = GlyphsWeb()
    shop_prices: list[int]
    buttons: dict[str, ButtonData]
    items: dict[str, ItemData]

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        starting_chapter = "Menu"
        self.multiworld.push_precollected(create_item(self, starting_chapter))
        self.multiworld.push_precollected(create_item(self, "Map"))

        if not self.options.HatShuffle.value:
            for item_name, item_data in hats.items():
                for _ in range(item_data.count or 1):
                    self.multiworld.push_precollected(create_item(self, item_name))

        early_dash_possibility = True
        early_sword_possibility = True

        if self.options.StartingSword.value:
            self.multiworld.push_precollected(create_item(self, "Progressive Sword"))
            early_sword_possibility = False
        if self.options.StartingDash.value:
            self.multiworld.push_precollected(create_item(self, "Progressive Dash Orb"))
            early_dash_possibility = False

        randomize_buttons(self, self.options.RandomButtonColorPercent.value, self.options.ButtonShardPercent.value)

        early_button_1 = self.buttons["R1C First"]
        early_button_2 = self.buttons["R1C Second"]

        #if early_button_1.color != ButtonColor.RED or early_button_2.color != ButtonColor.RED or early_button_1.isBroken or early_button_2.isBroken:
        #    early_sword_possibility = False
        if not self.options.StartingDash.value:
            if early_button_1.color != ButtonColor.RED:
                early_button_1.color = ButtonColor.RED
            if early_button_2.color != ButtonColor.RED:
                early_button_2.color = ButtonColor.RED

        if early_dash_possibility:
            self.multiworld.early_items[self.player]["Progressive Dash Orb"] = 1
        if early_sword_possibility:
            self.multiworld.early_items[self.player]["Progressive Sword"] = 1

        r1_roadblock_button_1 = self.buttons["R1F Right"]
        r1_roadblock_button_2 = self.buttons["R2A Gate Left"]

        if r1_roadblock_button_1.isBroken and not self.options.LogicalWallJumps.value:
            self.multiworld.early_items[self.player][r1_roadblock_button_1.shardName] = 1
        if r1_roadblock_button_2.isBroken:
            self.multiworld.early_items[self.player][r1_roadblock_button_2.shardName] = 1
    
    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    def fill_slot_data(self) -> Dict[str, object]:
        prices = get_shop_prices(self)
        slot_data: Dict[str, object] = {
            "options": {
                "Goal":                    self.options.Goal.value,
                #"Multiplayer":             self.options.Multiplayer.value,
                "DeathLink":               self.options.DeathLink.value,
                "ButtonColorsRandomized":  self.options.RandomButtonColorPercent.value != 0,
                "ButtonShardsRandomized":  self.options.ButtonShardPercent.value != 0,
                "WizardRequirements":      self.options.WizardRequirements.value,
                "WraithRequirements":      self.options.WraithRequirements.value,
                "WraithSilverCount":       self.options.WraithSilverCount.value,
                "WraithGoldCount":         self.options.WraithGoldCount.value,
                "WraithSmileCount":        self.options.WraithSmileCount.value,
                "WraithRuneCount":         self.options.WraithRuneCount.value,
                "WraithGlyphstoneCount":   self.options.WraithGlyphstoneCount.value,
            },
            "shop_prices": prices,
            "button_colors": get_raw_button_color_data(self),
            "broken_buttons": get_broken_button_spoiler_data(self),
            "Seed": self.multiworld.seed_name,
            "Slot": self.multiworld.player_name[self.player],
            "TotalLocations": get_total_locations(self)
        }

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.options.RandomShopPrices.value:
            spoiler_handle.write(f"\nGLYPHS: Smile Shop Prices ({self.player_name}): {get_shop_prices(self)}\n")
        if self.options.RandomButtonColorPercent.value != 0:
            spoiler_handle.write(f"\nGLYPHS: Button Colors ({self.player_name}): {get_button_color_spoiler_data(self)}\n")
        if self.options.ButtonShardPercent.value != 0:
            spoiler_handle.write(f"\nGLYPHS: Broken Buttons ({self.player_name}): {get_broken_button_spoiler_data(self)}\n")

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)