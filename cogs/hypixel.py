import requests
import math
import discord
import os
import PyPixel
from discord.ext import commands

@commands.command()
async def level(ctx, name):
  lvl = hypixel.get_level(name)
  if lvl is None:
    await ctx.send("Player could not be found, please check for errors and try again. Thank you!")
  else:
    await ctx.send(f"Level for {name}: {lvl}")

API_KEY = os.environ.get("API_KEY")
hypixel = PyPixel.Hypixel(API_KEY="API_KEY")
bot.run(API_KEY)

#Network Level Calculator

BASE = 10_000
GROWTH = 2_500
RPQPRE = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = RPQPRE
GROWTH_DIVIDES_2 = 2 / GROWTH

def get_level(player_name):
  url = f"
  res = requests.get(url)
  data = res.json()
  if data["player"] is None:
    return Nothing
  exp = int(dat["player"]["NetworkEXP"]
  return math.floor(1 + REVERSE_PQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp)) 
 
 #Get Skyblock Profiles of a user          
            
 @commands.command(aliases = ['profile', 'profiles', 'prof', 'sbprof', 'sb'])
 async def sbprofile(ctx, name,):
   UniqueUserID = await hypixel.get_uuid('')
   profiles = await hypixel.get_profiles(UniqueUserID)
   print([str(profile) for profile in profiles]])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
            
            
 def setup(bot):
    bot.add_cog(Hypixel(bot))
