from typing import Dict, TYPE_CHECKING
from .Types import LocData

if TYPE_CHECKING:
    from . import GlyphsWorld

def get_total_locations(world: "GlyphsWorld") -> int:
    total = 0
    for name in location_table:
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items() if data.ap_code is not None}
    return names

# Intended to use for YAML options but not currently implemented
def is_valid_location(world: "GlyphsWorld", name) -> bool:
    return True

def create_additional_locations(world: "GlyphsWorld") -> None:
    if world.options.ButtonShardPercent.value != 0:
        from .Buttons import create_button_locations
        location_table.update(create_button_locations(world))

glyphs_locations = {
    # Region 1
    "(R1) Starting Item":                               LocData(1,  "Region 1A"),
    "(R1) Sword Pedestal":                              LocData(2,  "Region 1D"),
    "(R1) Runic Construct Reward":                      LocData(3,  "Region 1E"),
    "(R1) Map Pedestal":                                LocData(4,  "Region 1B"),
    "(R1) Silver Shard Puzzle 1 - Map":                 LocData(5,  "Region 1B"),
    "(R1) Silver Shard Puzzle 2 - Grapple":             LocData(6,  "Region 1F"),
    "(R1) Silver Shard Puzzle 3 - Spike Tunnel":        LocData(7,  "Region 2A"), # this location was lumped in to part of region 2 for logical reasons
    "(R1) Smile Token Puzzle 1 - Hidden Bounce Pad":    LocData(8,  "Region 1D"),
    "(R1) Smile Token Puzzle 9 - Moving Platforms":     LocData(9,  "Region 1B"),
    "(R1) Color Cypher Room Pickup":                    LocData(10, "Region 1F"),
    "(R1) Master Puzzle 2 - Silence":                   LocData(11, "Region 1D"),

    # Region 2
    "(R2S1) Silver Shard Puzzle 4 - Save Button":       LocData(12, "Region 2C"),
    "(R2) Silver Shard Puzzle 5 - Respawn":             LocData(13, "Region 2E"),
    "(R2) Silver Shard Puzzle 6 - Invisible":           LocData(14, "Region 2B"),
    "(R2S2) Silver Shard Puzzle 7 - Timed":             LocData(15, "Region 2G"),
    "(R2) Silver Shard Puzzle 8 - Avoid Respawn":       LocData(16, "Region 2P"),
    "(R2) Silver Shard Puzzle 9 - Color Dash Puzzle":   LocData(17, "Region 2Q"),
    "(R2) Silver Shard Puzzle 15 - Escape Serpent":     LocData(18, "Region 2N"),
    "(R2S2) Smile Token Puzzle 3 - Car Hall":           LocData(19, "Region 2H"),
    "(R2) Smile Token Puzzle 6 - Above Serpent":        LocData(20, "Region 2N"),
    "(R2S1) Smile Token Puzzle 8 - Erosion":            LocData(21, "Region 2E"),
    "(R2S2) Smile Token Puzzle 10 - Chaos":             LocData(22, "Region 2K"),
    "(R2) Gilded Serpent Reward":                       LocData(23, "Region 2P"),
    "(R2S1) Cameo Room Pickup":                         LocData(24, "Region 2E"),
    "(R2S2) Car Hall Pickup":                           LocData(25, "Region 2H"),
    "(R2S1) Near Shooters Pickup":                      LocData(26, "Region 2E"),
    "(R2S3) Collapsed Tunnel Pickup":                   LocData(27, "Region 2L"),
    "(R2) Nest Room Pickup":                            LocData(28, "Region 2B"),
    "(R2) Serpent Boss Room Pickup":                    LocData(29, "Region 2O"),
    "(R2) Shadow Chase Reward":                         LocData(30, "Region 2K"),
    "(R2S4) Water Room Pickup":                         LocData(31, "Region 2M"),
    "(R2) George Reward 1":                             LocData(32, "Region 2B"),
    "(R2) George Reward 2":                             LocData(33, "Region 2B"),
    "(R2S2) Shadow Chase Pickup":                       LocData(34, "Region 2K"),
    "(R2S2) Master Puzzle 1 - Map":                     LocData(35, "Region 2G"),

    # Region 3
    "(R3) Green Stone Trial":                           LocData(36, "Region 3D"),
    "(R3) Blue Stone Trial":                            LocData(37, "Region 3I"),
    "(R3) Red Stone Trial":                             LocData(38, "Region 3F"),
    "(R3) Silver Shard Puzzle 10 - Mirror":             LocData(39, "Region 3A"),
    "(R3) Silver Shard Puzzle 11 - No Dash":            LocData(40, "Region 3B"),
    "(R3) Silver Shard Puzzle 12 - QR":                 LocData(41, "Region 3E"),
    "(R3) Silver Shard Puzzle 13 - Black Button":       LocData(42, "Region 3E"),
    "(R3) Silver Shard Puzzle 14 - Grapple":            LocData(43, "Region 3I"),
    "(R3) Smile Token Puzzle 2 - Wizard":               LocData(44, "Region 3E"),
    "(R3) Smile Token Puzzle 7 - No Dash":              LocData(45, "Region 3G"),
    "(R3) Wizard Reward":                               LocData(46, "Region 3E"),
    "(R3) Room Below Wizard Pickup":                    LocData(47, "Region 3E"),
    "(R3) Master Puzzle 3 - Counters":                  LocData(48, "Region 3F"),

    # Region 4
    "(R4) Spearman Reward":                             LocData(49, "Region 4C"),
    "(R4) Multiparry Gold Shard Puzzle":                LocData(50, "Region 4D"),
    "(R4) Platforming Gold Shard Room":                 LocData(51, "Region 4D"),
    "(R4) Flower Puzzle Reward":                        LocData(52, "Region 4E"),
    "(R4) Smile Token Puzzle 4 - Multiparry":           LocData(53, "Region 4D"),
    "(R4) Smile Token Puzzle 5 - Entrance":             LocData(54, "Region 4A"),
    "(R4) Rosetta Stone Pickup":                        LocData(55, "Region 4D"),
    "(R4) Long Parry Platforming Room Pickup":          LocData(56, "Region 4G"),

    # Dark Region
    "(Dark) Secret Room Pickup":                        LocData(57, "Dark Region A"),
    "(Dark) Large Room Pickup in the Corner":           LocData(58, "Dark Region A"),
    "(Dark) Null Reward":                               LocData(59, "Dark Region A"),

    # Smile Shop
    "(Smile) Shop Item 1":                              LocData(60, "Smile Shop"),
    "(Smile) Shop Item 2":                              LocData(61, "Smile Shop"),
    "(Smile) Shop Item 3":                              LocData(62, "Smile Shop"),
    "(Smile) Shop Item 4":                              LocData(63, "Smile Shop"),
    "(Smile) Dash Puzzle Reward":                       LocData(64, "Smile Shop"),

    # The Between
    "(Between) Construct Reward":                       LocData(65, "The Between"),
    "(Between) Serpent Reward":                         LocData(66, "The Between"),
    "(Between) Wizard Reward":                          LocData(67, "The Between"),
    "(Between) Hot Spring Item":                        LocData(68, "The Between"),
    "(Between) Between Reward 1":                       LocData(69, "The Between"),
    "(Between) Between Reward 2":                       LocData(70, "The Between"),

    # Collapse
    "(Esc) Escape the Escape Sequence":                 LocData(71, "Collapse"),

    # Act 1
    "(Void 1) Enter Void Reward":                       LocData(72, "Act 1"),
    "(Void 1) Void Gate Shard Location 1":              LocData(73, "Act 1"),
    "(Void 1) Void Gate Shard Location 2":              LocData(74, "Act 1"),
    "(Void 1) Void Gate Shard Location 3":              LocData(75, "Act 1"),
    "(Void 1) Void Gate Shard Location 4":              LocData(76, "Act 1"),
    "(Void 1) Void Gate Shard Location 5":              LocData(77, "Act 1"),
    "(Void 1) Void Gate Shard Location 6":              LocData(78, "Act 1"),
    "(Void 1) Void Gate Shard Location 7":              LocData(79, "Act 1"),
    "(Void 1) John Room Pickup":                        LocData(80, "Act 1"),
    
    # Act 2
    "(Void 2) Free Item":                               LocData(81, "Act 2"),
    "(Void 2) Boss Rush Heal 1":                        LocData(82, "Act 2"),
    "(Void 2) Boss Rush Heal 2":                        LocData(83, "Act 2"),
    "(Void 2) Boss Rush Heal 3":                        LocData(84, "Act 2"),
    "(Void 2) Boss Rush Heal 4":                        LocData(85, "Act 2"),
    "(Void 2) Pink Bow Pickup":                         LocData(86, "Act 2"),

    # Act 3
    "(Void 3) Preminition Reward":                      LocData(87, "Act 3"),
}

location_table = {
    **glyphs_locations,
}
