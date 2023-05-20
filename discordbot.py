import discord
from discord.ext import commands

from crawler.crystal import crystal
from crawler.userinfo import get_userinfo
from crawler.marishop import get_marishop_item
from crawler.banlist import get_banlist

from DISCORDTOKEN import TOKEN

from discord.ui import Select, View

import asyncio
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
 
@bot.event
async def on_ready():
    print("Ready to use DiscordBot!")
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # CommandNotFound 예외 처리 로직
        await ctx.send("모코코봇에서 사용 가능한 명령어를 확인하시려면 `/커맨드`를 입력해주세요!")
        # 또는 다른 동작 수행

@bot.command()
async def 커맨드(ctx):
    select = Select(
        placeholder="커맨드를 선택하세요", 
        options=[
            discord.SelectOption(
                label="!모험가",
                description="모험가의 전투정보를 조회합니다."
            ),
            discord.SelectOption(
                label="!마리샵",
                description="마리샵 [전투ㆍ생활 추천]탭을 확인합니다."
            ),
            discord.SelectOption(
                label="!크리값",
                description="현재 크리스탈-골드 시세를 확인합니다."
            )
        ])

    view = View()
    view.add_item(select)

    async def my_callback(interaction):
        selected_option = select.values[0]

        if selected_option == "!마리샵":
            await 마리샵(ctx)
        elif selected_option == "!크리값":
            await 크리값(ctx)
        elif selected_option == "!모험가":
            await ctx.send("조회하고 싶은 모험가의 닉네임을 입력해주세요.")

            view.stop()  # View를 종료

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                response = await bot.wait_for("message", check=check, timeout=60)  # 60초 동안 메시지 입력을 기다립니다.

                name = response.content
                await ctx.invoke(모험가, name=name)

            except asyncio.TimeoutError:
                await ctx.send("시간 초과로 입력이 취소되었습니다.")

    
    select.callback = my_callback
    await ctx.send("모코코봇에서 사용할 수 있는 커맨드입니다.", view=view)

@bot.command()
async def 모험가(ctx, *, name): #/모험가 정대만의무릎보호대
    try:
        userinfo = get_userinfo(name)

        embed=discord.Embed(title=name, description=userinfo['server'], color=0xca7cee)

        embed.set_author(name="모코코테스트")
        embed.set_thumbnail(url=userinfo['thumnail'])
        embed.add_field(name="원정대 레벨", value=f"`{userinfo['level-info__expedition']}`", inline=True)
        embed.add_field(name="전투 레벨", value=f"`{userinfo['level-info__item']}`", inline=True)
        embed.add_field(name="장착 아이템 레벨", value=f"`{userinfo['level-info2__expedition']}`", inline=True)
        embed.add_field(name="달성 아이템 레벨", value=f"`{userinfo['level-info2__item']}`", inline=True)
        embed.add_field(name="칭호", value=f"`{userinfo['game-info__title']}`", inline=True)
        embed.add_field(name="길드", value=f"`{userinfo['game-info__guild']}`", inline=True)
        embed.add_field(name="PVP", value=f"`{userinfo['level-info__pvp']}`", inline=True)
        embed.add_field(name="영지", value=f"`{userinfo['game-info__wisdom']}`", inline=True)
        
        formatted_engraves = [f"`{engrave}`" for engrave in userinfo['engraves']]
        value = '\n'.join(formatted_engraves)

        embed.add_field(name="각인효과", value = value, inline=True)
        embed.set_footer(text="Dev by 지상최고의개발자")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"닉네임이 {name}인 유저는 존재하지 않습니다.")

@bot.command()
async def 마리샵(ctx):
    items = get_marishop_item()
    
    embed=discord.Embed(title="마리샵", description="전영팩 떴냐??", color=0xca7cee)
    embed.set_author(name="모코코테스트")

    formatted_items = [f"`{item}`" for item in items]
    value = '\n'.join(formatted_items)

    embed.add_field(name="전투ㆍ생활 추천", value=value, inline=False)
    embed.set_footer(text="Dev by 지상최고의개발자")
    await ctx.send(embed=embed)

@bot.command()
async def 크리값(ctx):
    result = await crystal()

    embed=discord.Embed(title="크리스탈 가격 확인하기", url="https://loatool.taeu.kr/lospi", description="지금 크리스탈 얼마지?", color=0xca7cee)
    embed.set_author(name="모코코테스트")

    embed.add_field(name="현재시각", value=result['serverParseDt'], inline=False)

    embed.add_field(name="판매가", value=result['sell'], inline=True)
    embed.add_field(name="구매가", value=result['buy'], inline=True)

    embed.set_footer(text="Dev by devsosin")
    await ctx.send(embed=embed)

@bot.command()
async def 사사게(ctx, *, name):
    # 데이터가 너무 많으면 임베드 메시지에 안담김
    # 현재 제목이 담기지 않음
    ban_list = get_banlist(name)[:10]

    formatted_list = [f"[{discord.utils.escape_markdown(ban[1])}]({ban[2]})" for ban in ban_list]

    value = '\n'.join(formatted_list)

    embed=discord.Embed(title="사건사고 게시판", color=0xca7cee)
    embed.add_field(name="⛔️밴먹어", value=value, inline=False)
    
    embed.set_footer(text="Dev by 지상최고개발자")
    await ctx.send(embed=embed)
    return

bot.run(TOKEN())