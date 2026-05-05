ROLE_MAP = {
    "finance": ["finance"],
    "marketing": ["marketing"],
    "hr": ["hr"],
    "engineering": ["engineering"],
    "c_level": ["finance", "marketing", "hr", "engineering"],
    "employee": ["general"]
}

ROLE_HIERARCHY = {
    "employee": 1,
    "finance": 2,
    "marketing": 2,
    "hr": 2,
    "engineering": 2,
    "c_level": 3
}