import time
from flask import Flask, request, session, redirect, render_template
from flask_cors import CORS
from flask_session import Session
import spotipy
import os
import SpotifyTools
import AI
import dotenv
from AIPlaylistDetails import PlaylistDetails, generate_question, filter_response, update_details
import constants

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
TOKEN_INFO = "token_info"
USER_INFO = "user_info"
ASK_FOR = "ask_for"
PLAYLIST_DETAILS = "playlist_details"

CORS(app)

Session(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    write_to_dotenv("SPOTIFY_ACCESS_TOKEN")
    write_to_dotenv("SPOTIFY_USER_ID")
    
    #print("AI: ", generate_question(constants.ASK_FOR_INITIAL))    
    
    return redirect('http://localhost:3000/home')

@app.route('/get_display_name')
def get_display_name():

    return SpotifyTools.display_name()

@app.route('/get_initial_interaction')
def get_initial_AI_response():
    

    display_name = get_display_name()

    greeting_message = constants.GREETING_MESSAGE.format(display_name=display_name)
    #getting AI question will go here
    initial_question = "dookie doo, dookie doo doo?"

    return {'greetingMessage': greeting_message, 'initialQuestion': initial_question}

@app.route('/get_user_input', methods=["POST"])
def get_user_input():
    ai_response = 'YUH!'
    react_input = request.get_json()

    print("Input from react: ", react_input)

    user_input = react_input["user_input"]
    playlist_details = set_p_details(react_input["p_details"])
    ask_for = react_input["ask_for"]

    #ask_for, new_details = filter_response(user_input, playlist_details )
    #playlist_details = update_details(playlist_details, new_details)
    
    
    if ask_for:
        #ai_response = generate_question(ask_for)
        print("AI: ", ai_response)     
    else:
        print("thats everything, thank you!:) i'll get to creating your playlist now")
        print(ask_for,  ", ", playlist_details)

    #time.sleep(60)

    return{'updatedAskList':ask_for, 
           'updatedPlaylistDetails':{'playlistName':playlist_details.playlist_name,
                                     'artistName':playlist_details.artist_name,
                                     'userMoodOccasion':playlist_details.user_mood_occasion},
            'AIResponse': ai_response}

def set_p_details(p_details_dict):
    p_details = PlaylistDetails(playlist_name=p_details_dict["playlistName"],
                                artist_name=p_details_dict["artistName"],
                                user_mood_occasion=p_details_dict["userMoodOccasion"])
    
    return p_details
    

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
        
        #initial question from gathering agent
        #print(generate_question(session[ASK_FOR]))
        return home()

    #if denied access, return to landing page ('/')
    if request.args.get('error'):

        return redirect('http://localhost:3000')

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