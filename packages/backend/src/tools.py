import time
from flask import session
import spotify_tools
from constants import TOKEN_INFO

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