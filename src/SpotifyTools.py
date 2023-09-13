from flask import Flask, request, url_for,session, redirect, render_template
from flask_session import Session
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv

load_dotenv()

clientID = os.getenv("SPOTIPY_CLIENT_ID")
clientSecret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirectURI = os.getenv("SPOTIPY_REDIRECT_URI")

#do not have this as global variable. create new oauth object for each use
def create_spotify_oauth():
    return spotipy.oauth2.SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=url_for('callback', _external=True),
            scope="user-top-read")

#getter for current user's display name
def get_display_name(session):
    return session['user_info']['display_name']

#getter for current user's top 20 artists
def get_top_artists(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(time_range='medium_term', limit=10)

    # Extract artist names from the response
    artist_names = [artist['name'] for artist in top_artists['items']]

    for i, artist in enumerate(artist_names, start=1):
        print(f"{i}. {artist}")

    return top_artists


    #sp = spotipy.Spotify(auth=token_info['access_token'])
    #return sp.current_user_top_artists(limit=20, offset=0)

#getter for current user's top 20 tracks
def get_top_tracks(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_user_top_tracks(limit=20, offset=0)['items'][2]


    

    