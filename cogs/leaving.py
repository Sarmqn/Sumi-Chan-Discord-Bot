import discord
from discord.ext import commands

@bot.event
async def on_member_remove(member):
    print (f"{member} has left this server :-(")
