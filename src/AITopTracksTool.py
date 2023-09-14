from langchain.tools.base import BaseTool
import spotipy
import json
import os


class TopTracksTool(BaseTool):
    """Tool that fetches the user's top 5 tracks."""

    name = "TopTracksTool"
    description = (
        "Tool that fetches the user's top 5 tracks."
        "Use this tool when the user is asking what their top tracks (also referred to as: songs) are"
        "This tool does not require any arguments."
    )

    def _run(self, *args, **kwargs) -> str:
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("token not found in dotenv")
        sp = spotipy.Spotify(auth=token)
        

        #fetching top 5 tracks of user
        top_tracks = sp.current_user_top_tracks(time_range='medium_term', limit=5, offset=0)

        #extract track names from response
        top_tracks_names = [track['name'] for track in top_tracks['items']]

        #top tracks can be found in top_tracks_names_json
        top_tracks_names_json = json.dumps(top_tracks_names)

        return top_tracks_names_json
    
    def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")

  