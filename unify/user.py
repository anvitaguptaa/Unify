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
            # analysis is the required information we are going to use to base the recommendations off of.
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
        # Initialize the database.
        database.main()
        # create the connection.
        cnx = mysql.connector.connect(user='root', database='HeartBeat')
        # initialize the cursor.
        cursor = cnx.cursor()
        # Empty dict called music_data which will be filled.
        music_data = {} 
        # n is required for proper indexing when filling the database with information from the list of songs       
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
            # add_data is the sql command to add data, with values in %(key)s
            # music data contains the key-pair values that are used to add to the db.
            cursor.execute(add_data, music_data)
            # indexing purposes since there are 11 pieces of information attached to each song, indexing is done as such.
            n += 11
        # Insert initial information that is not the averages for user_data.
        cursor.execute("INSERT INTO user_info (user_name, date_accessed) VALUES (%s, %s)", (self.username, str_now))
        for x in music_data:
            # x will result in being all the keys in the dictionary, and since we already have the user_name and date in there, 
            # we do not need this information.
            if x == 'song_id' or x == 'song_name' or x == 'username':
                pass
            else:
                # the execute below is a SQL command that can find the average of a column in a table
                # and we do this for all songs associated to the user.
                cursor.execute("SELECT AVG(%s) FROM music_info WHERE username=%s", (x, self.username))
                for value in cursor:
                    # value itself is a tuple and was immutable, hence the change to val, which is a list.
                    val = list(value)
                    # Inserts into the table where user_name is already set the average values we find.
                    cursor.execute("UPDATE user_info SET avg_{}=%s WHERE user_name=%s".format(x), (str(val[0]), self.username))
        cnx.commit()


 

if __name__ == '__main__':
    set_env()
    username = input("Please enter your username: ")
    user = User('{}'.format(username))
    user.process_user()
 
