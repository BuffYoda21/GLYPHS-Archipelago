from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .Regions import to_generic_readable_region_name
from .Options import GlyphsOptions
from .Types import ButtonData, ButtonColor, GlyphsItem, LocData
from copy import deepcopy

options: GlyphsOptions

if TYPE_CHECKING:
    from . import GlyphsWorld

def randomize_buttons(world: "GlyphsWorld", color_percentage: int = 0, shard_percentage: int = 0) -> None:
    buttons_to_randomize = []
    world.buttons = {
        name: deepcopy(button)
        for name, button in glyphs_buttons.items()
    }

    # Randomize colors
    if color_percentage > 0:
        count = len(glyphs_buttons) * color_percentage / 100
        tmp = glyphs_buttons.copy()
        for _ in range(int(count)):
            key = world.random.choice(list(tmp.keys()))
            buttons_to_randomize.append(key)
            del tmp[key]
        
        for button in buttons_to_randomize:
            world.buttons[button].color = world.buttons[button].validColors[world.random.randint(0, len(world.buttons[button].validColors) - 1)]
            for _ in range(5): # Attempt to re-randomize any buttons that would force too much early progression
                if button.startswith("R1") and (world.buttons[button].color == ButtonColor.GREEN or world.buttons[button].color == ButtonColor.YELLOW):
                    world.buttons[button].color = world.buttons[button].validColors[world.random.randint(0, len(world.buttons[button].validColors) - 1)]
                if button.startswith("R2") and not button.startswith("R2K") and world.buttons[button].color == ButtonColor.YELLOW:
                    world.buttons[button].color = world.buttons[button].validColors[world.random.randint(0, len(world.buttons[button].validColors) - 1)]
            
            while world.options.ExcludeBlack.value and world.buttons[button].color == ButtonColor.BLACK:
                world.buttons[button].color = world.buttons[button].validColors[world.random.randint(0, len(world.buttons[button].validColors) - 1)]

    buttons_to_randomize.clear()

    # Randomize shards
    if shard_percentage > 0:
        count = len(glyphs_buttons) * shard_percentage / 100
        tmp = glyphs_buttons.copy()
        for _ in range(int(count)):
            key = world.random.choice(list(tmp.keys()))
            buttons_to_randomize.append(key)
            del tmp[key]
        
        for button in buttons_to_randomize:
            if button == "R1A Save":    # Special case for starting button
                continue
            world.buttons[button].isBroken = True
    
def create_button_shard_items(world: "GlyphsWorld") -> list[Item]:
    shard_items: list[Item] = []
    for button in world.buttons:
        if world.buttons[button].isBroken:
            shard_items.append(GlyphsItem(get_shard_name(world, button), ItemClassification.progression_skip_balancing, world.buttons[button].id * 10000, world.player))
    return shard_items

def create_button_locations(world: "GlyphsWorld") -> dict[str, LocData]:
    button_locations: dict[str, LocData] = {}
    for button in world.buttons:
        button_locations[get_button_name(world, button)] = LocData(world.buttons[button].id * 10000, world.buttons[button].region)
    return button_locations

def get_button_color(world: "GlyphsWorld", button: str) -> ButtonColor:
    return world.buttons[button].color

def is_broken(world: "GlyphsWorld", button: str) -> bool:
    return world.buttons[button].isBroken

def get_button_name(world: "GlyphsWorld", button: str) -> str:
    return f"Button {world.buttons[button].id} ({to_generic_readable_region_name(world.buttons[button].region)})"

def get_shard_name(world: "GlyphsWorld", button: str) -> str:
    return f"Button Shard {world.buttons[button].id}"

def get_raw_button_color_data(world: "GlyphsWorld") -> dict[int, int]:
    button_data: dict[int, int] = {}
    for _, button in world.buttons.items():
        button_data[button.id] = button.color.value
    return button_data

def get_button_color_spoiler_data(world: "GlyphsWorld") -> dict[str, str]:
    button_data: dict[str, str] = {}
    for key, value in world.buttons.items():
        button_data[key] = value.color.name
    return button_data

def get_broken_button_spoiler_data(world: "GlyphsWorld") -> list[str]:
    broken_buttons: list[str] = []
    for key, value in world.buttons.items():
        if value.isBroken:
            broken_buttons.append(key)
    return broken_buttons

