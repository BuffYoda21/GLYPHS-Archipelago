from typing import List

from BaseClasses import Item, ItemClassification, MultiWorld

from .apquest import APQuestWorld
from .glyphs import GlyphsWorld

from .glyphs.Items import progression_items, hats, create_item, place_event_items, place_goals
from .glyphs.Types import ItemData
from .glyphs.Buttons import get_broken_buttons, get_shard_name

# This is where I can override methods from subworlds should I need to modify behavior without editing upstream code.

class APQuestSubworld(APQuestWorld):
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def create_all_items(self) -> list[Item]:
        """
        Modified version of APQuestWorld.create_all_items.
        All that is changed is the return type is now a list of items,
        filler items are not created, and the itempool is returned instead
        of being added to the multiworld itempool.
        """
        itempool: list[Item] = [
            self.create_item("Key"),
            self.create_item("Sword"),
            self.create_item("Shield"),
            self.create_item("Health Upgrade"),
            self.create_item("Health Upgrade"),
        ]

        if self.options.hammer:
            itempool.append(self.create_item("Hammer"))

        # number_of_items = len(itempool)
        # number_of_unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        # needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
        # itempool += [self.create_filler() for _ in range(needed_number_of_filler_items)]
        # self.multiworld.itempool += itempool
        if self.options.start_with_one_confetti_cannon:
            starting_confetti_cannon = self.create_item("Confetti Cannon")
            self.push_precollected(starting_confetti_cannon)
        return itempool


class GlyphsSubworld(GlyphsWorld):
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def create_filler(self) -> Item:
        return self.create_item("HP Refill")

    def create_itempool(self) -> List[Item]:
        """
        Modified glyphs.items.create_itempool.
        Removes filler creation.
        """
        itempool: List[Item] = []

        self.items = {}
        for item_name, item_data in progression_items.items():
            self.items[item_name] = ItemData(
                item_data.ap_code,
                item_data.classification,
                item_data.count
            )

        self.items.pop("Map")

        if self.options.StartingSword.value:
            sword = self.items["Progressive Sword"]
            assert sword.count is not None

            self.items["Progressive Sword"] = ItemData(
                1, 
                ItemClassification.progression | ItemClassification.useful,
                sword.count - 1
            )

        if self.options.StartingDash.value:
            dash = self.items["Progressive Dash Orb"]
            assert dash.count is not None

            self.items["Progressive Dash Orb"] = ItemData(
                2, 
                ItemClassification.progression | ItemClassification.useful,
                dash.count - 1
            )

        for item_name, item_data in self.items.items():
            for _ in range(item_data.count or 1):
                itempool.append(create_item(self, item_name))

        if self.options.HatShuffle.value:
            for item_name, item_data in hats.items():
                for _ in range(item_data.count or 1):
                    itempool.append(create_item(self, item_name))

        for button in get_broken_buttons(self):
            itempool.append(create_item(self, get_shard_name(self, button)))
            
        place_event_items(self)
        place_goals(self)

        # total_locs = get_total_locations(self)
        # num_junk_needed = total_locs - len(itempool)
        # if num_junk_needed > 0:
        #     itempool += create_junk_items(self, num_junk_needed)
        return itempool