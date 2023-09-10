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
Session(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("main.html")

@app.route('/getinput', methods=['POST'])
def getInput():
    input = request.form['user_input']
    print(input)
    return home()

@app.route('/login')
def login():
    spOauth = create_spotify_oauth()
    authURL = spOauth.get_authorize_url()
    
    return redirect(authURL)

@app.route('/redirect')
def callback():
    
    # if given access, continue to home page
    if request.args.get('code'):
       
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


