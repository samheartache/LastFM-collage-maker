from pystyle import *

from ascii_arts import LOGO, MENU
from utils import SETTINGS, get_autoname, PathType, FileType
from validate import *
import user_interact


def main():
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(LOGO)))
    print(Colorate.Vertical(Colors.red_to_white, Center.XCenter(MENU)))

    choice = input()
    while choice not in '12345':
        print('Please enter your choice correctly')
        choice = input()
    
    if choice == '1':
        auto_dir = SETTINGS['auto name image directory']
        auto_collage = SETTINGS['auto name collage file']
        dir_suffix = SETTINGS['image directory suffix']
        collage_suffix = SETTINGS['collage file suffix']
        

        if auto_dir:
            if isinstance(auto_dir, str):
                covers_dir = auto_dir
            covers_dir = get_autoname(type=PathType.DIRECTORY, suffix=dir_suffix)
        else:
            covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))
        
        if auto_collage:
            if isinstance(auto_collage, str):
                collage_path = auto_collage
            collage_path = get_autoname(type=PathType.FILE, format=FileType.JPG, suffix=collage_suffix)
        else:
            collage_path = get_valid_input('file name for the collage (.jpg, .png)', validate_imagepath)

        user_interact.albums_to_text()
        user_interact.process_imagesearching(covers_dir=covers_dir, delay=0)
        user_interact.process_collage(covers_dir=covers_dir, collage_path=collage_path)
 
    elif choice == '2':
        user_interact.albums_to_text()

    elif choice == '3':
        user_interact.process_imagesearching()

    elif choice == '4':
        user_interact.process_collage()


if __name__ == '__main__':
    while True:
        main()