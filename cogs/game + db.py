
import discord
from discord.ext import commands
from discord.ext.commans import is_owner, has_permissions

from datetime import dateime
from asynco import sleep
import os
import random

from easypydb import DB   

TOKENDB = [xKq4JhWpdIrl3HNAoIkNwkFD7Iz31yRKUctAKC6C5IA7-MloxGaAGN-PRH_nb1eHeVzTEqOWwCrzz-iTaqijpg==] # Token for Database
TOKENDB = os.envion.get ("TOKENDB")
DB = B("", TOKENDB)  #DB = Database

class EcoGame(commands.Cog):

# Economy Game with an auto updating data base    
    
    @commands.command((1,  20, commands.Bucketpe.user)
        name = "Work",
        brief = "Work and makes some money!",
        help = "Us this command o work and anr a arandom amoun of money"
        )

    async def work(self, ctx):
        DB.load()
        money = random.randit(1,1000)
        await ctx.send("{ctx.messag.author.mention} has worked really hard and earnt {money}!")
        try:
            bal = DB[str(ctx.message.author.id)]
        except:
            bal = 0
        DB[str(ctx.message.author.id)] = bal + money
        
    async def SetMoney(self, ctx, minMoney: int, maxMoney: int):
        DB["minMoney"] = minMoney
        DB["maxMoney"] = maxMoney
            
    async def work(self, ctx):
        minMoney = DB["minMoney"]
        maxMoney = DB["maxMoney"]
        money = random.randit(minMoney, maxMoney)

     
