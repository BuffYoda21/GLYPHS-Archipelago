import logging
from BaseClasses import Item, ItemClassification
from .Types import ItemData, GlyphsItem
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

def create_itempool(world: "GlyphsWorld") -> List[Item]:
    itempool: List[Item] = []

    world.items = {}
    for item_name, item_data in glyphs_items.items():
        world.items[item_name] = ItemData(
            item_data.ap_code,
            item_data.classification,
            item_data.advancement,
            item_data.count
        )
    
    world.items.pop("Map")

    if world.options.StartingSword.value:
        world.items["Progressive Sword"] = ItemData(
            1, 
            ItemClassification.progression | ItemClassification.useful, 
            True, 
            world.items["Progressive Sword"].count - 1
        )
    if world.options.StartingDash.value:
        world.items["Progressive Dash Orb"] = ItemData(
            2, 
            ItemClassification.progression | ItemClassification.useful, 
            True, 
            world.items["Progressive Dash Orb"].count - 1
        )

    for item_name, item_data in world.items.items():
        for _ in range(item_data.count or 1):
            itempool.append(create_item(world, item_name))

    if world.options.HatShuffle.value:
        for item_name, item_data in glyphs_hats.items():
            for _ in range(item_data.count or 1):
                itempool.append(create_item(world, item_name))
        
    place_event_items(world)
    place_goals(world)

    total_locs = get_total_locations(world)
    num_junk_needed = total_locs - len(itempool)
    if num_junk_needed > 0:
        itempool += create_junk_items(world, num_junk_needed)
    return itempool

def place_event_items(world: "GlyphsWorld") -> None:
    world.multiworld.get_location("Defeat Runic Construct", world.player).place_locked_item(create_event_item(world, "Defeat Runic Construct"))
    world.multiworld.get_location("Serpent Lock 1",         world.player).place_locked_item(create_event_item(world, "Serpent Lock 1"))
    world.multiworld.get_location("Serpent Lock 2",         world.player).place_locked_item(create_event_item(world, "Serpent Lock 2"))
    world.multiworld.get_location("Serpent Lock 3",         world.player).place_locked_item(create_event_item(world, "Serpent Lock 3"))
    world.multiworld.get_location("Defeat Gilded Serpent",  world.player).place_locked_item(create_event_item(world, "Defeat Gilded Serpent"))
    world.multiworld.get_location("Stalker Sigil 1",        world.player).place_locked_item(create_event_item(world, "Stalker Sigil 1"))
    world.multiworld.get_location("Stalker Sigil 2",        world.player).place_locked_item(create_event_item(world, "Stalker Sigil 2"))
    world.multiworld.get_location("Stalker Sigil 3",        world.player).place_locked_item(create_event_item(world, "Stalker Sigil 3"))
    world.multiworld.get_location("Solve Flower Puzzle",    world.player).place_locked_item(create_event_item(world, "Solve Flower Puzzle"))
    world.multiworld.get_location("Collapse Unlock",        world.player).place_locked_item(create_event_item(world, "Collapse Unlock"))
    world.multiworld.get_location("Wizard True Defeat",     world.player).place_locked_item(create_event_item(world, "Wizard True Defeat"))
    world.multiworld.get_location("Defeat Spearman",        world.player).place_locked_item(create_event_item(world, "Defeat Spearman"))
    world.multiworld.get_location("Defeat Null",            world.player).place_locked_item(create_event_item(world, "Defeat Null"))
    world.multiworld.get_location("Clarity",                world.player).place_locked_item(create_event_item(world, "Clarity"))
    world.multiworld.get_location("Last Fracture",          world.player).place_locked_item(create_event_item(world, "Last Fracture"))
    world.multiworld.get_location("Clear Act 1",            world.player).place_locked_item(create_event_item(world, "Clear Act 1"))
    world.multiworld.get_location("Clear Act 2",            world.player).place_locked_item(create_event_item(world, "Clear Act 2"))

