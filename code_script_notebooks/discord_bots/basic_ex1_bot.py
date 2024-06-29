import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog
from dotenv import load_dotenv
import os
import random

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

description = """Example bot to show case the discord.ext.commands"""

intents = discord.Intents.default()

intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?",
                   description=description,
                   intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("--------")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers and sends the data back"""
    await ctx.send(left + right)
# ?add 1 2 to invoke the above command

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format"""
    try:
        rolls, limit = map(int, dice.split('d'))
        # splits the input and converts them to int
    except Exception:
        await ctx.send("Format has to be NdN")
        return

    result = ', '.join(str(random.randint(1, limit) for r in range(rolls))) 
    await ctx.send(result)


# Another way of creating commands
@commands.command()
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

bot.add_command(choose)


@bot.command()
async def argcount(ctx, *args):
    "Lets count the given arguments"
    await ctx.send(len(args))


@bot.command()
async def repeatme(ctx, times: int, content="May be..."):
    "Repeats the content times time"
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def showjoined(ctx, member: discord.Member):
    "Reports a member joined"
    await ctx.send(f"{member.name} joined {discord.utils.format_dt(member.joined_at)}")


# this is different, commands with sub commands
@bot.group()
async def cool(ctx: Context):
    "Checks if the user is cool"
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} is not called")


    @cool.command(name='tob')
    async def _bot(ctx):
        "is the bot cool"
        await ctx.send("Yep, its cool")

token = os.environ["DISCORD_KEY"]
bot.run(token=token)