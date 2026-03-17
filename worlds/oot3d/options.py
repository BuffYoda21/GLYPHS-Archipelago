from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class Placeholder(Toggle):
    """
    Placeholder
    """
    display_name = "Placeholder"

class TrapChance(Range):
    """
    Percent chance any given filler will be an ice trap.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class OoT3DOptions(PerGameCommonOptions):
    placeholder: Placeholder
    trap_chance: TrapChance

option_groups = [
    OptionGroup(
        "Gameplay Options",
        [Placeholder, TrapChance],
    ),
]

option_presets = {
    "placeholder": {
        "placeholder": True,
        "trap_chance": 50,
    },
}
