# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# When a list is described its described as a list of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, ChapterType, GlyphsItem, chapter_type_to_name
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import GlyphsWorld

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "GlyphsWorld") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []

    # In this function is where you would remove any starting items that you add in options such as starting chapter
    # This is also the place you would add dynamic amounts of items from options
    # I can point to Sly Cooper and the Thievious Raccoonus since I did that

    # This is a good place to grab anything you need from options
    starting_chapter = chapter_type_to_name[ChapterType(world.options.StartingChapter)]

    # For this example I'll make it so there is a starting chapter
    # We loop through all the chapters in the my_chapter section
    for chapter in glyphs_chapters.keys():
        # If the starting chapter equals the chapter we're looking at skip it
        # We skip it since we dont want to add the chapter the player started with to the item pool
        print("-------------------------")
        print(starting_chapter)
        print("-------------------------")
        if starting_chapter == chapter:
            continue
        # Otherwise then we create an item with that name and add it to the item pool
        else:
            itempool.append(create_item(world, chapter))
    
    # It's up to you and how you want things organized but I like to deal with victory here
    # This creates your win item and then places it at the "location" where you win
    goal = create_item(world, "Goal")
    world.multiworld.get_location("add dynamic goal here", world.player).place_locked_item(goal)    #dont forget to change this

    # Then junk items are made
    # Check out the create_junk_items function for more details
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 1)

    return itempool

# This is a generic function to create a singular item
def create_item(world: "GlyphsWorld", name: str) -> Item:
    data = item_table[name]
    return GlyphsItem(name, data.classification, data.ap_code, world.player)

# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "GlyphsWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [GlyphsItem(name, item_type, data.ap_code, world.player)]

    return itemlist

# Finally, where junk items are created
def create_junk_items(world: "GlyphsWorld", count: int) -> List[Item]:
    trap_chance = world.options.TrapChance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    junk_weights = {
        "HP Refill":        50,
        "Pink Bow":         10,
        "Propeller Hat":    10,
        "Traffic Cone":     10,
        "John Hat":         10,
        "Top Hat":          10,
        "Fez":              10,
        "Party Hat":        10,
        "Bomb Hat":         10,
        "Crown":            10,
    }

    # This grabs all the junk items and trap items
    for name in item_table.keys():
        # Here we are getting all the junk item names and weights
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        # This is for traps if your randomization includes it
        # It also grabs the trap weights from the options page
        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "sMiLE Trap":
                trap_list[name] = world.options.sMiLETrapWeight.value
            elif name == "John Trap":
                trap_list[name] = world.options.JohnTrapWeight.value
            elif name == "Spear Trap":
                trap_list[name] = world.options.SpearTrapWeight.value
            elif name == "Death Trap":
                trap_list[name] = world.options.DeathTrapWeight.value

    # Where all the magic happens of adding the junk and traps randomly
    # AP does all the weight management so we just need to worry about how many are created
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

# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well
glyphs_items = {
# ---Item Name------------------------ap_code-----------------------classifications-------------------------------count--
    
    # Major Upgrades
    "Sword":                    ItemData(1,     ItemClassification.progression + ItemClassification.useful,         1),
    "Progressive Dash Orb":     ItemData(2,     ItemClassification.progression + ItemClassification.useful,         2),
    "Map":                      ItemData(3,     ItemClassification.progression + ItemClassification.useful,         1),     # might make this a starting item
    "Grapple":                  ItemData(4,     ItemClassification.progression + ItemClassification.useful,         1),
    "Parry":                    ItemData(5,     ItemClassification.progression + ItemClassification.useful,         1),

    # Collectables
    "Silver Shard":             ItemData(6,     ItemClassification.progression_skip_balancing,                      15),
    "Gold Shard":               ItemData(7,     ItemClassification.useful,                                          3),
    "Smile Token":              ItemData(8,     ItemClassification.progression_skip_balancing,                      10),
    "Rune Cube":                ItemData(9,     ItemClassification.progression,                                     3),
    "Void Gate Shard":          ItemData(10,    ItemClassification.progression_skip_balancing,                      7),
    "Green Stone":              ItemData(11,    ItemClassification.progression,                                     1),
    "Red Stone":                ItemData(12,    ItemClassification.progression,                                     1),
    "Blue Stone":               ItemData(13,    ItemClassification.progression,                                     1),
    "Seeds":                    ItemData(14,    ItemClassification.progression,                                     10),

    # Upgrades
    "Sword Rune":               ItemData(14,    ItemClassification.useful,                                          1),
    "Shroud":                   ItemData(15,    ItemClassification.useful,                                          1),
    "Fast Magic":               ItemData(16,    ItemClassification.useful,                                          1),
    "Swift Parry":              ItemData(17,    ItemClassification.useful,                                          1),
    "Progressive Chicken Hat":  ItemData(18,    ItemClassification.useful,                                          2),

    # Events (not shuffled)
    "Runic Construct Defeated": ItemData(19,    ItemClassification.progression_skip_balancing,                      1),
    "Gilded Serpent Defeated":  ItemData(20,    ItemClassification.progression_skip_balancing,                      1),
    "Collapse Unlocked":        ItemData(21,    ItemClassification.progression_skip_balancing,                      1),
    "Wizard True Defeat":       ItemData(22,    ItemClassification.progression_skip_balancing,                      1),
    "Spearman Defeated":        ItemData(23,    ItemClassification.progression_skip_balancing,                      1),
    "Serpent Lock Activated":   ItemData(24,    ItemClassification.progression_skip_balancing,                      3),
    "Stalker Sigil Collected":  ItemData(25,    ItemClassification.progression_skip_balancing,                      3),
    "Clarity":                  ItemData(25,    ItemClassification.progression_skip_balancing,                      1),
    "Act 1 Unlocked":           ItemData(26,    ItemClassification.progression_skip_balancing,                      1),
    "Act 2 Unlocked":           ItemData(27,    ItemClassification.progression_skip_balancing,                      1),
    "Act 3 Unlocked":           ItemData(28,    ItemClassification.progression_skip_balancing,                      1),

    # Goal items (still not sure this is how I want to structure this)
    "False Ending":             ItemData(29,    ItemClassification.progression_skip_balancing,                      1),
    "Good Ending":              ItemData(30,    ItemClassification.progression_skip_balancing,                      1),
    "True Ending":              ItemData(31,    ItemClassification.progression_skip_balancing,                      1),
    "Perfect Clarity":          ItemData(32,    ItemClassification.progression_skip_balancing,                      1),
    "Smilemask Ending":         ItemData(33,    ItemClassification.progression_skip_balancing,                      1),
    "Omnipotence Ending":       ItemData(34,    ItemClassification.progression_skip_balancing,                      1),
    "Epilouge Ending":          ItemData(35,    ItemClassification.progression_skip_balancing,                      1),
    "All Main Endings":         ItemData(36,    ItemClassification.progression_skip_balancing,                      1),
    "All Star Endings":         ItemData(37,    ItemClassification.progression_skip_balancing,                      1),
    "All Endings":              ItemData(38,    ItemClassification.progression_skip_balancing,                      1),
    "Goal":                     ItemData(39,    ItemClassification.progression_skip_balancing,                      1),
}

# I like to split up the items so that its easier to look at and since sometimes you only need to look at one specific type of list
# An example of that is in create_itempool where I simulated having a starting chapter
glyphs_chapters = {
    "Menu":                     ItemData(40,    ItemClassification.progression),    # using this as starting chapter to allow randomized starting spawns
    "Region 1":                 ItemData(41,    ItemClassification.progression),
    "Region 2":                 ItemData(42,    ItemClassification.progression),
    "Region 3":                 ItemData(43,    ItemClassification.progression),
    "Region 4":                 ItemData(44,    ItemClassification.progression),
    "Collapse":                 ItemData(45,    ItemClassification.progression),
    "Smile Shop":               ItemData(46,    ItemClassification.progression),
    "Dark Region":              ItemData(47,    ItemClassification.progression),
    "The Between":              ItemData(48,    ItemClassification.progression),
    "Act 1":                    ItemData(49,    ItemClassification.progression),
    "Act 2":                    ItemData(50,    ItemClassification.progression),
    "Act 3":                    ItemData(51,    ItemClassification.progression),
    "Epilogue":                 ItemData(52,    ItemClassification.progression),
}

# In the way that I made items, I added a way to specify how many of an item should exist
# That's why junk has a 0 since how many are created is in the create_junk_items
# There is a better way of doing this but this is my jank
junk_items = {
    # Junk Items
    "HP Refill":                ItemData(53,    ItemClassification.filler,                                          0),
    "Pink Bow":                 ItemData(54,    ItemClassification.filler,                                          0),
    "Propeller Hat":            ItemData(55,    ItemClassification.filler,                                          0),
    "Traffic Cone":             ItemData(56,    ItemClassification.filler,                                          0),
    "John Hat":                 ItemData(57,    ItemClassification.filler,                                          0),
    "Top Hat":                  ItemData(58,    ItemClassification.filler,                                          0),
    "Fez":                      ItemData(59,    ItemClassification.filler,                                          0),
    "Party Hat":                ItemData(60,    ItemClassification.filler,                                          0),
    "Bomb Hat":                 ItemData(61,    ItemClassification.filler,                                          0),
    "Crown":                    ItemData(62,    ItemClassification.filler,                                          0),

    # Traps
    "sMiLE Trap":               ItemData(63,    ItemClassification.trap,                                            0),
    "John Trap":                ItemData(64,    ItemClassification.trap,                                            0),
    "Spear Trap":               ItemData(65,    ItemClassification.trap,                                            0),
    "Death Trap":               ItemData(66,    ItemClassification.trap,                                            0),
}

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **glyphs_items,
    **glyphs_chapters,
    **junk_items
}