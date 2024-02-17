import streamlit as st
from grokking_linklist import linkedlist
from challenge_recorder import challenge_rec

st.set_page_config(layout='wide')

st.title("Achieving Grokking Excellence")

data_structure = ['DS_Grokking', 'stack', 'queue', 'graph', 'linkedlist']


def overview():
    import streamlit as st
    st.markdown("#### Mapping out Data Structures")
    st.image('grokking_ds.PNG', caption='Grokking 4 Data Structures')


page_function = {
    "overview": overview,
    "challenge_register": challenge_rec,
    "LinkedList": linkedlist,
}

page_name = st.sidebar.selectbox(label="Whats Grinding?",
                                 options=page_function.keys())
page_function[page_name]()
