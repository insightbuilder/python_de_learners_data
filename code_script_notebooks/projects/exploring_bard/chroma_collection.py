from chromadb.config import Settings
import chromadb

from langchain.schema import Document
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = VertexAIEmbeddings()

persist_directory = 'lc_helpdb'

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=persist_directory # Optional, defaults to .chromadb/ in the current directory
))

client.delete_collection(name="langchain_concepts")

lc_collect = client.create_collection(name="langchain_concepts", 
                                      embedding_function=embeddings.embed_documents)
# Embed the docs step by step, as the 
# vertex AI embedding api is timing out
start = 0
inter = 100

while True:
  lc_collect.add(ids=ids[start:inter], 
              documents=documents[start:inter],
              metadatas=metadatas[start:inter])
  
  start = start + inter + 1
  inter = inter + 100
