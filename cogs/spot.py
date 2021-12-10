from discord import *
from discord.ext import *

class spot(commands.Cog, name = '🎵 Spotify'):
    """
    Command that grabs information about a user's spotify activity
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description = "
