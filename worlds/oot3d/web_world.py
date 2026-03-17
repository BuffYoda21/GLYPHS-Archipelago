from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets

class OoT3DWebWorld(WebWorld):
    game = "Ocarina of Time 3D"

    # Valid themes: dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up OoT3D for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["BuffYoda21"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets
