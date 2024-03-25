import json
import os 
from pprint import pprint
import requests
from dotenv import load_dotenv

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''
load_dotenv("/home/aicoder/gitfolder/python_de_learners_data/code_script_notebooks/.env")

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"

# Query term(s) to search for. 
query = input("Provide your query") # "Devika AI"

# Construct a request
mkt = 'en-US'
params = { 'q': query, 'mkt': mkt }
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("Headers:")
    print(response.headers)

    pprint(response.json())
except Exception as ex:
    raise ex

