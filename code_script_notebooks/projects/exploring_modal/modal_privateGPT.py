import modal 
#!/usr/bin/env python3

stub = modal.Stub('modal_pgpt')

stub.pvtgpt_img = (modal.Image.debian_slim()
                   .pip_install("torch","transformers","langchain","llama-cpp-python","gpt4all")
                   .apt_install("wget")
                   .run_commands(
                       "mkdir model_path",
                       "cd model_path",
                       "wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin",
                       "pwd")
                   )

if stub.is_inside():
    from langchain.chains import RetrievalQA
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from langchain.llms import GPT4All


@stub.function(image=stub.pvtgpt_img)
def generate(query):
    model_type = "GPT4All"
    model_path = "/ggml-gpt4all-j-v1.3-groovy.bin"
    model_n_ctx = 250

    callbacks = [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    llm = GPT4All(model=model_path,
                  n_ctx=model_n_ctx,
                  backend='gptj',
                  callbacks=callbacks, verbose=False)
       # Get the answer from the chain
    res = llm(query)
    return res
        
@stub.local_entrypoint()
def call_main(query):
    """This function takes the query and generates output"""
    res = generate.call(query)
    print("\n> Answer:")
    print(res)

