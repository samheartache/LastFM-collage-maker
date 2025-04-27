import requests
from bs4 import BeautifulSoup


class LastFM:
    def __init__(self, username, quantity):
        self.username = username
        self.quantity = quantity

        self.get_songs()
    
    def get_songs(self):
        not_found_tracks = []

        page_tracks = requests.get(f'https://www.last.fm/user/{self.username}/library?page=1')
        bs_tracks = BeautifulSoup(page_tracks.text, 'lxml')

        tracks = bs_tracks.find_all('tr', class_='chartlist-row')
        for row in tracks:
            track = row.find('td', class_='chartlist-name')
            track_link = f'https://www.last.fm{track.find('a')['href']}'

            track_page = requests.get(track_link)
            bs_track = BeautifulSoup(track_page.text, 'lxml')
            album_name = bs_track.find('h4', class_='source-album-name')
            album_artist = bs_track.find('p', class_='source-album-artist')

            if album_artist and album_name:
                album_artist = album_artist.text.replace('\n', '')
                album_name = album_name.text.replace('\n', '')
                
            print(f'{album_artist} - {album_name}')
            input()





if __name__ == '__main__':
    parser = LastFM('SamHeartache', 10)

