"""
import requests
import math
import discord
from discord.ext import commands

@commands.command()
async def level(ctx, name):
  lvl = hypixel.get_level(name)
  if lvl is None:
    await ctx.send("Player could not be found, please check for errors and try again. Thank you!")
  els:
    await ctx.send(f"Level for {name}: {lvel})

API_KEY = os.environ.get("API_KEY")
bot.run(API_KEY)

#Network Level Calculator

BASE = 10_000
GROWTH = 2_500
REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2 / GROWTH

def get_level(player_name):
  url = f"
  res = requests.get(url)
  data = res.json()
  if data["playe"] is None:
    return Nothing
  exp = int(dat["player"]["NetworkEXP"]
  return math.floor(1 + REVERSE_PQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp)) 
            
 def setup(bot):
    bot.add_cog(Hypixel(bot))
"""
