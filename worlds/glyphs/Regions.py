from BaseClasses import Region
from .Types import GlyphsLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

# This is where you will create your imaginary game world
# IE: connect rooms and areas together
# This is NOT where you'll add requirements for how to get to certain locations thats in Rules.py
# This is also long and tediouos
def create_regions(world: "GlyphsWorld"):
    # The functions that are being used here will be located at the bottom to view
    # The important part is that if its not a dead end and connects to another place then name it
    # Otherwise you can just create the connection. Not that naming it is bad

    # You can technically name your connections whatever you want as well
    # You'll use those connection names in Rules.py

    # Kinda messy, might rework later
    menu = create_region(world, "Menu")
    region1 = create_region_and_connect(world, "Region 1", "Menu -> Tomb Main Entrance", menu)
    region2 = create_region_and_connect(world, "Region 2", "Region 1 Gate -> Region 2", region1)
    region3 = create_region_and_connect(world, "Region 3", "Region 2 Long Fall -> Region 3", region2)
    region4 = create_region_and_connect(world, "Region 4", "Region 2 Collapsed Tunnel -> Region 4", region2)
    region3.connect(region4, "Region 3 Flower Passage -> Region 4")
    collapse = create_region_and_connect(world, "Collapse", "Region 3 Wizard Boss Room -> Collapse", region3)
    smile_shop = create_region_and_connect(world, "Smile Shop", "Region 2 Smile Shop Entrance -> Smile Shop", region2)
    dark_region = create_region_and_connect(world, "Dark Region", "Region 2 Long Fall Hidden Passage-> Dark Region", region2)
    the_between = create_region_and_connect(world, "The Between", "Region 2 Hole in the Wall-> The Between", region2)
    act1 = create_region_and_connect(world, "Act 1", "Menu -> Act 1", menu)
    act2 = create_region_and_connect(world, "Act 2", "Act 1 -> Act 2", act1)
    menu.connect(act2, "Menu -> Act 2")
    act3 = create_region_and_connect(world, "Act 3", "Act 2 -> Act 3", act2)
    menu.connect(act3, "Menu -> Act 3")
    epilogue = create_region_and_connect(world, "Epilogue", "Act 1 -> Epilogue", act1)

def create_region(world: "GlyphsWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = GlyphsLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

# This runs the create region function while also connecting to another region
# Just simplifies process since you woill be connecting a lot of regions
def create_region_and_connect(world: "GlyphsWorld",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg