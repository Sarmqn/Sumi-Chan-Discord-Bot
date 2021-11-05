import requests, math, discord, os, pypixel
from discord.ext import commands

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def level(player_name: str): # Player Level command
    data = requests.get(url = "https://api.hypixel.net/player", params = {"key": API_KEY,"name": player_name}).json() # Create an api get request to recieve data about the players account
    return data
    
def setup(bot):
    bot.add_cog(Hypixel(bot))

# There's vomit on his sweater already
