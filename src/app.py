from flask import Flask, request, url_for,session, redirect, render_template
from flask_session import Session
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

clientID = os.getenv("SPOTIPY_CLIENT_ID")
clientSecret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirectURI = os.getenv("SPOTIPY_REDIRECT_URI")

app.sercret_key = "AKjhnd79Huha"
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
    displayname = get_display_name()
    return render_template("main.html", displayname = displayname)

@app.route('/login')
def login():
    spOauth = create_spotify_oauth()
    authURL = spOauth.get_authorize_url()
    
    return redirect(authURL)

@app.route('/redirect')
def callback():
    spOauth = create_spotify_oauth()
    session.clear()
    # if given access, continue to home page
    if request.args.get('code'):
        tokenInfo = spOauth.get_access_token(request.args.get('code'))
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
    
#do not have this as global variable. create new oauth object for each use
def create_spotify_oauth():
    return spotipy.oauth2.SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=url_for('callback', _external=True),
            scope="user-library-read")

def get_display_name():
    return session[USER_INFO]['display_name']