from BaseClasses import Region
from .Types import GlyphsLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld

def create_regions(world: "GlyphsWorld"):
    create_region(world, "Menu")
    create_region(world, "Region 1A")
    create_region(world, "Region 1B")
    create_region(world, "Region 1C")
    create_region(world, "Region 1D")
    create_region(world, "Region 1E")
    create_region(world, "Region 1F")
    create_region(world, "Region 2A")
    create_region(world, "Region 2B")
    create_region(world, "Region 2C")
    create_region(world, "Region 2D")
    create_region(world, "Region 2E")
    create_region(world, "Region 2F")
    create_region(world, "Region 2G")
    create_region(world, "Region 2H")
    create_region(world, "Region 2I")
    create_region(world, "Region 2J")
    create_region(world, "Region 2K")
    create_region(world, "Region 2L")
    create_region(world, "Region 2M")
    create_region(world, "Region 2N")
    create_region(world, "Region 2O")
    create_region(world, "Region 2P")
    create_region(world, "Region 2Q")
    create_region(world, "Region 3A")
    create_region(world, "Region 3B")
    create_region(world, "Region 3C")
    create_region(world, "Region 3D")
    create_region(world, "Region 3E")
    create_region(world, "Region 3F")
    create_region(world, "Region 3G")
    create_region(world, "Region 3H")
    create_region(world, "Region 3I")
    create_region(world, "Region 4A")
    create_region(world, "Region 4B")
    create_region(world, "Region 4C")
    create_region(world, "Region 4D")
    create_region(world, "Region 4E")
    create_region(world, "Region 4F")
    create_region(world, "Region 4G")
    create_region(world, "Region 4H")
    create_region(world, "Region 4I")
    create_region(world, "Region 4J")
    create_region(world, "Collapse")
    create_region(world, "Smile Shop")
    create_region(world, "Dark Region A")
    create_region(world, "Dark Region B")
    create_region(world, "The Between")
    create_region(world, "Act 1")
    create_region(world, "Act 2")
    create_region(world, "Act 3")
    create_region(world, "Epilogue")

event_locations = {
    "Defeat Runic Construct":                "Region 1E",
    "Stalker Sigil 1":                       "Region 1E",
    "Serpent Lock 1":                        "Region 2E",
    "Serpent Lock 2":                        "Region 2H",
    "Serpent Lock 3":                        "Region 2M",
    "Defeat Gilded Serpent":                 "Region 2N",
    "Stalker Sigil 2":                       "Region 2O",
    "Stalker Sigil 3":                       "Region 2L",
    "Solve Flower Puzzle":                   "Region 2M",
    "Collapse Unlock":                       "Region 3E",
    "Wizard True Defeat":                    "Region 3E",
    "Defeat Spearman":                       "Region 4B",
    "Good Ending":                           "Region 4I",
    "Last Fracture":                         "Region 4I",
    "False Ending":                          "Collapse",
    "Smilemask Ending":                      "Smile Shop",
    "Defeat Null":                           "Dark Region A",
    "Clarity":                               "Dark Region B",
    "Perfect Clarity":                       "Dark Region B",
    "Omnipotence Ending":                    "Act 1",
    "Clear Act 1":                           "Act 1",
    "Clear Act 2":                           "Act 2",
    "True Ending":                           "Act 3",
    "Epilogue Ending":                       "Epilogue",
}

def create_region(world: "GlyphsWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = GlyphsLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)

    for loc_name, loc_region in event_locations.items():
        if loc_region == name:
            event = GlyphsLocation(world.player, loc_name, None, reg)
            event.event = True
            reg.locations.append(event)
    
    world.multiworld.regions.append(reg)
    return reg