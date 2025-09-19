from pystyle import *

from images_handle import fast_search_images, make_collage
from lastfm import LastfmAPI
from utils import timestamp_handle, BasePath, SETTINGS, change_setting
from validate import *


def albums_to_text():
    if SETTINGS['username']:
        username = SETTINGS['username']
    else:
        username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))
        change_setting(setting='username', value=username)

    if SETTINGS['time']:
        time = timestamp_handle(time=SETTINGS['time'])
    else:
        time = timestamp_handle(time=get_valid_input('the time from which the albums will be selected', validate_time))

    parser = LastfmAPI(username=username, timestamp=time)
    parser.save_to_files()
    print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {BasePath.ALBUMS.value} and songs with unknowkn album were saved to {BasePath.UNKNOWN.value}'))


def process_imagesearching(covers_dir=None, delay=1):
    queries = [album for album in open(BasePath.ALBUMS.value, encoding='utf-8')]

    if covers_dir is None:
        auto_dir = SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))

    if delay:
        s_delay = SETTINGS['delay']
        if s_delay:
            delay = s_delay
        else:
            delay = get_valid_input('delay (seconds) between image searching to avoid bot detection', validate_num)

    fast_search_images(queries=queries, covers_dir=covers_dir, delay=int(delay))

    print(Colorate.Vertical(Colors.green_to_white, f'All album covers were saved in {covers_dir}'))


def process_collage(collage_path=None, covers_dir=None):
    s_collage_size = SETTINGS['collage size']
    if not s_collage_size:
        collage_size = get_valid_input('the size of a collage (height)', validate_num)
    else:
        collage_size = SETTINGS['collage size']
    
    if collage_path is None:
        auto_collage = SETTINGS['auto name collage file']
        if isinstance(auto_collage, str):
            collage_path = auto_collage
        else:
            collage_path = get_valid_input('file name for the collage (.jpg, .png)', validate_imagepath)
    if covers_dir is None:
        auto_dir = SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where your images are saved: '))
            
    make_collage(collage_path=collage_path, images_path=covers_dir, collage_size=collage_size)

    print(Colorate.Vertical(Colors.green_to_white, f'Your collage is done and saved as {collage_path}'))