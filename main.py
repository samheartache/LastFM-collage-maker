from pystyle import *

from ascii_arts import LOGO, MENU
from lastfm import LastFM
from images_handle import make_collage, search_images


def main():
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(LOGO)))
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(MENU)))

    choice = input()
    while choice not in '1234':
        print('Please enter your choice correctly')
        choice = input()
    
    if choice == '1':
        username = get_valid_input('LastFM username')
        password = get_valid_input('LastFM password')
        album_save_path = get_valid_input('album save path (.txt)', validate_textpath)
        songs_save_path = get_valid_input('songs save path (.txt)', validate_textpath)
        num_pages = get_valid_input('num pages', validate_num)

        parser = LastFM(username=username, password=password, num_pages=num_pages, album_save_path=album_save_path, songs_save_path=songs_save_path)
        parser.authorize()
        parser.save_results()

    elif choice == '2':
        queries = [album for album in open(get_valid_input('file path where your albums names are saved', validate_textpath), encoding='utf-8')]
        covers_dir = input('Enter directory name where album covers will be saved: ')
        delay = get_valid_input('delay betweem image searching to avoid bot detection', validate_num)
        search_images(queries=queries, covers_dir=covers_dir, delay=int(delay))
        print(f'All album covers were saved in {covers_dir}')

    elif choice == '3':
        collage_path = get_valid_input('file name for collage', validate_imagepath)
        covers_dir = input('Enter directory name where your images are saved: ')
        make_collage(collage_path=collage_path, covers_dir=covers_dir)


def get_valid_input(value, validation_func):
    while True:
        user_input = input(f'Enter {value}: ')
        if validation_func(value):
            return user_input
        print(f'Please enter {value} correctly ')


def validate_textpath(path: str):
    if path.strip().endswith('.txt'):
        return True
    return False

def validate_imagepath(path:str):
    if path.strip().endswith('.jpg') or path.strip().endswith('.png'):
        print('fjhs')
        return True
    return False


def validate_num(num: str):
    if num.isdigit():
        if 1 < int(num) < 100:
            return True
    return False


if __name__ == '__main__':
    while True:
        main()