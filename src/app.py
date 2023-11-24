import time
from flask import Flask, request, session, redirect, render_template
from flask_cors import CORS
from flask_session import Session
import spotipy
import os
from ai_playlist_details import set_p_details
from constants import TOKEN_INFO, USER_INFO
from tools import get_token, refresh_token, write_to_dotenv
import spotify_tools
import ai
from ai_playlist_details import generate_question, filter_response, update_details 
import constants

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

CORS(app)

Session(app)

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/Home')
def home():

    write_to_dotenv("SPOTIFY_ACCESS_TOKEN")
    write_to_dotenv("SPOTIFY_USER_ID")
    refresh_token() 

    return redirect('http://localhost:3000/home')

@app.route('/get_display_name')
def get_display_name():

    return spotify_tools.display_name()

@app.route('/get_greeting_message', methods=["POST"])
def get_greeting_message():

    react_input = request.get_json()
    display_name = react_input['display_name']

    greeting_message = constants.GREETING_MESSAGE.format(display_name=display_name)

    input_dict = {'include_greeting': True,
                      'instructions': (constants.GREETING_INSTRUCTIONS.format(display_name=display_name))

                 }
    
    greeting_message = ai.generate_message(input_dict)
    
    return{'greetingMessage': greeting_message}

@app.route('/get_initial_question')
def get_initial_AI_response():

    initial_question = generate_question(constants.ASK_FOR_INITIAL)

    return {'initialQuestion': initial_question}

#TODO reset function here
@app.route('/initiate_new_playlist')
def initiate_new_playlist():
    return 'hi'

@app.route('/get_user_pic')
def get_user_pic():

    return spotify_tools.user_pic()

@app.route('/get_user_input', methods=["POST"])
def get_user_input():

    react_input = request.get_json()

    print("Input from react: ", react_input)

    ai_prev_question = react_input["ai_response"]
    ai_prev_question = ai_prev_question + " "
    
    user_input = react_input["user_input"]

    user_input_question = "".join([ai_prev_question, user_input])

    playlist_details = set_p_details(react_input["p_details"])
    ask_for = react_input["ask_for"]

    ask_for, new_details = filter_response(user_input_question, playlist_details)
    playlist_details = update_details(playlist_details, new_details)
    
    if ask_for:
        ai_response = generate_question(ask_for)
        print("AI: ", ai_response)
    else:
        input_dict = {'include_greeting': False,
                      'instructions': constants.WORKING_INSTRUCTIONS}
        ai_response = ai.generate_message(input_dict)

    time.sleep(45)

    return{'updatedAskList':ask_for, 
           'updatedPlaylistDetails':{'userMoodOccasion':playlist_details.user_mood_occasion,
                                     'artistNames':playlist_details.artist_names,
                                     'playlistName':playlist_details.playlist_name
                                     },
            'AIResponse': ai_response}

@app.route('/generate_playlist', methods=["POST"])
def generate_playlist():
    react_input = request.get_json()

    playlist_details_input = react_input['playlist_details']
    user_mood = playlist_details_input['userMoodOccasion']

    features_and_genres = ai.generate_feature_rating(user_mood) 
    playlist_details = set_p_details(playlist_details_input)

    generated = spotify_tools.create_playlist(features_and_genres, playlist_details)

    playlist_url = generated['playlist_url']

    playlist_id = generated['playlist_id']

    artist_not_found_list = generated['artist_not_found_list']

    if artist_not_found_list:
        #ai_response = constants.ARTIST_NOT_FOUND_MESSAGE
        input_dict = {'include_greeting': False,
                      'instructions': constants.ARTIST_NOT_FOUND_INSTRUCTION.format(artist_not_found_list=artist_not_found_list)
        }
        ai_response = ai.generate_message(input_dict)
    else:
        ai_response = "True"
    
    return {
        'playlistUrl': playlist_url,
        'playlistID': playlist_id,
        'AIResponse': ai_response
    }

@app.route('/getTracks')
def getTracks():

    return spotify_tools.get_top_tracks(get_token())

@app.route('/login')
def login():

    sp_oauth = spotify_tools.create_spotify_oauth()
    authURL = sp_oauth.get_authorize_url()
    
    return authURL

@app.route('/redirect')
def callback():
    sp_oauth = spotify_tools.create_spotify_oauth()
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

        return redirect('http://localhost:3000')

    #TODO if neither, handle error in future. For now, return message
    return "something went wrong"


