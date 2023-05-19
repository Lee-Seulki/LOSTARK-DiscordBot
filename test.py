import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup 
 
app = commands.Bot(command_prefix='/')

discord_config = {}

with open('discord_config', 'r', encoding='utf-8') as f:
    configs = f.readlines()
    for config in configs:
        key, value = config.rstrip().split('=')
        discord_config[key] = value

DISCORD_TOKEN = discord_config['DISCORD_TOKEN']
 
@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def hello(ctx):
    await ctx.send('Hello I am Bot!')

@app.command()
async def 모험가(ctx, *, name): #/모험가 정대만의무릎보호대
    try:
        # https://lostark.game.onstove.com/Profile/Character
        
        LOSTARK_URL = 'https://lostark.game.onstove.com/Profile/Character/'
        response = requests.get(LOSTARK_URL + name,  verify=False)

        data = response.text
        print(data)
        
    except Exception as e:
        print(e)
    
    except discord.ext.commands.errors.MissingRequiredArgument:
        await ctx.send(f'{name}인 모험가는 존재하지 않습니다.')
    
app.run(DISCORD_TOKEN)