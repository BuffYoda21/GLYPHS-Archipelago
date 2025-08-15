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

    place_event_items(world)
    place_goals(world)
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 1)

    return itempool

def place_event_items(world: "GlyphsWorld") -> None:
    world.multiworld.get_location("Defeat Runic Construct", world.player).place_locked_item(glyphs_events["Runic Construct Defeated"])
    world.multiworld.get_location("Serpent Lock 1",         world.player).place_locked_item(glyphs_events["Serpent Lock Activated"])
    world.multiworld.get_location("Serpent Lock 2",         world.player).place_locked_item(glyphs_events["Serpent Lock Activated"])
    world.multiworld.get_location("Serpent Lock 3",         world.player).place_locked_item(glyphs_events["Serpent Lock Activated"])
    world.multiworld.get_location("Defeat Gilded Serpent",  world.player).place_locked_item(glyphs_events["Gilded Serpent Defeated"])
    world.multiworld.get_location("Stalker Sigil 1",        world.player).place_locked_item(glyphs_events["Stalker Sigil Collected"])
    world.multiworld.get_location("Stalker Sigil 2",        world.player).place_locked_item(glyphs_events["Stalker Sigil Collected"])
    world.multiworld.get_location("Stalker Sigil 3",        world.player).place_locked_item(glyphs_events["Stalker Sigil Collected"])
    world.multiworld.get_location("Solve Flower Puzzle",    world.player).place_locked_item(glyphs_events["Solved Flower Puzzle"])
    world.multiworld.get_location("Collapse Unlock",        world.player).place_locked_item(glyphs_events["Collapse Unlocked"])
    world.multiworld.get_location("Defeat Spearman",        world.player).place_locked_item(glyphs_events["Spearman Defeated"])
    world.multiworld.get_location("Defeat Null",            world.player).place_locked_item(glyphs_events["Null Defeated"])
    world.multiworld.get_location("Clarity",                world.player).place_locked_item(glyphs_events["Clarity"])
    world.multiworld.get_location("Last Fracture",          world.player).place_locked_item(glyphs_events["Act 1 Unlocked"])
    world.multiworld.get_location("Clear Act 1",            world.player).place_locked_item(glyphs_events["Act 2 Unlocked"])
    world.multiworld.get_location("Clear Act 2",            world.player).place_locked_item(glyphs_events["Act 3 Unlocked"])

def place_goals(world: "GlyphsWorld") -> None:
    world.multiworld.get_location("False Ending",           world.player).place_locked_item(glyphs_goals["False Ending"])
    world.multiworld.get_location("Good Ending",            world.player).place_locked_item(glyphs_goals["Good Ending"])
    world.multiworld.get_location("True Ending",            world.player).place_locked_item(glyphs_goals["True Ending"])
    world.multiworld.get_location("Perfect Clarity",        world.player).place_locked_item(glyphs_goals["Perfect Clarity"])
    world.multiworld.get_location("Smilemask Ending",       world.player).place_locked_item(glyphs_goals["Smilemask Ending"])
    world.multiworld.get_location("Omnipotence Ending",     world.player).place_locked_item(glyphs_goals["Omnipotence Ending"])
    world.multiworld.get_location("Clear Epilouge",         world.player).place_locked_item(glyphs_goals["Epilouge Ending"])

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

        elif ic == ItemClassification.trap:
            trap_list[name] = 0
            if name == "sMiLE Trap" and "Smile Trap" in world.options.TrapTypes.value:
                trap_list[name] = 20
            elif name == "John Trap" and "John Trap" in world.options.TrapTypes.value:
                trap_list[name] = 10
            elif name == "Spear Trap" and "Spear Trap" in world.options.TrapTypes.value:
                trap_list[name] = 20
            elif name == "Enemy Trap" and "Enemy Trap" in world.options.TrapTypes.value:
                trap_list[name] = 30
            elif name == "Screen Flip Trap" and "Screen Flip Trap" in world.options.TrapTypes.value:
                trap_list[name] = 15
            elif name == "Instakill Trap" and "Instakill Trap" in world.options.TrapTypes.value:
                trap_list[name] = 5
                
    for i in range(count):
        if not world.options.EnableTraps.value:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))
            continue
        if world.random.randint(1, 100) <= 70:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

glyphs_items = {
# ---Item Name------------------------ap_code-----------------------classifications-------------------------------count--
    
    # Upgrades
    "Progressive Sword":        ItemData(1,     ItemClassification.progression + ItemClassification.useful,         2),
    "Progressive Dash Orb":     ItemData(2,     ItemClassification.progression + ItemClassification.useful,         3),
  # "Map":                      ItemData(3,     ItemClassification.progression + ItemClassification.useful,         1),     # decided to make this not a check for now
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
    
    # Limited junk items
    "Pink Bow":                 ItemData(37,    ItemClassification.filler,                                          1),
    "Propeller Hat":            ItemData(38,    ItemClassification.filler,                                          1),
    "Traffic Cone":             ItemData(39,    ItemClassification.filler,                                          1),
    "John Hat":                 ItemData(40,    ItemClassification.filler,                                          1),
    "Top Hat":                  ItemData(41,    ItemClassification.filler,                                          1),
    "Fez":                      ItemData(42,    ItemClassification.filler,                                          1),
    "Party Hat":                ItemData(43,    ItemClassification.filler,                                          1),
    "Bomb Hat":                 ItemData(44,    ItemClassification.filler,                                          1),
    "Crown":                    ItemData(45,    ItemClassification.filler,                                          1),
}

