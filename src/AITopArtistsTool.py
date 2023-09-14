from langchain.tools.base import BaseTool
import spotipy
import json
import os


class TopArtistsTool(BaseTool):
    """Tool that fetches the user's top 5 artists."""

    name = "TopArtistsTool"
    description = (
        "Tool that fetches the user's top 5 artists."

        "Use this tool when the user is asking who their top artists are."
        "Use this tool when the user is asking what their top songs are"
        "This tool does not require any arguments."
    )

    def _run(self, *args, **kwargs) -> str:
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("token not found in dotenv")
        sp = spotipy.Spotify(auth=token)

        #fetching top 5 artists of user
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)
        # Extract artist names from the response
        artist_names = [artist['name'] for artist in top_artists['items']]

        #top artists can be found in artist_names_json
        artist_names_json = json.dumps(artist_names)

        return artist_names_json
    
    def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")

  