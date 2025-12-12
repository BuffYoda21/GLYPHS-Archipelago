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

event_locations = {
    "Defeat Runic Construct":                "Region 1 - Central",
    "Stalker Sigil 1":                       "Region 1 - Central",
    "Serpent Lock 1":                        "Region 2 - Sector 1",
    "Serpent Lock 2":                        "Region 2 - Sector 2",
    "Serpent Lock 3":                        "Region 2 - Sector 4 End",
    "Defeat Gilded Serpent":                 "Region 2 - Serpent Upper",
    "Stalker Sigil 2":                       "Region 2 - Serpent Lower",
    "Stalker Sigil 3":                       "Region 2 - Sector 4",
    "Solve Flower Puzzle":                   "Region 2 - Sector 4 End",
    "Collapse Unlock":                       "Region 3",
    "Wizard True Defeat":                    "Region 3",
    "Defeat Spearman":                       "Region 4 - Entrance",
    "Good Ending":                           "Region 4 - Lower",
    "Last Fracture":                         "Region 4 - Lower",
    "False Ending":                          "Collapse",
    "Smilemask Ending":                      "Smile Shop",
    "Defeat Null":                           "Dark Region",
    "Clarity":                               "Dark Region",
    "Perfect Clarity":                       "Dark Region",
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