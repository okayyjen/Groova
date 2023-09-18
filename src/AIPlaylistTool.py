from langchain.tools.base import BaseTool, StructuredTool
import spotipy
import os
import json

class PlaylistTool(BaseTool):
    """Tool that creates a new playlist and adds tracks to it on Spotify."""

    name = "PlaylistTool"
    description = (
        "Use this tool when the user asks you to make a playlist"
        "A tool that creates a new playlist and adds tracks to it on Spotify."
        "The argument tracks is a dictionary list of the user's top tracks, obtained from TopTracksTool"
        "This tool requires a dictionary of tracks as a keyword argument. You will get this from your TopTracksTool. The argument is NOT A STRING"
    )

    def _run(self, tracks, *args, **kwargs) -> str:
        user = os.getenv('SPOTIFY_USER_ID')
        if not user:
            raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
        
        sp = spotipy.Spotify(auth=token)

        # Create a new playlist
        user_playlist = sp.user_playlist_create(user, "New Playlist", public=False, collaborative=False, description="desc")
        #coverting string dictionary into dictionary.
        tracks_dict = json.loads(tracks)
        
        #getting urls from track list
        track_URLs = []
        for track in tracks_dict['items']:
            track_url = track['external_urls']['spotify']
            track_URLs.append(track_url)
        playlist_id = user_playlist['id']
        sp.playlist_add_items(playlist_id, track_URLs, position=None)
        playlist_url = user_playlist['external_urls']['spotify']

        return playlist_url

    async def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")
    


