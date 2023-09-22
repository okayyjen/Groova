from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from AIPlaylistTool import PlaylistTool
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder

content_chain_1 = PromptTemplate(input_variables=['user_mood'], template="""
                        ### Instruction:
                        About you:
                        You are an AI Agent tasked with rating the type of music a user should listen to based on the user's given situation or mood, using the music attributes provided below.Please provide ratings based on your assessment, and do not rely on the example values I have given you. Do not reply on your past answers.
                        
                        Music attributes:

                        "acousticness":
                            "description": "Confidence measure of whether the track is acoustic.",
                            "example_value": 0.242,
                            "range": "0 - 1"
                        ,
                        "danceability": 
                            "description": "How suitable a track is for dancing.",
                            "example_value": 0.585
                        
                        "tempo": 
                            "description": "Estimated tempo of a track in BPM.",
                            "example_value": 118.211
                        
                        "valence": 
                            "description": "Musical positiveness conveyed by a track.",
                            "example_value": 0.428,
                            "range": "0 - 1"
                        
                        "energy": 
                            "description": "Perceptual measure of intensity and activity.",
                            "example_value": 0.842
                        
                        --end of things to rate--

                        The prompt you will be given is a human's described situation, or mood.
                        
                        RULES:
                        follow the response template below

                        response template (where each "x" should be replaced with your number rating for each corresponding music attribute):

                        acousticness: x
                        danceability: x
                        tempo: x
                        valence: x
                        energy: x
                
                        ### Prompt:
                        {user_mood}
                        ### Response:""")

content_chain_2 = """
About you:
You are an AI Agent that operates the Spotify API defined as a tool to respond to User's requests. Do not chat to the user, simply use the PlaylistTool provided to you. 

Execution:
You should plan the execution using the PlaylistTool provided to you using the user's input

Output format:
print the return statement from your PlaylistTool

"""

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




#// going to return feature ratings
#chain1(user_input)
#    return feature_rating

#//going to create playlist based on feature ratings
#chain2(feature_rating)
#    return playlist 


#get_rating --rating-->playlist_agent == outputs playlist












