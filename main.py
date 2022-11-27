# https://realpython.com/how-to-make-a-discord-bot-python/  based by
#Import necessary library
# https://stackoverflow.com/questions/70714205/discord-py-how-to-wait-for-user-input-that-can-be-different
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional
import re
import numpy
import genshin as gi
import asyncio
import pandas as pd

#https://genshin.hoyoverse.com/en/gift?code=NS8BD6EPS77Z

#Init
load_dotenv()   #Load neccessary env
TOKEN = os.getenv('DISCORD_TOKEN')  #Load token into variable
intents = discord.Intents.all() #Set intents
bot = commands.Bot(command_prefix='>>',intents=intents, case_insensitive=True) #Bot init
df_chat =  pd.DataFrame(columns=['discord_user_id','discord_username','uid'])   #Creating dataframe, it's wiser to make dataframe than expost it into hard csv
isLoggedIn = False  #Flag for checking if user already logged in
cookies = ''
ltuid = ''
lttoken = ''
client = gi.Client(game=gi.Game.GENSHIN)

@bot.event
async def on_connect():
    print(f'{bot.user.name} has connected to Discord!') #just for debugging

@bot.event
async def on_ready():
    global df_chat  #make dataframe become global so it can be access by other function
    print(f'{bot.user.name} is starting to scrape message from UID channel')    #for just debugging
    ch =  bot.get_channel(821006600424652840)   #Channel id of UID Channel
    async for msg in ch.history(limit=75,oldest_first=True):    #Get all message from UID Channel
        df_chat = df_chat.append({  # it's append data into dataframe
            'discord_user_id':msg.author.id,    #Insert user discord ID into discord_user_id column
            'discord_username':msg.author.name, #Insert user discord username into discord_user_name column
            'uid': msg.content, #Insert user message into uid column
        }, ignore_index=True)
    
    df_chat['uid'].replace(to_replace=r'\D+', value='', regex=True, inplace=True)   #Sanitize all UID
    #print(df_chat.head(70))    #Just for debug

    #This brute force sanitize, my brain can't create sophisticated regex, awk, or grep equivalent gibberish.
    #Since I pulled DC data as it and ordered it from oldest to new (from top to bottom)
    df_chat.loc[2,'uid'] = '817082429'
    df_chat.loc[20,'uid'] = '807802802'
    df_chat.loc[23,'uid'] = '813693892'
    df_chat.loc[24,'uid'] = '833076864'
    df_chat.loc[2.5] = '629284960112476160', 'lacie', '813746049'
    df_chat.loc[23.5] = '516850719609978883', 'Lost', '817011863'
    df_chat.drop([6],axis=0,inplace=True)
    df_chat = df_chat.sort_index().reset_index(drop=True)
    df_chat.insert(3, "primary_account", True)
    df_chat.loc[2,'primary_account'] = False
    df_chat.loc[20,'primary_account'] = False
    print(f'{bot.user.name} success fully scrape message from UID Channel') #Just for debugging
    print(df_chat.tail(5)) #Just for debugging

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):  #Handling Error missing argument
        await ctx.send("Missing Argument ! <:jean_question:833542806001025056>")    #Post into Text Channel if something go wrong
    elif isinstance(error, discord.ext.commands.errors.BadArgument):    #Handling Bad Argument
        await ctx.send("Bad Argument ! <:PaimonAngry:833542865690558515>")  #Post into Text Channel if something go wrong
    elif isinstance(error, asyncio.TimeoutError):   #Handling asyncio timeout error
        await ctx.send("Request Timeout ! <:hutao_cry:833542698455007232>") #POst into Text Channel if something go wrong

@bot.command(name='list', brief="Usage: >>list_uid 'user[Optional]'", usage='It will list all UID and discord username respectically. If discord username are given it will display that user UID')
async def list_uid(ctx,user:Optional[str]=None):
    print(f'{bot.user.name} getting input from discord client') #Just for debugging
    if(user is None):   #Check if username is not given
        uid_data = df_chat[df_chat.columns[1:4]]    #get all column except discord user ID
    else:
        if(user is not None):   #Check if username is given
            uid_data = df_chat[df_chat['discord_username'] == user] #Check if username given are in dataframe
            if(uid_data.empty): #Check if return of dataframe are empty raise an error
                raise discord.ext.commands.errors.BadArgument
    await ctx.send(f'```\n{uid_data}```')

