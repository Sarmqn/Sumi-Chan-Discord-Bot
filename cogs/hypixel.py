import requests, math, discord, hypixel, os, pypixel
from discord.ext import commands

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

BASE = 10_000
GROWTH = 2_500
RPQPRE = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = RPQPRE
GROWTH_DIVIDES_2 = 2 / GROWTH
API_KEY = os.environ.get("API_KEY")
hypixel = PyPixel.Hypixel(API_KEY=f"{API_KEY}")

def level(player_name: str): # Player Level command
    data = requests.get(url = "https://api.hypixel.net/player", params = {"key": API_KEY,"name": player_name}).json(): # Create an api get request to recieve data about the players account
    
                                                                          
                                                             
  # From https://hypixel.net/threads/python-how-to-get-a-person%E2%80%99s-network-level-from-their-network-exp.3242392/
  hypixel_data = requests.get(url).json()
  network_experience = hypixel_data["player"]["networkExp"]
  network_level = (math.sqrt((2 * network_experience) + 30625) / 50) - 2.5
  network_level = round(network_level, 2)
  return network_level
  #res = requests.get(url, params = {auth: api_key, uuid='b0ab95fc29254fda9ce5d30af3111a84'})
  #data = res.json()
  #if data["player"] is None:
  #  return Nothing
  #exp = int(dat["player"]["NetworkEXP"]
  #return math.floor(1 + RPQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp)) 
    
@commands.command()
async def level(ctx, name: str):
  lvl = get_level(name)
  if lvl is None:
    await ctx.send("Player could not be found, please check for errors and try again. Thank you!")
  else:
    await ctx.send(f"Level for {name}: {lvl}")

#Network Level Calculator
 
#Get Skyblock Profiles of a user          
            
@commands.command(aliases = ['profile', 'profiles', 'prof', 'sbprof', 'sb'])
async def sbprofile(ctx, name: str):
    UniqueUserID = await hypixel.get_uuid(f'name')
    profiles = await hypixel.get_profiles(UniqueUserID)
    print([str(profile) for profile in profiles])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
            
def setup(bot):
    bot.add_cog(Hypixel(bot))

# There's vomit on his sweater already
