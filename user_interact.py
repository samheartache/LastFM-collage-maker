from pystyle import *

from images_handle import fast_search_images, make_collage
from lastfm import LastfmAPI
from validate import *


def albums_to_text(album_save_path=None, unknown_save_path=None):
    username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))
    if album_save_path is None:
        album_save_path = get_valid_input('path where the album titles will be saved', lambda x: not validate_num(x))
    if unknown_save_path is None:
        unknown_save_path = get_valid_input('path where the song titles from unknown albums will be saved', lambda x: not validate_num(x))

    parser = LastfmAPI(username=username, album_path=album_save_path, unknown_path=unknown_save_path)
    parser.save_to_files()
    print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {album_save_path} and songs with unknowkn album were saved to {unknown_save_path}'))


def process_imagesearching(covers_dir=None, album_save_path=None, delay=1):
    if album_save_path is None:
        queries = [album for album in open(get_valid_input('file path where your albums names are saved', lambda x: not validate_num(x)), encoding='utf-8')]
    else:
        queries = [album for album in open(album_save_path, encoding='utf-8')]
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