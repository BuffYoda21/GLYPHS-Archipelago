from .glyphs.Locations import get_location_names as glyphs_get_location_names
from .apquest.locations import LOCATION_NAME_TO_ID as APQUEST_LOCATION_NAME_TO_ID

def build_location_name_to_id() -> dict[str, int]:
    location_name_to_id = {}
    location_name_to_id.update(glyphs_get_location_names())
    location_name_to_id.update(APQUEST_LOCATION_NAME_TO_ID)
    return location_name_to_id