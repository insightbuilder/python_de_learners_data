import logging
import json
clean_log = logging.getLogger("parser")
clean_handler = logging.StreamHandler()
clean_handler.setLevel(level=logging.INFO)
handler_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
clean_handler.setFormatter(handler_formatter)
clean_log.addHandler(clean_handler)
# Script contains the code for cleaning the data in 
# implementation_of_ds, problem_solved_ds, salient_pt_of_ds
# solutioncode_of_ds.txt.


# Extract the DS name, as that will be the first in each string
def extract_name(snippet: str) -> str:
    "Extract the name of the Data Structure"
    temp = snippet.split('\n')[0]  # split with \n and take first element
    temp = temp.replace(":", "").strip()  # remove the : and white spaces
    return temp


def extract_python(snippet: str) -> str:
    "Extract Implementation & Example usage of DS"
    splits = snippet.split("```")
    # check how many pieces are formed
    # clean_log.warning(len(splits))
    if len(splits) == 1:
        return splits[0]
    elif len(splits) == 3:
        return splits[1].replace('python', '')
    else:
        return splits[1].replace('python', '') + splits[3]


# Extract the Datastructure introduction
def extract_introduction(snippet: str) -> str:
    "Extract the introduction, and content"
    if 'Introduction' in snippet:
        return snippet.split('Introduction:')[1].strip()
    # split with Introduction: and take first element
    else:
        return '\n'.join(snippet.split('\n')[1:])


# Extract the problems that can be solves
def extract_probsolved(snippet: str) -> str:
    "Extract the Problem solved"
    return '\n'.join(snippet.split('\n')[1:])
    # split with \n char, and drop the first element and rejoin rest with \n char


# Extract the solution implementation using the datastructure
def extract_solutionimp(snippet: str) -> str:
    "Extract the Problem statement, solution explanation and implementation"
    return '\n'.join(snippet.split('\n')[1:])
    # split with \n char, and drop the first element and rejoin rest with \n char

# Start by reading the whole file as text
with open('implementation_of_ds.txt', mode='r') as ids:
    ids_data = ids.read()
# Split the data using "Datastructure" word into list of string
ids_top_list = ids_data.split('Data Structure')
# print(ids_top_list[1])
ids_top_list = ids_top_list[1:]  # dropping 1st element, as it is empty
# print(len(ids_top_list))

# create storage for IDS info
ids = []
# enumerate over the ids_top_list
for ind, snip in enumerate(ids_top_list):
    clean_log.warning(f"Processing ds_implementation {ind} snippet")
    imp = extract_python(snip)
    ids.append(imp)

# Working on the salient_pt_of_ds.txt
# Start by reading the whole file as text
with open('salient_pt_of_ds.txt', mode='r') as sds:
    sds_data = sds.read()
# Split the data using "Datastructure" word into list of string
sds_top_list = sds_data.split('Data Structure')
# print(sds_top_list[1])
sds_top_list = sds_top_list[1:]  # dropping 1st element, as it is empty
# print(len(ids_top_list))

sds = []
# enumerate over the sds_top_list
for ind, snip in enumerate(sds_top_list):
    clean_log.warning(f"Processing salient point {ind} snippet")
    sp = extract_introduction(snip)
    sds.append(sp)


# working on the problem solved data
with open('problem_solved_ds.txt', mode='r') as pds:
    pds_data = pds.read()
# Split the data using "Datastructure" word into list of string
pds_top_list = pds_data.split('Data Structure')
# print(pds_top_list[1])
pds_top_list = pds_top_list[1:]  # dropping 1st element, as it is empty
# print(len(pds_top_list))

pds = []
# enumerate over the sds_top_list
for ind, snip in enumerate(pds_top_list):
    clean_log.warning(f"Processing various probs solved {ind} snippet")
    ps = extract_probsolved(snip)
    pds.append(ps)

# Working on solution code implementation data
with open('solutioncode_of_ds.txt', mode='r') as scds:
    scds_data = scds.read()
# Split the data using "Datastructure" word into list of string
scds_top_list = scds_data.split('Data Structure')
# print(scds_top_list[1])
scds_top_list = scds_top_list[1:]  # dropping 1st element, as it is empty
# print(len(scds_top_list))

scds = []
# enumerate over the scds_top_list
for ind, snip in enumerate(scds_top_list):
    clean_log.warning(f"Processing solution code {ind} snippet")
    sc = extract_solutionimp(snip)
    ds = extract_name(snip)
    scds.append([ds, sc])

final_json = dict() 

# enumerate over all the data lists above, and populate 
# final json
for ind, data in enumerate(scds):
    ds = extract_name(snip)
    final_json[data[0]] = dict({
            'python_implementation': ids[ind],
            'salient_points': sds[ind],
            'solution_implement': data[1],
            'problem_solved': pds[ind],
            })


with open(file='complete_ds_data.json', mode='+w') as fsd:
    json.dump(final_json, fsd)
