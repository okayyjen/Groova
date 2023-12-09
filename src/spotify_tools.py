from datetime import datetime
from flask import url_for
import spotipy
import os
import re
from dotenv import load_dotenv
import requests
from lyricsgenius import Genius
import random
import response_format

load_dotenv()

clientID = os.getenv("SPOTIPY_CLIENT_ID")
clientSecret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirectURI = os.getenv("SPOTIPY_REDIRECT_URI")

def create_spotify_oauth():

    scopes = ["user-top-read", "playlist-modify-private","playlist-modify-public"]

    return spotipy.oauth2.SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=url_for('callback', _external=True),
            scope=' '.join(scopes))

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

#getter for current user's top 5 artists
def get_top_artists(token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])

    top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)

    # Extract artist names from the response
    artist_names = [artist['name'] for artist in top_artists['items']]

    for i, artist in enumerate(artist_names, start=1):
        print(f"{i}. {artist}")

    return top_artists

#creates empty playlist
def create_playlist(session, token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = session['user_info']['id']
    playlist = sp.user_playlist_create(user_id, "New Playlist", public=True,collaborative=False, description="")
    playlist_url = playlist['external_urls']['spotify']

    return playlist

#getter for current user's top 20 tracks
def get_top_tracks(token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=3, offset=0)
    top_tracks_names = [track['name'] for track in top_tracks['items']]

    for i, track in enumerate(top_tracks_names, start=1):
        print(f"{i}. {track}")

    return top_tracks

def get_song_features(tracks, token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])

    tracks_id_list = []
    for track in tracks['items']:
        track_id = track['id']
        tracks_id_list.append(track_id)

    features = sp.audio_features(tracks_id_list)
    return features

def get_recommendations(token_info, top_artists, target_features) -> dict:

    sp = spotipy.Spotify(auth=token_info['access_token'])

    artist_URLs = []
    for artist in top_artists['items']:
        artist_url = artist['external_urls']['spotify']
        artist_URLs.append(artist_url)

    recommended_tracks = sp.recommendations(seed_artists=artist_URLs, limit=20, target_features=target_features)
    return recommended_tracks


def add_tracks(token_info,session,tracks):

    sp = spotipy.Spotify(auth=token_info['access_token'])
    track_uris = [track['uri'] for track in tracks['tracks']]

    #creating playlist and getting playlist_id
    playlist = create_playlist(session, token_info)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_uris, position=None)

    return playlist['external_urls']['spotify']

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

def recommendations_genres(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    print(sp.recommendation_genre_seeds())

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

        if song_name.lower() in track['name'].lower() and artist_list[0].lower() in track['artists'][0]['name'].lower():
            song_url = results['tracks']['items'][0]['external_urls']['spotify']

    return song_url

def get_artist_id(artist_name):
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)

    results = sp.search(q=artist_name, type='artist', limit=1)
    
    # Extract the artist ID from the search results
    if results['artists']['items']:
        return results['artists']['items'][0]['id']
    else:
        return None

def get_artist_recent_discography(artist_name):
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)

    artist_id = get_artist_id(artist_name)

    albums = sp.artist_albums(artist_id, album_type='album', limit=10)
    albums_recent = []
    for album in albums['items']:

        string = album['release_date']
        date = datetime.strptime(string, "%Y-%m-%d")

        if date.year < 2023:
            albums_recent.append(album)

    songs = []
    for album in albums_recent:
        album_tracks = sp.album_tracks(album['id'])
        
        for track in album_tracks['items']:

            song_name = track['name']
            songs.append(song_name)

    return songs

def get_lyrics(song_title, artist_name):
    genius_token = os.getenv('SPOTIFY_USER_ID')
    genius = Genius(genius_token)
    song = genius.search_song(song_title, artist_name)

    return song.lyrics

def get_playlist_id(playlist_url):
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    sp = spotipy.Spotify(auth=token)

def create_playlist_song_list(song_info_list, playlist_name):

    user = os.getenv('SPOTIFY_USER_ID')
    if not user:
        raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
    
    sp = spotipy.Spotify(auth=token)

    # Create a new empty playlist
    user_playlist = sp.user_playlist_create(user, playlist_name, public=False, collaborative=False, description="Made with Groova")
    playlist_id = user_playlist['id']

    song_URLs = []
    #if the user given song exists, add it to song_URLs
    for song_info in song_info_list:
        song_link = get_song_link(song_info.song_name, song_info.artist_name_list)

        if song_link and song_link not in song_URLs:
            song_URLs.append(song_link)
        
        if len(song_URLs) == 30:
            break

    if song_URLs:
        random.shuffle(song_URLs)

    if len(song_URLs) < 30:
        extra = 30 - len(song_URLs)
        recommended_tracks = sp.recommendations(seed_tracks=song_URLs[:5], limit=extra)
        recommended_track_uris = [track['uri'] for track in recommended_tracks['tracks']]
        
        song_URLs.extend(recommended_track_uris)

    #add tracks to playlist
    sp.playlist_add_items(playlist_id, song_URLs, position=None)
    playlist_url = user_playlist['external_urls']['spotify']

    return {'playlist_url': playlist_url,
            'playlist_id': playlist_id
            }


def create_playlist(features_and_genres, pdetails):
    user = os.getenv('SPOTIFY_USER_ID')
    if not user:
        raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
        
    #convert string dict into dict
    features_dict, genre_list = extract_and_format(features_and_genres)
    
    sp = spotipy.Spotify(auth=token)

    # Create a new empty playlist
    user_playlist = sp.user_playlist_create(user, pdetails.playlist_name, public=False, collaborative=False, description="Made with Groova")

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
    
    recommended_tracks = sp.recommendations(seed_artists=artist_URLs, limit=20, target_features=features_dict)
    recommended_track_uris = [track['uri'] for track in recommended_tracks['tracks']]
    playlist_id = user_playlist['id']

    #add tracks to playlist
    sp.playlist_add_items(playlist_id, recommended_track_uris, position=None)
    playlist_url = user_playlist['external_urls']['spotify']

    return {'playlist_url': playlist_url,
            'playlist_id': playlist_id,
            'artist_found': artist_found,
            'artist_not_found_list': artist_not_found_list
            }