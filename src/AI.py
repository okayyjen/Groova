from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from AIPlaylistTool import PlaylistTool
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
import constants

content_chain_1 = PromptTemplate(input_variables=['user_mood'], template=constants.CONTENT_CHAIN_1)

content_chain_2 = constants.CONTENT_CHAIN_2

#language model that BOTH chains will be using
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")

#initializing feature rating agent --> aka first chain 
feature_rating_chain = LLMChain(prompt=content_chain_1, llm=llm)

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

def get_feature_rating(user_prompt):
    print("thinking...")
    feature_rating = feature_rating_chain.run(user_prompt)
    print('your rating is: ')
    return feature_rating

def playlist_generate(rating):
    print('thinking bout dooks...')
    response = mrkl.run(rating)
    print('here: ')
    return response