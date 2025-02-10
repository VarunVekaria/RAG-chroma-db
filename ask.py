import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="ai_coding_assistant")


user_query = input("What do you need help with? ")

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

print(results['documents'])
#print(results['metadatas'])

client = OpenAI()

system_prompt = """
You are a helpful assistant who is master at coding. You answer questions and give informational paragraphs based on the data provided to you.
You answer should be based on knowledge I'm providing you. You use your internal 
knowledge in a limited fashion but DO NOT MAKE THINGS UP. You may paraphrase a bit here and there and you may answer 
even if the information presented to you is not 100 percent informative towards the question.
If you don't know the answer, just say: I don't know
--------------------
The data:
"""+str(results['documents'])+"""
"""

#print(system_prompt)

response = client.chat.completions.create(
    model="gpt-4o",
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}    
    ]
)

print("\n\n---------------------\n\n")

print(response.choices[0].message.content)