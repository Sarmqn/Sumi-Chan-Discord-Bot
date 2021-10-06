import discord
from discord.ext import commands


class General(commands.Cog):
    """
    General commands that server members can use
    """

    def __init__(self, bot):  # Defining the Init constructor
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):  # When ping is in instance:
        """
        Checks the current ping for the bot
        """
        if self.bot.latency >= 0.125:
            await ctx.send(
                f"Pong! Bot latency is {round(self.bot.latency * 1000)}ms. Might want to check this out <@701817552778559510>."
            )  # Pings me if the ping is above 125ms
        else:
            await ctx.send(
                f"Pong! Bot latency is {round(self.bot.latency * 1000)}ms"
            )  # Says in chat what the current ping is and rounds it to the nearest whole number

    # --Getting information about the server--
    @commands.command(name="server")
    async def server_info(
        self, ctx: commands.Context
    ):  # When server_info is in instance:
        guild = ctx.guild  # Collect data about the server
        await ctx.send(f"Server Name: {guild.name}")  # Print out the Server's Name.
        await ctx.send(
            f"Owner Name: {guild.owner.display_name}"
        )  # Print out the Server's Owner.
        await ctx.send(
            f"Server Size: {len(guild.members)}"
        )  # Print out the member size of the server.

    # --Bot replying to a message if it contains a trigger word--
    @commands.Cog.listener()
    async def on_message(
        self, message: discord.Message
    ):  # When on_message is in instance:
        if message.content == "test":  # If bot sees "test" in chat
            await message.channel.send(
                "Testing 1, 2, 3!"
            )  # It will print out "Testing 1, 2, 3!"
        if message.content == "hello":  # If bot sees "hello" in chat
            await message.channel.send("Hewo!")  # It will print out "Hewo!"


def setup(bot):
    bot.add_cog(General(bot))


# Knees weak
