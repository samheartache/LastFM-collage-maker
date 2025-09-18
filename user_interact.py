from pystyle import *

from images_handle import fast_search_images, make_collage
from lastfm import LastfmAPI
from utils import timestamp_handle, BasePath
from validate import *


def albums_to_text():
    username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))
    time = timestamp_handle(time=get_valid_input('the time from which the albums will be selected', validate_time))

    parser = LastfmAPI(username=username, timestamp=time)
    parser.save_to_files()
    print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {BasePath.ALBUMS.value} and songs with unknowkn album were saved to {BasePath.UNKNOWN.value}'))


def process_imagesearching(covers_dir=None, delay=1):
    queries = [album for album in open(BasePath.ALBUMS.value, encoding='utf-8')]
    if covers_dir is None:
        covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))
    if delay:
        delay = get_valid_input('delay (seconds) between image searching to avoid bot detection', validate_num)
    fast_search_images(queries=queries, covers_dir=covers_dir, delay=int(delay))

    print(Colorate.Vertical(Colors.green_to_white, f'All album covers were saved in {covers_dir}'))


def process_collage(collage_path=None, covers_dir=None):
    if collage_path is None:
        collage_path = get_valid_input('file name for the collage (.jpg, .png)', validate_imagepath)
    if covers_dir is None:
        covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where your images are saved: '))
    make_collage(collage_path=collage_path, images_path=covers_dir)

    print(Colorate.Vertical(Colors.green_to_white, f'Your collage is done and saved as {collage_path}'))