# @bot.command(name='redeem', brief="Usage: >>redeem 'redeem_code*' 'uid[Optional]' 'second_acc[Optional]' 'server_region[Optional]'", usage="It will make a link for redeeming genshin impact code. If server region is ommited it will assume asia server, and if second_acc is not given it will set to primary")
# async def redeem(ctx,redeem_code,uid:Optional[str] = None, second_acc:Optional[bool] = False,srv_reg: Optional[str] = None):
#     print(f'{bot.user.name} getting input from discord client') #Just for debugging
#     redeem_code = redeem_code.upper()   #This will make redeem code become capitalized
#     res_wrn=''
#     if(uid is not None):    #check if "UID" are given
#         if(len(uid) != 9 and (not uid.isnumeric())):
#             raise discord.ext.commands.errors.BadArgument   #raising error if UID is not numeric and less or more than 9 digits
#         else:
#             uid=uid #store UID to UID, this is dumb move but more logical
#     if(uid is None):  #check if "UID" are not given
#         auth = ctx.author.id    #get the message author
#         if(second_acc is False):    #Check if second account flag are False
#             prime_acc=True
#         else:
#             prime_acc=False
#         uid = df_chat.query('discord_user_id == @auth and primary_account == @prime_acc')['uid'].to_string(index=False) #querying UID from dataframe

#     if(srv_reg is None):    #Check if server_region are given
#         srv_reg = 'asia'    #Handling if server_region are not given
#         res_wrn = f'Since no server region get specified, it will assume asia region'   #just ordinary warning string

#     res = res_wrn+f'\nhttps://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_{srv_reg}&lang=en&cdkey={redeem_code}&game_biz=hk4e_global'
#     #print (uid,redeem_code,srv_reg) #Just for debugging
#     await ctx.send(res) #send back response

@bot.command(name='redeem', brief="Usage: >>redeem 'redeem_code*'", usage="It will make a link for redeeming genshin impact gift code.")
async def redeem(ctx, redeem_code):
    print(f'{bot.user.name} getting input for redeem links')
    if(len(redeem_code) != 12):
        raise discord.ext.commands.errors.BadArgument
    else:
        redeem_code = redeem_code.upper()
        res = "https://genshin.hoyoverse.com/en/gift?code="+redeem_code
    
    print(res)
    await ctx.send(res)

@bot.command(name='stat', brief="Usage: >>stat",usage="It's will display stat of your genshin account")
async def stat(ctx):
    print(f'{bot.user.name} getting input from discord client') #Just for debugging
    global cookies, lttoken, ltuid  #Cache user credential here
    if (cookies == ''): #Check if user already logged in
        await ctx.send(f"Hey, {ctx.author.name} you need login before you can pull data from Hoyoverse, your message will get destroyed after you input you cookie token.\n**You can use spoiler (\||<lttoken> <ltuid>||) tag if you want**")   #Prompt
    
    def check(m):
        return (m.author.id == ctx.author.id)   #Check if author is same as who requested the command

    while True: #wait
        msg = await bot.wait_for("message",check=check,timeout=30) #wait for message given, and check if author is the same as requested. Timeout 30s
        auth = msg.author.id
        await msg.delete()  #Delete message for security
        prime_acc = True
        uid = df_chat.query('discord_user_id == @auth and primary_account == @prime_acc')['uid'].to_string(index=False)
        if(str(msg.content).startswith('||')):  #Check if start with || (spoiler tag)
            msg_split = re.sub(r'\|\|',' ',str(msg.content)).split() #Remove "||" and convert it into array
        else:
            msg_split = str(msg.content).split()    #convert it into array
        lttoken = msg_split[0]  #get first element from array
        ltuid = msg_split[1]   #get second element from array
        print(f'{lttoken} {ltuid} {uid}')
        client.set_cookies(f'ltuid={ltuid}; ltoken={lttoken}')
        user = await client.get_genshin_user(uid)
        # print("ok")
        print(user.stats.characters)
    embed = discord.Embed(title="Genshin User stats", description="All of your stat on Battle Chronicle", color=0x1abc9c)
    await ctx.send('In progress')

bot.run(TOKEN)  #Run the bot using existing token