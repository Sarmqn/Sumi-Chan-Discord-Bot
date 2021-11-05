import discord, discord.utils, asyncio, os, json, requests
from discord import errors
from discord.ext import commands

class Genshin(commands.Cog, name='<:GenshinImpact:905489184205197322> Genshin Impact'):
    """
    Trying out a Genshin API
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=['gi', 'g', 'genshinimpact', 'genshin_impact'], description='Get information about Genshin Impact! Use `sc!help genshin` for subcommands.')
    async def genshin(self, ctx):
      await ctx.reply('Genshin Impact is a free-to-play action RPG developed and published by miHoYo. The game features a fantasy open-world environment and action based combat system using elemental magic, character switching, and gacha monetization system for players to obtain new characters, weapons, and other resources. The game can only be played with an internet connection and features a limited multiplayer mode allowing up to four players in a world.\n\nUse `sc!help genshin` for subcommands!', mention_author=False)

    @genshin.command(aliases=['ch', 'char'], description='Get character profiles.')
    async def character(self, ctx, character = None):
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
                embed.add_field(name='Birthday', value=response.json()['birthday'][-5:], inline=True)
                embed.add_field(name='Skills', value=f'Use `sc!genshin skills {character}`', inline=True)
                embed.add_field(name='Constellations', value=f'Use `sc!genshin constellation {character}`', inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the character command.\nArguments: {character}")
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @genshin.command(aliases=['s', 'skill', 't', 'talents'], description="Look at a character's skills.")
    async def skills(self, ctx, character: str = None):
        if character is None:
            embed = discord.Embed(title='Character Profiles', description="Learn about a Genshin characters' skills! For a list of available characters use `sc!genshin characters`.")
        else:
            character = character.lower()
            response = requests.get(f'https://api.genshin.dev/characters/{character}/')
            if response.status_code == 200:
                skills = response.json()['skillTalents']
                for i in skills:
                    upgradesText = ''
                    for j in i['upgrades']:
                        upgradesText += f"{j['name']}: {j['value']}"
                    embed.add_field(name=f"{i['name']} ({i['unlock']})", value=f"{i['description']}\n**Upgrades:**\n{upgradesText}", inline=True)
            elif response.status_code == 404:
                embed = discord.Embed(title='Character Profiles', description='That person does not exist! Please make sure you typed their name correctly!', color=discord.Color.from_rgb(200,0,0))
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/737096050598346866/906223201166704640/ehe_te_nandayo.png')
            else:
                embed = discord.Embed(title='Character Profiles', description='Uh oh, an error has occured!\nThe developer has been informed and will work on this issue ASAP!', color=discord.Color.from_rgb(200,0,0))
                self.bot.get_user(221188745414574080).send(f"There was a {response.status_code} code from the Genshin API in the character command.\nArguments: {character}")
        embed.set_author(name='Character Profiles', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @genshin.command(aliases=['co'], description="Look at a character's constellation.")
    async def constellation(self, ctx, * character: str):
        await ctx.reply('Hi!')
    
            
def setup(bot):
    bot.add_cog(Genshin(bot))
