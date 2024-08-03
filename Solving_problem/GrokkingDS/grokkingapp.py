import streamlit as st
# from grokking_linklist import linkedlist
from challenge_recorder import challenge_rec
from code_recorder import code_recorder
import pathlib
from PIL import Image

st.set_page_config(layout='wide')

st.title("Achieving Grokking Excellence")

data_structure = ['DS_Grokking', 'stack', 'queue', 'graph', 'linkedlist']


def overview():
    import streamlit as st
    st.markdown("#### Mapping out Data Structures")
    file_path = pathlib.Path(__file__).parent.resolve()
    file_png = file_path / "grokking_ds.PNG"
    file_png = file_png.resolve()
    st.image(Image.open(file_png),
             caption='Grokking 4 Data Structures',
             output_format="PNG")


page_function = {
    "overview": overview,
    "challenge_register": challenge_rec,
    "Implemented_Algo": code_recorder,
}

page_name = st.sidebar.selectbox(label="Whats Grinding?",
                                 options=page_function.keys())
page_function[page_name]()
