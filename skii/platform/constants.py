import copy
LATITUDE_RANGE_CONFIG = {
    "left_digits": 3,
    "right_digits": 4,
    "positive": False,
    "min_value": -90,
    "max_value": 90,
}
LONGITUDE_RANGE_CONFIG = copy.deepcopy(LATITUDE_RANGE_CONFIG)
LONGITUDE_RANGE_CONFIG.update(
    {
        "min_value": -180,
        "max_value": 180,
    }
)
