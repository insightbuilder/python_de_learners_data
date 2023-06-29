import streamlit as st
import json
import base64
from io import StringIO

st.title('Json Reader')

st.markdown("""Reads the Json file and prints the output""")

st.sidebar.header('File Upload')
your_file = st.sidebar.file_uploader(label="Upload the file here")

if your_file is not None: 
    bytes_data = your_file.getvalue()

    #reading data as json

    #st.write(bytes_data)

    json_data = json.loads(bytes_data)
    
    try:
        length = len(json_data)
        indices = st.sidebar.slider("Start n End",0,length,(0,5))

        st.write(json_data[indices[0]:indices[1]])
    except Exception as e:
        st.write(json_data)

