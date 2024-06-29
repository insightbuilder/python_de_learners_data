import discord
from discord import Client, Member, Guild
from dotenv import load_dotenv
import os
load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")
token = os.environ["DISCORD_KEY"]


class JoinClient(Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_member_join(self, member: Member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}"
            await guild.system_channel.send(to_send)


intents = discord.Intents.default()
intents.members = True

client = JoinClient(intents=intents)
client.run(token=token)
