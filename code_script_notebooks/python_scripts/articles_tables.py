#!/bin/python
"""Code to add table_format column in medium_articles dataset
by creating it in vertexAI using langchain"""

from datasets import load_dataset, load_metric
from langchain.llms import VertexAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/run/media/solverbot/repoA/gitFolders/generativeaitrial-trialLC.json"

article_dataset = load_dataset("Kamaljp/articles_samples")

print(article_dataset)
llm = VertexAI(temperature=0)

# Define the prompt template for text-to-SQL conversion
prompt_template = PromptTemplate(
    input_variables=["article_body"],
    template="""Convert the above {article_body} to a table.
    Table must contain column of tags, explanation. 
    Explanation column contains 25 word explanation of tag""",
)
article_chain = LLMChain(llm=llm, prompt=prompt_template)

def get_table(line_item):
    text = line_item['text']
    time.sleep(5) #better to slow down the API calls
    try:
        line_item['tabled_format']=article_chain.run(text).strip()
    except Exception as e:
        print(f"Encountered Error. {e}\n Entering Sleep for 60 seconds")
        time.sleep(60)
        line_item['tabled_format']=article_chain.run(text).strip()
    return line_item

article_trial_100 = article_dataset['train'].select(range(100)) 

article_table_100 = article_trial_100.map(get_table)

print(article_table_100)

article_table_100.push_to_hub('Kamaljp/article_table_100')

print("Completed 100 datasets and pushed to hub")
