import logging
from BaseClasses import Item, ItemClassification
from .Types import ItemData, ChapterType, GlyphsItem, chapter_type_to_name
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

def create_itempool(world: "GlyphsWorld") -> List[Item]:
    itempool: List[Item] = []
    starting_chapter = chapter_type_to_name[ChapterType(world.options.StartingChapter)]
    
    for chapter in glyphs_chapters.keys():
        print("-------------------------")
        print(starting_chapter)
        print("-------------------------")
        if starting_chapter == chapter:
            continue
        else:
            itempool.append(create_item(world, chapter))
    
    goal = create_item(world, "Goal")
    world.multiworld.get_location("add dynamic goal here", world.player).place_locked_item(goal)    # dont forget to change this
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 1)

    return itempool

def create_item(world: "GlyphsWorld", name: str) -> Item:
    data = item_table[name]
    return GlyphsItem(name, data.classification, data.ap_code, world.player)

def create_multiple_items(world: "GlyphsWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [GlyphsItem(name, item_type, data.ap_code, world.player)]

    return itemlist

def create_junk_items(world: "GlyphsWorld", count: int) -> List[Item]:
    trap_chance = world.options.TrapChance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    # Formatted like this so that I can add more later if needed
    junk_weights = {
        "HP Refill":        100,
    }

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "sMiLE Trap":
                trap_list[name] = 20
            elif name == "John Trap":
                trap_list[name] = 10
            elif name == "Spear Trap":
                trap_list[name] = 20
            elif name == "Enemy Trap":
                trap_list[name] = 30
            elif name == "Screen Flip Trap":
                trap_list[name] = 15
            elif name == "Instakill Trap":
                trap_list[name] = 5
                
    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))
            if junk_pool[-1].name != "HP Refill":
                junk_weights[junk_pool[-1].name] = 0

    return junk_pool

glyphs_items = {
# ---Item Name------------------------ap_code-----------------------classifications-------------------------------count--
    
    # Upgrades
    "Progressive Sword":        ItemData(1,     ItemClassification.progression + ItemClassification.useful,         2),
    "Progressive Dash Orb":     ItemData(2,     ItemClassification.progression + ItemClassification.useful,         3),
    "Map":                      ItemData(3,     ItemClassification.progression + ItemClassification.useful,         1),     # might make this a starting item
    "Grapple":                  ItemData(4,     ItemClassification.progression + ItemClassification.useful,         1),
    "Progressive Parry":        ItemData(5,     ItemClassification.progression + ItemClassification.useful,         2),
    "Shroud":                   ItemData(6,     ItemClassification.useful,                                          1),
    "Progressive Chicken Hat":  ItemData(7,     ItemClassification.useful,                                          2),

    # Collectables
    "Silver Shard":             ItemData(8,     ItemClassification.progression_skip_balancing,                      15),
    "Gold Shard":               ItemData(9,     ItemClassification.useful,                                          3),
    "Smile Token":              ItemData(10,    ItemClassification.progression_skip_balancing,                      10),
    "Rune Cube":                ItemData(11,    ItemClassification.progression,                                     3),
    "Void Gate Shard":          ItemData(12,    ItemClassification.progression_skip_balancing,                      7),
    "Green Stone":              ItemData(13,    ItemClassification.progression,                                     1),
    "Red Stone":                ItemData(14,    ItemClassification.progression,                                     1),
    "Blue Stone":               ItemData(15,    ItemClassification.progression,                                     1),
    "Seeds":                    ItemData(16,    ItemClassification.progression_skip_balancing,                      10),

    # Events (not shuffled)
    "Runic Construct Defeated": ItemData(17,    ItemClassification.progression_skip_balancing,                      1),
    "Gilded Serpent Defeated":  ItemData(18,    ItemClassification.progression_skip_balancing,                      1),
    "Collapse Unlocked":        ItemData(19,    ItemClassification.progression_skip_balancing,                      1),
    "Wizard True Defeat":       ItemData(20,    ItemClassification.progression_skip_balancing,                      1),
    "Spearman Defeated":        ItemData(21,    ItemClassification.progression_skip_balancing,                      1),
    "Serpent Lock Activated":   ItemData(22,    ItemClassification.progression_skip_balancing,                      3),
    "Stalker Sigil Collected":  ItemData(23,    ItemClassification.progression_skip_balancing,                      3),
    "Clarity":                  ItemData(24,    ItemClassification.progression_skip_balancing,                      1),
    "Act 1 Unlocked":           ItemData(25,    ItemClassification.progression_skip_balancing,                      1),
    "Act 2 Unlocked":           ItemData(26,    ItemClassification.progression_skip_balancing,                      1),
    "Act 3 Unlocked":           ItemData(27,    ItemClassification.progression_skip_balancing,                      1),

    # Goal items (still not sure this is how I want to structure this)
    "False Ending":             ItemData(28,    ItemClassification.progression_skip_balancing,                      1),
    "Good Ending":              ItemData(29,    ItemClassification.progression_skip_balancing,                      1),
    "True Ending":              ItemData(30,    ItemClassification.progression_skip_balancing,                      1),
    "Perfect Clarity":          ItemData(31,    ItemClassification.progression_skip_balancing,                      1),
    "Smilemask Ending":         ItemData(32,    ItemClassification.progression_skip_balancing,                      1),
    "Omnipotence Ending":       ItemData(33,    ItemClassification.progression_skip_balancing,                      1),
    "Epilouge Ending":          ItemData(34,    ItemClassification.progression_skip_balancing,                      1),
    
    # Limited junk items
    "Pink Bow":                 ItemData(35,    ItemClassification.filler,                                          1),
    "Propeller Hat":            ItemData(36,    ItemClassification.filler,                                          1),
    "Traffic Cone":             ItemData(37,    ItemClassification.filler,                                          1),
    "John Hat":                 ItemData(38,    ItemClassification.filler,                                          1),
    "Top Hat":                  ItemData(39,    ItemClassification.filler,                                          1),
    "Fez":                      ItemData(40,    ItemClassification.filler,                                          1),
    "Party Hat":                ItemData(41,    ItemClassification.filler,                                          1),
    "Bomb Hat":                 ItemData(42,    ItemClassification.filler,                                          1),
    "Crown":                    ItemData(43,    ItemClassification.filler,                                          1),
}

