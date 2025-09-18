import os
import sys
import difflib
from datetime import datetime, timedelta
from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class BasePath(Enum):
    ALBUMS = 'albums.txt'
    UNKNOWN = 'unknown.txt'


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
    if time.isdigit():
        return int((datetime.now() - timedelta(days=int(time))).timestamp())
    elif time.lower() in ('week', 'month'):
        if time == 'week':
            return int((datetime.now() - timedelta(weeks=1)).timestamp())
        else:
            return int((datetime.now() - timedelta(weeks=4)).timestamp())