# Agent takes an objective from the user as input
# Sends the objective to LLMs with ChainOfThought prompting to get the steps
# Returned steps are parsed into a list of tasks, are plan steps
# The steps are classified into different kind of tasks 
# They are rendered into a appropriate Template into text prompt 
# Sent to LLM for getting the output
# Output is collected in a single file or object
# Presented to the user
import questionary
import logging
import json
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from jinja2 import (
    Environment,
    select_autoescape,
    FileSystemLoader,
    meta,
)

aglog = logging.getLogger(__file__)
aglog.setLevel(logging.INFO)
aghnd = logging.StreamHandler()
aghnd.setLevel(logging.INFO)
fmtr = logging.Formatter(fmt="%(levelname)s|%(message)s")
aghnd.setFormatter(fmtr)
aglog.addHandler(aghnd)
load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
openai.api_key = os.environ['OPENAI_API_KEY']

model_used_eco = "gpt-3.5-turbo"
model_used_super = "gpt-4-1106-preview"

architect_system_message = """You are an experienced project owner (project manager) who manages 
the entire process of creating software applications for clients from the client
specifications to the development. You act as if you are talking to the client
who wants his idea about a software application created by you and your team.
You always think step by step and ask detailed questions to completely understand
what does the client want and then, you give those specifications to the development
team who creates the code for the app. Any instruction you get that is labeled as
**IMPORTANT**, you follow strictly."""
specwrite_system_message = """You are a product owner working in a software 
development agency."""
techlead_system_message = """You are an experienced tech lead in a software
development agency and your main task is to break down the project into
smaller tasks that developers will do. You must specify each task as clear
as possible. Each task must have a description of what needs to be implemented."""
fstak_dev = """You are an expert full stack software developer who works in a 
software development agency.
You write modular, well-organized code split across files that are not too 
big, so that the codebase is maintainable. Your code is clean, readable,
production-level quality, and has proper error handling and logging.
Your job is to implement tasks that your tech lead assigns you. Each task 
has a description of what needs to be implemented.
"""
task_sorting_expert = """You are expert in classifying a given task"""
data_analysis_expert = """You are expert data analyst who can provide
insightful answers from the context provided to you"""

env_template = Environment(
    loader=FileSystemLoader('jinja_prompt'),
    autoescape=select_autoescape
)
total_tokens = 0


def get_required_vars(environ, template_file):
    temp_source = environ.loader.get_source(environ,
                                            template_file)
    parsed_content = environ.parse(temp_source)
    return meta.find_undeclared_variables(parsed_content)


def get_avbl_templates(environ):
    "Returns a list of available templates"
    return environ.list_templates()


def load_render_template(environ,
                         template_file,
                         context):
    template = environ.get_template(template_file)
    return template.render(**context)


def llm_call_openai(user_message: str,
                    system_message: str,
                    model_used: str):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    try:
        response = client.chat.completions.create(
            model=model_used,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "system", "content": user_message}
            ],
            temperature=0.0,
            top_p=1,
            frequency_penalty=0.1,
            presence_penalty=0.1,
        )
        assistant_message = response.choices[0].message.content
        aglog.info(f"Tokens used: {response.usage.total_tokens}")
        global total_tokens
        total_tokens += response.usage.total_tokens
        return {"response": assistant_message}
    except Exception as e:
        aglog.info(e)
        return {"error": "An error occurred while processing the request."}


def write_responses(file_name, prep_data):
    with open(file_name, 'a',) as wds:
        json.dump(prep_data, wds)


def return_json_data(file_name):
    with open(file_name, 'r') as ads:
        return json.load(ads)


avbl_template = get_avbl_templates(environ=env_template)
aglog.debug(avbl_template)

get_vars = get_required_vars(env_template, avbl_template[0])
aglog.debug(get_vars)
tasks = ["ask_tasks", "class_tasks", "analyse_data", "cancel"]

