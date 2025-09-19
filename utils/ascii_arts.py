LOGO = '''
LLLLLLLLLLL                                                        tttt               FFFFFFFFFFFFFFFFFFFFFFMMMMMMMM               MMMMMMMM
L:::::::::L                                                     ttt:::t               F::::::::::::::::::::FM:::::::M             M:::::::M
L:::::::::L                                                     t:::::t               F::::::::::::::::::::FM::::::::M           M::::::::M
LL:::::::LL                                                     t:::::t               FF::::::FFFFFFFFF::::FM:::::::::M         M:::::::::M
  L:::::L                 aaaaaaaaaaaaa      ssssssssss   ttttttt:::::ttttttt           F:::::F       FFFFFFM::::::::::M       M::::::::::M
  L:::::L                 a::::::::::::a   ss::::::::::s  t:::::::::::::::::t           F:::::F             M:::::::::::M     M:::::::::::M
  L:::::L                 aaaaaaaaa:::::ass:::::::::::::s t:::::::::::::::::t           F::::::FFFFFFFFFF   M:::::::M::::M   M::::M:::::::M
  L:::::L                          a::::as::::::ssss:::::stttttt:::::::tttttt           F:::::::::::::::F   M::::::M M::::M M::::M M::::::M
  L:::::L                   aaaaaaa:::::a s:::::s  ssssss       t:::::t                 F:::::::::::::::F   M::::::M  M::::M::::M  M::::::M
  L:::::L                 aa::::::::::::a   s::::::s            t:::::t                 F::::::FFFFFFFFFF   M::::::M   M:::::::M   M::::::M
  L:::::L                a::::aaaa::::::a      s::::::s         t:::::t                 F:::::F             M::::::M    M:::::M    M::::::M
  L:::::L         LLLLLLa::::a    a:::::assssss   s:::::s       t:::::t    tttttt       F:::::F             M::::::M     MMMMM     M::::::M
LL:::::::LLLLLLLLL:::::La::::a    a:::::as:::::ssss::::::s      t::::::tttt:::::t     FF:::::::FF           M::::::M               M::::::M
L::::::::::::::::::::::La:::::aaaa::::::as::::::::::::::s       tt::::::::::::::t     F::::::::FF           M::::::M               M::::::M
L::::::::::::::::::::::L a::::::::::aa:::as:::::::::::ss          tt:::::::::::tt     F::::::::FF           M::::::M               M::::::M
LLLLLLLLLLLLLLLLLLLLLLLL  aaaaaaaaaa  aaaa sssssssssss              ttttttttttt       FFFFFFFFFFF           MMMMMMMM               MMMMMMMM                                      
'''

MAIN_MENU = '''
┌───────────────────────────────────────────────────────────────────────────────────────────────┐  
│                   [1] Make a collage of album covers                                          │
│                   [2] Parse your albums to text file                                          │  
│                   [3] Download album covers (text file with titles is needed)                 │  
│                   [4] Make a collage of already downloaded images                             │
│                   [5] Change/view default settings                                            │                                       
│                   [6] Guidance on the use                                                     │
│                   [7] Stop the software                                                       │                                                   
└───────────────────────────────────────────────────────────────────────────────────────────────┘  
'''


def settings_menu(settings: dict) -> str:
    upper_row = '┌───────────────────────────────────────────────────────────────────────────────────────────────┐'
    lower_row = '└───────────────────────────────────────────────────────────────────────────────────────────────┘'
    left_padding = 30
    left_margin = 39
    menu = f'{' ' * left_margin}{upper_row}\n'
    for ind, (setting, value) in enumerate(settings.items(), start=1):
        row_content = f'[{ind}] {setting.capitalize()} - {value}'
        row = f'{' ' * left_margin}│{' ' * left_padding}{row_content}{' ' * (len(upper_row) - len(row_content) - left_padding - 2)}│\n'
        menu += row
        last = ind
    menu += f'{' ' * left_margin}│{' ' * left_padding}[{last + 1}] Set settings to default{' ' * (len(upper_row) - len(row_content) - left_padding - 6)}│\n'
    menu += f'{' ' * left_margin}│{' ' * left_padding}[{last + 2}] Go back to menu{' ' * (len(upper_row) - len(row_content) - left_padding + 1)}│\n'
    menu += f'{' ' * left_margin}{lower_row}'
    return menu