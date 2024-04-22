import os

from groq import Groq
from dotenv import load_dotenv
load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
