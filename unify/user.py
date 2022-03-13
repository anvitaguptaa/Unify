import tekore as tk
import configparser
import os
import sys
 
 
def set_env():
    config = configparser.ConfigParser()
    config.read('credentials.config')
    os.environ['client_secret'] = config['DEFAULT']['SPOTIFY_CLIENT_SECRET']
    os.environ['client_id'] = config['DEFAULT']['SPOTIFY_CLIENT_ID']
    os.environ['redirect_uri'] = config['DEFAULT']['SPOTIFY_REDIRECT_URI']
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
        tk.config_to_file('credentials.config', {'SPOTIFY_USER_REFRESH': str(refresh_token)})
       
        return refresh_token
 
 
    def authorization(self):
        conf = tk.config_from_file('credentials.config', return_refresh=True)
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
            tracks_arr.append(track.name)
        print(tracks_arr)
        return(tracks_arr)
       
       
    def process_user(self):
        self.get_top_tracks()
 

if __name__ == '__main__':
    set_env()
    user = User('av_pr')
    user.process_user()
 
