import discord
import random
import asyncio
from discord import app_commands

from lib.datasc import weaponlist
list = weaponlist() #weaponlistで取得した武器一覧を格納

from lib.env import get_env
envs = get_env()

TOKEN = envs['TOKEN']

#特定のテキストチャンネルやボイスチャンネルを指定する場合
#TEXT_CHANNEL_ID = envs['TEXT_CHANNEL_ID']
# TEAM_1_VOICE_CHANNEL_ID = envs['TEAM_1_VOICE_CHANNEL_ID']
# TEAM_2_VOICE_CHANNEL_ID = envs['TEAM_2_VOICE_CHANNEL_ID']

#discordのスラッシュコマンドで指定する場合
TEAM_1_VOICE_CHANNEL_ID = 0
TEAM_2_VOICE_CHANNEL_ID = 0

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('login')
    await tree.sync()

#スラッシュコマンド 参考：https://qiita.com/Kodai0417/items/3abff9575e132e2955ec
@tree.command(name="voice_channel1",description="ボイスチャンネル1を選択してください")
async def test_command(interaction: discord.Interaction,text:discord.VoiceChannel):
    voicechannel_id = int(text.id)
    global TEAM_1_VOICE_CHANNEL_ID
    TEAM_1_VOICE_CHANNEL_ID = voicechannel_id
    await interaction.response.send_message(f"ボイスチャンネル1を {text} に設定しました　次にボイスチャンネル2を登録してください",ephemeral=True)

@tree.command(name="voice_channel2",description="ボイスチャンネル2を選択してください")
async def test_command(interaction: discord.Interaction,text:discord.VoiceChannel):
    voicechannel_id = int(text.id)
    global TEAM_2_VOICE_CHANNEL_ID
    TEAM_2_VOICE_CHANNEL_ID = voicechannel_id
    await interaction.response.send_message(f"ボイスチャンネル2を {text} に設定しました",ephemeral=True)


@tree.command(name="help",description="操作説明コマンドです")
async def test_command(interaction: discord.Interaction):
    help_message = (
            "操作説明:\n"
            "!t: ボイスチャンネルごとにメンバー名と武器名をセットとして送信します。\n"
            "!hi: 2つのボイスチャンネルにいるメンバーの合計が二人以上の時、姫ヤグラの姫様の決定をランダムで行います。\n"
            "1から8までの数字のいずれか: 数字に応じてランダムに武器名を送信します。\n"
            #"!4 または !6 または !8: それぞれ2対2,3対3,4対4になっていることを仮定し、α,βチームごとに武器名を送信します。 \n"
    )
    await interaction.response.send_message(help_message,ephemeral=False)


@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    #team_channel_text = client.get_channel(TEXT_CHANNEL_ID)
    #voice_channel_1 = client.get_channel(TEAM_1_VOICE_CHANNEL_ID)
    #voice_channel_2 = client.get_channel(TEAM_2_VOICE_CHANNEL_ID)
    #team_channel_text = await client.fetch_channel(TEXT_CHANNEL_ID)
    team_channel_text = message.channel
    voice_channel_1 = await client.fetch_channel(TEAM_1_VOICE_CHANNEL_ID)
    voice_channel_2 = await client.fetch_channel(TEAM_2_VOICE_CHANNEL_ID)

    if message.content == '!t': 
        user_name = [member.name for member in voice_channel_1.members] 
        #user_ID = [member.id for member in message.voice_channel_1.members] #ボイチャ接続中のメンバーID
        
        user_name_2 = [member.name for member in voice_channel_2.members]

        t1 = []
        t2 = []

        for name in user_name:
            t1.append(name)
        await team_channel_text.send('------')
        await team_channel_text.send('αチーム')
        for i in range(len(t1)):
            j = random.randint(0,len(list)-1)
            
            await team_channel_text.send(f'{t1[i]} さんの武器は\n{list[j]} です。\n')
            #await team_channel_text.send(t1[i])
            #await team_channel_text.send(list[j])
        
        for name in user_name_2:
            t2.append(name)
        await team_channel_text.send('------')
        await team_channel_text.send('βチーム')
        for i in range(len(t2)):
            j = random.randint(0,len(list)-1)
            
            await team_channel_text.send(f'{t2[i]} さんの武器は\n{list[j]} です。\n')

