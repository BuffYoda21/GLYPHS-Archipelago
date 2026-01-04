import logging
from BaseClasses import ItemClassification, MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict, TextIO

from worlds.glyphs.SmileShopRando import get_shop_prices
from worlds.glyphs.Types import GlyphsItem
from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import GlyphsOptions
from .Regions import create_regions
from .Rules import set_rules, connect_entrances

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

    game = "GLYPHS"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = GlyphsOptions
    web = GlyphsWeb()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        starting_chapter = "Menu"
        self.multiworld.push_precollected(GlyphsItem(starting_chapter, ItemClassification.progression, None, self.player))
        self.multiworld.push_precollected(GlyphsItem("Map", ItemClassification.progression | ItemClassification.useful, 3, self.player))
        if self.options.StartingSword.value:
            self.multiworld.push_precollected(GlyphsItem("Progressive Sword", ItemClassification.progression | ItemClassification.useful, 1, self.player))
        if self.options.StartingDash.value:
            self.multiworld.push_precollected(GlyphsItem("Progressive Dash Orb", ItemClassification.progression | ItemClassification.useful, 1, self.player))
    
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
                "GenericParries":          self.options.GenericParries.value,
                "Multiplayer":             self.options.Multiplayer.value,
                "SwordlessCombat":         self.options.SwordlessCombat.value,
                "BulletCombat":            self.options.BulletCombat.value,
                "DashPuzzlesSolved":       self.options.DashPuzzlesSolved.value,
                "LogicalWallJumps":        self.options.LogicalWallJumps.value,
                "WizardRequirements":      self.options.WizardRequirements.value,
                "WraithRequirements":      self.options.WraithRequirements.value,
                "WraithSilverCount":       self.options.WraithSilverCount.value,
                "WraithGoldCount":         self.options.WraithGoldCount.value,
                "WraithSmileCount":        self.options.WraithSmileCount.value,
                "WraithRuneCount":         self.options.WraithRuneCount.value,
                "WraithGlyphstoneCount":   self.options.WraithGlyphstoneCount.value,
            },
            "shop_prices": prices,
            "Seed": self.multiworld.seed_name,
            "Slot": self.multiworld.player_name[self.player],
            "TotalLocations": get_total_locations(self)
        }

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nSmile Shop Prices ({self.player_name}): {get_shop_prices(self)}")

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)