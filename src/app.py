from flask import Flask, request, url_for,session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")


app = Flask(__name__)

app.sercret_key = "AKjhnd79Huha"
app.config['SESSION_COOKIE_NAME'] = 'cookie dookie'


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    return "Some aphex twins song"

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=url_for('redirectPage', _external=True),
            scope="user-library-read")
