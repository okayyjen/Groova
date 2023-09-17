import time
from flask import Flask, request, url_for,session, redirect, render_template
from flask_session import Session
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os
import SpotifyTools
import AI
import dotenv

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
TOKEN_INFO = "token_info"
USER_INFO = "user_info"
Session(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    write_to_dotenv("SPOTIFY_ACCESS_TOKEN")
    write_to_dotenv("SPOTIFY_USER_ID")

    displayname = SpotifyTools.get_display_name(session)
    #SpotifyTools.get_top_artists(get_token())
    #SpotifyTools.get_top_tracks(get_token())
    SpotifyTools.get_song_features(get_token())

    #SpotifyTools.create_playlist(session, get_token())

    return render_template("main.html", displayname = displayname)

@app.route('/getinput', methods=['POST'])
def getInput():
    print("get input request")
    input = request.form['user_input']

    #if u wanna try AI, uncomment this
    #print(AI.response(input))


    return home()

@app.route('/getTracks')
def getTracks():
    return SpotifyTools.get_top_tracks(get_token())

@app.route('/login')
def login():
    sp_oauth = SpotifyTools.create_spotify_oauth()
    authURL = sp_oauth.get_authorize_url()
    
    return redirect(authURL)

@app.route('/redirect')
def callback():
    sp_oauth = SpotifyTools.create_spotify_oauth()
    session.clear()
    # if given access, continue to home page
    if request.args.get('code'):
        tokenInfo = sp_oauth.get_access_token(request.args.get('code'))
        session[TOKEN_INFO] = tokenInfo
        sp = spotipy.Spotify(auth=tokenInfo['access_token'])
        userInfo = sp.current_user()
        session[USER_INFO] = userInfo

        return home()

    #if denied access, return to landing page ('/')
    if request.args.get('error'):

        return index()

    #if neither, handle error in future. For now, return message
    return "something went wrong"

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = SpotifyTools.create_spotify_oauth
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def write_to_dotenv(name):
    if name == "SPOTIFY_ACCESS_TOKEN":
        token_info = get_token()
        string = token_info['access_token']
        
    if name == "SPOTIFY_USER_ID":
        string = session['user_info']['id']

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ[name] = string
    dotenv.set_key(dotenv_file, name, os.environ[name])

    # Add tracks to the playlist
        #sp.playlist_add_items(user_playlist['id'], items=track_ids, position=None)

        #return f"Playlist '{playlist_name}' created with {len(track_ids)} tracks."
