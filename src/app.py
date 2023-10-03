import time
from flask import Flask, jsonify, request, session, redirect, render_template
from flask_session import Session
import spotipy
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

@app.route('/get_display_name')
def get_display_name():

    return SpotifyTools.display_name()

@app.route('/home')
def home():
    
    write_to_dotenv("SPOTIFY_ACCESS_TOKEN")
    write_to_dotenv("SPOTIFY_USER_ID")

    return redirect('http://localhost:3000/home')

    

@app.route('/getinput', methods=['POST'])
def getInput():
    print("get input request")
    input = request.form['user_input']

    #if u wanna try AI, uncomment this
    rating = AI.get_feature_rating(input)#returns ratings
    #AI.playlist_generate(rating)


    return AI.playlist_generate(rating)

@app.route('/getTracks')
def getTracks():
    return SpotifyTools.get_top_tracks(get_token())

@app.route('/login')
def login():
    sp_oauth = SpotifyTools.create_spotify_oauth()
    authURL = sp_oauth.get_authorize_url()
    
    return authURL

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
        session.modified = True

        return home()


    #if denied access, return to landing page ('/') 
    if request.args.get('error'):

        return redirect('http://localhost:3000')

    #if neither, handle error in future. For now, return message
    return "something went wrong ERRA ERRA"

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