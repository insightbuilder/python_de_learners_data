import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"
os.environ["OPENAI_API_KEY"] = ""

from langchain.llms import OpenAI
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType

tools = load_tools(['llm-math'], llm=OpenAI(temperature=0))
agent = initialize_agent(tools, OpenAI(temperature=0), 
                         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                         verbose=True)

output = agent.run("What is 5 + 58")

print(output)
