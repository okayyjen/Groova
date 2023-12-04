from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from ai_playlist_tool import PlaylistTool
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import ai_playlist_details
import response_format

content_chain_1 = PromptTemplate(input_variables=['user_mood'], template=constants.CONTENT_CHAIN_1)
content_chain_2 = constants.CONTENT_CHAIN_2
content_chain_3 = PromptTemplate(input_variables=['ask_for'], template=constants.CONTENT_CHAIN_3)
content_chain_5 = PromptTemplate(input_variables=['include_greeting','instructions'], template=constants.CONTENT_CHAIN_5)

content_chain_1_new = PromptTemplate(input_variables=['keywords'], template=constants.CONTENT_CHAIN_CHAIN_NEW)

#language model that BOTH chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

#new AI TESTING agent
song_curator = LLMChain(prompt=content_chain_1_new, llm=llm)

#initializing feature rating agent 
feature_rating_chain = LLMChain(prompt=content_chain_1, llm=llm)

#initializing message chain
messenger_chain = LLMChain(prompt=content_chain_5, llm=llm)

#initializing tool agent chain (aka second chain/ tool chain)
tools = [PlaylistTool()]
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": SystemMessage(
            content= content_chain_2
        ),
}

memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, agent_kwargs=agent_kwargs, memory=memory, verbose=True)

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

def generate_playlist_ai(features_genres_pdetails):
    response = mrkl.run(features_genres_pdetails)
    return response

def curate_songs(keywords):
    song_list = song_curator.run(keywords)

    song_list_filtered = response_format.filter_ai_response(song_list)

    return song_list_filtered