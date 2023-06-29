import streamlit as st
import json
import base64
import requests
from io import StringIO
from streamlit_agraph import agraph, Node, Edge, Config

st.title('Json File Reader')

@st.cache_data
def get_json(url):
    js = requests.get(url) 
    data = js.json()
    return data

st.markdown("""Reads the Json file of Comments data extracted from Youtube API & creates graph""")
st.sidebar.header('File Upload')
your_file = st.sidebar.file_uploader(label="Upload the file here")

if your_file is not None: 
    bytes_data = your_file.getvalue()

    json_data = json.loads(bytes_data)

else:
    st.write("Example api file can be located here")

    st.write("""https://raw.githubusercontent.com/Kamalabot/streamlit_deploys/main/json_reader/toplevel_comment_zGAkhN1YZXM.json""")
    json_data = get_json("""https://raw.githubusercontent.com/Kamalabot/streamlit_deploys/main/json_reader/toplevel_comment_zGAkhN1YZXM.json""")
try:
        length = len(json_data)
        if length < 15:
            indices = st.sidebar.slider("Start n End",0,length,(0,10))
        else:
            indices = st.sidebar.slider("Start n End",0,length,(0,int(length/15)))
        
        selected_indices = json_data[indices[0]:indices[1]] 
        #st.write(selected_indices)
        #creating the graph of the connection

        nodes = []
        edges = []
        authors = []

        video_id = selected_indices[0]['snippet']['videoId']


        nodes.append(Node(id=video_id,lable='Youtube Video',
                          size = 25, symbolType='square'))
        
        for data in selected_indices:
            author = data['snippet']['topLevelComment']['snippet']['authorDisplayName'].split(' ')[0] 
            author_img = data['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'] 
            if author not in authors:
                nodes.append(Node(id=author, 
                                  size=25, 
                                  shape="circularImage",
                                  image=author_img) )
                authors.append(author)
            if 'replies' in data:
                replies = data['replies']['comments']
                for reply in replies:
                    reply_author = reply['snippet']['authorDisplayName'].split(' ')[0]
                    reply_author_img = reply['snippet']['authorProfileImageUrl']
                    if reply_author not in authors:
                        nodes.append(Node(id=reply_author, 
                                          size=15, 
                                          shape="circularImage", 
                                          image=reply_author_img) )
                        authors.append(reply_author)

                    edges.append( Edge(source=reply_author, 
                                       target=author, 
                                       type="CURVE_SMOOTH"))

            edges.append(Edge(source=author, target=video_id,type="CURVE_SMOOTH"))

        #st.write(authors)

        config = Config(width=750,
                    height=950,
                    directed=True,
                    physics=False,
                    hierarchical=False,
                    node={'labelProperty':'label','renderLabel':True})

        return_value = agraph(nodes = nodes, edges = edges, config = config)

except Exception as e:
    st.write(e)
    st.markdown("Provided Json is not Youtube API data. Unable to Parse")
    #st.write(json_data)

    

