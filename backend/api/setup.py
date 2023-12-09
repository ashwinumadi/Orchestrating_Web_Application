import pandas as pd
from api.models import DBSongs

data=pd.read_csv('Spotify-2023.csv', encoding='ISO-8859-1')

for row in range(len(data['track_name'])):
    entry = DBSongs.objects.create(
        song_name = data['track_name'][row],
        artist_name = data['artist(s)_name'][row],
        bpm = data['bpm'][row],
        key = data['key'][row],
        mode = data['mode'][row],
        danceability = data['danceability_%'][row],
        valence = data['valence_%'][row],
        energy = data['energy_%'][row],
        acousticness = data['acousticness_%'][row],
        instrumentalness = data['instrumentalness_%'][row],
        liveness = data['liveness_%'][row],
        speechiness = data['speechiness_%'][row]
    )
    entry.save()