glyphs_buttons = {
    "R1A Save":                 ButtonData(0,   "Region 1A",        ButtonColor.RED,    validColors=[ButtonColor.RED]),
    "R1B Lowest":               ButtonData(1,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R1B 2nd Lowest":           ButtonData(2,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1B 3rd Lowest":           ButtonData(3,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R1B 4th Lowest":           ButtonData(4,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1B 5th Lowest":           ButtonData(5,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1B 6th Lowest":           ButtonData(6,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R1B 7th Lowest":           ButtonData(7,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1B Map Room":             ButtonData(8,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1B Upper Puzzle":         ButtonData(9,   "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R1B Lower Puzzle":         ButtonData(10,  "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R1B Save":                 ButtonData(11,  "Region 1B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R1C First":                ButtonData(12,  "Region 1C",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1C Second":               ButtonData(13,  "Region 1C",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R1E Save":                 ButtonData(14,  "Region 1E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R1F Right":                ButtonData(15,  "Region 1F",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R2A Gate Left":            ButtonData(16,  "Region 2A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2A Gate Right":           ButtonData(17,  "Region 2A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2A Left Save":            ButtonData(18,  "Region 2A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2A Right Save":           ButtonData(19,  "Region 2A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2A Upper":                ButtonData(20,  "Region 2A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2B Puzzle":               ButtonData(21,  "Region 2B",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R2B Gate Left":            ButtonData(22,  "Region 2B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2B Left Save":            ButtonData(23,  "Region 2B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2B Right Save":           ButtonData(24,  "Region 2B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2D Save":                 ButtonData(25,  "Region 2D",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2E Lower Save":           ButtonData(26,  "Region 2E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2E Upper Save":           ButtonData(27,  "Region 2E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2E Lower":                ButtonData(28,  "Region 2E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2E Upper":                ButtonData(29,  "Region 2E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2E Upper Puzzle":         ButtonData(30,  "Region 2E",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.GREEN]),
    "R2E Serpent Lock 1":       ButtonData(31,  "Region 2E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2F Save":                 ButtonData(32,  "Region 2F",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2G Lower":                ButtonData(33,  "Region 2G",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.GREEN]),
    "R2G Middle":               ButtonData(34,  "Region 2G",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2G Moving Platform":      ButtonData(35,  "Region 2G",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2G Upper Left":           ButtonData(36,  "Region 2G",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R2G Upper Middle":         ButtonData(37,  "Region 2G",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R2G Upper Right":          ButtonData(38,  "Region 2G",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R2G Hidden":               ButtonData(39,  "Region 2G",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2H Save":                 ButtonData(40,  "Region 2H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2H Lower":                ButtonData(41,  "Region 2H",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2H Serpent Lock 2":       ButtonData(42,  "Region 2H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R2I Lower Left":           ButtonData(43,  "Region 2I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2I Lower Middle":         ButtonData(44,  "Region 2I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2I Upper Left":           ButtonData(45,  "Region 2I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2I Upper Middle":         ButtonData(46,  "Region 2I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2I Right":                ButtonData(47,  "Region 2I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2I Save":                 ButtonData(48,  "Region 2I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2J Gate Left":            ButtonData(49,  "Region 2J",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2J Save":                 ButtonData(50,  "Region 2J",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2K Chase 1":              ButtonData(51,  "Region 2K",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chase 2":              ButtonData(52,  "Region 2K",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chase 3":              ButtonData(53,  "Region 2K",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chase 4":              ButtonData(54,  "Region 2K",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R2K Chase 5":              ButtonData(55,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chase 6":              ButtonData(56,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chase Hidden":         ButtonData(57,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2K Chaos Upper 1":        ButtonData(58,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Upper 2":        ButtonData(59,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Upper 3":        ButtonData(60,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Upper 4":        ButtonData(61,  "Region 2K",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Middle 1":       ButtonData(62,  "Region 2K",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Middle 2":       ButtonData(63,  "Region 2K",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Middle 3":       ButtonData(64,  "Region 2K",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Middle 4":       ButtonData(65,  "Region 2K",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Middle 5":       ButtonData(66,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Lower 1":        ButtonData(67,  "Region 2K",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Lower 2":        ButtonData(68,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Lower 3":        ButtonData(69,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Lower 4":        ButtonData(70,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Lower 5":        ButtonData(71,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Lower 6":        ButtonData(72,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Pivot 1":        ButtonData(73,  "Region 2K",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Pivot 2":        ButtonData(74,  "Region 2K",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK, ButtonColor.BLACK]),
    "R2K Chaos Sliding Platform": ButtonData(75, "Region 2K",       ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2K Chaos Gate Left":      ButtonData(76,  "Region 2K",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2L Right":                ButtonData(77,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2L Save":                 ButtonData(78,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2L Decent Upper Left":    ButtonData(79,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2L Decent Upper Right":   ButtonData(80,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED]),
    "R2L Decent Upper Middle":  ButtonData(81,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.GREEN]),
    "R2L Decent Middle":        ButtonData(82,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2L Decent Lower":         ButtonData(83,  "Region 2L",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.GREEN]),
    "R2M Save":                 ButtonData(84,  "Region 2M",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2M Water":                ButtonData(85,  "Region 2M",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R2M Serpent Lock 3":       ButtonData(86,  "Region 2M",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R2N Save":                 ButtonData(87,  "Region 2N",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2N Chase 1":              ButtonData(88,  "Region 2N",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2N Chase 2":              ButtonData(89,  "Region 2N",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2P Left":                 ButtonData(90,  "Region 2P",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R2P Puzzle":               ButtonData(91,  "Region 2P",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R2P Save":                 ButtonData(92,  "Region 2P",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R2Q Save":                 ButtonData(93,  "Region 2Q",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3A Mirror Green":         ButtonData(94,  "Region 3A",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R3A Mirror Blue":          ButtonData(95,  "Region 3A",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3A Left":                 ButtonData(96,  "Region 3A",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3A Middle Upper":         ButtonData(97,  "Region 3A",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3A Middle Lower":         ButtonData(98,  "Region 3A",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3A Save":                 ButtonData(99,  "Region 3A",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3B Save":                 ButtonData(100, "Region 3B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3C Left":                 ButtonData(101, "Region 3C",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3C Middle":               ButtonData(102, "Region 3C",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3C Right":                ButtonData(103, "Region 3C",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3C Gate Right":           ButtonData(104, "Region 3C",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3C Save":                 ButtonData(105, "Region 3C",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3D Upper":                ButtonData(106, "Region 3D",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3D Lower":                ButtonData(107, "Region 3D",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3D Gate Upper":           ButtonData(108, "Region 3D",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3D Save":                 ButtonData(109, "Region 3D",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3E Upper":                ButtonData(110, "Region 3E",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R3E Puzzle":               ButtonData(111, "Region 3E",        ButtonColor.BLACK,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R3E QR Upper Left":        ButtonData(112, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3E QR Upper Right":       ButtonData(113, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3E QR Lower Left":        ButtonData(114, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R3E QR Lower Right":       ButtonData(115, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R3E Lower Room 1":         ButtonData(116, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3E Lower Room 2":         ButtonData(117, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R3E Lower Room 3":         ButtonData(118, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R3E Gate Upper":           ButtonData(119, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R3E Save":                 ButtonData(120, "Region 3E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3F Right":                ButtonData(121, "Region 3F",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3F Save":                 ButtonData(122, "Region 3F",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3G Left":                 ButtonData(123, "Region 3G",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3G Right":                ButtonData(124, "Region 3G",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3G Save":                 ButtonData(125, "Region 3G",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3H Left":                 ButtonData(126, "Region 3H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R3H Middle":               ButtonData(127, "Region 3H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3H Right":                ButtonData(128, "Region 3H",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3H Gate Left":            ButtonData(129, "Region 3H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R3H Save":                 ButtonData(130, "Region 3H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R3I Challenge 1":          ButtonData(131, "Region 3I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3I Challenge 2":          ButtonData(132, "Region 3I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3I Challenge 3":          ButtonData(133, "Region 3I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3I Challenge 4":          ButtonData(134, "Region 3I",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R3I Save":                 ButtonData(135, "Region 3I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4A Left":                 ButtonData(136, "Region 4A",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R4A Middle":               ButtonData(137, "Region 4A",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4A Right":                ButtonData(138, "Region 4A",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4B Save":                 ButtonData(139, "Region 4B",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4C 1st":                  ButtonData(140, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 2nd":                  ButtonData(141, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 3rd":                  ButtonData(142, "Region 4C",        ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4C 4th":                  ButtonData(143, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 5th":                  ButtonData(144, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 6th":                  ButtonData(145, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 7th":                  ButtonData(146, "Region 4C",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4C 8th":                  ButtonData(147, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 9th":                  ButtonData(148, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 10th":                 ButtonData(149, "Region 4C",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4C 5 Parry 1":            ButtonData(150, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 5 Parry 2":            ButtonData(151, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 5 Parry 3":            ButtonData(152, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 5 Parry 4":            ButtonData(153, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C 5 Parry 5":            ButtonData(154, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4C Gate Right":           ButtonData(155, "Region 4C",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4D Platforming 1st":      ButtonData(156, "Region 4D",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R4D Platforming 2nd":      ButtonData(157, "Region 4D",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R4D Platforming 3rd":      ButtonData(158, "Region 4D",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "R4D Platforming 4th":      ButtonData(159, "Region 4D",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4D Platforming 5th":      ButtonData(160, "Region 4D",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4D Multiparry":           ButtonData(161, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4D Ultra-Multiparry":     ButtonData(162, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4D Main Route 1st":       ButtonData(163, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4D Main Route 2nd":       ButtonData(164, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4D Main Route 3rd":       ButtonData(165, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4D Main Route 4th":       ButtonData(166, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4D Main Route 5th":       ButtonData(167, "Region 4D",        ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4D Main Route 6th":       ButtonData(168, "Region 4D",        ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4D Main Route 7th":       ButtonData(169, "Region 4D",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4D Save":                 ButtonData(170, "Region 4D",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4E Save":                 ButtonData(171, "Region 4E",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4F Lower":                ButtonData(172, "Region 4F",        ButtonColor.GREEN,  validColors=[ButtonColor.GREEN, ButtonColor.PINK]),
    "R4F Save":                 ButtonData(173, "Region 4F",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4G 1st":                  ButtonData(174, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4G 2nd":                  ButtonData(175, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4G 3rd":                  ButtonData(176, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4G 4th":                  ButtonData(177, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4G 5th":                  ButtonData(178, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4G 6th":                  ButtonData(179, "Region 4G",        ButtonColor.PINK,   validColors=[ButtonColor.PINK]),
    "R4H Middle":               ButtonData(180, "Region 4H",        ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "R4H Save":                 ButtonData(181, "Region 4H",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4I Left":                 ButtonData(182, "Region 4I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4I Right":                ButtonData(183, "Region 4I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "R4I Gate Upper":           ButtonData(184, "Region 4I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.BLACK]),
    "R4I Save":                 ButtonData(185, "Region 4I",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "R4J Save":                 ButtonData(186, "Region 4J",        ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "Dark 1":                   ButtonData(187, "Dark Region A",    ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "Dark 2":                   ButtonData(188, "Dark Region A",    ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "Dark 3":                   ButtonData(189, "Dark Region A",    ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Dark 4":                   ButtonData(190, "Dark Region A",    ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Dark 5":                   ButtonData(191, "Dark Region A",    ButtonColor.GREEN,  validColors=[ButtonColor.GREEN]),
    "Dark 6":                   ButtonData(192, "Dark Region A",    ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Dark Save":                ButtonData(193, "Dark Region B",    ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "Smile Refund":             ButtonData(194, "Smile Shop",       ButtonColor.RED,    validColors=[ButtonColor.RED]),
    "Smile Hidden":             ButtonData(195, "Smile Shop",       ButtonColor.GREEN, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Collapse George Rescue":   ButtonData(196, "Collapse",         ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Void Chase 1":             ButtonData(197, "Act 1",            ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Void Chase 2":             ButtonData(198, "Act 1",            ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Void Chase 3":             ButtonData(199, "Act 1",            ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Void Chase 4":             ButtonData(200, "Act 1",            ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Void Chase Gate":          ButtonData(201, "Act 1",            ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Epilogue 1":               ButtonData(202, "Epilogue",         ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between Save":             ButtonData(203, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN]),
    "Between Gate Left":        ButtonData(204, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm1":              ButtonData(205, "The Between",      ButtonColor.GREEN,  validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm4":              ButtonData(206, "The Between",      ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm5":              ButtonData(207, "The Between",      ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm10":             ButtonData(208, "The Between",      ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm13":             ButtonData(209, "The Between",      ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm19":             ButtonData(210, "The Between",      ButtonColor.YELLOW, validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm28":             ButtonData(211, "The Between",      ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "Between rm30":             ButtonData(212, "The Between",      ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "Between rm39":             ButtonData(213, "The Between",      ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm40":             ButtonData(214, "The Between",      ButtonColor.PINK,   validColors=[ButtonColor.GREEN, ButtonColor.PINK]),
    "Between rm42 Button 1":    ButtonData(215, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 2":    ButtonData(216, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 3":    ButtonData(217, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 4":    ButtonData(218, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 5":    ButtonData(219, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 6":    ButtonData(220, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm42 Button 7":    ButtonData(221, "The Between",      ButtonColor.RED,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm43 Button 1":    ButtonData(222, "The Between",      ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "Between rm43 Button 2":    ButtonData(223, "The Between",      ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "Between rm57":             ButtonData(224, "The Between",      ButtonColor.PINK,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW, ButtonColor.PINK]),
    "Between rm66":             ButtonData(225, "The Between",      ButtonColor.BLUE,   validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between rm71":             ButtonData(226, "The Between",      ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
    "Between Pre-Boss 1":       ButtonData(227, "The Between",      ButtonColor.RED,    validColors=[ButtonColor.RED, ButtonColor.BLUE, ButtonColor.GREEN, ButtonColor.YELLOW]),
}