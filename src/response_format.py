import time
from typing import List
from pydantic import BaseModel, Field
from langchain.chains import create_tagging_chain_pydantic
import time
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic

class ResponseFormat(BaseModel):
    song_list: List[str] = Field(
        default=None,
        description = "A list of 45 song names. No artist names included.")


def filter_ai_response(user_input):
    print("before: ", user_input)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = create_tagging_chain_pydantic(ResponseFormat, llm)
    response = chain.run(user_input)  
    print("after: ", response.song_list)
    return response