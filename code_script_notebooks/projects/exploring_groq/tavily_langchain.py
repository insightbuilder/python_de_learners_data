import os
from dotenv import load_dotenv
import openai
from langchain_community.tools.tavily_search import (
    TavilySearchResults,
    TavilyAnswer,
)
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
# https://docs.tavily.com/docs/tavily-api/langchain
from langchain.retrievers import TavilySearchAPIRetriever  
# This is present in https://python.langchain.com/docs/integrations/retrievers/tavily 
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI


load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
openai.api_key = os.environ['OPENAI_API_KEY']
tool = TavilySearchResults()
qna = TavilyAnswer()

llm = ChatOpenAI(model='gpt-3.5-turbo',
                 temperature=0.6)
search = TavilySearchAPIWrapper(tavily_api_key=os.environ['TAVILY_API_KEY'])
tavily_tool = TavilySearchResults(api_wrapper=search)
tavily_retriever = TavilySearchAPIRetriever(k=3)

tavily_just_search = TavilySearchResults()
# https://python.langchain.com/docs/integrations/tools/tavily_search

# try:
    # agent_chain = initialize_agent(
        # tools=[tavily_tool],
        # llm=llm,
        # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        # verbose=True
    # )
# except Exception as e:
    # print(e, 'fails due to issue with agents...')

query = input(f"What you want to know? ")

# result = agent_chain.run(query)
# result = tavily_retriever.invoke(query)
# print(result)

# Document(page_content='Open the Google Pay app. Go into Send or request. Select the contact you want to send money to. Alternatively, you can create a group or select the option that reads Split with friends. Once you ...', metadata={'title': 'How to use Google Pay: A step by step guide - Android Authority', 'source': 'https://www.androidauthority.com/how-to-use-google-pay-890614/', 'score': 0.91538, 'images': None})

search_res = tavily_just_search.invoke({"query": query})
print(search_res)
# {'url': 'https://themunim.com/a-detailed-guide-for-rupay-card-better-things-to-know/', 'content': 'Some benefits of using a RuPay card include: Increased acceptance at merchant outlets and ATMs across India. Reduced foreign currency conversion charges for card transactions. Earn Reward Points on spending which can be redeemed for cash back, gift vouchers, and other benefits. 24×7 customer service support.'}