from discord import voice_client
from discord.channel import VoiceChannel
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

players = {}

@commands.Cog.listener(pass_context=True, aliases = ["Connect", "JoinVC"])
async def Join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_Voice_Channel(channel)

@commands.Cog.listener(pass_context=True, aliases = ["fuckoff", "dc", "disconnect", "LeaveVC"])
async def leave(ctx):
    server = ctx.message.server
    Voice_client = client.voice_channel_in(server)
    await Voice_client.disconnect()

@commands.Cog.listener(pass_context=Truealiases = ["p"])
async def play(ctx, url):
    server = ctx.message.server
    Voice_client = client.Voice_client_in(server)
    player = await Voice_client.create.ytdl_player(url)
    players[server.id] = player
    player.start()

    def setup(bot):
    bot.add_cog(Music(bot))
