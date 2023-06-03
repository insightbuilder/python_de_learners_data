import modal 
#!/usr/bin/env python3

stub = modal.Stub('modal_langchain')

from pathlib import Path

from modal import Image, Secret, Stub, web_endpoint

image = Image.debian_slim().pip_install(
    # langchain pkgs
    "faiss-cpu~=1.7.3",
    "chromadb",
    "langchain~=0.0.138",
    "google-cloud-aiplatform",
    "google-auth",
)

stub = Stub(
    name="modal-langchain",
    image=image,
)

docsearch = None  # embedding index that's relatively expensive to compute, so caching with global var.

def retrieve_sources(sources_refs: str, 
                     texts: list[str]) -> list[str]:
    """
    Map back from the references given by the LLM's output to the original text parts.
    """
    clean_indices = [
        r.replace("-pl", "").strip() for r in sources_refs.split(",")
    ]
    numeric_indices = (int(r) if r.isnumeric() else None for r in clean_indices)
    return [
        texts[i] if i is not None else "INVALID SOURCE" for i in numeric_indices
    ]

if stub.is_inside():
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain
    from langchain.llms import VertexAI
    from langchain.embeddings import VertexAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import Chroma
    import os

def qanda_langchain(query: str, vector_db: str):
    print("selecting text parts by similarity to query")
    docs = vector_db.similarity_search(query)

    chain = load_qa_with_sources_chain(
        VertexAI(temperature=0), 
        chain_type="stuff")

    print("running query against Q&A chain.\n")
    
    result = chain(
        {"input_documents": docs, "question": query}, return_only_outputs=True
    )
    output: str = result["output_text"]
    parts = output.split("SOURCES: ")
    
    return output

@stub.function(mounts=[modal.Mount.from_local_dir("/run/media/solverbot/repoA/gitFolders/python_de_learners_data/code_script_notebooks/projects/exploring_modal/lc_documentdb", 
                                                  remote_path="/root/lc_documentdb")])
def cli(query: str):
    print("generating docsearch indexer")
    #print(os.listdir("/root/lc_documentdb"))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/root/lc_documentdb/generativeaitrial-trialLC.json' 
    docsearch = Chroma(
            persist_directory='/root/lc_documentdb/',
            embedding_function=VertexAIEmbeddings())
    answer = qanda_langchain(query,docsearch)
    print(f"ANSWER: \n")
    print(answer) 
