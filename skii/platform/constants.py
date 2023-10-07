latitude_config = {
    "left_digits": 3,
    "right_digits": 4,
    "positive": False,
    "min_value": -90,
    "max_value": 90,
}
longitude_config = latitude_config.copy()
longitude_config.update(
    {
        "min_value": -180,
        "max_value": 180,
    }
)
