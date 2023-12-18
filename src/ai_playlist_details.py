from typing import List
from pydantic import BaseModel, Field
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic, LLMChain

class PlaylistDetails(BaseModel):
    
    user_mood_occasion: str = Field(
        default="",
        description="This is the mood or the occasion that the playlist will be based on. The user may give any mood or occasion."
    )

    artist_names: List[str] = Field(
        default=None,
        description="This is a list of artist names that a user would like to be featured on the playlist"
    )

    playlist_name: str = Field(
        default="",
        description="This is the name of a playlist that the user will choose."
    )

#language model that ALL chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

#this function takes a playlist details objects, and returns a list of its missing fields. playlist_details->[]
def check_empty_fields(playlist_details):
    print("CHECK_EMPTY_FIELDS ", playlist_details)
    ask_for = []
    # Check if fields are empty
    for field, value in playlist_details.dict().items():
        if value in [None, "", 0]:  # You can add other 'empty' conditions as per your requirements
            print(f"Field '{field}' is empty.")
            ask_for.append(f'{field}')
    print("EMPTY FIELDS FUNC", ask_for)

    return ask_for

#this function takes the playlist details object with all previously attained playlist details and an additional playlist details object containing new details, and 
# returns a new object with the combined information
def update_details(current_playlist_details: PlaylistDetails, new_playlist_details: PlaylistDetails):
    non_empty_details = {k: v for k, v in new_playlist_details.dict().items() if v not in [None, ""]}
    updated_details = current_playlist_details.copy(update=non_empty_details)
    print("UPDATED DETAILS FROM FUNCTION: ", updated_details)
    return updated_details

#given a list of things to ask for, this function generates a new question in order to fill in missing details
def generate_question(ask_for):
    # prompt template 1
    first_prompt = ChatPromptTemplate.from_template(constants.CONTENT_CHAIN_QUESTION_GENERATE)
    # a chain used for gathering a users playlist details
    question_generating_chain = LLMChain(llm=llm, prompt=first_prompt)
    print("RUNNING QUESTION CHAIN WITH THIS LIST: ", ask_for)
    
    question = question_generating_chain.run(ask_for)
    
    return question

#this function takes in the users response (user_input) to the gathering agent's question and their current playlist details.
# it then filters the user response, and extracts relevant playlist details, and adds them to the user's current playlist details object.
# the return is the users updated playlist details, and the new ask_for list containing missing details 
def filter_response(user_input, playlist_details ):
    
    chain = create_tagging_chain_pydantic(PlaylistDetails, llm, prompt=ChatPromptTemplate.from_template(constants.CONTENT_CHAIN_PYDANTIC))
    
    res = chain.run(user_input)
    # add filtered info to the
    new_playlist_details = update_details(playlist_details,res)

    ask_for = check_empty_fields(new_playlist_details)
    print("NEW ASK FOR RETRIEVED IN FILTER RESPONSE ", ask_for)
    print("NEW PLAYLIST DETAILS AFTER UPDATE: ", new_playlist_details)

    return ask_for, new_playlist_details

def set_p_details(p_details_dict):
    p_details = PlaylistDetails(user_mood_occasion=p_details_dict["userMoodOccasion"],
                                artist_names=p_details_dict["artistNames"],
                                playlist_name=p_details_dict["playlistName"])

    return p_details



