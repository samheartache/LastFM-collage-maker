from pystyle import *


def get_valid_input(value, validation_func, enter_message=None):
    while True:
        if enter_message is not None:
            user_input = input(Colorate.Horizontal(Colors.cyan_to_green, enter_message))
        else:
            user_input = input(Colorate.Horizontal(Colors.cyan_to_green, f'Enter {value}: '))
        if validation_func(user_input):
            return user_input
        print(Colorate.Vertical(Colors.red_to_white, f'Please enter {value} correctly'))


def validate_imagepath(path:str):
    return (path.strip().endswith('.jpg') or path.strip().endswith('.png'))


def validate_num(num: str):
    return num.isdigit()


def validate_time(time: str):
    return (time.lower() in ('week', 'month') or time.isdigit())


def validate_bool(value):
    if isinstance(value, str):
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
    return isinstance(value, bool)