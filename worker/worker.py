import re
import redis
import os
import json
import psycopg2
import logging

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

LOGGER.debug('Starting Worker Deployment')
# Connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db-service',  # Use the actual hostname or IP address
    'port': '5432',  # Default PostgreSQL port
}


def song_retreival():
    redisHost = os.getenv("REDIS_HOST") or "redis-service"
    redisPort = os.getenv("REDIS_PORT") or 6379
    REDIS_KEY = "toWorkers"
    r = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    LOGGER.info("Looking for a message")
    newdescription = r.blpop(REDIS_KEY)
    description = newdescription[1].decode('utf-8')
    input_string = description

    # Using regular expression to extract the internal string
    match = re.search(r'"([^"]*)"', input_string)
    if match:
        description = match.group(1)
    try:
        connection = psycopg2.connect(**db_params)
        LOGGER.info("Connected to the database!")
        # Create a cursor
        cursor = connection.cursor()
        norm = {
            'very_low': [0,20],
            'low': [21,40],
            'medium': [41,60],
            'high':[61,80],
            'very_high': [81,100]
        }
        try:
            REDIS_KEY = "toWorkers"
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
            filter = {
                'artist_name__icontains': '',
                'bpm__gte': 0,
                'bpm__lte': 100,
                'danceability__gte': 0,
                'danceability__lte': 100,
                'valence__gte': 0,
                'valence__lte': 100,
                'energy__gte': 0,
                'energy__lte': 100,
                'acousticness__gte': 0,
                'acousticness__lte': 100,
                'instrumentalness__gte': 0,
                'instrumentalness__lte': 100,
                'liveness__gte': 0,
                'liveness__lte': 100,
                'speechiness__gte': 0,
                'speechiness__lte': 100
            }

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

            sql_query = "SELECT song_name FROM api_dbsongs WHERE artist_name LIKE %s AND bpm BETWEEN %s AND %s AND danceability BETWEEN %s AND %s AND valence BETWEEN %s AND %s AND energy BETWEEN %s AND %s AND acousticness BETWEEN %s AND %s AND instrumentalness BETWEEN %s AND %s AND liveness BETWEEN %s AND %s AND speechiness BETWEEN %s AND %s;"
            cursor.execute(sql_query, (
                                       filter['artist_name__icontains'],
                                       filter['bpm__gte'],
                                       filter['bpm__lte'],
                                       filter['danceability__gte'],
                                       filter['danceability__lte'],
                                       filter['valence__gte'],
                                       filter['valence__lte'],
                                       filter['energy__gte'],
                                       filter['energy__lte'],
                                       filter['acousticness__gte'],
                                       filter['acousticness__lte'],
                                       filter['instrumentalness__gte'],
                                       filter['instrumentalness__lte'],
                                       filter['liveness__gte'],
                                       filter['liveness__lte'],
                                       filter['speechiness__gte'],
                                       filter['speechiness__lte']
                                        ))
            queried_songs = cursor.fetchall()
            output_list = []
            for song in queried_songs:
                output_list.append({'song': song[0]})
            output = {
                'songs_list': output_list
            }
            # Sending the Output to 'fromWorkers' Key. Reporting Back to Django
            REDIS_KEY = "fromWorkers"
            count = r.lpush(REDIS_KEY,json.dumps(output))
            r.lpush("logging", f"Pushed Output file to queue {output}")
            LOGGER.info("Current queue length", count)
        except Exception as exp:
            LOGGER.info(exp)

    except Exception as e:
        LOGGER.error("Error: Unable to connect to the database")
        LOGGER.error(e)

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()
            LOGGER.info("Connection closed.")

while True:
  song_retreival()
