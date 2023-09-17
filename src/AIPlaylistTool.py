from langchain.tools.base import BaseTool, StructuredTool
import spotipy
import os

class PlaylistTool(BaseTool):
    """Tool that creates a new playlist and adds tracks to it on Spotify."""

    name = "PlaylistTool"
    description = (
        "Use this tool when the user asks you to make a playlist"
        "A tool that creates a new playlist and adds tracks to it on Spotify."
        "The playlist name is the name of the new playlist to be created."
        "The playlist description is a description for the new playlist, just put the word empty"
        "The arguments should be passed as keyword arguments like so: tool._run(playlist_name='the dance music', playlist_description='danceable music')"
    )

    def _run(self, *args, **kwargs) -> str:
        user = os.getenv('SPOTIFY_USER_ID')
        if not user:
            raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
        
        sp = spotipy.Spotify(auth=token)

        # Create a new playlist
        user_playlist = sp.user_playlist_create(user, "New Playlist", public=False, collaborative=False, description="desc")
        playlist_url = user_playlist['external_urls']['spotify']
        

        return playlist_url

    async def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")
    


