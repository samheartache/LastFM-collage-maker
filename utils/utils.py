import os
import shutil
import sys
import difflib
import json
from datetime import datetime, timedelta
from enum import Enum, auto

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from utils.validate import *

with open('base_settings.json', encoding='utf-8') as json_file:
    BASE_SETTINGS = json.load(json_file)

with open('collage_settings.json', encoding='utf-8') as json_file:
    COLLAGE_SETTINGS = json.load(json_file)


class BasePath(Enum):
    ALBUMS = 'albums.txt'
    UNKNOWN = 'unknown.txt'
    

class PathType(Enum):
    DIRECTORY = auto()
    FILE = auto()


class FileType(Enum):
    JPG = '.jpg'
    PNG = '.png'


settings_validate = {
    'time': validate_time,
    'delay': validate_num,
    'collage size': validate_num,
    'image directory suffix': lambda x: not validate_bool(x),
    'collage file suffix': lambda x: not validate_bool(x),
    'delete omitted images': validate_bool,
}

base_settings_defaults = {
    "username": None,
    "time": None,
    "delay": 2,
    "auto name image directory": False,
    "image directory suffix": None,
    "auto name collage file": False,
    "collage file suffix": None
}

collage_settings_defaults = {
    "collage size": 1200,
    "margin": 0,
    "create numerate collage": False,
    "scale center": True,
    "ask about changing the collage": False
}


def initialize_driver(is_headless=True, logs=False):
    chrome_options = Options()
    
    if is_headless:
        chrome_options.add_argument('--headless=new')
    
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if not logs:
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--silent')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-path=' + os.devnull)
        chrome_options.add_argument('--disable-features=VoiceTranscription,OptimizationHints')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-background-networking')
        
        service = Service(
            executable_path=ChromeDriverManager().install(),
            service_args=['--verbose=0', '--log-path=' + os.devnull],
        )
        
        if os.name == 'nt':
            service.creation_flags = 0x08000000 
        
        with open(os.devnull, 'w') as f:
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = f
            sys.stderr = f
            try:
                driver = webdriver.Chrome(service=service, options=chrome_options)
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def remove_similar_strings(strings, threshold=0.85):
    result = []
    for s in strings:
        if not any(difflib.SequenceMatcher(None, s, r).ratio() > threshold for r in result):
            result.append(s)
    return result


def timestamp_handle(time):
    time = str(time)
    if time.isdigit():
        return int((datetime.now() - timedelta(days=int(time))).timestamp())
    elif time.lower() in ('week', 'month'):
        if time == 'week':
            return int((datetime.now() - timedelta(weeks=1)).timestamp())
        else:
            return int((datetime.now() - timedelta(weeks=4)).timestamp())


def change_setting(setting, value, is_collage_setting=False):
    if not is_collage_setting:
        with open('base_settings.json', 'w', encoding='utf-8') as json_file:
            BASE_SETTINGS[setting] = value
            json.dump(BASE_SETTINGS, json_file, indent=4)
    else:
        with open('collage_settings.json', 'w', encoding='utf-8') as json_file:
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


def get_autoname(type: PathType, format: FileType = None, suffix: str = '') -> str:
    name = f'{datetime.now().strftime("%d.%m.%Y %H:%M")}'.replace(':', ' ')
    if suffix:
        name += f' - {suffix}'
    if type == PathType.DIRECTORY:
        return name
    elif type == PathType.FILE:
        return f'{name}{format.value}'


def reset_settings(defaults: dict, is_collage_settings: bool=False) -> None:
    if not is_collage_settings:
        with open('base_settings.json', 'w', encoding='utf-8') as json_file:
            for key, value in defaults.items():
                BASE_SETTINGS[key] = value
            json.dump(BASE_SETTINGS, json_file, indent=4)
    else:
        with open('collage_settings.json', 'w', encoding='utf-8') as json_file:
            for key, value in defaults.items():
                COLLAGE_SETTINGS[key] = value
            json.dump(COLLAGE_SETTINGS, json_file, indent=4)


def mv_del_files(inds: str, files_path: str, delete_files: bool=False, mv_dir: str | None=None) -> None:
    inds_lst = list(map(int, inds.split()))
    omit_files = set()

    for ind, file in enumerate(os.listdir(files_path), start=1):
        file_path = os.path.join(files_path, file)
        if ind in inds_lst:
            omit_files.add(file_path)
    
    if delete_files:
        for file in omit_files:
            os.remove(file)
    else:
        os.makedirs(mv_dir, exist_ok=True)

        for file in omit_files:
            filename = os.path.basename(file)
            mv = os.path.join(mv_dir, filename)
            shutil.move(file, mv)