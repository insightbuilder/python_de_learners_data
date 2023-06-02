#/bin/python
#The script will create the gui that can  
#create the vector store based on the file 
#provided by you. Then it will use the 
#openai key to do QA.

import PySimpleGUI as sg
import os.path

from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader
from langchain.llms import VertexAI 
from langchain.chains import RetrievalQA
import textwrap

file_api_column = [
            [
            sg.Text("Vertex AI Google App Cred Path:"),
            sg.InputText()]
            ]
qa_extract = [
        [sg.Text("QA Extraction")],
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
            ],
        ]
embed_file_column = [
        [sg.Text("Embedding Process")],
        [
            sg.Text("Provide file / folder path:"),
            sg.In(size=(25,1),enable_events=True,key='-EMBED-'),
            sg.FolderBrowse()
            ],
        [
            sg.Text("FAISS Index save folder"),
            sg.InputText()
            ],
        [
            sg.Button("Split_Data"),
            sg.Button("Embed_Save")
            ]
        ]
query_output = [
            [
            sg.Text("Your reply here:"),
            sg.Text(key='-TEXT-')
            ]
        ]
plain_llm_chain = [
        [
            sg.Text("Ask PaLM LLM directly"),
            sg.InputText()
            ],
        [
            sg.Button("Ask_Palm"),
            sg.Button("Close")
            ],
        [
            sg.Text("Plain LLM Output"),
            sg.Text(key='-P_llm-')
            ]
        ]
layout = [[sg.Column(file_api_column)],
            [sg.HSeparator()],
            [sg.Column(plain_llm_chain)],
            [sg.HSeparator(pad=(0,5))],
            [sg.Column(embed_file_column)],
            [sg.HSeparator()],
            [sg.Column(qa_extract)],
            [sg.HSeparator(pad=(0,5))],
            [sg.Column(query_output)]
        ]
window = sg.Window("Embed & Chat your Data...", 
                   layout)

def load_single_document(file_path: str):
    # Loads a single document from a file path
    # Taken from https://github.dev/PromtEngineer/localGPT
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf8")
    elif file_path.endswith(".pdf"):
        loader = PDFMinerLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    return loader.load()[0]


def load_documents(source_dir: str):
    # Loads all documents from source documents directory
    # Taken from https://github.dev/PromtEngineer/localGPT
    all_files = os.listdir(source_dir)
    return [load_single_document(f"{source_dir}/{file_path}") for file_path in all_files if file_path[-4:] in ['.txt', '.pdf', '.csv'] ]

while True:
    event, values = window.read()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = values[0]

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    elif event == "-FOLDER-":
        #This path will load the FAISS index already available.
        vs_path = values['-FOLDER-']
        #print(type(vs_path))
        try:
            embedding = VertexAIEmbeddings()
            new_db = FAISS.load_local(folder_path=vs_path,
                                      embeddings=embedding)
        except Exception as e:
            print(e)
    elif event == "Split_Data":
        #This path will create the FAISS Embedding from the data 
        #provided by you in the path
        try:
            data_path = values['-EMBED-']
            print(data_path)
        except Exception as e:
            print(e)

        try:
            if '.' in data_path:
                file_docs = load_single_document(data_path)

            else:
                file_docs = load_documents(data_path)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, 
                                                           chunk_overlap=20)
            texts = text_splitter.split_documents(file_docs)
            print(f"Loaded {len(file_docs)} documents from {data_path}")
            print(f"Split into {len(texts)} chunks of text")

            # Create embeddings
            print("Splitting completed")
        except Exception as e:
            print(e)

    elif event == 'Embed_Save':
        #print(values)
        embeddings = VertexAIEmbeddings()
        try:
            new_db = FAISS.from_documents(texts[:100], 
                                          embeddings)
            #saving the index to local folder
            new_db.save_local(values[4])
            print("Saving the FAISS index")
        except Exception as e:

            print(f"Check the errors: {e}")
        
    elif event == "Get_Output" and new_db:
        #print(values)
        query = values[6]

        docs = new_db.as_retriever().get_relevant_documents(query=query)
        print(docs)
        chain = load_qa_chain(VertexAI(temperature=0.1),
                              chain_type="stuff")
        output =  chain.run(input_documents=docs[:1],
                            question=query)
        wrap_out1 = textwrap.fill(output,80)
        window['-TEXT-'].update(wrap_out1)

    elif event == 'Ask_Palm':
        print(values)
        llm_query = values[2]
        llm = VertexAI(temperature=0.1)
        reply = llm(llm_query)
        wrap_out2 = textwrap.fill(reply,80)
        window['-P_llm-'].update(wrap_out2)
