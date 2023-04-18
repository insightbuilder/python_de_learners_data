import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"
##This file will be used for questioning the documents that is already 
##stored inside the chromadb

from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain import PromptTemplate, LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY']=''

database = 'faiss_index'
loading_database = FAISS.load_local(database,
                                     OpenAIEmbeddings())
print("Loading database completed")

data_retriever = loading_database.as_retriever()

print("Retriver created.")

while True:
    qa_endpoint = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0),
                                              chain_type='stuff',
                                              retriever=data_retriever)
    query = input("Please enter your query: ")

    output = qa_endpoint.run(query)

    print(f"The answer to your question : {query}",end='\n')

    print(output)
