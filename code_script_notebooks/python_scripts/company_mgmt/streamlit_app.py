import streamlit as st
import json
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import pandas as pd
from time import time

st.title('Companies & their Management')

@st.cache_data
def load_data_a():
    df = pd.read_csv('https://raw.githubusercontent.com/Kamalabot/M3nD3/main/ObservableData/companyManagement.csv')
    return df 

df = load_data_a()


unique_names = df.name.unique()
unique_orgs = df.company.unique()

st.sidebar.write("Filters")

filter_orgs = st.sidebar.multiselect("Select Orgs",
                                     unique_orgs,
                                     max_selections=5,
                                     default=unique_orgs[:5])

filtered_df = df[df.company.isin(filter_orgs)]

mgmt_data = filtered_df.to_json(orient='values')

dict_convert = json.loads(mgmt_data)
#st.write(dict_convert)

def make_graph(dict_convert):
    nodes = []
    edges = []
    execs = []
    orgs = []

    for data in dict_convert: 
        #st.write(data)
        name = data[1]
        org = data[3]

        if name not in execs:
            nodes.append(Node(id=name,symbolType='diamond',color='#FDD00F'))
            execs.append(name)

        if org not in orgs:
            nodes.append(Node(id=org,label=org,color="#07A7A6"))
            orgs.append(org)
        
        position = f"{data[2]} of"
        
        edges.append(Edge(source=name,target=org,label=position))

    return [nodes, edges]

config = Config(width=750,
                    height=950,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    highlightColor='#FF00FF',
                    nodeHighlightBehavior=True,
                    node={'labelProperty':'label','renderLabel':False})

filter_nodes, filter_edges = make_graph(dict_convert)

return_value = agraph(nodes = filter_nodes, 
                      edges = filter_edges, 
                      config = config)
