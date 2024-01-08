from flask import url_for
from unidecode import unidecode
import spotipy
import os
import re
from dotenv import load_dotenv
import random
import base64
import random
import constants

load_dotenv()

clientID = os.environ["SPOTIPY_CLIENT_ID"]
clientSecret = os.environ["SPOTIPY_CLIENT_SECRET"]
redirectURI = os.environ["SPOTIPY_REDIRECT_URI"]

def create_spotify_oauth():

    scopes = ["user-top-read", "playlist-modify-private","playlist-modify-public", "ugc-image-upload"]

    return spotipy.oauth2.SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=url_for('callback', _external=True),
            scope=' '.join(scopes))

def get_spotify_user_token():
    user = os.getenv('SPOTIFY_USER_ID')
    if not user:
        raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
    
    return user, token

def display_name():
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)
    user_info = sp.current_user()
    
    return user_info['display_name']

def user_pic():
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)
    user_info = sp.current_user()
    url = user_info['images'][0]['url'] if user_info['images'] else "no pfp"
    return url

def create_playlist_song_list(song_info_list, playlist_name):

    user, token = get_spotify_user_token()
    
    sp = spotipy.Spotify(auth=token)

    song_URLs = get_song_URL_list(song_info_list, sp)

    # Create a new empty playlist
    user_playlist = sp.user_playlist_create(user, playlist_name, public=False, collaborative=False, description="Made with Groovify")
    playlist_id = user_playlist['id']

    #Add playlist cover
    add_playlist_cover(sp, playlist_id)

    #add tracks to playlist
    sp.playlist_add_items(playlist_id, song_URLs, position=None)
    playlist_url = user_playlist['external_urls']['spotify']

    #get playlist cover
    playlist_cover_url = sp.playlist_cover_image(playlist_id)
    print(playlist_cover_url)

    return {'playlist_url': playlist_url,
            'playlist_id': playlist_id,
            'playlist_cover_url': playlist_cover_url
            }

def create_playlist(features_and_genres, pdetails):
    user, token = get_spotify_user_token()
        
    #convert string dict into dict
    features_dict, genre_list = extract_and_format(features_and_genres)
    
    sp = spotipy.Spotify(auth=token)

    #if the user given artist exists, add it to artist_URLs, if not, use user's top artist
    artist_URLs = []
    artist_not_found_list = []
    artist_names_list = pdetails.artist_names
    
    for artist in artist_names_list:
        artist_link = get_artist_link(artist)
        if len(artist_URLs) == 5:
            break
        if artist_link:
            artist_found = True
            artist_URLs.append(artist_link)
        else: 
            artist_not_found_list.append(artist)

    if not artist_URLs:
        artist_found = False
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=1)
        artist_name = top_artists['items'][0]['name']
        top_artist_url = get_artist_link(artist_name)
        artist_URLs.append(top_artist_url)
    
    recommended_tracks = sp.recommendations(seed_artists=artist_URLs, seed_genres= genre_list, limit=30, target_features=features_dict)
    recommended_track_uris = [track['uri'] for track in recommended_tracks['tracks']]

    # Create a new empty playlist
    user_playlist = sp.user_playlist_create(user, pdetails.playlist_name, public=False, collaborative=False, description="Made with Groova")
    playlist_id = user_playlist['id']

    #Add playlist cover
    add_playlist_cover(sp, playlist_id)

    #add tracks to playlist
    sp.playlist_add_items(playlist_id, recommended_track_uris, position=None)
    playlist_url = user_playlist['external_urls']['spotify']

    #get playlist cover
    playlist_cover_url = sp.playlist_cover_image(playlist_id)
    print(playlist_cover_url)

    return {'playlist_url': playlist_url,
            'playlist_id': playlist_id,
            'playlist_cover_url': playlist_cover_url,
            'artist_found': artist_found,
            'artist_not_found_list': artist_not_found_list
            }

def get_song_URL_list(song_info_list, sp):
    #if the user given song exists, add it to song_URLs
    song_URLs = []
    for song_info in song_info_list:
        song_link = get_song_link(song_info.song_name, song_info.artist_name_list)

        #Ensure no duplicates
        if song_link and song_link not in song_URLs:
            song_URLs.append(song_link)

        #cut playlist off at len == 30
        if len(song_URLs) == 30:
            break

    #if song url list is not empty, shuffle songs
    if song_URLs:
        random.shuffle(song_URLs)
    
    #if songs are between 1 - 29, fill out playlist until 30
    if len(song_URLs) < 30:
        print(len(song_URLs))
        extra = 30 - len(song_URLs)
        recommended_tracks = sp.recommendations(seed_tracks=song_URLs[:5], limit=extra)
        recommended_track_uris = [track['uri'] for track in recommended_tracks['tracks']]
        
        song_URLs.extend(recommended_track_uris)

    return song_URLs

def add_playlist_cover(sp, playlist_id):

    path = random.choice(constants.IMAGE_PATH_LIST)

    try:
        with open(path, 'rb') as image_file:
            # Read image data
            image_data = image_file.read()

            # Encode image data to Base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')

            # Upload and set playlist cover
            sp.playlist_upload_cover_image(playlist_id, image_b64)

        print("Playlist cover image updated successfully.")
    except spotipy.SpotifyException as e:
        print(f"Error: {e}")

def get_artist_link(artist_name):
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)

    if results['artists']['total'] > 0:
    # Get the artist URL from the first result
        artist_url = results['artists']['items'][0]['external_urls']['spotify']
        print(f"Artist URL: {artist_url}")
    else:
        artist_url = None

    return artist_url

def get_song_link(song_name, artist_list):
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)
    
    query = f"track:{song_name} artist:{artist_list}"
    results = sp.search(q=query, type='track', limit=1)

    song_url = None

    if results['tracks']['total'] > 0:
        #Get the song URL from the first result
        track = results['tracks']['items'][0]
        
        translation_table = {ord('\'') : None, ord('"') : None}

        song_name_str = unidecode(song_name.lower().translate(translation_table))
        song_name_spotify = unidecode(track['name'].lower().translate(translation_table))
        artist_name = unidecode(artist_list[0].lower().translate(translation_table))
        artist_name_spotify = unidecode(track['artists'][0]['name'].lower().translate(translation_table))

        song_name_match = song_name_str in song_name_spotify
        contains_artist_name = artist_name in artist_name_spotify
        artist_name_length_match = artist_name_spotify.count(artist_name) == 1

        if  song_name_match and contains_artist_name and artist_name_length_match:
            song_url = track['external_urls']['spotify']
        else:
            print("NOT FOUND: ", song_name_str, " ", song_name_spotify, " ", artist_name, " ", artist_name_spotify)

    return song_url

def extract_and_format(response):
    features_pattern = r'(acousticness|danceability|tempo|valence|energy|loudness|liveness|instrumentalness):?\s*(\d+(\.\d+)?)'
    genres_pattern = r'genres:\s*([^,]+(,\s*[^,]+)*)'
    
    features_match = re.findall(features_pattern, response)
    genres_match = re.search(genres_pattern, response)
    
    for key, value, _ in features_match:
        if key == "valence":
            if float(value) <= 0.5:
                min_or_max = 'max'
                break
            else:
                min_or_max = 'min'
                break

    features_dict = {}
    
    for key, value, _ in features_match:
        features_dict[key] = {'target': float(value)}

    genres_list = []
    if genres_match:
        genres_data = genres_match.group(1).strip().split(', ')
        genres_list = genres_data

    return features_dict, genres_list