import discord
from discord.ext import commands

class General(commands.Cog):
    """
    General commands that server members can use
    """
    def __init__(self, bot): # Defining the constructor method
        self.bot = bot

    # --Gets the latency of the bot--
    @commands.command()
    async def ping(self, ctx): # When the command has been called:
        """
        Checks the current ping for the bot
        """
        msg = f'Pong! Bot latency is {round(self.bot.latency * 1000)}ms.' # Says in chat what the current ping is and rounds it to the nearest whole number
        if self.bot.latency >= 0.125:
            msg += ' Might want to check this out <@701817552778559510>.' # Pings me if the ping is above 125ms
        await ctx.send(msg)
        
    
    # --Getting information about the server--
    # --Checks that the user is me--
    @commands.command(description='Server Information', aliases = ['si', 'info', 'serverinfo'])
    async def server(self, ctx): # When server command is in instance, it will display and embed with the following information
        embed = discord.Embed (title = 'Server Information', description='This embed shows information about the server you are currently in.', colour=discord.Colour.random())
        embed.set_thumbnail (url = 'https://media.discordapp.net/attachments/885197499319603242/895396695532265472/unknown.png')
        embed.set_author (name = 'Server Information', icon_url=ctx.author.avatar_url)
        # For loop to add fields (More code efficient)
        fieldlist = [['Server Name', ctx.guild.name], ['Server Owner', ctx.guild.owner.mention], ['Server Member Count', len([m for m in ctx.guild.members if not m.bot])], ['Bot Creator', '<@448753852863479818>']]
        for i in fieldlist:
            embed.add_field (name = i[0], value=i[1])
        await ctx.reply (embed=embed)

    # --Bot replying to a message if it contains a trigger word--    
    @commands.Cog.listener()
    async def on_message(self, message): # When a message is detected by the bot
         if message.content.lower() == "test": # If bot sees "test" in chat
                await message.reply("Testing, 1, 2, 3!") # It will reply with "Testing, 1, 2, 3!"
         if message.content.lower() == "hello": # If bot sees "hello" in chat
                await message.reply("Hewo!") # It will reply with "Hewo!"

def setup(bot):
    bot.add_cog(General(bot))
