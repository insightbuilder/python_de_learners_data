import dbm
import random
import discord
from discord import Message, Member, Role
import os
import requests
import json
from dotenv import load_dotenv

# this bot will work when we chat with it in its channel
# not by mentioning it from other channel. Find how to 
# do that

# the script allows the users to add information to the 
# bot through the KV store that has been created. 
# Users are requesting key and value with single data, 
# not a row/ list of output.


load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
token = os.environ["DISCORD_KEY"]
intents = discord.Intents.default()
intents.members = True
# intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# when using client, the messages themselves contain the 
# trigger words/ symbols to get replies or work done
sad_words = ["sad", "depressed", "unhappy",
             "angry", "anxious", "miserable"]



def get_quotes():
    url_quote = "https://zenquotes.io/api/random"
    resp = requests.get(url=url_quote)
    quodata = json.loads(resp.text)
    quote = quodata[0]['q'] + " - " + quodata[0]['a']
    return quote


def add_enco_message(encourage_msg):
    with dbm.open("encostore", 'c') as db:
        # get the last db key id if already has keys
        if db.keys():
            last_key = str(db.keys()[-1])
            # cast it to int, as it will be used for 
            # getting next key
            last_key = str(last_key).replace("'", '')
            print(last_key)
            last_key_id = int(str(last_key).split('-')[-1])
        else:
            last_key_id = 0
        next_key = f'enco-{last_key_id + 1}'
        db[next_key] = encourage_msg


def del_enco_message(idx):
    with dbm.open('encostore', 'c') as db:
        # first check if the idx can be present in
        # the key value store. See if the idx is 
        # less than len(db.keys) - 1
        idx = idx.strip()
        print(db.keys())
        if int(idx) <= len(db.keys()) - 1:
            key_to_del = f'enco-{idx}'
            # https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
            key_to_del = key_to_del.encode('utf-8')
            print(key_to_del)
            del db[key_to_del]
        # else don't do anything


@client.event
async def on_ready():
    print(f"Bot has landed as {client.user}")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return  # just return if the user is messager

    if message.content.startswith("#inspire"):
        quote = get_quotes()
        # send the quote back in the channel it was 
        # requested
        await message.channel.send(quote)

    cheering_words = ["cheer, up", "Giddy up",
                      "You are a awesome human being"]
    
    # get the cheering messages from db
    with dbm.open("encostore", 'c') as db:
        cheering_words += db.values()
        print(f"Number of cheering words: {len(cheering_words)}")

    if message.content.startswith("#new"):
        enco_mess = message.content.split("#new", 1)[1]
        print(enco_mess)
        add_enco_message(encourage_msg=enco_mess)
        await message.channel.send(f"Added {enco_mess} to db")

    if message.content.startswith("#del"):
        msg_id = message.content.split("#del", 1)[1]
        print(msg_id)
        del_enco_message(msg_id)
   
    if message.content.startswith("#list"):
        with dbm.open("encostore", 'c') as db:
            added_messages = ''
            if len(db.values()) != 0:
                for vals in db.values():
                    added_messages += "\n" + str(vals)
            else:
                added_messages = "Nothing in kv store"
        await message.channel.send(added_messages)

    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(cheering_words))

client.run(token=token)
