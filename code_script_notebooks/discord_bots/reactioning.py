from discord import (
    Client,
    PartialEmoji,
    RawReactionActionEvent,
    HTTPException
)
from dotenv import load_dotenv

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

class ReactClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 0 # ID of the role that can be reacted to
        self.emoji_to_role = {
            PartialEmoji(name="🔴"): 0,
            PartialEmoji(name="🟢", id=0): 0,
            PartialEmoji(name="🟡"): 0,
        }
    
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """Gives role based on the reaction emoji"""
        # make sure the message the user reacting to is the one 
        # we care about
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            print("Returning due to none guild") 
            return
       
        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return  # the emoji is not the one we can use
     
        role = guild.get_role(role_id)

        if role is None:
            return
        
        try:
            await payload.member.add_roles(role)
        except HTTPException:
            print("Excepting HTTP error")
            pass

    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass    

import os
from discord import Intents
intents = Intents.default()
intents.members = True

client = ReactClient(intents=intents)

client.run(os.environ["DISCORD_KEY"])