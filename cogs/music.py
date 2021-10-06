import discord
from discord import client
from discord.ext import commands
import youtube_dl


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(f"You are not within a Voice Channel.")
        voice_channel = ctx.authur.connect()
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2",
            "options": "-vn",
        }
        YDL_OPTIONS = {"format": "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(2, download=False)
        url2 = info["formats"][0]["url"]
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play[source]

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_cleint.pause()
        await ctx.send(f"Paused ")

    @commands.command()
    async def Resume(self, ctx):
        await ctx.voice_cleint.resume()
        await ctx.send(f"Resumed")


def setup(client):
    client.add_cog(music(client))


# He's nervous
