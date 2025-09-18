from pystyle import *

from ascii_arts import LOGO, MENU
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
        covers_dir = input(Colorate.Horizontal(Colors.cyan_to_green, 'Enter directory name for saving images of album covers: '))
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