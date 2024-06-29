import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot
from dotenv import load_dotenv
from discord import HTTPException
import os

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

import random

class CustContext(Context):
    async def selftick(self, value):
        """Reacts with a emoji depending on value is true or
        false"""
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            await self.message.add_reaction(emoji)
        except HTTPException:
            pass 


class CustBot(Bot):
    async def get_context(self, message, *, cls=CustContext):
        # override the method to pass the custom context
        return await super().get_context(message, cls=cls)

intents = discord.Intents.default()
intents.message_content = True

bot = CustBot(command_prefix="#", intents=intents)

@bot.command()
async def guess(ctx: Context, number: int):
    "Guess a random number"
    value = random.randint(1, 6)
    # value = 5 
    # check if value you gave is matching the 
    # random generated number
    # ctx_guild = ctx.guild.name
    ctx_message = ctx.message.content
    ctx_author = ctx.author.name
    print(f"Guild Name: ctx_guild Message: {ctx_message} author {ctx_author}")
    await ctx.selftick(number == value)
    # this is basically calling the method in the 
    # custom context, which is internally checking 
    # the logic, but why? 
    # The new context can be used for building complex
    # contexts

token = os.environ["DISCORD_KEY"]
bot.run(token=token)