import os
import re
import sys
import requests
import spotipy
import spotipy.util as util
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv('/Users/Anvi/Documents/PythonProjects/credentials.env')

CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
USERNAME = input('Enter your Spotify username: ')
SCOPE = '''user-top-read user-read-playback-state user-read-recently-played
        user-follow-read playlist-read-private playlist-read-collaborative'''

# Requests URL
URL = 'https://api.spotify.com/v1/'


# Prompts user for authorization
def oauth_token():
    token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID,
                                       CLIENT_SECRET, REDIRECT_URI)

    return token


# Makes header for API request
def make_headers(token):
    headers = {'Authorization': 'Bearer ' + token}

    return headers


# Program start user prompt
def user_introduction():
    num_dashes = int((65 - len(USERNAME + '|Hello |')) / 2)
    dashes = num_dashes*('-')

    if len(USERNAME) % 2 == 1:
        greeting = '|' + dashes + f'Hello {USERNAME}' + dashes + '|'
    else:
        greeting = '|-' + dashes + f'Hello {USERNAME}' + dashes + '|'

    print()
    print('*****************************************************************')
    print(greeting)
    print('|------------Are you ready to discover your Spotify?------------|')
    print('|-------------------Press ENTER to continue...------------------|')
    print('*****************************************************************')


# Displays program options for user to choose from
def user_menu():
    print('\n')
    print('|----SELECT AN OPTION FROM THE MENU AND PRESS THE ENTER KEY:----|')
    print('|                                                               |')
    print('|------- OPTION: ------------------------------ PRESS: ---------|')
    print('|--------- LIST ALL SPOTIFY GENRES ----------------- G ---------|')
    print('|--------- SEARCH FOR AN ALBUM ID ------------------ A ---------|')
    print('|--------- SEARCH FOR A TRACK ID ------------------- T ---------|')
    print('|--------- SEE YOUR MOST RECENTLY PLAYED TRACKS ---- R ---------|')
    print('|--------- DISPLAY YOUR USER PLAYLISTS ------------- P ---------|')
    print('|--------- EXIT ------------------------------------ X ---------|')
    print()


# Lists all spotify genres
def list_genres():
    get_genres = requests.get(URL + 'recommendations/available-genre-seeds',
                              headers=headers).json()

    print('DISPLAYING ALL GENRES:')
    for item in get_genres['genres']:
        print(item)


# Displays user recently played tracks
def recently_played_tracks():
    rp_tracks = requests.get(URL + 'me/player/recently-played',
                             headers=headers)
    tracks_response = rp_tracks.json()

    print('YOUR MOST RECENTLY PLAYED TRACKS ARE:')
    for item in tracks_response['items']:
        name = item['track']['name']
        artist = item['track']['artists'][0]['name']
        print(f'SONG: {name}  ---  ARTIST: {artist}')


# Search for tracks
def get_track_id():
    track = input('ENTER THE NAME OF THE SONG YOU ARE SEARCHING FOR: ')
    artist = input('ENTER THE NAME OF THE ARTIST (OPTIONAL): ')
    print()

    if artist == '':
        results = sp.search('track:' + track, limit='15', type='track')
    else:
        results = sp.search('artist:' + artist + ' track:' + track,
                            limit='15', type='track')

    if results['tracks']['items'] != []:
        print('TOP SEARCH RESULTS:')
        for item in results['tracks']['items']:
            song = item['name']
            artist = item['artists'][0]['name']
            song_id = item['id']
            print(f'SONG: {song}  ---  ARTIST: {artist}  ---  ' +
                  f'SONG ID: {song_id}')
    else:
        print('NO RESULTS WERE FOUND.')


# Search for albums
def get_album_id():
    album_name = input('ENTER THE NAME OF THE ALBUM YOU ARE SEARCHING FOR: ')
    print()

    results = sp.search('album:' + album_name, limit='15', type='album')

    if results['albums']['items'] != []:
        print('TOP SEARCH RESULTS:')
        for item in results['albums']['items']:
            album = item['name']
            artist = item['artists'][0]['name']
            album_id = item['id']
            print(f'ALBUM: {album}  ---  ARTIST: {artist}  ---  ' +
                  f'ALBUM ID: {album_id}')
    else:
        print('NO RESULTS WERE FOUND.')


#  Display all user playlists
def display_user_playlists():
    playlists = sp.current_user_playlists(50)

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            json_uri = playlist['uri']
            uri = re.search('((?<=\\:)[^playlist:].*)', json_uri).group(1)
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['name']
                                 + '  ---  ', 'Playlist URI: ' + str(uri)))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    return playlists


# Display on program exit
def prompt_exit():
    print()
    print('*****************************************************************')
    print('|--------------------- Hope you enjoyed :) ---------------------|')
    print('|------------------ Bye now, happy listening! ------------------|')
    print('*****************************************************************'
          + '\n')
    sys.exit()


# User command functionality
def prompt_command(kb_input):
    if kb_input == 'g':
        list_genres()
    elif kb_input == 'x':
        prompt_exit()
    elif kb_input == 'a':
        get_album_id()
    elif kb_input == 't':
        get_track_id()
    elif kb_input == 'r':
        recently_played_tracks()
    elif kb_input == 'p':
        display_user_playlists()


if __name__ == '__main__':

    token = oauth_token()
    headers = make_headers(token)

    if token:
        sp = spotipy.Spotify(auth=token)
        user_introduction()
        user_continue = input()

        if user_continue == '':
            choice = ''
            while choice != 'x':
                user_menu()
                choice = input()
                print()
                prompt_command(choice)
        else:
            prompt_exit()
    else:
        print(f'Can\'t get token for {USERNAME}')
