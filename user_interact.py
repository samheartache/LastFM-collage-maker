from pystyle import Colorate, Colors, Center

import os

from image.images_handle import fast_search_images, make_collage, show_image
from lastfm.lastfm import LastfmAPI
from lastfm.lastfm import get_apikey

from utils.ascii_arts import LOGO, LOGO_small, MAIN_MENU
from utils.messages import NOT_API_MESSAGE
from utils.enums import BasePath, PathType, FileType
from utils.ascii_arts import settings_menu
from utils.validate import *
from utils.utils import timestamp_handle, check_for_api_key
from utils.files import mv_del_files, get_autoname, write_apikey_to_env_file

from settings.settings_edit import reset_settings, change_setting, process_setting_value
from settings.settings_data import MAIN_SETTINGS, MAIN_SETTINGS_DEFAULTS, COLLAGE_SETTINGS, COLLAGE_SETTINGS_DEFAULTS, SETTINGS_VALIDATE


def print_main_menu():
    if MAIN_SETTINGS['logo'] == 0:
        print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(LOGO_small)))
    else:
        print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(LOGO)))
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(MAIN_MENU)))


def ask_for_apikey(change=False):
    if not change:
        print(Colorate.Horizontal(Colors.red_to_white, NOT_API_MESSAGE))
    
    API_KEY = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your Lastfm API key: '))
    write_apikey_to_env_file(api_key=API_KEY)

    return API_KEY


def error_exit(error_message: str):
    print(Colorate.Horizontal(Colors.red_to_white, error_message))
    exit()


def handle_choice(choice):
    API_KEY = get_apikey()
    if not check_for_api_key(API_KEY=API_KEY):
        API_KEY = ask_for_apikey()
    
    if choice == '1':
        auto_dir = MAIN_SETTINGS['auto name image directory']
        auto_collage = MAIN_SETTINGS['auto name collage file']
        dir_suffix = MAIN_SETTINGS['image directory suffix']
        collage_suffix = MAIN_SETTINGS['collage file suffix']
        collage_size = COLLAGE_SETTINGS['collage size']

        if collage_size is None:
            collage_size = int(get_valid_input('the size of a collage (height)', validate_num))

        if auto_dir:
            if isinstance(auto_dir, str):
                covers_dir = auto_dir
            else:
                covers_dir = get_autoname(type=PathType.DIRECTORY, suffix=dir_suffix)
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))
        
        if auto_collage:
            if isinstance(auto_collage, str):
                collage_path = auto_collage
            else:
                collage_path = get_autoname(type=PathType.FILE, format=FileType.JPG, suffix=collage_suffix)
        else:
            collage_path = get_valid_input('file name for the collage', validate_path)

        albums_to_text(api_key=API_KEY)
        process_imagesearching(covers_dir=covers_dir)
        process_collage(covers_dir=covers_dir, collage_path=collage_path, collage_size=collage_size)
 
    elif choice == '2':
        albums_to_text(api_key=API_KEY)

    elif choice == '3':
        process_imagesearching()

    elif choice == '4':
        process_collage()
    
    elif choice == '5':
        settings_interact(settings=MAIN_SETTINGS, swap_smenu_caption='Change/view the collage settings')
    
    elif choice == '6':
        process_image_omit()
    
    elif choice == '7':
        ask_for_apikey(change=True)
    
    elif choice == '9':
        exit()


def albums_to_text(api_key: str):
    if MAIN_SETTINGS['username']:
        username = MAIN_SETTINGS['username']
    else:
        username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))

    if MAIN_SETTINGS['time']:
        time = timestamp_handle(time=MAIN_SETTINGS['time'])
    else:
        time = timestamp_handle(time=get_valid_input('the time from which the albums will be selected', validate_time))

    parser = LastfmAPI(username=username, API_KEY=api_key, timestamp=time)
    parser.save_to_files()
    print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {BasePath.ALBUMS.value} and songs with unknowkn album were saved to {BasePath.UNKNOWN.value}'))


def process_imagesearching(covers_dir=None, delay=1):
    queries = [album for album in open(BasePath.ALBUMS.value, encoding='utf-8')]

    if covers_dir is None:
        auto_dir = MAIN_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))

    if delay:
        s_delay = MAIN_SETTINGS['delay']
        if s_delay is not None:
            delay = s_delay
        else:
            delay = get_valid_input('delay (seconds) between image searching to avoid bot detection', validate_num)

    fast_search_images(queries=queries, covers_dir=covers_dir, delay=int(delay), timeout=MAIN_SETTINGS['timeout'])

    print(Colorate.Vertical(Colors.green_to_white, f'All album covers were saved in {covers_dir}'))


