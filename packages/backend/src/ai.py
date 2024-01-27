from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import ai_playlist_details
import response_format
from dotenv import load_dotenv

load_dotenv()

content_chain_curator = PromptTemplate(input_variables=['keywords'], template=constants.CONTENT_CHAIN_CURATOR)
content_chain_feature_rating = PromptTemplate(input_variables=['user_mood'], template=constants.CONTENT_CHAIN_FEATURE_RATING)
content_chain_messenger = PromptTemplate(input_variables=['include_greeting','instructions'], template=constants.CONTENT_CHAIN_MESSENGER)

#language model that BOTH chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

#song curator agent
song_curator = LLMChain(prompt=content_chain_curator, llm=llm, verbose=True)

#initializing feature rating agent 
feature_rating_chain = LLMChain(prompt=content_chain_feature_rating, llm=llm)

#initializing message chain
messenger_chain = LLMChain(prompt=content_chain_messenger, llm=llm)

#information gathering chain
def gather_playlist_details(user_input, ask_for, playlist_details):
    if ask_for:
        print(ai_playlist_details.ask_question(ask_for))
        playlist_details, ask_for = ai_playlist_details.filter_response(user_input, playlist_details)
        
    return playlist_details

#generative functions
def generate_feature_rating(user_prompt):
    features_and_genres = feature_rating_chain.run(user_prompt)
    return features_and_genres

def generate_message(input_dict):
    message = messenger_chain.run(input_dict)
    return message


def curate_songs(keywords):
    song_list = song_curator.run(keywords)

    song_list_filtered = response_format.filter_ai_response(song_list)

    return song_list_filtered