def place_goals(world: "GlyphsWorld") -> None:
    world.multiworld.get_location("False Ending",           world.player).place_locked_item(create_event_item(world, "False Ending"))
    world.multiworld.get_location("Good Ending",            world.player).place_locked_item(create_event_item(world, "Good Ending"))
    world.multiworld.get_location("True Ending",            world.player).place_locked_item(create_event_item(world, "True Ending"))
    world.multiworld.get_location("Perfect Clarity",        world.player).place_locked_item(create_event_item(world, "Perfect Clarity"))
    world.multiworld.get_location("Smilemask Ending",       world.player).place_locked_item(create_event_item(world, "Smilemask Ending"))
    world.multiworld.get_location("Omnipotence Ending",     world.player).place_locked_item(create_event_item(world, "Omnipotence Ending"))
    world.multiworld.get_location("Epilogue Ending",        world.player).place_locked_item(create_event_item(world, "Epilogue Ending"))

def create_item(world: "GlyphsWorld", name: str) -> Item:
    data = item_table[name]
    return GlyphsItem(name, data.classification, data.ap_code, world.player)

def create_event_item(world: "GlyphsWorld", name: str) -> Item:
    data = item_table[name]
    return GlyphsItem(name, data.classification, None, world.player)

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

    for name in junk_items.keys():
        ic = junk_items[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name, 1)

        elif ic == ItemClassification.trap:
            trap_list[name] = 0
            if name == "John Trap" and "John Trap" in world.options.TrapTypes.value:
                trap_list[name] = 10
            elif name == "Momentum Trap" and "Momentum Trap" in world.options.TrapTypes.value:
                trap_list[name] = 40
            elif name == "Slow Trap" and "Slow Trap" in world.options.TrapTypes.value:
                trap_list[name] = 30
            elif name == "Screen Flip Trap" and "Screen Flip Trap" in world.options.TrapTypes.value:
                trap_list[name] = 20
            elif name == "Dash Trap" and "Dash Trap" in world.options.TrapTypes.value:
                trap_list[name] = 30
                
    for i in range(count):
        if not world.options.EnableTraps.value or not world.options.TrapTypes.value:
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
# ---Item Name------------------------ap_code-----------------------classifications-------------------------------advancement--count--
    
    # Upgrades
    "Progressive Sword":             ItemData(1,     ItemClassification.progression | ItemClassification.useful,         True,        2),
    "Progressive Dash Orb":          ItemData(2,     ItemClassification.progression | ItemClassification.useful,         True,        3),
    "Map":                           ItemData(3,     ItemClassification.progression | ItemClassification.useful,         True,        0),     # decided to make this a starting item
    "Grapple":                       ItemData(4,     ItemClassification.progression | ItemClassification.useful,         True,        1),
    "Progressive Parry":             ItemData(5,     ItemClassification.progression | ItemClassification.useful,         True,        2),
    "Shroud":                        ItemData(6,     ItemClassification.progression | ItemClassification.useful,         False,       1),
    "Progressive Essence of George": ItemData(7,     ItemClassification.progression | ItemClassification.useful,         False,       2),

    # Collectables
    "Silver Shard":                  ItemData(8,     ItemClassification.progression_skip_balancing,                      True,        15),
    "Gold Shard":                    ItemData(9,     ItemClassification.progression | ItemClassification.useful,         False,       3),
    "Smile Token":                   ItemData(10,    ItemClassification.progression_skip_balancing,                      True,        10),
    "Rune Cube":                     ItemData(11,    ItemClassification.progression,                                     True,        3),
    "Void Gate Shard":               ItemData(12,    ItemClassification.progression_skip_balancing,                      True,        7),
    "Glyphstone":                    ItemData(13,    ItemClassification.progression,                                     True,        3),
    "Seeds":                         ItemData(16,    ItemClassification.progression_skip_balancing,                      True,        10),
}

glyphs_hats = {
    "Pink Bow":                      ItemData(17,    ItemClassification.filler,                                          False,       1),
    "Propeller Hat":                 ItemData(18,    ItemClassification.filler,                                          False,       1),
    "Traffic Cone":                  ItemData(19,    ItemClassification.filler,                                          False,       1),
    "John Hat":                      ItemData(20,    ItemClassification.filler,                                          False,       1),
    "Top Hat":                       ItemData(21,    ItemClassification.filler,                                          False,       1),
    "Fez":                           ItemData(22,    ItemClassification.filler,                                          False,       1),
    "Party Hat":                     ItemData(23,    ItemClassification.filler,                                          False,       1),
    "Bomb Hat":                      ItemData(24,    ItemClassification.filler,                                          False,       1),
    "Crown":                         ItemData(25,    ItemClassification.filler,                                          False,       1),
    "Progressive Chicken Hat":       ItemData(26,    ItemClassification.filler,                                          False,       2),
}

