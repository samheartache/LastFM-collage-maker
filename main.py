from pystyle import *

from ascii_arts import LOGO, MENU
from lastfm import LastFM
from images_handle import make_collage, search_images
from validate import *


def main():
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(LOGO)))
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(MENU)))

    choice = input()
    while choice not in '1234':
        print('Please enter your choice correctly')
        choice = input()
    
    if choice == '1':
        username = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM username: '))
        password = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter your LastFM password: '))
        album_save_path = get_valid_input('album save path (.txt)', validate_textpath)
        songs_save_path = get_valid_input('songs save path (.txt)', validate_textpath)
        num_pages = get_valid_input('num pages', validate_num)

        parser = LastFM(username=username, password=password, num_pages=num_pages, album_save_path=album_save_path, songs_save_path=songs_save_path)
        parser.authorize()
        parser.save_results()

        print(Colorate.Vertical(Colors.green_to_white, f'All data on your albums was saved to {album_save_path} and songs with unknowkn album were saved to {songs_save_path}'))

    elif choice == '2':
        queries = [album for album in open(get_valid_input('file path where your albums names are saved', validate_textpath), encoding='utf-8')]
        covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where album covers will be saved: '))
        delay = get_valid_input('delay betweem image searching to avoid bot detection', validate_num)
        search_images(queries=queries, covers_dir=covers_dir, delay=int(delay))

        print(Colorate.Vertical(Colors.green_to_white, f'All album covers were saved in {covers_dir}'))

    elif choice == '3':
        collage_path = get_valid_input('file name for collage', validate_imagepath)
        covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name where your images are saved: '))
        make_collage(collage_path=collage_path, images_path=covers_dir)

        print(Colorate.Vertical(Colors.green_to_white, f'Your collage is done and saved as {collage_path}'))


if __name__ == '__main__':
    while True:
        main()