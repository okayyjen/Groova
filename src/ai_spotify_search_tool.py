from langchain.tools.base import BaseTool
import spotipy
import os
import spotify_tools

class SpotifySearchTool(BaseTool):
    """Tool that searches Spotify for a specific track by a specific artist to verify the track is on Spotify."""

    name = "SpotifySearchTool"
    description = (
        "Descriptors go here"

    )

    def _run(self, s:str, *args, **kwargs) -> str:


        return 'hi'

    async def _arun(self, input,args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")