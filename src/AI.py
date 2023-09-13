from langchain.llms import GPT4All
from langchain import PromptTemplate, LLMChain, OpenAI, Cohere, HuggingFaceHub, LLMMathChain
from langchain.model_laboratory import ModelLaboratory


from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.agents import AgentType, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from SpotifyAITool import DookTool

from langchain.schema.messages import (
    SystemMessage,
)

sys_msg = """
About you:
You are an AI Agent that operates the Spotify API defined as a tool to respond to User's requests. Do not chat to the user, simply use the tools provided to you. If question is off topic, do not reply.

Execution:
You should plan the execution using the Tool in response to the User's input

Output format (where each '?' is a name from the list returned from your SpotifyTool):
1.'?'
2.'?'
3.'?'
4.'?'
5.'?'

"""

#llm = OpenAI()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

conversational_memory = ConversationBufferMemory(
    memory_key='chat_history',
    k=2,
    return_messages=True
)

tools = [DookTool()]


agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    max_iterations=2,
    early_stopping_method='generate',
    memory=conversational_memory
)

new_prompt = agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)

agent.agent.llm_chain.prompt = new_prompt



#llm chain
#chain = LLMChain(prompt=prompt, llm=llm)

def response(prompt):
    print('thinking...')
    response = agent(prompt)
    return response

#def response(prompt):
#    print("thinking...")
#    response = chain.run(prompt)
#    return response