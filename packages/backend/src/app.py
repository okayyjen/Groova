from flask import Flask, request, session, redirect
from flask_cors import CORS
from flask_session import Session
import spotipy
import os
from constants import TOKEN_INFO, USER_INFO
from tools import get_token, write_token
import spotify_tools
import ai
from ai_playlist_details import generate_question, filter_response, update_details, set_p_details 
import constants
import key

app = Flask(__name__)

app.config['SECRET_KEY'] = '4evJEHqfPw1epn0Z5MLQUw=='
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

CORS(app)

Session(app)

@app.route('/')
def index():

    return "Hello, world!-Jenny & Amirah"

@app.route('/api/Home')
def home():

    return redirect('http://localhost:3000/home')

@app.route('/api/get_display_name')
def get_display_name():

    return spotify_tools.display_name()

@app.route('/api/get_greeting_message', methods=["POST"])
def get_greeting_message():

    react_input = request.get_json()
    display_name = react_input['display_name']

    input_dict = {'include_greeting': True,
                  'instructions': (constants.GREETING_INSTRUCTIONS.format(display_name=display_name))
                 }
    
    #greeting_message = ai.generate_message(input_dict)
    greeting_message = 'yuh'
    return{'greetingMessage': greeting_message}

@app.route('/api/get_initial_question')
def get_initial_AI_response():

    #initial_question = generate_question(constants.ASK_FOR_INITIAL)
    initial_question = 'yuh?'
    return {'initialQuestion': initial_question}

@app.route('/api/get_user_pic')
def get_user_pic():

    return spotify_tools.user_pic()

@app.route('/api/get_user_input', methods=["POST"])
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

    ai_comment = ""
    
    if ask_for:

        input_dict = {'include_greeting': False,
                      'instructions': constants.COMMENT_INSTRUCTIONS.format(user_input=user_input)}
        
        ai_comment = ai.generate_message(input_dict)

        ai_response = generate_question(ask_for)

    else:
        input_dict = {'include_greeting': False,
                      'instructions': constants.WORKING_INSTRUCTIONS}
        ai_response = ai.generate_message(input_dict)

    return{'updatedAskList':ask_for, 
           'updatedPlaylistDetails':{'userMoodOccasion':playlist_details.user_mood_occasion,
                                     'artistNames':playlist_details.artist_names,
                                     'playlistName':playlist_details.playlist_name
                                     },
            'AIResponse': ai_response,
            'AIComment': ai_comment}

@app.route('/api/generate_playlist', methods=["POST"])
def generate_playlist():

    react_input = request.get_json()
    playlist_details_input = react_input['playlist_details']
    user_mood = playlist_details_input['userMoodOccasion']

    keywords_list = playlist_details_input['artistNames']
    keywords_list.append(user_mood)

    input_dict = {'include_greeting': True,
                  'instructions': (constants.COMPLETE_INSTRUCTIONS)
                 }
    
    ai_response = ai.generate_message(input_dict)

    try: 
        songs = ai.curate_songs(keywords_list)
        playlist = spotify_tools.create_playlist_song_list(songs.song_list, playlist_details_input['playlistName'])
        
    except Exception as e:
        print(f"First attempt failed: {e}")
        try:
            songs = ai.curate_songs(keywords_list)
            playlist = spotify_tools.create_playlist_song_list(songs.song_list, playlist_details_input['playlistName'])
        except Exception as e:
            print(f"Second attempt failed, initiating alternate method: {e}")
            features_and_genres = ai.generate_feature_rating(user_mood)
            playlist_details = set_p_details(playlist_details_input)
            playlist = spotify_tools.create_playlist(features_and_genres, playlist_details)
    
    

    return {
        'playlistUrl': playlist['playlist_url'],
        'playlistID': playlist['playlist_id'],
        'AIResponse': ai_response
    }


@app.route('/api/getTracks')
def getTracks():

    return spotify_tools.get_top_tracks(get_token(session))

@app.route('/api/login')
def login():

    sp_oauth = spotify_tools.create_spotify_oauth(session)
    authURL = sp_oauth.get_authorize_url()
    
    return authURL

@app.route('/api/redirect')
def callback():

    sp_oauth = spotify_tools.create_spotify_oauth(session)
    session.clear()
    
    # if given access, continue to home page
    
    if request.args.get('code'):
        tokenInfo = sp_oauth.get_access_token(request.args.get('code'))
        session[TOKEN_INFO] = tokenInfo
        sp = spotipy.Spotify(auth=tokenInfo['access_token'])
        userInfo = sp.current_user()
        session[USER_INFO] = userInfo
        #write_token("SPOTIFY_ACCESS_TOKEN")
        #write_token("SPOTIFY_USER_ID")
        return home()

    return redirect('http://localhost:3000')