glyphs_events = {
    "Runic Construct Defeated": ItemData(17,    ItemClassification.progression_skip_balancing,                      1),
    "Gilded Serpent Defeated":  ItemData(18,    ItemClassification.progression_skip_balancing,                      1),
    "Collapse Unlocked":        ItemData(19,    ItemClassification.progression_skip_balancing,                      1),
    "Wizard True Defeat":       ItemData(20,    ItemClassification.progression_skip_balancing,                      1),
    "Null Defeated":            ItemData(21,    ItemClassification.progression_skip_balancing,                      1),
    "Spearman Defeated":        ItemData(22,    ItemClassification.progression_skip_balancing,                      1),
    "Serpent Lock Activated":   ItemData(23,    ItemClassification.progression_skip_balancing,                      3),
    "Stalker Sigil Collected":  ItemData(24,    ItemClassification.progression_skip_balancing,                      3),
    "Solved Flower Puzzle":     ItemData(25,    ItemClassification.progression_skip_balancing,                      1),
    "Clarity":                  ItemData(26,    ItemClassification.progression_skip_balancing,                      1),
    "Act 1 Unlocked":           ItemData(27,    ItemClassification.progression_skip_balancing,                      1),
    "Act 2 Unlocked":           ItemData(28,    ItemClassification.progression_skip_balancing,                      1),
    "Act 3 Unlocked":           ItemData(29,    ItemClassification.progression_skip_balancing,                      1),
}

glyphs_goals = {
    "False Ending":             ItemData(30,    ItemClassification.progression_skip_balancing),
    "Good Ending":              ItemData(31,    ItemClassification.progression_skip_balancing),
    "True Ending":              ItemData(32,    ItemClassification.progression_skip_balancing),
    "Perfect Clarity":          ItemData(33,    ItemClassification.progression_skip_balancing),
    "Smilemask Ending":         ItemData(34,    ItemClassification.progression_skip_balancing),
    "Omnipotence Ending":       ItemData(35,    ItemClassification.progression_skip_balancing),
    "Epilouge Ending":          ItemData(36,    ItemClassification.progression_skip_balancing),
}

glyphs_chapters = {
    "Menu":                     ItemData(46,    ItemClassification.progression),    # using this as starting chapter to allow randomized starting spawns
    "Region 1 - Central":       ItemData(47,    ItemClassification.progression),
    "Region 1 - Left":          ItemData(48,    ItemClassification.progression),
    "Region 1 - Upper Left":    ItemData(49,    ItemClassification.progression),
    "Region 1 - Upper Right":   ItemData(50,    ItemClassification.progression),
    "Region 2 - Left":          ItemData(51,    ItemClassification.progression),
    "Region 2 - Central":       ItemData(52,    ItemClassification.progression),
    "Region 2 - Sector 1":      ItemData(53,    ItemClassification.progression),
    "Region 2 - Sector 2":      ItemData(54,    ItemClassification.progression),
    "Region 2 - Sector 4":      ItemData(55,    ItemClassification.progression),
    "Region 2 - Sector 4 End":  ItemData(56,    ItemClassification.progression),
    "Region 2 - Lower":         ItemData(57,    ItemClassification.progression),
    "Region 2 - Serpent Upper": ItemData(58,    ItemClassification.progression),
    "Region 2 - Serpent Lower": ItemData(59,    ItemClassification.progression),
    "Region 2 - Shadow Chase":  ItemData(60,    ItemClassification.progression),
    "Region 3":                 ItemData(61,    ItemClassification.progression),
    "Region 4 - Entrance":      ItemData(62,    ItemClassification.progression),
    "Region 4 - Upper":         ItemData(63,    ItemClassification.progression),
    "Region 4 - Central":       ItemData(64,    ItemClassification.progression),
    "Region 4 - Lower":         ItemData(65,    ItemClassification.progression),
    "Collapse":                 ItemData(66,    ItemClassification.progression),
    "Smile Shop":               ItemData(67,    ItemClassification.progression),
    "Dark Region":              ItemData(68,    ItemClassification.progression),
    "The Between":              ItemData(69,    ItemClassification.progression),
    "Act 1":                    ItemData(70,    ItemClassification.progression),
    "Act 2":                    ItemData(71,    ItemClassification.progression),
    "Act 3":                    ItemData(72,    ItemClassification.progression),
    "Epilogue":                 ItemData(73,    ItemClassification.progression),
}

junk_items = {
    # Junk Items
    "HP Refill":                ItemData(74,    ItemClassification.filler,                                          0),

    # Traps
    "sMiLE Trap":               ItemData(75,    ItemClassification.trap,                                            0),
    "John Trap":                ItemData(76,    ItemClassification.trap,                                            0),
    "Spear Trap":               ItemData(77,    ItemClassification.trap,                                            0),
    "Instakill Trap":           ItemData(78,    ItemClassification.trap,                                            0),
    "Screen Flip Trap":         ItemData(79,    ItemClassification.trap,                                            0),
    "Enemy Trap":               ItemData(80,    ItemClassification.trap,                                            0),
}

item_table = {
    **glyphs_items,
    **glyphs_events,
    **glyphs_goals,
    **glyphs_chapters,
    **junk_items
}