glyphs_chapters = {
    "Menu":                     ItemData(44,    ItemClassification.progression),    # using this as starting chapter to allow randomized starting spawns
    "Region 1 - Central":       ItemData(45,    ItemClassification.progression),
    "Region 1 - Left":          ItemData(46,    ItemClassification.progression),
    "Region 1 - Upper Left":    ItemData(47,    ItemClassification.progression),
    "Region 1 - Upper Right":   ItemData(48,    ItemClassification.progression),
    "Region 2 - Left":          ItemData(49,    ItemClassification.progression),
    "Region 2 - Central":       ItemData(50,    ItemClassification.progression),
    "Region 2 - Sector 1":      ItemData(51,    ItemClassification.progression),
    "Region 2 - Sector 2":      ItemData(52,    ItemClassification.progression),
    "Region 2 - Sector 4":      ItemData(53,    ItemClassification.progression),
    "Region 2 - Sector 4 End":  ItemData(54,    ItemClassification.progression),
    "Region 2 - Lower":         ItemData(55,    ItemClassification.progression),
    "Region 2 - Serpent Upper": ItemData(56,    ItemClassification.progression),
    "Region 2 - Serpent Lower": ItemData(57,    ItemClassification.progression),
    "Region 2 - Shadow Chase":  ItemData(58,    ItemClassification.progression),
    "Region 3":                 ItemData(59,    ItemClassification.progression),
    "Region 4 - Entrance":      ItemData(60,    ItemClassification.progression),
    "Region 4 - Upper":         ItemData(61,    ItemClassification.progression),
    "Region 4 - Central":       ItemData(62,    ItemClassification.progression),
    "Region 4 - Lower":         ItemData(63,    ItemClassification.progression),
    "Collapse":                 ItemData(64,    ItemClassification.progression),
    "Smile Shop":               ItemData(65,    ItemClassification.progression),
    "Dark Region":              ItemData(66,    ItemClassification.progression),
    "The Between":              ItemData(67,    ItemClassification.progression),
    "Act 1":                    ItemData(68,    ItemClassification.progression),
    "Act 2":                    ItemData(69,    ItemClassification.progression),
    "Act 3":                    ItemData(70,    ItemClassification.progression),
    "Epilogue":                 ItemData(71,    ItemClassification.progression),
}

junk_items = {
    # Junk Items
    "HP Refill":                ItemData(72,    ItemClassification.filler,                                          0),

    # Traps
    "sMiLE Trap":               ItemData(73,    ItemClassification.trap,                                            0),
    "John Trap":                ItemData(74,    ItemClassification.trap,                                            0),
    "Spear Trap":               ItemData(75,    ItemClassification.trap,                                            0),
    "Instakill Trap":           ItemData(76,    ItemClassification.trap,                                            0),
    "Screen Flip Trap":         ItemData(77,    ItemClassification.trap,                                            0),
    "Enemy Trap":               ItemData(78,    ItemClassification.trap,                                            0),
}

item_table = {
    **glyphs_items,
    **glyphs_chapters,
    **junk_items
}