from enum import Enum
import time
from pydantic import BaseModel, Field
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic, LLMChain, TransformChain, SimpleSequentialChain

class PlaylistDetails(BaseModel):
    playlist_name: str = Field(
        default="",
        description="This is the name chosen by the user of the playlist that we are creating"
    )
    artist_name: str = Field(
        default="",
        description="This is the name of an artist that a user would like to be featured on the playlist"
    )
    user_mood_occasion: str = Field(
        default="",
        description="This is the mood or the occasion that the playlist will be based on. The user may give any mood or occasion."
    )

ask_for_list = ['playlist_name', 'artist_name', 'user_mood_occasion']
playlist_details_initial = PlaylistDetails(playlist_name="",
                                artist_name="",
                                user_mood_occasion="")

content_chain_3 = ChatPromptTemplate.from_template(constants.CONTENT_CHAIN_3)

#language model that ALL chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")

#initializing form agent to extract information from user input
pydantic_chain = create_tagging_chain_pydantic(PlaylistDetails, llm)
playlist_detail_gathering_chain = LLMChain(prompt=content_chain_3, llm=llm)


first_prompt = ChatPromptTemplate.from_template(template=constants.CONTENT_CHAIN_3)


#call ai to ask question about whatever is left over on the list given
def ask_question(ask_for):
    print("ASK_Q_SLEEP")
    time.sleep(20)
    info_gathering_chain = LLMChain(llm=llm, prompt=first_prompt)
    question = info_gathering_chain.run(ask_for)

    return question

#pass user response here, and add 
def filter_response(text_input, playlist_details ):
    print("FILTER_RESP_SLEEP")
    time.sleep(20)
    chain = create_tagging_chain_pydantic(PlaylistDetails, llm)
    print("FILTER_RESP_SLEEP")
    time.sleep(20)
    res = chain.run(text_input)
    # add filtered info to playlist_details, and check whatever is left over on the ask_for list (list of missing details)
    playlist_details = add_non_empty_details(playlist_details,res)
    ask_for = check_what_is_empty(playlist_details)
    return playlist_details, ask_for

def run_it_betch(playlist_details, ask_for, user_input):
    if ask_for:
        print("ASK_FOR_SLEEP")
        time.sleep(20)
        print(ask_question(ask_for))
        print("ASK_FOR_SLEEP")
        time.sleep(20)
        playlist_details, ask_for = filter_response(user_input, playlist_details)
        

    print("RUN_IT_BETCH RETURN")
    return playlist_details




    


















## checking the response and adding it
def add_non_empty_details(current_details: PlaylistDetails, new_details: PlaylistDetails):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details

def check_what_is_empty(user_peronal_details):
    ask_for = []
    # Check if fields are empty
    for field, value in user_peronal_details.dict().items():
        if value in [None, "", 0]:  # You can add other 'empty' conditions as per your requirements
            print(f"Field '{field}' is empty.")
            ask_for.append(f'{field}')
    return ask_for