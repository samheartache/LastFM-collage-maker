def get_valid_input(value, validation_func):
    while True:
        user_input = input(f'Enter {value}: ')
        if validation_func(user_input):
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
        if 1 <= int(num) <= 100:
            return True
    return False