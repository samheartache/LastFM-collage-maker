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

LOGO_small = '''
      :::            :::      :::::::: :::::::::::
     :+:          :+: :+:   :+:    :+:    :+:     
    +:+         +:+   +:+  +:+           +:+      
   +#+        +#++:++#++: +#++:++#++    +#+       
  +#+        +#+     +#+        +#+    +#+        
 #+#        #+#     #+# #+#    #+#    #+#         
########## ###     ###  ########     ###          
      :::::::::: :::   :::                        
     :+:       :+:+: :+:+:                        
    +:+      +:+ +:+:+ +:+                        
   :#::+::# +#+  +:+  +#+                         
  +#+      +#+       +#+                          
 #+#      #+#       #+#                           
###      ###       ###                            
'''

MAIN_MENU = '''
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                   [1] Make a collage of album covers                                          │
│                   [2] Parse your albums to text file                                          │
│                   [3] Download album covers (text file with titles is needed)                 │
│                   [4] Make a collage of already downloaded images                             │
│                   [5] Change/view default settings                                            │
│                   [6] Delete images from a collage by the index number                        │
│                   [7] Guidance on the use                                                     │
│                   [8] Stop the software                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
'''


def settings_menu(settings: dict, swap_smenu_caption: str) -> str:
    upper_row = '┌───────────────────────────────────────────────────────────────────────────────────────────────┐'
    lower_row = '└───────────────────────────────────────────────────────────────────────────────────────────────┘'
    left_padding = 19
    menu = f'{upper_row}\n'

    for ind, (setting, value) in enumerate(settings.items(), start=1):
        row_content = f'[{ind}] {setting.capitalize()} - {value}'
        row = f'│{' ' * left_padding}{row_content}{' ' * (len(upper_row) - len(row_content) - left_padding - 2)}│\n'
        menu += row
        last = ind
    
    another_settings_caption = f'[{last + 1}] {swap_smenu_caption}'
    default_settings_caption = f'[{last + 2}] Set settings to default'
    back_to_menu_caption = f'[{last + 3}] Go back to menu'

    menu += f'│{' ' * left_padding}{another_settings_caption}{' ' * (len(upper_row) - len(another_settings_caption) - left_padding - 2)}│\n'
    menu += f'│{' ' * left_padding}{default_settings_caption}{' ' * (len(upper_row) - len(default_settings_caption) - left_padding - 2)}│\n'
    menu += f'│{' ' * left_padding}{back_to_menu_caption}{' ' * (len(upper_row) - len(back_to_menu_caption) - left_padding - 2)}│\n'
    menu += f'{lower_row}'
    return menu