# Starting top-level while loop
while True:
    choose_task = questionary.select("What task you want the Agent to Do? ",
                                     choices=tasks).ask()
    if choose_task == "ask_tasks":
        file_name = questionary.path("Provide filename to store Tasks: ").ask()
        app_type = questionary.text("Provide app type: ").ask()
        app_name = questionary.text("Provide app name: ").ask()
        prompt = questionary.text("Provide the prompt: ").ask()
        context = {"app_type": app_type,
                   "name": app_name,
                   "prompt": prompt}

        rendered_prompt = load_render_template(env_template,
                                               'specs.prompt',
                                               context)
        aglog.debug(rendered_prompt)

        get_tasks = llm_call_openai(specwrite_system_message,
                                    rendered_prompt,
                                    model_used=model_used_eco,)

        split_tasks = get_tasks['response'].split('\n')
        if len(split_tasks) < 2:
            aglog.info(split_tasks)
            split_tasks = 'There is some issue with the tasks returned.'
        context['tasks'] = split_tasks
        if file_name in os.listdir("."):
            os.remove(file_name)
        write_responses(file_name, context)
        temp = tasks.pop(0)  # once a task is done, pop it 

    if choose_task == "class_tasks":
        file_task_classified = questionary.path("Provide filename to store classification data").ask()  # create a new file
        retrieved_data = return_json_data(file_name)  # read entire file from earlier step
        retrieved_tasks = retrieved_data['tasks']  # get the tasks key
        classified_tasks = []
        # create classification prompts for each task
        for task in retrieved_tasks:
            if "###" not in task and task != "":  # ensure the task is not heading
                aglog.info(f"Classifying `{task}`")
                task_context = {"task": task}
                get_task_class = load_render_template(env_template,
                                                      'task_classifying.prompt',
                                                      task_context)
                classify_task = llm_call_openai(task_sorting_expert,
                                                get_task_class,
                                                model_used_eco)
                # create task object that contains the classification
                task_obj = {"task": task,
                            "task_class": classify_task['response']}
                classified_tasks.append(task_obj)

        # write the classified list to file
        retrieved_data['classified_tasks'] = classified_tasks
        del retrieved_data['tasks']  # remove the tasks keys
        if file_task_classified in os.listdir("."):
            os.remove(file_task_classified)
            # ensure the existing file is removed
        write_responses(file_task_classified, retrieved_data)
        temp = tasks.pop(0)

    if choose_task == "analyse_data":
        file_task_analysed = questionary.path("Provide filename for storing analysis task").ask()  # create a new file
        retrieved_data = return_json_data(file_task_classified)
        # question = "How many code generation tasks are present in above tasks"
        question = questionary.text("Provide your question below: ").ask()
        analysis_context = {"question": question,
                            "task_list": retrieved_data['classified_tasks']}
        get_analysis_task = load_render_template(env_template,
                                                 'data_analysis.prompt',
                                                 analysis_context)
        aglog.info(get_analysis_task)
        analyse_task = llm_call_openai(data_analysis_expert,
                                       get_analysis_task,
                                       model_used_eco)
        question_reply = {"question": question,
                          "llm_reply": analyse_task}
        aglog.info(question_reply)
        if file_task_analysed in os.listdir("."):
            data_to_process = return_json_data(file_task_analysed)
            os.remove(file_task_analysed)
            # remove the file after taking its data
            if 'task_analysis' in data_to_process:
                data_to_process['task_analysis'].append(question_reply)
            else:
                data_to_process['task_analysis'] = [question_reply]
            write_responses(file_task_analysed, data_to_process)

        else:  # only when code is executed for the first time
            retrieved_data['task_analysis'] = [question_reply]
            write_responses(file_task_analysed, retrieved_data)
        tasks.pop(0)

    if choose_task == 'cancel':
        break

    require_continue = questionary.confirm("Do you have more question? ").ask()

    # after completing the tasks, break out of the loop 
    if not require_continue:
        break