junk_items = {
    # Junk Items
    "HP Refill":                     ItemData(27,    ItemClassification.filler,                                          False,       0),

    # Traps
    "John Trap":                     ItemData(28,    ItemClassification.trap,                                            False,       0),
    "Momentum Trap":                 ItemData(29,    ItemClassification.trap,                                            False,       0),
    "Slow Trap":                     ItemData(30,    ItemClassification.trap,                                            False,       0),
    "Screen Flip Trap":              ItemData(31,    ItemClassification.trap,                                            False,       0),
    "Dash Trap":                     ItemData(32,    ItemClassification.trap,                                            False,       0),
}

glyphs_events = {
    "Defeat Runic Construct":        ItemData(1000,  ItemClassification.progression_skip_balancing,                      True),
    "Defeat Gilded Serpent":         ItemData(1001,  ItemClassification.progression_skip_balancing,                      True),
    "Collapse Unlock":               ItemData(1002,  ItemClassification.progression_skip_balancing,                      True),
    "Wizard True Defeat":            ItemData(1003,  ItemClassification.progression_skip_balancing,                      True),
    "Defeat Null":                   ItemData(1004,  ItemClassification.progression_skip_balancing,                      True),
    "Defeat Spearman":               ItemData(1005,  ItemClassification.progression_skip_balancing,                      True),
    "Serpent Lock 1":                ItemData(1006,  ItemClassification.progression_skip_balancing,                      True),
    "Serpent Lock 2":                ItemData(1007,  ItemClassification.progression_skip_balancing,                      True),
    "Serpent Lock 3":                ItemData(1008,  ItemClassification.progression_skip_balancing,                      True),
    "Stalker Sigil 1":               ItemData(1009,  ItemClassification.progression_skip_balancing,                      True),
    "Stalker Sigil 2":               ItemData(1010,  ItemClassification.progression_skip_balancing,                      True),
    "Stalker Sigil 3":               ItemData(1011,  ItemClassification.progression_skip_balancing,                      True),
    "Solve Flower Puzzle":           ItemData(1012,  ItemClassification.progression_skip_balancing,                      True),
    "Clarity":                       ItemData(1013,  ItemClassification.progression_skip_balancing,                      True),
    "Last Fracture":                 ItemData(1014,  ItemClassification.progression_skip_balancing,                      True),
    "Clear Act 1":                   ItemData(1015,  ItemClassification.progression_skip_balancing,                      True),
    "Clear Act 2":                   ItemData(1016,  ItemClassification.progression_skip_balancing,                      True),
}

glyphs_goals = {
    "False Ending":                  ItemData(2000,    ItemClassification.progression_skip_balancing,                      True),
    "Good Ending":                   ItemData(2001,    ItemClassification.progression_skip_balancing,                      True),
    "True Ending":                   ItemData(2002,    ItemClassification.progression_skip_balancing,                      True),
    "Perfect Clarity":               ItemData(2003,    ItemClassification.progression_skip_balancing,                      True),
    "Smilemask Ending":              ItemData(2004,    ItemClassification.progression_skip_balancing,                      True),
    "Omnipotence Ending":            ItemData(2005,    ItemClassification.progression_skip_balancing,                      True),
    "Epilogue Ending":               ItemData(2006,    ItemClassification.progression_skip_balancing,                      True),
}

