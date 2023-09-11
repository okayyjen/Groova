from langchain.llms import GPT4All
from langchain import PromptTemplate, LLMChain, OpenAI, Cohere, HuggingFaceHub
from langchain.model_laboratory import ModelLaboratory

#path
#PATH = 'C:/Users/harba/AppData/Local/nomic.ai/GPT4All/ggml-model-gpt4all-falcon-q4_0.bin'
#PATH = 'C:/Users/harba/AppData/Local/nomic.ai/GPT4All/llama-2-7b-chat.ggmlv3.q4_0.bin'
#llm = GPT4All(model=PATH, verbose = True)
#llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature": 1})

llm = OpenAI()

#prompt template
prompt = PromptTemplate(input_variables=['question'], template="""
                        ### Instruction:
                        About you:
                        You are an AI Agent that will rate a the type of music a user should listen to based on the user's given situation / mood based on the things to rate provided to you below. 
                        
                        things to rate:

                        "acousticness":
                            "description": "Confidence measure of whether the track is acoustic.",
                            "example_value": 0.00242,
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
                        
                        DO NOT GIVE SONG SUGGESTIONS.
                        SIMPLY GIVE THE RATINGS.
                        DO NOT SAY ANYTHING ELSE BESIDES THE RATINGS.

                        example response:

                        acousticness: 0.00134
                        danceability: 0.378
                        tempo: 100
                        valence: 0.565
                        energy: 0.235
                
                        ### Prompt:
                        {question}
                        ### Response:""")
#llm chain
chain = LLMChain(prompt=prompt, llm=llm)

def response(prompt):
    print("thinking...")
    response = chain.run(prompt)
    return response