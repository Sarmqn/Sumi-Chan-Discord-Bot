from discord import voice_client
from discord.channel import VoiceChannel
from discord.ext import commands


players = {}

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
        server = ctx.guild
        channel = ctx.author.voice.channel
        await Voice_client.disconnect()

    @commands.command(aliases = ["p"])
    async def play(self, ctx, url):
        server = ctx.guild
        player = await Voice_client.create.ytdl_player(url)
        players[server.id] = player
        player.start()

def setup(bot):
    bot.add_cog(music(bot))