#----------------------------------------------#

    #t3 = []
    #t4 = []
    t = []
    
    if message.content == '!hi': #姫ヤグラ用
    
        user_name = [member.name for member in voice_channel_1.members] 
        user_name_2 = [member.name for member in voice_channel_2.members]


        for name in user_name:
            t.append(name)
        for name in user_name_2:
            t.append(name)

        if len(t) >= 2:
            for k in range(len(t) // 2):
                for i in range(1,3):
                    j = random.randint(len(t)-1) #ランダムに選ぶ
                    await team_channel_text.send(f'{i}人目の姫さまは、{t[j]}さんです。\n')
                    t.pop(j)
                await team_channel_text.send('---next---')
                return 
                                
        else:
            await team_channel_text.send("終了 武器ランダムは!tを入力")

    if message.content == '!help':
        help_message = (
            "操作説明:\n"
            "!t: ボイスチャンネルごとにメンバー名と武器名をセットとして送信します。\n"
            "!hi: 2つのボイスチャンネルにいるメンバーの合計が二人以上の時、姫ヤグラの姫様の決定をランダムで行います。\n"
            "1から8までの数字のいずれか: 数字に応じてランダムに武器名を送信します。\n"
            #"!4 または !6 または !8: それぞれ2対2,3対3,4対4になっていることを仮定し、α,βチームごとに武器名を送信します。 \n"
        )
        await team_channel_text.send(help_message) 
            
    if message.content.startswith(('1', '2', '3', '4', '5', '6', '7', '8')):
        count = int(message.content)
        for i in range(1, count + 1):
            j = random.randint(0, len(list) - 1)
            await message.channel.send(f"{i}\n{list[j]}")

client.run(TOKEN)

#     if message.content == '!team':  #チーム分け
#         if message.author.guild_permissions.administrator:

#             user_name = [member.name for member in voice_channel_1.members]  #ボイスチャットに接続中のメンバーネームを得る
#             user_ID = [member.id for member in voice_channel_1.members] #ボイスチャットに接続中のメンバーのIDを得る

#             index = [0] * len(user_name)

#             if len(index) % 2 == 0:

#                 tmp1_name = [""] * int(len(user_name) / 2)
#                 tmp2_name = [""] * int(len(user_name) / 2)
#                 tmp1_id = [0] * int(len(user_name) / 2)
#                 tmp2_id = [0] * int(len(user_name) / 2)

#                 for i in range(len(user_name)):
#                     index[i] = i
#                 random.shuffle(index)

#                 n = int(len(index)/2) #indexの要素数/2

#                 index = random.sample(index,len(index))

#                 index_1 = index[:n]
#                 index_2 = index[n:]

#                 for i in range(len(index_1)):
#                     tmp1_name[i] = user_name[index_1[i]]
#                     tmp1_id[i] = user_ID[index_1[i]]

#                 for i in range(len(index_2)):
#                     tmp2_name[i] = user_name[index_2[i]]
#                     tmp2_id[i] = user_ID[index_2[i]]



# #----------------------------テキストチャンネルにメンバー出力-------------------------
#                 t1 = ""
#                 t2 = ""

#                 for name in tmp1_name:          #チーム分け(名前)
#                     t1 += name + '\n'

#                 for name in tmp2_name:
#                     t2 += name + '\n'

#                 team = "```\n"
#                 team += "====team1====\n"
#                 team += t1
#                 team += "\n"
#                 team += "====team2====\n"
#                 team += t2
#                 team += "\n"

#                 rnd = random.randint(0,1)

#                 team += "====CT:T=====\n"
#                 if rnd == 0:
#                     team += "CT:team1\nT:team2"
#                 else:
#                     team += "T:team1\nCT:team2"

#                 team += "\n```"
#                 await team_channel_text.send(team)

# #--------------------------------------------------------------



# #------------------------------移動させるメンバー---------------------------
#                 move_team1 = [0] * int(len(user_name)/2)
#                 move_team2 = [0] * int(len(user_name)/2)

#                 if len(user_name) % 2 != 0:                     #チーム分け配列(ID)
#                     move_team1 = [0] * int(len(user_name)/2)
#                     move_team2 = [0] * int(len(user_name)/2)

#                 for i in range(len(move_team1)):
#                     move_team1[i] = tmp1_id[i]

#                 for i in range(len(move_team2)):
#                     move_team2[i] = tmp2_id[i]            



#                 move_voice = client.get_channel(TEAM_1_VOICE_CHANNEL_ID)
#                 for tm1_member in move_team1:
#                     mv_tm1 = discord.Guild.get_member(message.guild,tm1_member)
#                     await mv_tm1.move_to(move_voice)
#                     await asyncio.sleep(0.1)


#                 move_voice = client.get_channel(TEAM_2_VOICE_CHANNEL_ID)
#                 for tm2_member in move_team2:
#                     mv_tm2 = discord.Guild.get_member(message.guild,tm2_member)
#                     await mv_tm2.move_to(move_voice)
#                     await asyncio.sleep(0.1)


#             else:
#                 await team_channel_text.send("奇数人なのでランダムに抽選し，１人移動させます．")
#                 move_voice = client.get_channel(TEAM_2_VOICE_CHANNEL_ID)
#                 rand_move = random.choice(user_ID)
#                 mv_tm2 = discord.Guild.get_member(message.guild,rand_move)
#                 await mv_tm2.move_to(move_voice)
#                 await team_channel_text.send("もう一度「!team」を入力してください")
#         else:
#             await team_channel_text.send("あなたは管理者ではありません．")

#---------------------------------------------------------------------
        
    # if message.content.startswith('1'):
    #     for i in range(1):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(1)
    #         await message.channel.send(list[j])
        
    # if message.content.startswith('2'):
    #     for i in range(1,3):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])
    
    # if message.content.startswith('3'):
    #     for i in range(1,4):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])
    
    # if message.content.startswith('4'):
    #     for i in range(1,5):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])
    
    # if message.content.startswith('5'):
    #     for i in range(1,6):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])

    # if message.content.startswith('6'):
    #     for i in range(1,7):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])

    # if message.content.startswith('7'):
    #     for i in range(1,8):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])

    # if message.content.startswith('8'):
    #     for i in range(1,9):
    #         j = random.randint(0,len(list)-1)
    #         await message.channel.send(i)
    #         await message.channel.send(list[j])

#    if message.content.startswith('6'):
#         await message.channel.send('αチーム')
#         for i in range(1,4):
#             j = random.randint(0,len(list)-1)
#             await message.channel.send(i)
#             await message.channel.send(list[j])
#         await message.channel.send('-------')
#         await message.channel.send('βチーム')
#         for i in range(1,4):
#             j = random.randint(0,len(list)-1)
#             await message.channel.send(i)
#             await message.channel.send(list[j])

#     if message.content.startswith('8'):
#         await message.channel.send('αチーム')
#         for i in range(1,5):
#             j = random.randint(0,len(list)-1)
#             await message.channel.send(i)
#             await message.channel.send(list[j])
#         await message.channel.send('-------')
#         await message.channel.send('βチーム')
#         for i in range(1,5):
#             j = random.randint(0,len(list)-1)
#             await message.channel.send(i)
#             await message.channel.send(list[j])
# #@client.event   
# #async def Imessage(message):
#  content = message.content
#     if content.startswith(('1','2','3','4','5','6','7','8')):#全部一気に出力
#         num = int(content)
#         process(message,num)
#     if content.startswith('!4'): #チームごと
#         await process_teams(message,2)
#         await process_teams(message,2)
#     if content.startswith('!6'):
#         await process_teams(message, 3)
#         await process_teams(message, 3)
#     if content.startswith('!8'):
#         await process_teams(message, 4)
#         await process_teams(message, 4)

# async def process_teams(message, count):
#     team_names = ['αチーム', 'βチーム']
#     for team in team_names:
#         await message.channel.send(team)
#         for i in range(1, count + 1):
#             j = random.randint(0, len(list) - 1)
#             await message.channel.send(i)
#             await message.channel.send(list[j])
#         await message.channel.send('-------')

# async def process(message,count):
#     for i in range(1, count + 1):
#         j = random.randint(0, len(list) - 1)
#         await message.channel.send(i)
#         await message.channel.send(list[j])


                