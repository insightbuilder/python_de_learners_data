from dotenv import load_dotenv
load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
api_key = os.environ.get("GROQ_API_KEY")
chat = ChatGroq(temperature=0,
                groq_api_key=api_key,
                model_name="mixtral-8x7b-32768")

system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system),
                                           ("human", human)])

chain = prompt | chat
print(chain.invoke({"text": "Tell me where is the moon now..."}))