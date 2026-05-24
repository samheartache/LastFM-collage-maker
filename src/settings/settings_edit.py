import json

from settings.settings_data import MAIN_SETTINGS, COLLAGE_SETTINGS, MAIN_SETTINGS_PATH, COLLAGE_SETTINGS_PATH


def change_setting(setting, value, is_collage_setting=False):
    if not is_collage_setting:
        with open(MAIN_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
            MAIN_SETTINGS[setting] = value
            json.dump(MAIN_SETTINGS, json_file, indent=4)
    else:
        with open(COLLAGE_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
            COLLAGE_SETTINGS[setting] = value
            json.dump(COLLAGE_SETTINGS, json_file, indent=4)
 

def process_setting_value(value: str):
    if value.lower() == 'true' or value.lower() == 'y':
        value = True
    elif value.lower() == 'false' or value.lower() == 'n':
        value = False
    elif value.isdigit():
        value = int(value)
    return value


def reset_settings(defaults: dict, is_collage_settings: bool=False) -> None:
    if not is_collage_settings:
        with open(MAIN_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
            for key, value in defaults.items():
                MAIN_SETTINGS[key] = value
            json.dump(MAIN_SETTINGS, json_file, indent=4)
    else:
        with open(COLLAGE_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
            for key, value in defaults.items():
                COLLAGE_SETTINGS[key] = value
            json.dump(COLLAGE_SETTINGS, json_file, indent=4)