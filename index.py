import discord, datetime #discord, datetime 모듈 불러오기
import tasks
from discord.ext import tasks
from itertools import cycle
import random
import asyncio
import re
import os

token = "Nzk0NTcyMzM5MTA2NDE0NjQy.X-8xKA.3t7rHdhnvU8r68mpRrDmkAVEvGs" #봇 토큰 설정하기
client = discord.Client() #client 설정하기
intents = discord.Intents.all()
client = discord.Client(intents=intents)
async def on_ready(): #봇이 준비되었을때
    print("봇 준비 완료!")
    print(client.user)
    print("============================")
    user = len(client.users)
    server = len(client.guilds)
    message = ["1", "2", str(user) + "쓰는 사람들", str(server) + "쓰는 서버 수", "3"]
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(message[0]))
        message.append(message.pop(0))
        await asyncio.sleep(4)
@client.event
async def on_message(message): #사용자가 메세지를 입력했을때
    if message.content.startswith("!상메"):
            userid = message.content[4:]
            user = re.findall("\d+", userid)
            m = message.guild.get_member(int(user[0]))
            acts = m.activities
            act = [i for i in acts if isinstance(i, discord.CustomActivity)]
            if act:
                act = act[0]
            else:
                return await message.channel.send("상메가 없습니다")
            text = str(act.name)
            if text:
                await message.channel.send(f"상태메시지 : {text}")
            else:
                return await message.channel.send("상메가 없습니다")

    if message.content == "어이": #만일 사용자가 "야" 라고 입력했을때
        await message.channel.send("네?주인님?") #봇이 "왜" 라고 답한다.
    if message.content == "야": #만일 사용자가 "야" 라고 입력했을때
        await message.channel.send("네?") #봇이 "왜" 라고 답한다.
    if message.content == "선택":
        await message.channel.send(random.randint(1, 5000))    
    if message.content.startswith("정보"):
        status = str(message.author.status)
        if status == "online":
            status = "온라인🟢"
        elif status == "dnd":
            status = "방해금지⛔"
        elif status == "idle":
            status = "자리비움🟡"
        else:
                status = "오프라인⚪"
        if message.author.bot == False:
            bot = "유저"
        else:
            bot = "봇"
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(title=f'{message.author.name}의 정보')
        embed.add_field(name="이름", value=message.author.name, inline=False)
        embed.add_field(name="별명", value=message.author.display_name)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=False)
        embed.add_field(name="아이디", value=message.author.id)
        embed.add_field(name="상태", value=f"{status}", inline=False)
        embed.add_field(name="최상위 역할", value=message.author.top_role.mention, inline=False)
        embed.add_field(name="봇", value=bot)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    if message.content == "임배드 내놔":
        embed = discord.Embed(timestamp=message.created_at, colour=discord.Colour.red(), title="제-목", description="설-명")
        embed.set_thumbnail(url="https://prforest.ga/files/img/홍보숲.png")
        embed.set_image(url="https://ssl.pstatic.net/mimgnews/image/609/2020/12/01/202012010822031910_1_20201201082617583.jpg?type=w540")
        embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name="필트 제목", value="필드 설명", inline=False) #inline이 False라면 다음줄로 넘깁니다.
        await message.channel.send(embed=embed)
    if message.content == '받을 메시지': # 메시지를 받았을 때
        if message.author.dm_channel: # 만약 사용자와의 DM 채널이 있다면
            await message.author.dm_channel.send(f"{message.author.mention} , DM으로 보낼 메시지") # DM으로 메시지를 보낸다.
            await message.channel.send(f"{message.author.mention} , 메시지를 DM으로 전송했습니다. 확인해주세요 !") # 메시지를 입력한 채널에 그렇게 됨을 알린다.
        else: # 아니라면
            if message.author.dm_channel is None: # 사용자와의 DM 채널이 없다면
                channel = await message.author.create_dm() # DM 채널을 새로 만든다.
                await channel.send("DM으로 보낼 메시지") # DM으로 메시지를 보낸다.
                await message.channel.send(f"{message.author.mention} ,  DM 채널이 없어서 새로 만들고 DM을 보냈어요!") # 그렇게 됨을 알린다.
    if message.content.startswith("/투표"):
        vote = message.content[4:].split("/")
        await message.channel.send("투표 - " + vote[0])
        for i in range(1, len(vote)):
                choose = await message.channel.send("```" + vote[i] + "```")
                await choose.add_reaction('👍')
    if message.content.startswith("!청소"): # `!청소` 라는 메시지로 시작되었을 때
        if message.content == '!청소': # 메시지가 숫자 없이 `!청소` 만 있다면
            await message.channel.send(f"{message.author.mention} ,  \n그래서 몇 개를 치우라고요?\n올바른 명령어는 `!청소 (숫자)` 에요!") # 숫자를 넣어 달라고 말한다.
        else: # 아니라면 (숫자가 정상적으로 있다면)
             if message.author.guild_permissions.administrator: # 만약 명령어를 실행한 유저가 관리자 권한을 가지고 있다면
                 number = int(message.content.split(" ")[1]) # 입력한 숫자만큼 number 변수에 집어넣는다
                 await message.delete() # 그만큼 메시지를 지운다
                 await message.channel.purge(limit=number) # 대기한다
                 a = await message.channel.send(f"{message.author.mention} ,  \n{number}개의 메시지를 삭제했습니다.\n(이 메시지는 잠시 후에 삭제됩니다.)") # 메시지 삭제 성공을 알린다.
                 await asyncio.sleep(2) # 2초 동안 대기한다.
                 await a.delete() # 삭제했다는 메시지를 삭제한다.
             else: # 아니라면 (관리자 권한이 없다면)
                     await message.channel.send(f"{message.author.mention} ,  \n명령어를 수행할 관리자 권한을 소지하고 있지 않아요!\n서버 주인장에게 관리자 권한을 부탁해보는 건 어떨까요?") # 관리자 권한이 없다는 것을 알린다.
    if message.content == '내 정보':
        user = message.author
        date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
        await message.channel.send(f"{user} / {user.name} / {str(date.year)}/{str(date.month)}/{str(date.day)}")
    if(message.content.split(" ")[0] == "!뮤트"):
        if(message.author.guild_permissions.manage_channels):
            try:
                user = message.guild.get_member(int(message.content.split(' ')[1][3:21]))
                await message.guild.get_channel(message.channel.category_id).set_permissions(user, send_messages=False)
            except Exception as e:
                await message.channel.send(embed=discord.Embed(title="에러 발생", description = str(e), color = 0xff0000))
                return
        else:
            await message.channel.send(embed=discord.Embed(title="권한 부족", description = message.author.mention + "님은 채널을 관리 할 수 있는 권한이 없습니다.", color = 0xff0000))
            return

    if(message.content.split(" ")[0] == "!언뮤트"):
        if(message.author.guild_permissions.manage_channels):
            try:
                user = message.guild.get_member(int(message.content.split(' ')[1][3:21]))
                await message.guild.get_channel(message.channel.category_id).set_permissions(user, overwrite=None)
                await message.channel.send(embed=discord.Embed(title="언뮤트 성공!", color = 0x00ff00))
            except Exception as e:
                await message.channel.send(embed=discord.Embed(title="에러 발생", description = str(e), color = 0xff0000))
                return
        else:
            await message.channel.send(embed=discord.Embed(title="권한 부족", description = message.author.mention + "님은 채널을 관리 할 수 있는 권한이 없습니다.", color = 0xff0000))
client.run(token) #token으로 봇을 실행한다
