def to_generic_readable_region_name(region_name: str) -> str:
    if region_name.startswith("Region"):
        return region_name[:-1]
    if region_name.startswith("Dark Region"):
        return "Dark Region"
    return region_name