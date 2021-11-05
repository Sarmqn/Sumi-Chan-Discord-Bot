import discord, discord.utils, asyncio, os, json, requests, malclient, secrets
from discord import errors
from discord.ext import commands

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

print(len(code_verifier))
print(code_verifier)

class MyAnimeList(commands.Cog, name = "MyAnimeList"):
    """
    Trying out a MyAnimeList API
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases = ["MAL", "myanimelist", "anime"])
    async def MyAnimeList(self, ctx):
        await ctx.reply("A command for MyAnimeList")
    
    @MyAnimeList.command(aliases = ["Anime", "listanime", "animelist"])
    async def anime(self, ctx):
        anime = cli.search_anime("", limit = None:)
        for ani in anime:
            print(ani)
            print(ani.title)
            
cli = malclient.Client()
cli.init(access_token="<your-access-token>")



