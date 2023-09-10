from langchain.llms import GPT4All
from langchain import PromptTemplate, LLMChain

#path
PATH = 'C:/Users/harba/AppData/Local/nomic.ai/GPT4All/ggml-model-gpt4all-falcon-q4_0.bin'

llm = GPT4All(model=PATH, verbose = True)

#The prompt below is a question to answer, a task to complete, or a conversation to respond to; decide which and write an appropriate response.
#prompt template
prompt = PromptTemplate(input_variables=['question'], template="""
                        ### Instruction:
                        The prompt below is a human's described situation, or mood. what kind of words would you use to describe the type of music this person should be listening to given their described situation / mood? Give 5 words to describe it in a list format. DO NOT GIVE SONG SUGGESTIONS

                        ### Prompt:
                        {question}
                        ### Response:""")
#llm chain
chain = LLMChain(prompt=prompt, llm=llm)

def response(prompt):
    print("thinking...")
    response = chain.run(prompt)
    return response