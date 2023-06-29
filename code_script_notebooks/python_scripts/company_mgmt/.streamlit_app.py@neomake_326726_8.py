import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import pandas as pd
from time import time

st.title('Companies & their Management')

@st.cache_data
def load_data_a():
  df = pd.read_csv('https://raw.githubusercontent.com/Kamalabot/M3nD3/main/ObservableData/companyManagement.csv')
  mgmt_dict = df.to_json(orient='records')
  return mgmt_dict

mgmt_data = load_data_a()

st.write(mgmt_data)



