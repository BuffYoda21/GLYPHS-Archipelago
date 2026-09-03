from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict, TextIO

from .options import ComboOptions
from .subworld import GlyphsSubworld, APQuestSubworld
from .items import build_item_name_to_id, create_item, create_items
from .locations import build_location_name_to_id
from .rules import set_completion_rule

from .apquest.options import APQuestOptions
from .glyphs.Options import GlyphsOptions

class ComboWeb(WebWorld):
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

class ComboWorld(World):
    """
    Test world for combining multiple apworlds
    """

    game = "Combo"
    item_name_to_id = build_item_name_to_id()
    location_name_to_id = build_location_name_to_id()
    options: ComboOptions
    options_dataclass = ComboOptions
    web = ComboWeb()
    apquest: APQuestSubworld
    glyphs: GlyphsSubworld

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.apquest = APQuestSubworld(multiworld, player)
        self.glyphs = GlyphsSubworld(multiworld, player)

    def _project_options(self, source: ComboOptions, target_type):
        return target_type(**{
            name: getattr(source, name)
            for name in target_type.type_hints
        })

    def generate_early(self):
        self.glyphs.options = self._project_options(self.options, GlyphsOptions)
        self.apquest.options = self._project_options(self.options, APQuestOptions)

        self.glyphs.generate_early()
        self.apquest.generate_early()
    
    def set_rules(self):
        self.glyphs.set_rules()
        self.apquest.set_rules()

        set_completion_rule(self)

    def create_regions(self):
        self.glyphs.create_regions()
        self.apquest.create_regions()

    def connect_entrances(self):
        self.glyphs.connect_entrances()
        self.apquest.connect_entrances()

        self.glyphs.get_region("Menu").connect(self.apquest.get_region("Overworld"))

    def create_items(self):
        create_items(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_filler(self) -> Item:
        if self.random.randint(0,1) == 0:
            return self.glyphs.create_filler()
        return self.apquest.create_filler()
    
    def fill_slot_data(self) -> Dict[str, object]:
        data: Dict[str, object] = {}
        data.update(self.glyphs.fill_slot_data())
        data.update(self.apquest.fill_slot_data())
        return data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        self.glyphs.write_spoiler(spoiler_handle)
        self.apquest.write_spoiler(spoiler_handle)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)