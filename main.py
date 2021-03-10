import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random

os.environ["SPOTIPY_CLIENT_ID"] = '04e9593b8574411ea1640433ea464fb8'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'dd80d98d0c9845a6bef36bc4d10c308a'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8080'  # all the auth
username = "bytmjoltm7yu5hq50um4ik6sb"
device_id = 'b0a12c11905ae21baa4400d765bbca53a6df2e0b'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

import spotipy.util as util

username = 'bytmjoltm7yu5hq50um4ik6sb'
client_id = '04e9593b8574411ea1640433ea464fb8'
client_secret = 'dd80d98d0c9845a6bef36bc4d10c308a'
redirect_uri = 'http://localhost:8080'
scope = 'user-read-recently-played'  # more auth, to get token

token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

import ast
from typing import List
from os import listdir


def get_streamings(path: str = 'MyData') -> List[dict]:
    files = ['MyData/' + x for x in listdir(path)
             if x.split('.')[0][:-1] == 'StreamingHistory']

    all_streamings = []

    for file in files:
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming
                               in new_streamings]
    return all_streamings  # opens the streamingHistory jsons and turns them into dictionaries. get the first track
    # name with get_streamings("MyData")[i]["trackName"], from there, you can get the track id using
    # song_id = get_id('Cabaret', token), and from there, you can get the album name using
    # track = (spotify.track(song_id))  print(track["album"]["name"])


import requests


def get_id(track_name: str, token: str):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer ' + token, }
    params = [
        ('q', track_name),
        ('type', 'track'),
    ]
    try:
        response = requests.get('https://api.spotify.com/v1/search',
                                headers=headers, params=params, timeout=5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None


# print(token)
scope_token = token
# BQBO9yjPUAVnddWwb2lzn9t6ZLvN_IRFzpKdO1Y0IW4dKk2T7e8PP5nhr6BRl0nsvv3L1LtK5dlSi6FAgQplOgpRoIbsRqY7w-GsiFaGh8FeTNZH2_LhCjGkr_u74Wd70C1Z-yWPrvfmaE666kfnWCHQV5VxdqbpT8YJ-nwTfHc
i = 0
all_songs = []
all_albums = {}
long_albums = []
# print(len((get_streamings("MyData"))))
# len 25908
for ii in range(25907):
    try:
        song_name = (get_streamings("MyData")[i]["trackName"])
        if song_name not in all_songs:
            all_songs.append(song_name)
        song_id = get_id(song_name, token)
        track = (spotify.track(song_id))
        album_name = (track["album"]["name"])
        if album_name not in all_albums:
            all_albums[album_name] = 1
        elif album_name in all_albums:
            all_albums[album_name] += 1
    except:
        continue
    i += 1
# song_id = get_id('Cabaret', token)
# print(song_id)
# track = (spotify.track(song_id))
# print(track["album"]["name"])
print(all_songs)
print(all_albums)
for key, value in all_albums.items():
    if value >= 5:
        long_albums.append(key)
print(long_albums)
