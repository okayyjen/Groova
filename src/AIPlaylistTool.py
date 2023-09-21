from langchain.tools.base import BaseTool, StructuredTool
import spotipy
import os
import json

class PlaylistTool(BaseTool):
    """Tool that creates a new playlist and adds tracks to it on Spotify."""

    name = "PlaylistTool"
    description = (
        "Always use this tool when given input"
        "This tool requires a string representation of musical features as a keyword argument. You will get this from the input given to you. The argument is A STRING"
        "Features is the input you received from the user"
    )

    def _run(self, features,*args, **kwargs) -> str:
        user = os.getenv('SPOTIFY_USER_ID')
        if not user:
            raise ValueError("SPOTIFY_USER_ID environment variable is not set.")
        
        token = os.getenv('SPOTIFY_ACCESS_TOKEN')
        if not token:
            raise ValueError("SPOTIFY_ACCESS_TOKEN environment variable is not set.")
        

        return features

    async def _arun(self, features,*args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")
    


