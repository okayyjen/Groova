import json
from langchain.tools.base import BaseTool
import spotipy
import os
import SpotifyTools

class PlaylistTool(BaseTool):
    """Tool that creates a new playlist and adds tracks to it on Spotify based on the given features and genres received on input."""

    name = "PlaylistTool"
    description = (
        "Always use this tool when given input"
        "This tool requires a string representation of musical features, genres, and details of a playlist (including playlistName, artistName, and userMoodOccasion) as one keyword argument. You will get this from the input given to you. The argument is A STRING. This STRING also contains curly braces, but they must be read as strings"
        "The features_genres_pdetails argument is the input you have received"
        "The return statement of this function is a dictionary of the link to the spotify playlist you have created, as well as the result of whether or not we have found an artist that matches avaiable on Spotify."
    )

    def _run(self, features_genres_pdetails:str,*args, **kwargs) -> str:
        user = os.getenv('SPOTIFY_USER_ID')
        if not user:
            raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
        
        print("RECEIVED ",features_genres_pdetails)

        #convert string dict into dict
        features_dict, genre_list, pdetails_dict = SpotifyTools.extract_and_format(features_genres_pdetails)
        print("PDEETS DICT: ", pdetails_dict)
        sp = spotipy.Spotify(auth=token)

        # Create a new empty playlist
        user_playlist = sp.user_playlist_create(user, pdetails_dict['playlistName'], public=False, collaborative=False, description="Made with Groova")

        #if the user given artist exists, add it to artist_URLs, if not, use user's top artist
        artist_URLs = []

        preferred_artist_url = SpotifyTools.get_artist_link(pdetails_dict['artistName'])

        if(preferred_artist_url):
            artist_found = True
            artist_URLs.append(preferred_artist_url)
        else:
            artist_found = False
            top_artists = sp.current_user_top_artists(time_range='medium_term', limit=1)
            artist_name = top_artists['items'][0]['name']
            top_artist_url = SpotifyTools.get_artist_link(artist_name)
            artist_URLs.append(top_artist_url)
            
        #get recommended tracks based on users top artists and features
        #recommended_tracks = sp.recommendations(seed_artists=artist_URLs, seed_genres= genre_list , limit=20, target_features=features_dict)
        recommended_tracks = sp.recommendations(seed_artists=artist_URLs, limit=20, target_features=features_dict)
        recommended_track_uris = [track['uri'] for track in recommended_tracks['tracks']]
        playlist_id = user_playlist['id']

        #add tracks to playlist
        sp.playlist_add_items(playlist_id, recommended_track_uris, position=None)
        playlist_url = user_playlist['external_urls']['spotify']

        return {'playlist_url': playlist_url,
                'artist_found': artist_found}

    async def _arun(self, features_genres_pdetails,*args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")
    


