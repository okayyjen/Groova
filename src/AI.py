from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from AIPlaylistTool import PlaylistTool
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic, LLMChain, TransformChain, SimpleSequentialChain
from AIPlaylistDetails import PlaylistDetails
import AIPlaylistDetails

content_chain_1 = PromptTemplate(input_variables=['user_mood'], template=constants.CONTENT_CHAIN_1)
content_chain_2 = constants.CONTENT_CHAIN_2
content_chain_3 = PromptTemplate(input_variables=['ask_for'], template=constants.CONTENT_CHAIN_3)
content_chain_5 = PromptTemplate(input_variables=['include_greeting','instructions'], template=constants.CONTENT_CHAIN_5)

#language model that BOTH chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")

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

#functions to run chains and pass chain 1 response to chain 2

def gather_playlist_details(user_input, ask_for, playlist_details):
    if ask_for:
        print(AIPlaylistDetails.ask_question(ask_for))
        playlist_details, ask_for = AIPlaylistDetails.filter_response(user_input, playlist_details)
        
    return playlist_details

def get_feature_rating(user_prompt):
    print("thinking...")
    features_and_genres = feature_rating_chain.run(user_prompt)
    print('your rating is: ')
    return features_and_genres

def playlist_generate(features_genres_pdetails):
    print('thinking bout dooks...')
    response = mrkl.run(features_genres_pdetails)
    print('here: ')
    return response

def generate_message(input_dict):
    message = messenger_chain.run(input_dict)
    return message