import re
from api.models import DBSongs, DBUserQueries


norm = {
    'very_low': [0,20],
    'low': [21,40],
    'medium': [41,60],
    'high':[61,80],
    'very_high': [81,100]
}

def song_matching(user, description):
    pattern_artist = r'\bsong by (\w+)\s+(\w+)\s+\b'
    pattern_bpm = r'\b(\w+)\s+bpm\b'
    pattern_key = r'\b(\w+)\s+key\b'
    pattern_mode = r'\b(\w+)\s+mode\b'
    pattern_danceability = r'\b(\w+)\s+danceability\b'
    pattern_valence = r'\b(\w+)\s+valence\b'
    pattern_energy = r'\b(\w+)\s+energy\b'
    pattern_acousticness = r'\b(\w+)\s+acousticness\b'
    pattern_instrumentalness = r'\b(\w+)\s+instrumentalness\b'
    pattern_liveness = r'\b(\w+)\s+liveness\b'
    pattern_speechiness = r'\b(\w+)\s+speechiness\b'
    filter = {}

    artist = re.findall(pattern_artist, description)
    if artist:
        artist = artist[0][0] + ' ' + artist[0][1]
        filter['artist_name__icontains'] = artist
    bpm = re.findall(pattern_bpm, description)
    if bpm:
        filter['bpm__gte'] = (norm[bpm[0]][0]/100)*206
        filter['bpm__lte'] = (norm[bpm[0]][1]/100)*206
    key = re.findall(pattern_key, description)
    if key:
        filter['key'] = key[0]
    mode = re.findall(pattern_mode, description)
    if mode:
        filter['mode'] = mode[0]
    danceability = re.findall(pattern_danceability, description)
    if danceability:
        filter['danceability__gte'] = norm[danceability[0]][0]
        filter['danceability__lte'] = norm[danceability[0]][1]
    valence = re.findall(pattern_valence, description)
    if valence:
        filter['valence__gte'] = norm[valence[0]][0]
        filter['valence__lte'] = norm[valence[0]][1]
    energy = re.findall(pattern_energy, description)
    if energy:
        filter['energy__gte'] = norm[energy[0]][0]
        filter['energy__lte'] = norm[energy[0]][1]
    acousticness = re.findall(pattern_acousticness, description)
    if acousticness:
        filter['acousticness__gte'] = norm[acousticness[0]][0]
        filter['acousticness__lte'] = norm[acousticness[0]][1]
    instrumentalness = re.findall(pattern_instrumentalness, description)
    if instrumentalness:    
        filter['instrumentalness__gte'] = norm[instrumentalness[0]][0]
        filter['instrumentalness__lte'] = norm[instrumentalness[0]][1]
    liveliness = re.findall(pattern_liveness, description)
    if liveliness:
        filter['liveness__gte'] = norm[liveliness[0]][0]
        filter['liveness__lte'] = norm[liveliness[0]][1]
    speechiness = re.findall(pattern_speechiness, description)
    if speechiness:
        filter['speechiness__gte'] = norm[speechiness[0]][0]
        filter['speechiness__lte'] = norm[speechiness[0]][1]

    queried_songs = DBSongs.objects.filter(**filter).values_list('song_name', flat=True)

    output_list = []
    for song in queried_songs:
        output_list.append({'song': song})
    output = {
        'songs_list': output_list
    }
    dbuserquery = DBUserQueries.objects.create(data=output_list,
                                               user=user,
                                               description=description)
    dbuserquery.save()
    return output


def get_user_queries(user):
    output_list = DBUserQueries.objects.filter(user=user).values('description')
    output = {
        'query_list': list(output_list)
    }
    return output

"""
'very_high bpm A key major mode high danceability low valence high energy low acousticness high instrumentalness high liveness medium speechiness'
'very_high bpm song by Taylor Swift A key major mode high danceability low valence high energy low acousticness high instrumentalness high liveness medium speechiness'
'give me a song by Taylor Swift with high energy'
"""