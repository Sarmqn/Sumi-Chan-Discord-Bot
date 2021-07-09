import discord
from discord.ext import commands
from random import randint

helplist = [['ban', 'Bans a user.'], ['mute', 'Indefinitely mutes a user.'], ['unmute', 'Unmutes a muted user.'], ['invite', 'Creates an invite link for the server.'], ['ping', "Checks the bot's ping."], ['server', 'Sends information about the server.'], ['disconnect', 'Disconnects the users voice channel.'], ['join', 'Joins the voice channel of the user.'], ['pause', 'Pauses the currently playing song.'], ['play', 'Plays a song!'], ['resume', 'Resumes the currently playing song!']]


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command('help')
    async def help(self, ctx, *hargs, member=discord.Member):
        hargs = ''.join(hargs)
        if hargs == '':
                HelpEmbed=discord.Embed(title=f'Help for {ctx.guild.me.display_name}!', description='This message will self-destruct in 2 minutes so as to not take up too much space.', color=discord.Color.from_rgb(randint(0, 255),randint(0, 255),randint(0, 255)))
                if member.guild_permissions.administrator==True:
                    HelpEmbed.add_field(name="Admin", value="ban\nmute\nunmute", inline=True)
                    HelpEmbed.add_field(name="Utility", value="invite\nping\nserver", inline=True)
                    HelpEmbed.add_field(name="Music", value="disconnect\njoin\npause\nplay\nresume", inline=True)
                    HelpMessage = await ctx.send(embed=HelpEmbed)
                else:
                    found = False
                for i in helplist:
                    if i[0] == f'{hargs}':
                        index = helplist.index(i)
                        found = True
                        break
                    else:
                        pass
                if found == False:
                    HelpMessage = await ctx.send(embed=discord.Embed(title='Misspelling?', description=f'I could not find {hargs} command in the list of commands {ctx.author.mention}!'))
                else:
                    HelpEmbed=discord.Embed(title=f"Help for '{hargs}'!", description='', color=discord.Color.from_rgb(randint(0, 255),randint(0, 255),randint(0, 255)))
                    HelpEmbed.add_field(name="Description", value=f'{helplist[index][1]}', inline=False)
                HelpMessage = await ctx.send(embed=HelpEmbed)
                await ctx.message.delete()
                await asyncio.sleep(120)
                await HelpMessage.delete()


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))
