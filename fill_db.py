from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import os
from  openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

client = OpenAI()

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# client = Op


class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata


def summarize_functions_with_openai(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        code = file.read()
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who summarizes functions in Python code."},
            {"role": "user", "content": f"Summarize the functions in the following Python code:\n\n{code}"}
        ],
        max_tokens=150
    )
    
    return response.choices[0].message.content

# loading the document

raw_documents = []
for root, _, files in os.walk(DATA_PATH):
    for file in files:
        print(file)
        if file.endswith(".py") or file.endswith(".ipynb"):
            file_path = os.path.join(root, file)
            summaries = summarize_functions_with_openai(file_path)
            # for summary in summaries:
            print(summaries)
            raw_documents.append(Document(page_content=summaries,metadata={"source": file_path}))

# splitting the document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, # 300 characters
    chunk_overlap=100, 
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents) 

# print((chunks))

# preparing to be added in chromadb

documents = []
metadata = []
ids = []

i = 0

for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append(chunk.metadata)

    i += 1

# adding to chromadb


collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)