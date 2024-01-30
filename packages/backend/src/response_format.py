from typing import List
from pydantic import BaseModel, Field
from langchain.chains import create_tagging_chain_pydantic
import constants
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class SongInfo(BaseModel):
    song_name: str = Field(..., description="The name of the song")
    artist_name_list: List[str] = Field(..., description="A list of all artists on the song")

class ResponseFormat(BaseModel):
    song_list: List[SongInfo] = Field(
        default=None,
        description="A list of songs, each represented as a dictionary with 'song_name' and 'artist_name_list' fields."
    )

def filter_ai_response(user_input):
    print("before: ", user_input)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = create_tagging_chain_pydantic(ResponseFormat, llm, prompt=ChatPromptTemplate.from_template(constants.CONTENT_CHAIN_PYDANTIC_2))
    response = chain.run(user_input)
    print("after: ", response.song_list)
    print("length ", len(response.song_list))
    return response