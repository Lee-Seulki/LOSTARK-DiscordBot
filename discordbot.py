import discord
from discord.ext import commands

from crawling_data import get_character_info, get_marishop_item
 
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
        character_info = get_character_info(name)

        if character_info is None:
            await ctx.send(f'{name}인 모험가는 존재하지 않습니다.')

        embed=discord.Embed(title=name, description=character_info['server'], color=0xca7cee)

        embed.set_author(name="모코코테스트")
        embed.set_thumbnail(url=character_info['thumnail'])
        embed.add_field(name="원정대 레벨", value=f"`{character_info['level-info__expedition']}`", inline=True)
        embed.add_field(name="전투 레벨", value=f"`{character_info['level-info__item']}`", inline=True)
        embed.add_field(name="장착 아이템 레벨", value=f"`{character_info['level-info2__expedition']}`", inline=True)
        embed.add_field(name="달성 아이템 레벨", value=f"`{character_info['level-info2__item']}`", inline=True)
        embed.add_field(name="칭호", value=f"`{character_info['game-info__title']}`", inline=True)
        embed.add_field(name="길드", value=f"`{character_info['game-info__guild']}`", inline=True)
        embed.add_field(name="PVP", value=f"`{character_info['level-info__pvp']}`", inline=True)
        embed.add_field(name="영지", value=f"`{character_info['game-info__wisdom']}`", inline=True)
        
        formatted_engraves = [f"`{engrave}`" for engrave in character_info['engraves']]
        value = '\n'.join(formatted_engraves)

        embed.add_field(name="각인효과", value = value, inline=True)
        embed.set_footer(text="Dev by 지상최고의개발자")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f'모험가 정보를 가져오는 중에 오류가 발생했습니다: {str(e)}')

@app.command()
async def 마리샵(ctx):
    items = get_marishop_item()
    
    embed=discord.Embed(title="마리샵", description="전영팩 떴냐??", color=0xca7cee)
    embed.set_author(name="모코코테스트")

    formatted_items = [f"`{item}`" for item in items]
    value = '\n'.join(formatted_items)

    embed.add_field(name="전투ㆍ생활 추천", value=value, inline=False)
    embed.set_footer(text="Dev by 지상최고의개발자")
    await ctx.send(embed=embed)
    
app.run(DISCORD_TOKEN)