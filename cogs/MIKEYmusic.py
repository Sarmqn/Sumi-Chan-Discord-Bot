
import asyncio
import re
import discord
import lavalink
from discord.ext import commands
from discord.ext.forms import Form
url_rx = re.compile(r'https?://(?:www\.)?.+')
ytrx = re.compile(r'https?:\/\/(?:www)?youtu(\.be|be\.com)')
spotifyuri = re.compile(r'spotify\:(track|album)\:.+')
beforebypass = ['lyrics','queue']
global que
que = {}

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('lava.link', 80, 'joemama', 'eu', 'sumichan')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        # Cog unload handler. This removes any event hooks that were registered.
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            voice = await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.
        else:
            return False

        return guild_check and voice

    async def ensure_voice(self, ctx: commands.Context):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            await ctx.send("You need to join a voice channel!")
            return False

        if not player.is_connected:
            if not should_connect:
                if ctx.command.name not in beforebypass:
                    await ctx.send("Not connected to a voice channel!")
                    return False

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                await ctx.send('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
            return True
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                await ctx.send('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await asyncio.sleep(30)
            if not event.player.is_playing:
                await self.connect_to(guild_id, None)

        if isinstance(event,lavalink.events.TrackEndEvent):
            gq = que[int(event.player.guild_id)]
            gq.pop(0)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if member == member.guild.me:
            return
        player = self.bot.lavalink.player_manager.get(member.guild.id)
        g = self.bot.get_guild(int(player.guild_id))
        vc = g.get_channel(int(player.channel_id))
        if before.channel is vc and after.channel is not vc and len(vc.members) < 2:
            await asyncio.sleep(15)
            if len(vc.members) > 2:
                return
            else:
                player.queue.clear()
                await player.stop()
                await self.connect_to(player.guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(name="play",description="Play a song/Unpause the player",aliases=['p'],usage="play <query>")
    async def play(self, ctx, *, query: str=None):
        empty = []
        try:
            test = str(que[ctx.guild.id])
            print(test)
        except:
            que[ctx.guild.id] = empty
        """ Searches and plays a song from a given query. """
        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if query == None:
            if player.paused:
                await player.set_pause(False)
                await ctx.message.add_reaction("▶")
                return
            else:
                await ctx.send("You forgot to tell me the song!")
                return
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)
                que[ctx.guild.id].append(track)
            embed = discord.Embed(title='Playlist Enqueued!',description=f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks',color=discord.Color.green())
        else:
            track = results['tracks'][0]
            embed = discord.Embed(title=f"Added {track['info']['title']} to the queue",color=discord.Color.green())
            embed.add_field(name='Duration',value=lavalink.format_time(int(track['info']['length'])),inline=True)
            embed.add_field(name='Author',value=track['info']['author'],inline=True)
            embed.set_thumbnail(url=f"https://img.youtube.com/vi/{track['info']['identifier']}/hqdefault.jpg")
            player.add(requester=ctx.author.id, track=track)
            track['requester'] = ctx.author.id
            que[ctx.guild.id].append(track)
        await ctx.send(embed=embed)
        if not player.is_playing:
            await player.play()

    @commands.command(name="skip",description="Skip the current playing song.",usage="skip")
    async def skip(self,ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            await ctx.send("I'm not playing anything!")
        else:
            await player.skip()
            await ctx.message.add_reaction("⏭")
            gq = que[int(player.guild_id)]
            gq.pop(0)

    @commands.command(name='pause',description='Pauses playback of the current playing song.',usage='pause')
    async def pause(self,ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused:
            await player.set_pause(False)
            await ctx.message.add_reaction("▶")
        else:
            await player.set_pause(True)
            await ctx.message.add_reaction("⏸")

    @commands.command(name="current",description="Sends the current playing song",usage="current",aliases=['np','nowplaying'])
    async def current(self,ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        current = await player.node.get_tracks(f"ytsearch:{player.current.identifier}")
        current = current['tracks'][0]
        embed=discord.Embed(title=f"Current Track for {ctx.guild.name}",description=f"{current['info']['title']} - {current['info']['author']}")

    @commands.command(name="queue",description="Check the current queue!",usage="queue",aliases=['q','que','cue'])
    async def queue(self,ctx):
        page = 1
        embed=discord.Embed(title=f"Queue for {ctx.guild.name}",color=discord.Color.green())
        try:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        except:
            await ctx.send("I'm not connected to a voice channel!")
        else:
            if player.queue == [] and not player.is_playing:
                embed=discord.Embed(title="There aren't any songs yet...",description="Doesn't mean you can't start the party! Use the `play` command to play a song!",color=discord.Color.green())
                await ctx.send(embed=embed)
                return
            ipp = 5
            start = (page-1) * ipp
            end = start + ipp
            current = await player.node.get_tracks(f"ytsearch:{player.current.identifier}")
            current = current['tracks'][0]
            emlist = []
            for i in range(0,len(que[ctx.guild.id])//5):
                embed=discord.Embed(title=f"Queue for {ctx.guild.name}",color=discord.Color.green())
                for t in que[ctx.guild.id][start:end]:
                    try:
                        d = que[ctx.guild.id][end]
                    except IndexError:
                        end = (len(que[ctx.guild.id]))
                    if int(que[ctx.guild.id].index(t)) == 0:
                        embed.add_field(name=f"1. {player.current.title}",value=f"**Duration:** {lavalink.format_time(int(current['info']['length']))}\n**Author:** {current['info']['author']}",inline=False)
                    else:
                        embed.add_field(name=f"{que[ctx.guild.id].index(t)+1}. {t['info']['title']}",value=f"**Duration:** {lavalink.format_time(int(t['info']['length']))}\n**Author:** {t['info']['author']}",inline=False)
                start += 5
                end += 5
                emlist.append(embed)
            if len(emlist) > 2:
                menu = forms.ReactionMenu(ctx, emlist)
                menu.set_timeout(60)
                menu.add_pages(emlist)
                await menu.start()
            else:
                await ctx.send(embed=emlist[0])

    @commands.command(name="clear",description="Clear the current queue",usage="clear",aliases=['clearqueue','clearq','clearque'])
    async def clear(self,ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.queue.clear()
        gq = que[ctx.guild.id]
        for i in range(1,(len(gq)-1)):
            gq.pop(i)

    @commands.command(name="disconnect",description="Disconnect the bot from the current voice channel.",usage="disconnect",aliases=['dc','stop'])
    async def disconnect(self, ctx):
        #Disconnects the player from the voice channel and clears its queue.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voice channel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')

def setup(bot):
    bot.add_cog(Music(bot))
   
