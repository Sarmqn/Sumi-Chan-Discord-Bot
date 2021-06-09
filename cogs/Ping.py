import time
import os
import discord

@bot.command(name = 'Ping', description= "Checks the current ping")
async def ping(ctx):
    await ctx.send(f'Pong! {round (bot.latency * 1000)} ms') #Says in chat what the current ping is and rounds it
