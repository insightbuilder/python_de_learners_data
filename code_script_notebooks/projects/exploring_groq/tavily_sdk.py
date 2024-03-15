import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

tavily = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])

question = input("Ask your question here...: ") 
chose = input(f"Chose search/ context/ qna: ")

# response = {'test':'tested'}
uid = "".join([x[0] for x in question.split(' ')])
date = datetime.today()

file_name = f'days_results_{date.day}_{date.month}_{uid}.json'

if chose.strip().lower() == 'search':
    response = tavily.search(query=question)
    for data in response['results']:
        print(data['title'])
        print(data['url'])
        print(data['content'])
 
    with open(file_name, '+a') as res:
        json.dump(response, res)

if chose.strip().lower() == 'context':
    search_ctxt = tavily.get_search_context(query=question,
                                            search_depth='advanced',
                                            max_tokens=6000)
    print(search_ctxt)
    with open(file_name, '+a') as res:
        json.dump(search_ctxt, res)

if chose.strip().lower() == 'qna':
    qna_search = tavily.qna_search(query=question,
                                   search_depth='advanced',)
    print(qna_search)
    with open(file_name, '+a') as res:
        json.dump(qna_search, res)
