from pystyle import Colorate, Colors

import os
import shutil
from datetime import datetime

from utils.enums import PathType, FileType


def get_autoname(type: PathType, format: FileType = None, suffix: str = '') -> str:
    name = f'{datetime.now().strftime("%d.%m.%Y %H:%M")}'.replace(':', ' ')
    if suffix:
        name += f' - {suffix}'
    if type == PathType.DIRECTORY:
        return name
    elif type == PathType.FILE:
        return f'{name}{format.value}'


def mv_del_files(inds: str, files_path: str, delete_files: bool=False, mv_dir: str | None=None) -> None:
    inds_lst = list(map(int, inds.split()))
    omit_files = set()

    for ind, file in enumerate(os.listdir(files_path), start=1):
        file_path = os.path.join(files_path, file)
        if ind in inds_lst:
            omit_files.add(file_path)
    
    if delete_files:
        for file in omit_files:
            os.remove(file)
    else:
        os.makedirs(mv_dir, exist_ok=True)

        for file in omit_files:
            filename = os.path.basename(file)
            mv = os.path.join(mv_dir, filename)
            shutil.move(file, mv)

            print(Colorate.Vertical(Colors.red_to_white, file))


def make_path_valid(path: str):
    forbidden_symbs = '<>:"/\|?*'
    for s in forbidden_symbs:
        path = path.replace(s, '')
    return path