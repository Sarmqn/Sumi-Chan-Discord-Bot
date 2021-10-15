import discord
from discord.ext import commands

# Defining a checking function to be used for certain commands only I want to be able to use
def is_me():
    def predicate(ctx):
        return (ctx.message.author.id == 701817552778559510) or (ctx.message.author.id == 221188745414574080) or (ctx.message.author.id == 448753852863479818)
    return commands.check(predicate)

class General(commands.Cog):
    """
    General commands that server members can use
    """
    def __init__(self, bot): # Defining the Init constructor
        self.bot = bot

    @commands.command(name = 'ping')
    async def ping(self, ctx: commands.Context): # When ping is in instance:
        """
        Checks the current ping for the bot
        """
        if self.bot.latency >= 0.125:
            await ctx.send(f'Pong! Bot latency is {round(self.bot.latency * 1000)}ms. Might want to check this out <@701817552778559510>.') # Pings me if the ping is above 125ms
        else:
            await ctx.send(f'Pong! Bot latency is {round(self.bot.latency * 1000)}ms') # Says in chat what the current ping is and rounds it to the nearest whole number
        
    
    # --Getting information about the server--
    # --Checks that the user is me
    @commands.command(description='Server Information', aliases = ['si', 'info', 'serverinfo'])
    @is_me
    async def server(self, ctx): # When server command is in instance, it will display and embed with the following information
        embed = discord.Embed (title = 'Server Information', description='This embed shows information about the server you are currently in.', colour=discord.Colour.random())
        embed.set_thumbnail (url = 'https://media.discordapp.net/attachments/885197499319603242/895396695532265472/unknown.png')
        embed.set_author (name = 'Server Information', icon_url=ctx.author.avatar_url)
        embed.add_field (name = 'Server Name:', value = ctx.guild.name)
        embed.add_field (name = 'Server Owner:', value = ctx.guild.owner.mention)
        embed.add_field (name = 'Server Member Count:', value = len(ctx.guild.members))
        embed.add_field (name = 'Bot Creator:', value = '<@701817552778559510>')
        await ctx.reply(embed=embed)

    # --Bot replying to a message if it contains a trigger word--    
    @commands.Cog.listener()
    async def on_message(self, message): # When on_message is in instance:
         if message.content == "test": # If bot sees "test" in chat
                await message.channel.send("Testing 1, 2, 3!") # It will print out "Testing 1, 2, 3!"
         if message.content == "hello": # If bot sees "hello" in chat
                await message.channel.send("Hewo!") # It will print out "Hewo!"

def setup(bot):
    bot.add_cog(General(bot))

# Knees weak
