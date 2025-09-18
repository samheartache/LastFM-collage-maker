from pystyle import *


def get_valid_input(value, validation_func):
    while True:
        user_input = input(Colorate.Horizontal(Colors.cyan_to_green, f'Enter {value}: '))
        if validation_func(user_input):
            return user_input
        print(Colorate.Vertical(Colors.red_to_white, f'Please enter {value} correctly'))


def validate_imagepath(path:str):
    return (path.strip().endswith('.jpg') or path.strip().endswith('.png'))


def validate_num(num: str):
    if num.isdigit():
        if 1 <= int(num) <= 100:
            return True
    return False

def validate_time(time: str):
    return (time.lower() in ('week', 'month') or time.isdigit())