from pystyle import *

from image.images_handle import fast_search_images, make_collage
from lastfm import LastfmAPI
from utils.ascii_arts import settings_menu
from utils.validate import *
from utils.utils import *


def albums_to_text():
    if BASE_SETTINGS['username']:
        username = BASE_SETTINGS['username']
    else:
        username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))

    if BASE_SETTINGS['time']:
        time = timestamp_handle(time=BASE_SETTINGS['time'])
    else:
        time = timestamp_handle(time=get_valid_input('the time from which the albums will be selected', validate_time))

    parser = LastfmAPI(username=username, timestamp=time)
    parser.save_to_files()
    print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {BasePath.ALBUMS.value} and songs with unknowkn album were saved to {BasePath.UNKNOWN.value}'))


def process_imagesearching(covers_dir=None, delay=1):
    queries = [album for album in open(BasePath.ALBUMS.value, encoding='utf-8')]

    if covers_dir is None:
        auto_dir = BASE_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))

    if delay:
        s_delay = BASE_SETTINGS['delay']
        if s_delay:
            delay = s_delay
        else:
            delay = get_valid_input('delay (seconds) between image searching to avoid bot detection', validate_num)

    fast_search_images(queries=queries, covers_dir=covers_dir, delay=int(delay))

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
        auto_collage = BASE_SETTINGS['auto name collage file']
        if isinstance(auto_collage, str):
            collage_path = auto_collage
        elif auto_collage == True:
            collage_path = get_autoname(type=PathType.FILE, format=FileType.JPG, suffix=BASE_SETTINGS['collage file suffix'])
        else:
            collage_path = get_valid_input('file name for the collage (.jpg, .png)', validate_imagepath)

    if covers_dir is None:
        auto_dir = BASE_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            covers_dir = auto_dir
        elif auto_dir == True:
            covers_dir = get_autoname(type=PathType.DIRECTORY, suffix=BASE_SETTINGS['image directory suffix'])
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where your images are saved: '))

    make_collage(collage_path=collage_path, images_path=covers_dir, collage_size=collage_size, margin=margin, scale=scale)
    print(Colorate.Vertical(Colors.green_to_white, f'Your collage is done and saved as "{collage_path}"'))

    numerate = COLLAGE_SETTINGS['create numerate collage']
    if numerate:
        make_collage(collage_path=f'num - {collage_path}', images_path=covers_dir, collage_size=collage_size, margin=margin, scale=scale, numerate=True)
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
            reset_settings(defaults=base_settings_defaults)
            settings_interact(settings=BASE_SETTINGS, swap_smenu_caption=swap_smenu_caption)
            return
        else:
            reset_settings(defaults=collage_settings_defaults, is_collage_settings=True)
            settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption=swap_smenu_caption, first_page=False)
            return
    elif choice == possible_choices[-3]:
        if first_page:
            settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption='Go back to the base settings', first_page=False)
            return
        else:
            settings_interact(settings=BASE_SETTINGS, swap_smenu_caption='Change/view the collage settings')
            return
    
    setting = list(settings.keys())[int(choice) - 1]
    value = process_setting_value(value=get_valid_input(f'new value for the "{setting}" setting', settings_validate.get(setting, lambda x: True)))
    change_setting(setting=setting, value=value, is_collage_setting=bool(not first_page))
    
    print(Colorate.Vertical(Colors.green_to_white, f'The "{setting.capitalize()}" setting was changed successfully.'))

    if first_page:
        settings_interact(settings=BASE_SETTINGS, swap_smenu_caption=swap_smenu_caption)
    else:
        settings_interact(settings=COLLAGE_SETTINGS, swap_smenu_caption=swap_smenu_caption, first_page=False)


def process_image_omit(images_path=None):
    delete_files = BASE_SETTINGS['delete omitted images']

    if not images_path:
        auto_dir = BASE_SETTINGS['auto name image directory']
        if isinstance(auto_dir, str):
            images_path = auto_dir
        else:
            images_path = get_valid_input('the name of the directory where your collage images are stored', lambda x: True)

    delete_inds = get_valid_input('the index numbers of images you want to delete from a collage (eg - 1 2 10)', validate_delete_inds)
    if delete_files:
        mv_del_files(inds=delete_inds, files_path=images_path, delete_files=True)
    else:
        mv_del_files(inds=delete_inds, files_path=images_path, mv_dir=BASE_SETTINGS['directory for the omitted images'])
    
    process_collage(covers_dir=images_path)