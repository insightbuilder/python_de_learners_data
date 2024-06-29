import discord
from dotenv import load_dotenv
import os
import logging

# manually setting up the logger

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

# this is the 2nd logger, with a different name
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=1024 * 1024 * 32, # max 1KiB
    backupCount=5
)

dt_fmt = "%Y-%m-%d %H| %M"
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}:{message}',
                              datefmt=dt_fmt, style="{")
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w',)
load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
# each of the intents have to enabled
# opted in based on the requirements
intents = discord.Intents.default()  

intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready(): # finished logging in
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):  # recieves a message from a new user
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("$listguilds"):
        guilds = discord.utils.get(client.guilds, name='GenAI Coder')
        logging.info(guilds)
        guild_string = ",".join(guilds)
        await message.channel.send(guild_string)

discord_key = os.environ["DISCORD_KEY"]
client.run(discord_key, log_handler=handler,
           log_level=logging.DEBUG)

