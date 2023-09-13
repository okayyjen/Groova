from langchain.tools.base import BaseTool
import spotipy
import json
import os


class DookTool(BaseTool):
    """Tool that fetches the user's top 10 artists."""

    name = "DookTool"
    description = (
        "Tool that fetches the user's top 10 artists."
        "Use this tool when the user is asking who their top artists are."
        "This tool does not require any arguments."
    )

    def _run(self, *args, **kwargs) -> str:
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("token not found in dotenv")
        sp = spotipy.Spotify(auth=token)
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)
        # Extract artist names from the response
        artist_names = [artist['name'] for artist in top_artists['items']]
        artist_names_json = json.dumps(artist_names)


        return artist_names_json
    
    def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")

  