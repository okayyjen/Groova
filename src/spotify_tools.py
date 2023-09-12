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
            scope="user-library-read")

def get_display_name(session):
    return session['user_info']['display_name']