def process_collage(collage_path=None, covers_dir=None, collage_size=None):
    if collage_size is None:
        s_collage_size = COLLAGE_SETTINGS['collage size']
        if s_collage_size is None:
            collage_size = int(get_valid_input('the size of a collage (height)', validate_num))
        else:
            collage_size = s_collage_size
    
    s_margin = COLLAGE_SETTINGS['margin']
    if not str(s_margin).isdigit():
        margin = int(get_valid_input('the margin between images of the collage', validate_num))
    else:
        margin = s_margin
    
    s_scale = COLLAGE_SETTINGS['scale center']
    if s_scale is None:
        scale = process_setting_value(get_valid_input(value='your choice', enter_message='Scale images to the center to avoid image distortion? (y/n)', validation_func=validate_yn))
    else:
        scale = s_scale
    
    if collage_path is None:
        auto_collage = MAIN_SETTINGS['auto name collage file']
        if isinstance(auto_collage, str):
            collage_path = auto_collage
        elif auto_collage == True:
            collage_path = get_autoname(type=PathType.FILE, format=FileType.JPG, suffix=MAIN_SETTINGS['collage file suffix'])
        else:
            collage_path = get_valid_input('file name for the collage', validate_path)

    if covers_dir is None:
        auto_dir = MAIN_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        elif auto_dir == True:
            covers_dir = get_autoname(type=PathType.DIRECTORY, suffix=MAIN_SETTINGS['image directory suffix'])
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where your images are saved: '))

    default_collage_dir = MAIN_SETTINGS['default collage directory']
    if default_collage_dir:
            collage_path = os.path.join(default_collage_dir, collage_path)
    
    make_collage(collage_path=collage_path, images_path=covers_dir, collage_size=collage_size, margin=margin, scale=scale)
    show_image(path=collage_path)

    print(Colorate.Vertical(Colors.green_to_white, f'Your collage is done and saved as "{collage_path}"'))

    numerate = COLLAGE_SETTINGS['create numerate collage']
    if numerate:
        make_collage(collage_path=f'num - {collage_path}', images_path=covers_dir, collage_size=collage_size, margin=margin, scale=scale, numerate=True)
        show_image(path=collage_path)

        print(Colorate.Vertical(Colors.green_to_white, f'Collage with numerate images is done and saved as "num - {collage_path}"'))
    
    change_choice = COLLAGE_SETTINGS['ask about changing the collage']
    if change_choice:
        choice = process_setting_value(get_valid_input(value='your choice', enter_message='Do you want to change your collage by deleting certain images by their index? (y/n)',\
                                                        validation_func=validate_yn))
        if choice:
            process_image_omit(images_path=covers_dir)
        return


def settings_interact(settings: dict, swap_smenu_caption: str, first_page: bool=True):
    SETTINGS_MENU = settings_menu(settings=settings, swap_smenu_caption=swap_smenu_caption)
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(SETTINGS_MENU)))
    choice = input()
    possible_choices = [str(i) for i in range(1, len(settings) + 4)]
    while choice not in possible_choices:
        print(Colorate.Vertical(Colors.red_to_white, 'Please enter your choice correctly'))
        choice = input()

    if choice == possible_choices[-1]:
        return
    elif choice == possible_choices[-2]:
        if first_page:
            reset_settings(defaults=MAIN_SETTINGS_DEFAULTS)
            settings_interact(settings=MAIN_SETTINGS, swap_smenu_caption=swap_smenu_caption)
            return
        else:
            reset_settings(defaults=COLLAGE_SETTINGS_DEFAULTS, is_collage_settings=True)
            settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption=swap_smenu_caption, first_page=False)
            return
    elif choice == possible_choices[-3]:
        if first_page:
            settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption='Go back to the base settings', first_page=False)
            return
        else:
            settings_interact(settings=MAIN_SETTINGS, swap_smenu_caption='Change/view the collage settings')
            return
    
    setting = list(settings.keys())[int(choice) - 1]
    value = process_setting_value(value=get_valid_input(f'new value for the "{setting}" setting', SETTINGS_VALIDATE.get(setting, lambda x: True)))
    change_setting(setting=setting, value=value, is_collage_setting=bool(not first_page))
    
    print(Colorate.Vertical(Colors.green_to_white, f'The "{setting.capitalize()}" setting was changed successfully.'))

    if first_page:
        settings_interact(settings=MAIN_SETTINGS, swap_smenu_caption=swap_smenu_caption)
    else:
        settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption=swap_smenu_caption, first_page=False)


def process_image_omit(images_path=None):
    delete_files = MAIN_SETTINGS['delete omitted images']

    if not images_path:
        auto_dir = MAIN_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            images_path = auto_dir
        else:
            images_path = get_valid_input('the name of the directory where your collage images are stored', lambda x: True)

    delete_inds = get_valid_input('the index numbers of images you want to delete from a collage (eg - 1 2 10)', validate_delete_inds)
    if delete_files:
        mv_del_files(inds=delete_inds, files_path=images_path, delete_files=True)
    else:
        mv_del_files(inds=delete_inds, files_path=images_path, mv_dir=MAIN_SETTINGS['directory for the omitted images'])
    
    process_collage(covers_dir=images_path)