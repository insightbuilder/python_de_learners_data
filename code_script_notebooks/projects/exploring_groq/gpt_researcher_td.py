from gpt_researcher import GPTResearcher
import asyncio
import os
import openai
from dotenv import load_dotenv


load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
# print(os.environ['API_KEY'])
# os.environ['OPENAI_API_KEY'] = ""
openai.api_key = os.environ['OPENAI_API_KEY']


# GR is using Tavily... So need to understand that service
async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    report = await researcher.run()
    return report

if __name__ == "__main__":
    query = input("Your query here: ")
    # print(query.split(' '))
    report_type = "research_report"
    report_fname = "".join([word[0] for word in query.split(' ')]) + ".txt"
    try:
        report = asyncio.run(get_report(query, report_type))
        print(report)
        with open(report_fname, 'w') as rpt:
            rpt.write(report)
    except Exception as e:
        print('Generation failed. Check the code...', e)
