from discord import voice_client
from discord.channel import VoiceChannel
from discord.ext import commands,tasks
from dotenv import load_dotenv
import youtube_dl
import os


load_dotenv()
players = {}

intents = discord.Intents().all.()
Client = discord.Client(intents=intents)

class music(commands.Cog):
    """
    Music Commands to join a VC, play music within that VC, and leave the VC.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["j"])
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        Voice_client = await channel.connect()

    @commands.command(aliases = ["fuckoff", "dc", "disconnect", "LeaveVC"])
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not currently connected to a voice channel.")

    @commands.command(aliases = ["p"])
    async def play(self, ctx, url):
        server = ctx.guild
        player = await Voice_client.create.ytdl_player(url)
        players[server.id] = player
        player.start()
        
    @commands.command(aliases = ["Pause", "halt])
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()
        print('Pause')
   
   @commands.command(aliases = ["Stop", "Discontinue", "end"])
   async def stop(self, ctx
                                 
def setup(bot):
    bot.add_cog(music(bot))
