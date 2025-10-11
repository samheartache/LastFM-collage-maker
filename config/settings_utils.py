from utils.validate import *

SETTINGS_VALIDATE = {
    'time': validate_time,
    'delay': validate_num,
    'collage size': validate_num,
    'image directory suffix': lambda x: not validate_bool(x) and validate_path(x),
    'collage file suffix': lambda x: not validate_bool(x) and validate_path(x),
    'delete omitted images': validate_bool,
    'auto name image directory': validate_path,
    'auto name collage file': validate_path,
    'timeout': validate_num,
    'default collage directory': validate_path,
    'delete omitted images': validate_bool,
    'directory for the omitted images': validate_path,
    'logo': validate_bool
}

BASE_SETTINGS_DEFAULTS = {
    "username": None,
    "time": None,
    "delay": 2,
    "timeout": 3,
    "auto name image directory": False,
    "image directory suffix": None,
    "auto name collage file": False,
    "collage file suffix": None,
    "default collage directory": "Collages",
    "delete omitted images": False,
    "directory for the omitted images": "Omitted",
    "logo": 0
}

COLLAGE_SETTINGS_DEFAULTS = {
    "collage size": 1200,
    "margin": 0,
    "create numerate collage": False,
    "scale center": True,
    "ask about changing the collage": False
}