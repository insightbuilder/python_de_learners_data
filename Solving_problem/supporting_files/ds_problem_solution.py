# Script extracts the various problems 
# data structures in the below list can
# solve
import openai
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
openai.api_key = os.environ['OPENAI_API_KEY']

ds_list = ["List", "Dict", "Tuples", "Strings", "Deque", "NamedTuple",
           "Heapq", "DefaultDict", "Counter", "ChainMap",
           "OrderedDict", "Set", "Arrays", "Queues", "Stacks",
           "Linked Lists", "Trees", "Graphs", "HashTables",
           "Trie", "BloomFilter", "SkipList", "B-Trees",
           "PriorityQueues", "DisjointSet", "BinaryIndexedTree",
           "SuffixArray"]

client = OpenAI()

your_prompt = """Provide the various problems that the above datastructure can solve.
                Make the output into a dictionary of problems and a short description."""
salient_point = """Provide a precise introduction and 5 distinguishing factor
                of the datastructure. Make the introduction less than 25 words.
                The distinguishing factor has to be less than 40 words.
                Ensure the subheadings and descriptions are in the same line."""
implementation = """Provide a simple python implementation of above datastructure.
                The implementation must be in form of Class or Function, along with helpful docstrings, 
                comments and example usage."""
solution_code = """Which is a most frequently solved problem using the above datastructure. 
                Provide that problem statement, solution explanation, and python 
                implementation of that solution. Keep the implementation code at the last"""

def custom_text(message, prompt):
    """Structured the message into """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content


# data_test = custom_text(f"Datastructure is {ds_list[0]}.",
                        # your_prompt)

with open("salient_pt_of_ds.txt", 'w') as ds:
    for struct in ds_list:
        print(f'Working on {struct}')
        out = custom_text(f"Datastructure is {struct}",
                          salient_point)
        print(f"Printing the output for the {struct} datastructure.")
        print('\n')
        print(out)
        print('\n\n')
        ds.write('\n')
        ds.write(f"Data Structure: {struct}\n") 
        ds.write(out)
        ds.write('\n')

