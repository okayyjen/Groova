import time
from flask import session
import yaml
import spotify_tools
from constants import TOKEN_INFO
import yaml_tools
import key

def get_token(session):
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = spotify_tools.create_spotify_oauth(session)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def write_token(name, session):
    if name == "SPOTIFY_ACCESS_TOKEN":
        token_info = get_token(session)
        string = token_info['access_token']

    if name == "SPOTIFY_USER_ID":
        string = session['user_info']['id']

    string = yaml_tools.encrypt(string, key.key)


    with open('configuration/access_token.yml', 'r') as file:
        data = yaml.safe_load(file)

    data[name] = string

    with open('configuration/access_token.yml', 'w') as file:
        yaml.dump(data, file)