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

    @bot.command()
    async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(aliases = ["fuckoff", "dc", "disconnect", "LeaveVC"])
    async def leave(self, ctx):
        server = ctx.message.server
        Voice_client = client.voice_channel_in(server)
        await Voice_client.disconnect()

    @commands.command(aliases = ["p"])
    async def play(self, ctx, url):
        server = ctx.message.server
        Voice_client = client.Voice_client_in(server)
        player = await Voice_client.create.ytdl_player(url)
        players[server.id] = player
        player.start()

def setup(bot):
    bot.add_cog(music(bot))
