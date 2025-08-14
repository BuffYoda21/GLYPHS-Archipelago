from BaseClasses import Region
from .Types import GlyphsLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

def create_regions(world: "GlyphsWorld"):
    # Kinda messy, might rework later
    menu = create_region(world, "Menu")
    region1ul = create_region_and_connect(world, "Region 1 - Upper Left", menu)
    region1c = create_region_and_connect(world, "Region 1 - Central", region1ul)
    region1l = create_region_and_connect(world, "Region 1 - Left", region1c)
    region1ur = create_region_and_connect(world, "Region 1 - Upper Right", region1ul)
    auto_connect(region1ur, region1c)
    region2lf = create_region_and_connect(world, "Region 2 - Left", region1ur)
    region2c = create_region_and_connect(world, "Region 2 - Central", region2lf)
    region2s1 = create_region_and_connect(world, "Region 2 - Sector 1", region2c)
    region2s2 = create_region_and_connect(world, "Region 2 - Sector 2", region2c)
    auto_connect(region2s1, region2s2)
    region2s4 = create_region_and_connect(world, "Region 2 - Sector 4", region2c)
    region2s4e = create_region_and_connect(world, "Region 2 - Sector 4 End", region2s4)
    region2spu = create_region_and_connect(world, "Region 2 - Serpent Upper", region2c)
    auto_connect(region2s2, region2spu)
    region2spl = create_region_and_connect(world, "Region 2 - Serpent Lower", region2spu)
    region2low = create_region_and_connect(world, "Region 2 - Lower", region2spl)
    region2sh = create_region_and_connect(world, "Region 2 - Shadow Chase", region2s2)
    region3 = create_region_and_connect(world, "Region 3", region2low)
    region4e = create_region_and_connect(world, "Region 4 - Entrance", region2c)
    auto_connect(region4e, region2s4)
    region4u = create_region_and_connect(world, "Region 4 - Upper", region4e)
    region4c = create_region_and_connect(world, "Region 4 - Central", region4u)
    region4l = create_region_and_connect(world, "Region 4 - Lower", region4c)
    auto_connect(region3, region4l)
    auto_connect(region4l, region2s4e)
    collapse = create_region_and_connect(world, "Collapse", region3)
    smile_shop = create_region_and_connect(world, "Smile Shop", region2s1)
    dark_region = create_region_and_connect(world, "Dark Region", region2low)
    the_between = create_region_and_connect(world, "The Between", region2lf)
    act1 = create_region_and_connect(world, "Act 1", menu)
    act2 = create_region_and_connect(world, "Act 2", act1)
    auto_connect(menu, act2)
    act3 = create_region_and_connect(world, "Act 3", act2)
    auto_connect(menu, act3)
    epilogue = create_region_and_connect(world, "Epilogue", act1)

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

def create_region_and_connect(world: "GlyphsWorld", name: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, connected_region.name + " -> " + name)
    return reg

def auto_connect(region_from: Region, region_to: Region) -> None:
    region_from.connect(region_to, region_from.name + " -> " + region_to.name)