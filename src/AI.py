from langchain.llms import GPT4All
from langchain import PromptTemplate, LLMChain, OpenAI, Cohere, HuggingFaceHub, LLMMathChain
from langchain.model_laboratory import ModelLaboratory


from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.agents import AgentType, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from AITopTracksTool import TopTracksTool
from AITopArtistsTool import TopArtistsTool
from AIPlaylistTool import PlaylistTool
from langchain.schema.messages import (
    SystemMessage,
)
from langchain.prompts import MessagesPlaceholder
#Each input given from a user will be a users given situation or mood. Based on the situation or mood that is provided to you, you will rate it based on these features:
content = """
About you:
You are an AI Agent that operates the Spotify API defined as a tool to respond to User's requests. Do not chat to the user, simply use the tools provided to you. If question is off topic, do not reply.


Execution:
You should plan the execution using the Tools provided to you in response to the User's input

Output format:
a link to the playlist created with your PlaylistTool

"""

#llm = OpenAI()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
tools = [TopTracksTool(), PlaylistTool()]
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": SystemMessage(
            content= content
        ),
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, agent_kwargs=agent_kwargs, memory=memory, verbose=True)



#llm chain
#chain = LLMChain(prompt=prompt, llm=llm)

def response(prompt):
    print('thinking...')
    response = mrkl.run(prompt)
    print('here: ')
    return response

#def response(prompt):
#    print("thinking...")
#    response = chain.run(prompt)
#    return response