# reference map here: https://docs.google.com/drawings/d/11DQQVcq0GAYjFShZs-McEZkcpY2-PP28NdRyncZrORw/edit?usp=sharing
# note: regions listed here are only for generation, vanilla region names will be listed for the user
glyphs_regions = {
    "Menu":                          ItemData(3000,    ItemClassification.progression,                                     True),    # used for both the main menu and map screen for warps and outer void act selection
    "Region 1A":                     ItemData(3001,    ItemClassification.progression,                                     True),
    "Region 1B":                     ItemData(3002,    ItemClassification.progression,                                     True),
    "Region 1C":                     ItemData(3003,    ItemClassification.progression,                                     True),
    "Region 1D":                     ItemData(3004,    ItemClassification.progression,                                     True),
    "Region 1E":                     ItemData(3005,    ItemClassification.progression,                                     True),
    "Region 1F":                     ItemData(3006,    ItemClassification.progression,                                     True),
    "Region 2A":                     ItemData(3007,    ItemClassification.progression,                                     True),
    "Region 2B":                     ItemData(3008,    ItemClassification.progression,                                     True),
    "Region 2C":                     ItemData(3009,    ItemClassification.progression,                                     True),
    "Region 2D":                     ItemData(3010,    ItemClassification.progression,                                     True),
    "Region 2E":                     ItemData(3011,    ItemClassification.progression,                                     True),
    "Region 2F":                     ItemData(3012,    ItemClassification.progression,                                     True),
    "Region 2G":                     ItemData(3013,    ItemClassification.progression,                                     True),
    "Region 2H":                     ItemData(3014,    ItemClassification.progression,                                     True),
    "Region 2I":                     ItemData(3015,    ItemClassification.progression,                                     True),
    "Region 2J":                     ItemData(3016,    ItemClassification.progression,                                     True),
    "Region 2K":                     ItemData(3017,    ItemClassification.progression,                                     True),
    "Region 2L":                     ItemData(3018,    ItemClassification.progression,                                     True),
    "Region 2M":                     ItemData(3019,    ItemClassification.progression,                                     True),
    "Region 2N":                     ItemData(3020,    ItemClassification.progression,                                     True),
    "Region 2O":                     ItemData(3021,    ItemClassification.progression,                                     True),
    "Region 2P":                     ItemData(3022,    ItemClassification.progression,                                     True),
    "Region 2Q":                     ItemData(3023,    ItemClassification.progression,                                     True),
    "Region 3A":                     ItemData(3024,    ItemClassification.progression,                                     True),
    "Region 3B":                     ItemData(3025,    ItemClassification.progression,                                     True),
    "Region 3C":                     ItemData(3026,    ItemClassification.progression,                                     True),
    "Region 3D":                     ItemData(3027,    ItemClassification.progression,                                     True),
    "Region 3F":                     ItemData(3028,    ItemClassification.progression,                                     True),
    "Region 3G":                     ItemData(3029,    ItemClassification.progression,                                     True),
    "Region 3H":                     ItemData(3030,    ItemClassification.progression,                                     True),
    "Region 3I":                     ItemData(3031,    ItemClassification.progression,                                     True),
    "Region 4A":                     ItemData(3032,    ItemClassification.progression,                                     True),
    "Region 4B":                     ItemData(3033,    ItemClassification.progression,                                     True),
    "Region 4C":                     ItemData(3034,    ItemClassification.progression,                                     True),
    "Region 4D":                     ItemData(3035,    ItemClassification.progression,                                     True),
    "Region 4E":                     ItemData(3036,    ItemClassification.progression,                                     True),
    "Region 4F":                     ItemData(3037,    ItemClassification.progression,                                     True),
    "Region 4G":                     ItemData(3038,    ItemClassification.progression,                                     True),
    "Region 4H":                     ItemData(3039,    ItemClassification.progression,                                     True),
    "Region 4I":                     ItemData(3040,    ItemClassification.progression,                                     True),
    "Region 4J":                     ItemData(3041,    ItemClassification.progression,                                     True),
    "Collapse":                      ItemData(3042,    ItemClassification.progression,                                     True),
    "Smile Shop":                    ItemData(3043,    ItemClassification.progression,                                     True),
    "Dark Region A":                 ItemData(3044,    ItemClassification.progression,                                     True),
    "Dark Region B":                 ItemData(3045,    ItemClassification.progression,                                     True),
    "The Between":                   ItemData(3046,    ItemClassification.progression,                                     True),
    "Act 1":                         ItemData(3047,    ItemClassification.progression,                                     True),
    "Act 2":                         ItemData(3048,    ItemClassification.progression,                                     True),
    "Act 3":                         ItemData(3049,    ItemClassification.progression,                                     True),
    "Epilogue":                      ItemData(3050,    ItemClassification.progression,                                     True),
}

item_table = {
    **glyphs_items,
    **glyphs_hats,
    **glyphs_events,
    **glyphs_goals,
    **glyphs_regions,
    **junk_items
}