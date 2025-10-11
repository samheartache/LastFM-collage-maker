import os

import dotenv
import requests
from bs4 import BeautifulSoup

from utils.enums import BasePath

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')


class LastfmAPI:
    def __init__(self, username: str, timestamp=None, limit=1000):
        self.username = username
        self.timestamp = timestamp
        self.limit = limit
        self.not_found = set()
        self.albums = self.get_user_albums()
    
    def get_user_albums(self) -> list:
        url = f'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={self.username}&api_key={API_KEY}&format=json'
        result_albums = []
        track_titles = set()
        album_titles = set()

        if self.timestamp:
            url += f'&from={self.timestamp}'
        if self.limit:
            url += f'&limit={self.limit}'
        
        response = requests.get(url=url)
        response_json = response.json()
        recent_tracks = response_json['recenttracks']['track']

        for track in recent_tracks:
            info = {}

            info['track'] = track['name']
            info['artist'] = track['artist']['#text']
            title = f'{info['artist']} - {info['track']}'
            if title not in track_titles:
                track_titles.add(title)
            else:
                continue

            album = track['album']['#text']
            if not album:
                try:
                    response = requests.get(url=track['url'], timeout=3)
                    bs = BeautifulSoup(response.text, 'lxml')

                    album_tag = bs.find('h4', class_='source-album-name')
                    if album_tag:
                        album = album_tag.get_text().strip()
                        info['album'] = album
                    else:
                        self.not_found.add(title)
                        continue
                except:
                    continue
            else:
                info['album'] = album
            
            if album not in album_titles:
                album_titles.add(album)
            else:
                continue

            info['images'] = track['image']
            images = []
            for im in info['images']:
                images.append(im['#text'])
            info['images'] = images

            date = track.get('date', None)
            if date:
                info['date'] = date['#text']

            info['url'] = track['url']
            
            result_albums.append(info)
        
        return result_albums
    
    def save_to_files(self):
        with open(BasePath.ALBUMS.value, 'w', encoding='utf-8') as file:
            for track in self.albums:
                file.write(f'{track['artist']} - {track['album']}, {track['images'][-1]}\n')
        
        with open(BasePath.UNKNOWN.value, 'w', encoding='utf-8') as file:
            for track in self.not_found:
                file.write(track + '\n')