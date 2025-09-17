import os

import dotenv
import requests

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')


def get_user_tracks(user: str, timestamp: int=0, limit: int=0) -> list:
    url = f'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={API_KEY}&format=json&to=1757462400'
    result_tracks = []

    if timestamp:
        url += f'&to={timestamp}'
    if limit:
        url += f'&limit={limit}'
    
    response = requests.get(url=url)
    response_json = response.json()
    recent_tracks = response_json['recenttracks']['track']

    for track in recent_tracks:
        d = {}
        d['track'] = track['name']
        d['album'] = track['album']['#text']
        d['image'] = track['image']
        d['artist'] = track['artist']['#text']
        d['url'] = track['url']
        
        date = track.get('date', None)

        if date:
            d['date'] = date['#text']

        result_tracks.append(d)
    
    return result_tracks