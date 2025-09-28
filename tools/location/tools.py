import tools.location.utils as location_utils

def get_current_location() -> dict:
    """
    Get your current location (latitude, longitude, address).
    Use this when location context is needed to provide accurate information.
    Returns:
        dict: Your current location (latitude, longitude, address).
    """
    return location_utils.get_current_location()

def call_function(name: str, args: dict):
    if name == "get_current_location":
        return get_current_location(**args)
    raise ValueError(f"Function 'location.{name}' not found")