import discord
from discord import errors
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import os
import json


async def add_rr(messageID: int, roleID: int, emoteID):
    if os.path.isfile("roles.json"):
        # Opens file and loads the data.
        with open("roles.json", "r") as votes:
            data = json.load(votes)
        try:
            data[f"{messageID}"] += {f"{emoteID}":{"roleID":roleID}}
        except KeyError:
            data[f"{messageID}"] = {f"{emoteID}":{"roleID":roleID}}
    else:
        data = {f"{messageID}": {f"{emoteID}":{"roleID":roleID}}}
    # Saves file to store the data.
    with open("roles.json", "w+") as votes:
        json.dump(data, votes, sort_keys=True, indent=4)


async def get_rr(messageID: int, emoteID):
    with open("roles.json", "r") as votes:
        data = json.load(votes)
    return data[f"{messageID}"][f"{emoteID}"]

async def check_rr(messageID):
    with open("roles.json", "r") as votes:
        data = json.load(votes)
    if data[f"{messageID}"]:
      return True
    else:
      return False

async def remove_rr(messageID: int, emoteID):
    if os.path.isfile("roles.json"):
        # Opens file and loads the data.
        with open("roles.json", "r") as votes:
            data = json.load(votes)
        data.pop(f'{messageID}')
        json.dump(data, open("roles.json", "w+"), indent=4)
        except KeyError:
            print(f"The message ID {messageID} has no reaction roles!")
        else:
            pass















class TempRoles(commands.Cog):
    """
    Temporarily trying to use a json file for reaction roles
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() # Detect discord.gg invite links and delete them.
    async def on_raw_reaction_add(self, payload):
        if check_rr(payload.messageid):
          guild = self.bot.get_guild(payload.guild_id)
          user = payload.member

          messageID = payload.message_id
          emoteID = payload.emoji
          print(emoteID)
          roleID = get_rr(messageID, emoteID)

          roletogive = discord.utils.get(guild.roles, id=roleID)

          await user.add_roles(roletogive)
            

def setup(bot):
    bot.add_cog(TempRoles(bot))
