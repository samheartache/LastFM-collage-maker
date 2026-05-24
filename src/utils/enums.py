from enum import Enum, auto


class BasePath(Enum):
    ALBUMS = 'albums.txt'
    UNKNOWN = 'unknown.txt'
    

class PathType(Enum):
    DIRECTORY = auto()
    FILE = auto()


class FileType(Enum):
    JPG = '.jpg'
    PNG = '.png'