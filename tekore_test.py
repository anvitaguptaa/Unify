import tekore as tk
import mysql.connector
from dotenv import load_dotenv
import os
import db_connection

def db_exist():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )   

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        if x[0] == 'HeartBeat':
            return 'HeartBeat'
    return False

def connect_db(db_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=db_name
    )
    
    
def main():
    load_dotenv()
    
    client_id = os.environ.get('CLIENT_ID')
    
    client_secret = os.environ.get('CLIENT_SECRET')
    
    redirect_uri = os.environ.get('REDIRECT_URI')
    
    db = db_exist()
    
    if db == 'HeartBeat':
        print("Database exists by the name of HeartBeat - Attempting to connect...")
        connect_db(db)
        
    else:
        db_connection()
        connect_db(db_pass, db_exist(db_pass))
    
    app_token = tk.request_client_token(client_id, client_secret)

    spotify = tk.Spotify(app_token)
    
    
    user_token = tk.prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=tk.scope.every
    )

    spotify.token = user_token

    total = 10
    total_energy = 0
    total_tempo = 0
    total_danceability = 0
    total_acousticness = 0
    total_instrumentalness = 0
    total_liveness = 0
    total_loudness = 0
    total_speechiness = 0
    total_time_signature = 0
    total_valence = 0
    tracks = spotify.current_user_top_tracks(limit=total)
    for track in tracks.items:
        print(track.name)
        analysis = spotify.track_audio_features(track.id)
        total_energy += analysis.energy
        total_tempo += analysis.tempo
        total_danceability += analysis.danceability
        total_acousticness += analysis.acousticness
        total_instrumentalness += analysis.instrumentalness
        total_liveness += analysis.liveness
        total_loudness += analysis.loudness
        total_speechiness += analysis.speechiness
        total_time_signature += analysis.time_signature
        total_valence += analysis.valence

    avg_energy = total_energy / total
    avg_tempo = total_tempo / total
    avg_danceability = total_danceability / total
    avg_acousticness = total_acousticness / total
    avg_instrumentalness = total_instrumentalness / total
    avg_liveness = total_liveness / total
    avg_loudness = total_loudness / total
    avg_speechiness = total_speechiness / total
    avg_time_signature = total_time_signature / total
    avg_valence = total_valence / total

    print("Energy: " + str(avg_energy))
    print("Tempo: " + str(avg_tempo))
    print("Danceability: " + str(avg_danceability))
    print("Acousticness: " + str(avg_acousticness))
    print("Instrumentalness: " + str(avg_instrumentalness))
    print("Liveness: " + str(avg_liveness))
    print("Loudness: " + str(avg_loudness))
    print("Speechiness: " + str(avg_speechiness))
    print("Time Signature: " + str(avg_time_signature))
    print("Valence: " + str(avg_valence))

if __name__ == "__main__":
    main()
