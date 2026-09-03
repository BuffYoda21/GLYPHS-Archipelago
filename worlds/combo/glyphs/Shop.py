from typing import TYPE_CHECKING
from .Options import GlyphsOptions

options: GlyphsOptions

if TYPE_CHECKING:
    from . import GlyphsWorld

def get_shop_prices(world: "GlyphsWorld") -> list[int]:
    if not hasattr(world, "shop_prices"):
        if world.options.RandomShopPrices.value:
            divisions = sorted(world.random.sample(range(1, 10), 3))
            divisions = [0] + divisions + [10]
            world.shop_prices = [divisions[i+1] - divisions[i] for i in range(4)]
        else:
            world.shop_prices = [2, 4, 2, 2]
    
    return world.shop_prices