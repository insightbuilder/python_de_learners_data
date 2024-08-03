import modal 
#!/usr/bin/env python3

stub = modal.Stub('modal_langchain')

from pathlib import Path

from modal import Image, Secret, Stub, web_endpoint

image = (Image.debian_slim().pip_install("torch","transformers","langchain",
                                         "chromadb","llama-cpp-python","gpt4all",
                                         "google-cloud-aiplatform","google-auth")
         .apt_install("wget")
         .run_commands(
           "mkdir model_path",
           "cd model_path",
           "wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin",
           "pwd")
        )

stub = Stub(
    name="pvtgpt-qna",
    image=image,
)

docsearch = None  # embedding index that's relatively expensive to compute, so caching with global var.

if stub.is_inside():
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain
    from langchain.vectorstores import Chroma
    from langchain.embeddings import VertexAIEmbeddings
    import os
    from langchain.chains import RetrievalQA
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from langchain.llms import GPT4All

def qanda_langchain(query: str, vector_db: str):
    print("selecting text parts by similarity to query")
    docs = vector_db.similarity_search(query)
        
    model_type = "GPT4All"
    model_path = "/ggml-gpt4all-j-v1.3-groovy.bin"
    model_n_ctx = 250

    callbacks = [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    llm = GPT4All(model=model_path,
                  n_ctx=model_n_ctx,
                  backend='gptj',
                  callbacks=callbacks, verbose=False)

    chain = load_qa_with_sources_chain(
        llm, 
        chain_type="stuff")

    print("running query against Q&A chain.\n")
    
    result = chain(
        {"input_documents": docs, "question": query}, 
        return_only_outputs=True
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
