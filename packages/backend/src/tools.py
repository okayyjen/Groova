import time
from flask import session
import spotify_tools
from constants import TOKEN_INFO
import dotenv
import os

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = spotify_tools.create_spotify_oauth
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