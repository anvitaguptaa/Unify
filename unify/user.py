#!/usr/bin/python3
import tekore as tk
import configparser
import mysql.connector
import database
import os
import sys
import datetime

now = datetime.datetime.utcnow()
str_now = now.date().isoformat()
 
def set_env():
    config = configparser.ConfigParser()
    config.read('./unify/credentials.config')
    os.environ['client_secret'] = config['DEFAULT']['spotifyclientsecret']
    os.environ['client_id'] = config['DEFAULT']['spotifyclientid']
    os.environ['redirect_uri'] = config['DEFAULT']['spotifyredirecturi']
    os.environ['scope'] = '''user-top-read user-read-playback-state user-read-recently-played
                            user-follow-read playlist-read-private playlist-read-collaborative'''
    os.environ['url'] = 'https://api.spotify.com/v1/'
 
 
class User:
    def __init__(self, username):
        self.username = username
        self.client_secret = os.environ.get('client_secret')
        self.client_id = os.environ.get('client_id')
        self.redirect_uri = os.environ.get('redirect_uri')
        self.scope = os.environ.get('scope')
        self.url = os.environ.get('url')
 
 
    def new_refresh_token(self):
        refresh_token = tk.prompt_for_user_token(self.client_id, self.client_secret, self.redirect_uri, self.scope)
        tk.config_to_file('./unify/credentials.config', {'spotifyuserrefresh': str(refresh_token)})
       
        return refresh_token
 
 
    def authorization(self):
        conf = tk.config_from_file('./unify/credentials.config', return_refresh=True)
        token = conf[3]
        if token:
            return token
        else:
            token = self.new_refresh_token()
            return token
 
 
    def create_client(self):
        token = self.authorization()
        spotify = tk.Spotify(token)
 
        return spotify
 
 
    def get_top_tracks(self):
        spotify = self.create_client()
        tracks = spotify.current_user_top_tracks(limit=10)
        tracks_arr = []
        for track in tracks.items:
            tracks_arr.append(track.id)
            tracks_arr.append(track.name)
            analysis = spotify.track_audio_features(track.id)
            tracks_arr.append(analysis.energy)
            tracks_arr.append(analysis.tempo)
            tracks_arr.append(analysis.danceability)
            tracks_arr.append(analysis.acousticness)
            tracks_arr.append(analysis.instrumentalness)
            tracks_arr.append(analysis.liveness)
            tracks_arr.append(analysis.loudness)
            tracks_arr.append(analysis.speechiness)
            tracks_arr.append(analysis.valence)
        return(tracks_arr)
       
       
    def process_user(self):
        songs = self.get_top_tracks()
        database.main()
        cnx = mysql.connector.connect(user='root', database='HeartBeat')
        cursor = cnx.cursor()
        music_data = {}        
        n = 0
        while n < 99:
            add_data = ("INSERT INTO music_info VALUES (%(song_id)s, %(song_name)s, %(username)s, %(energy)s, %(tempo)s, %(danceability)s, %(acousticness)s, %(instrumentalness)s, %(liveness)s, %(loudness)s, %(speechiness)s, %(valence)s)")
            music_data = {
                'song_id': songs[n + 0],
                'song_name': songs[n + 1],
                'username': self.username,
                'energy': songs[n + 2],
                'tempo': songs[n + 3],
                'danceability': songs[n + 4],
                'acousticness': songs[n + 5],
                'instrumentalness': songs[n + 6],
                'liveness': songs[n + 7],
                'loudness': songs[n + 8],
                'speechiness': songs[n + 9],
                'valence': songs[n + 10],
            }
            cursor.execute(add_data, music_data)
            n += 11
        cursor.execute("INSERT INTO user_info (user_name, date_accessed) VALUES (%s, %s)", (self.username, str_now))
        for x in music_data:
            if x == 'song_id' or x == 'song_name' or x == 'username':
                pass
            else:
                cursor.execute("SELECT AVG({}) FROM music_info".format(x))
                for value in cursor:
                    val = list(value)
                    cursor.execute("UPDATE user_info SET avg_{}=%s WHERE user_name=%s".format(x), (str(val[0]), self.username))
        cnx.commit()


 

if __name__ == '__main__':
    set_env()
    username = input("Please enter your username: ")
    user = User('{}'.format(username))
    user.process_user()
 
