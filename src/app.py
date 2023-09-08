from flask import Flask, request, url_for,session, redirect, render_template
from flask_session import Session
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")


app = Flask(__name__)

app.sercret_key = "AKjhnd79Huha"
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')
    
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()

        return render_template("index.html", auth_url=auth_url)

        

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return redirectPage()

@app.route('/redirect')
def redirectPage():
    return render_template("main.html")


@app.route('/logout')
def logout():
    
    for key in list(session.keys()):
        session.pop(key)
        
    return redirect('/')