import time
from pydantic import BaseModel, Field
from langchain.chains import create_tagging_chain_pydantic
import time
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic

class ResponseFormat(BaseModel):
    playlist_url: str = Field(
        default="Playlist not found",
        description = "A url to a spotify playlist")
    playlist_id: str = Field(
        default="",
        description="The id of a spotify playlist"
    )
    artist_found: bool = Field(
        default=False,
        description="a true or false value")

def filter_ai_response(user_input):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    time.sleep(60)   
    chain = create_tagging_chain_pydantic(ResponseFormat, llm)
    time.sleep(25)   
    response = chain.run(user_input)  
    
    return response