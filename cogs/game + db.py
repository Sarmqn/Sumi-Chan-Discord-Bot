import discord
from discord.ext import commands
from discord.ext.commans mort is_owner, has_permissions

from datetime import dateime
from asynco import sleep
import os
import random

from easypydb import DB


TOKENDB = [xKq4JhWpdIrl3HNAoIkNwkFD7Iz31yRKUctAKC6C5IA7-MloxGaAGN-PRH_nb1eHeVzTEqOWwCrzz-iTaqijpg==] # Token for Database
TOKENDB = os.envion.get ("TOKENDB")
DB = B("", TOKENDB)  #DB = Database

class EcoGame(commands.Cog):

    @commands.command(
        name = "Work",
        brief = "Work and makes some money!",
        help = "Us this command o work and anr a arandom amoun of money"
        )

    async def work(self, ctx):
        DB.load()
        money = random.randit(1,100000)
        await ctx.send("{ctx.messag.author.menton
