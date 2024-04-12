from websockets import serve
from peewee import (
    SqliteDatabase,
)
from models import Promptdata
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from ollama import Client
import os
import logging
import json
import random


load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
logging.basicConfig(format="%(message)s|%(levelname)s",
                    level=logging.INFO)


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
        logging.info(f"Tokens used: {response.usage.total_tokens}")
        return {"response": assistant_message}
    except Exception as e:
        logging.info(e)
        return {"error": "An error occurred while processing the request."}


db = SqliteDatabase("llm_data.db")
db.connect()


async def socket_llm(websocket):
    async for msg in websocket:
        in_data = json.loads(msg)
        logging.info(in_data)
        user_prompt = sys_prompt = None
        if 'user_prompt' in in_data:
            user_prompt = in_data['user_prompt']
        if 'sys_prompt' in in_data:
            sys_prompt = in_data['sys_prompt']
        if user_prompt and sys_prompt:
            logging.info('above llm call...')
            # llm_reply = llm_call_openai(user_prompt,
                                        # sys_prompt,
                                        # 'gpt-3.5-turbo')['response']
            llm_reply = "This is a placeholder reply from llm."
            p_tbl = Promptdata.create(user_prompt=user_prompt,
                                      system_prompt=sys_prompt,
                                      llm_reply=llm_reply)
            p_tbl.save()
        else:
            llm_reply = "Prompts were missing"
        if 'del_table' in in_data:
            send_data = {"ptdel": "Deleting Table"}
            logging.info(send_data)
            await websocket.send(json.dumps(send_data))
            query = Promptdata.delete()
            query.execute() 
    
        # ptbl_data = []
        if Promptdata.select():
            logging.info("Got SQL data...")
            for data in Promptdata.select():
                # ptbl_data.append(dict(user_prompt=data.user_prompt,
                                      # system_prompt=data.system_prompt,
                                      # llm_reply=data.llm_reply))
                row = dict(user_prompt=data.user_prompt,
                           system_prompt=data.system_prompt,
                           llm_reply=data.llm_reply)

                out_data = {"output": llm_reply,
                            "user_prompt": user_prompt,
                            "system_prompt": sys_prompt,
                            "ptbl": row}

                out_str = json.dumps(out_data)
                await websocket.send(out_str)
                await asyncio.sleep(random.randint(0, 5) + 1)
        else:
            send_data = {"ptdel": "Table deleted"}
            await websocket.send(json.dumps(send_data))


async def main():
    async with serve(socket_llm, 'localhost', 7568):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
