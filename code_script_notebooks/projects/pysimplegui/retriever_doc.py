#/bin/python
#The script will take the openAI key, the faiss_index path
#and take the query vector store

import PySimpleGUI as sg
import os.path

from langchain.vectorstores import FAISS
from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

file_api_column = [
        [
            sg.Text("Open AI API Key"),
            sg.InputText(),
            ],
        [
            sg.Text("Faiss Vector Store"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse()
            ],
        [
            sg.Text("Enter your Query"),
            sg.InputText()
            ],
        [
            sg.Button("Get_Output"),
            sg.Button("Close")
            ],
        ]
query_output = [
            [
            sg.Text("Your reply here:"),
            sg.Text(key='-TEXT-')
            ]
        ]
layout = [
        [sg.Column(file_api_column),
          sg.VSeperator(),
          sg.Column(query_output)
         ]
        ]

window = sg.Window("Chat your PDF", layout)
while True:
    event, values = window.read()

    os.environ['OPENAI_API_KEY'] = values[0] 

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    elif event == "-FOLDER-":
        vs_path = values['-FOLDER-']
        print(type(vs_path))
        try:
            embedding = OpenAIEmbeddings()
            new_db = FAISS.load_local(folder_path=vs_path,
                                      embeddings=embedding)
        except Exception as e:
            print(e)
    elif event == "Get_Output" and new_db:
        query = values[1]
        
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                         chain_type="stuff", 
                                         retriever=new_db.as_retriever())

        output = qa.run(query)
        window['-TEXT-'].update(output)

