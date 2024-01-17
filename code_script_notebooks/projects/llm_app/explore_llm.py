# App that allows to see the messages inside a given json document
# Read Json Document from the drive
# Render the message on display
# Create a scroll bar to move between messages
# Provide text box to enter prompts 
# Provide option to save the prompt and the output to the text file & download
import streamlit as st
import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field, conlist
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('.env')  # Loading the env file with the credentials 

openai.api_key = os.environ['OPENAI_API_KEY']
anyscale_key = os.environ['ANYSCALE']
# st.write(os.environ['ANYSCALE'])

client = OpenAI()  # declaring OpenAI client  

# declaring AnyScale Client
ascale_client = openai.OpenAI(
    base_url='https://api.endpoints.anyscale.com/v1',
    api_key=anyscale_key
)


def custom_text(message, prompt):
    """Wrap the call to OpenAI Chat Completion endpoint
     with the message and the prompt. Return the 
     message completion."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content


def anyscale_text(message: str, prompt: str, model: str):
    """Wrap the Anyscale chat completion endpoints with 
    selected model, message and prompt. Return the message
    completion"""
    response = ascale_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": message}],
        temperature=0.7)
    return response.choices[0].message.content


# Start of streamlit App
st.write("### View & Parse Messages with LLM")  # Heading

# Asking for file path
file_path = st.text_input(label='File Path', value='Your file path here',)

# st.write("File path is: \n", file_path)  # Got the file path

# Look at the file, and ensure it is json file.
st.write("Checking File Type: ")
if 'json' in file_path:
    st.write("File is json")
else:
    st.write("Provide a valid json file only.")
# Open the json file, and load the data into message list
with open(file=file_path, encoding='utf-8', mode='r') as js:
    msg_list = json.load(js)

message_count = len(msg_list)  # count the number of data points in the file

# create a slider object inside streamlit, that returns the index
idx = st.slider(label='Message Number', min_value=0, max_value=message_count)
# based on the slider object index, select the datapoint
if 'message' in msg_list[idx].keys():
    # if there is message key in the datapoint then use that data
    raw_message = msg_list[idx]['message']
else:
    raw_message = str(msg_list[idx])  # else consider the entire data point as text

st.write(raw_message)  # show the data point

# get the prompt from the user
your_prompt = st.text_input(label="Prompt: ", value="Enter your prompt")
# show the prompt back to the user
st.write("Your Prompt: ", your_prompt)
# declare the models available as list
models = ['OpenAI-GPT3.5',
          'meta-llama/Llama-2-7b-chat-hf',
          'meta-llama/Llama-2-13b-chat-hf',
          'meta-llama/Llama-2-70b-chat-hf',
          'mistralai/Mistral-7B-Instruct-v0.1',
          'mistralai/Mixtral-8x7B-Instruct-v0.1',
          'thenlper/gte-large',
          'BAAI/bge-large-en-v1.5',
          'Meta-Llama/Llama-Guard-7b',
          'codellama/CodeLlama-34b-Instruct-hf',
          'HuggingFaceH4/zephyr-7b-beta',
          'Open-Orca/Mistral-7B-OpenOrca']

# Create radio button list of models, so one of the models can be selected
model = st.radio('Model to Use: ',options=models)

# st.write("Model Selected: ", model)

if st.button("Submit"):  # once the submit button pressed
    if model == models[0]:  # check if the model selected is from OpenAI
        # call the openai endpoint
        parsed_output = custom_text(message=raw_message,
                                    prompt=your_prompt)
    else:
        # all the rest of the models call anyscale endpoint
        parsed_output = anyscale_text(message=raw_message,
                                      prompt=your_prompt,
                                      model=model)
    try:  # try to convert the output to Dictionary
        st.write("Parsed Output: ", json.loads(parsed_output,))
    except Exception as e:  # else inform message cannot be converted
        st.write('Cannot write as Json')
        st.write(parsed_output)
    # Format the parsed_output, raw_message and prompt in dictionary format
    to_write = str(dict({
        "raw_message": raw_message,
        "parsed_message": parsed_output,
        "prompt_used": your_prompt
    }))
    # Convert the dictionary into string, and write to file
    st.download_button('Get_file', to_write, 'text/plain')
