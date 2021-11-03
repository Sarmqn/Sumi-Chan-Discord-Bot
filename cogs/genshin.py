import discord
from discord import errors
from discord.ext import commands
import discord.utils
import asyncio
import os
import json
import requests

class Genshin(commands.Cog, name=' Genshin Impact'):
    """
    Trying out a Genshin API
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=['gi', 'g', 'genshinimpact', 'genshin_impact'], description='Get information about Genshin Impact! Use `sc!help genshin` for subcommands.')
    async def genshin(self, ctx):
      await ctx.reply('A Genshin command in the works.')

    @genshin.command(aliases=['ch', 'char'], description='Get character profiles.')
    async def character(self, ctx, character = None, *arguments):
        if character is None:
            embed = discord.Embed(title='Character Profiles', description='Learn more about characters in Genshin! For a list of available characters use `sc!genshin characters`.')
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                embed = discord.Embed(title=f"{character.capitalize()}'s Profile", description=response.json()['description'])
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
                embed.add_field(name='Vision', value=response.json()['vision'], inline=True)
                embed.add_field(name='Weapon Type', value=response.json()['weapon'], inline=True)
                embed.add_field(name='Place of Origin', value=response.json()['nation'], inline=True)
                embed.add_field(name='Place of Origin', value=response.json()['birthday'][-4:], inline=True)
                embed.add_field(name='Skills', value='Use `sc!genshin skills {character}`', inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed it correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_thumbnail(url=f'https://api.genshin.dev/characters/{character}/icon-big')
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
            

def setup(bot):
    bot.add_cog(Genshin(bot))
