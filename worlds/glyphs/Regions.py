from BaseClasses import Region
from .Types import GlyphsLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

def create_regions(world: "GlyphsWorld"):
    create_region(world, "Menu")
    create_region(world, "Region 1 - Upper Left")
    create_region(world, "Region 1 - Central")
    create_region(world, "Region 1 - Left")
    create_region(world, "Region 1 - Upper Right")
    create_region(world, "Region 2 - Left")
    create_region(world, "Region 2 - Central")
    create_region(world, "Region 2 - Sector 1")
    create_region(world, "Region 2 - Sector 2")
    create_region(world, "Region 2 - Sector 4")
    create_region(world, "Region 2 - Sector 4 End")
    create_region(world, "Region 2 - Serpent Upper")
    create_region(world, "Region 2 - Serpent Lower")
    create_region(world, "Region 2 - Lower")
    create_region(world, "Region 2 - Shadow Chase")
    create_region(world, "Region 3")
    create_region(world, "Region 4 - Entrance")
    create_region(world, "Region 4 - Upper")
    create_region(world, "Region 4 - Central")
    create_region(world, "Region 4 - Lower")
    create_region(world, "Collapse")
    create_region(world, "Smile Shop")
    create_region(world, "Dark Region")
    create_region(world, "The Between")
    create_region(world, "Act 1")
    create_region(world, "Act 2")
    create_region(world, "Act 3")
    create_region(world, "Epilogue")

def create_region(world: "GlyphsWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = GlyphsLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg