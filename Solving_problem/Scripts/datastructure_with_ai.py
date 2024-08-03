# Streamlit app that exhibits the 27 data structures
# their salient features, problems each can solve,
# their own implementation, and one of the problem
# solution
import pathlib
import streamlit as st
import json
st.set_page_config(layout='wide')
# provide the title
st.title("Learn & Document 27 Data structures with GPT 3.5")
# declare the list of data structures
ds_list = ["List", "Dict", "Tuples", "Strings", "Deque", "NamedTuple",
           "Heapq", "DefaultDict", "Counter", "ChainMap",
           "OrderedDict", "Set", "Arrays", "Queues", "Stacks",
           "Linked Lists", "Trees", "Graphs", "HashTables",
           "Trie", "BloomFilter", "SkipList", "B-Trees",
           "PriorityQueues", "DisjointSet", "BinaryIndexedTree",
           "SuffixArray"]

# locating the file
code_dir = pathlib.Path(__file__).parent.resolve()
files_location = code_dir / "complete_ds_data.json"  # Available data
files_location = files_location.resolve()
st.write(files_location)
# After the above resolution process, the complete_ds_data.json file
# is located correctly
with open(files_location, 'r') as cds:
    final_json = json.load(cds)

select_ds = st.radio('Select a Datastructure', ds_list)

selected_data = final_json[select_ds]
st.title(f"{select_ds} Introduction")
st.write(selected_data['salient_points'])
st.title(f"{select_ds} Applied Problem")
st.write(selected_data['problem_solved'])
st.title(f"{select_ds} Python Implementation")
st.write(f"```python{selected_data['python_implementation']}```")
st.title(f"{select_ds} Solution For Example Problem")
st.write(f"```python{selected_data['solution_implement']}```")
