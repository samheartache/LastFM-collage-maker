from user_interact import print_main_menu, handle_choice


def main():
    print_main_menu()

    choice = input()
    handle_choice(choice=choice)


if __name__ == '__main__':
    while True:
        main()