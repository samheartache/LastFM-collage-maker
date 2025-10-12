from user_interact import print_main_menu, handle_choice
from utils.validate import get_valid_input, validate_menuchoice


def main():
    print_main_menu()

    choice = get_valid_input(value='your choice', validation_func=validate_menuchoice)
    handle_choice(choice=choice)


if __name__ == '__main__':
    while True:
        main()