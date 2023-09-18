from langchain.tools.base import BaseTool
import spotipy
import json
import os


class TopTracksTool(BaseTool):
    """Tool that fetches the user's top 5 tracks."""

    name = "TopTracksTool"
    description = (
        "Tool that fetches the user's top 5 tracks."
        "Use this tool when getting a dictionary list of tracks to add to a new playlist"
        "This tool does not require any arguments."
    )

    def _run(self, *args, **kwargs) -> str:
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("token not found in dotenv")
        sp = spotipy.Spotify(auth=token)
        
        #fetching top 5 tracks of user
        tracks = sp.current_user_top_tracks(time_range='medium_term', limit=5, offset=0)
        print("toptracks", type(tracks))
        return tracks
    
    def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")

  