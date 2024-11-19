import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from myserver import server_on
import os

bot = commands.Bot(command_prefix="\\", intents=discord.Intents.all(),help_command=None)

TOKEN = os.environ.get('token')


status = ['Just Find A AFK Member','Move AKF Member']
stop_loop = False
numberChannel1 = 0
numberChannel2 = 0
check = False

#--------- check ---------
@bot.event
async def on_ready():
    global text
    text = "Now online!!"
    print(text)
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(status[0])) #bot status when start
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s)')

    
@bot.command(aliases=['set'])  
async def _set(ctx, new_numberChannel1, new_numberChannel2):
    global numberChannel1, numberChannel2,check
    numberChannel1 = int(new_numberChannel1)
    numberChannel2 = int(new_numberChannel2)
    check  = True
    await ctx.send("Room set")
    print(f"room1 = {numberChannel1} room2 = {numberChannel2}")

@bot.command(aliases=['ready','start'])
async def _ready(ctx):
    await ctx.send("online")
#--------- end check ---------
    

#--------- help ---------
@bot.command(aliases=['help','helpme','hp'])
async def _help(ctx):
    emmbed = discord.Embed(   
        title='Help Me! - Bot Commands',
        description='**Commands with "\\\\" prefix :**\n\help\n\move @name Set number of times\n\stop\n\set channel1 channel2\n\\tah\n\n'
                    '**Slash Commands with "/" prefix :**\n/move\n/stop\n/help\n/tah',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    await ctx.channel.send(embed=emmbed)


@bot.tree.command(name='help', description='Need help')
async def helpCommand(ctx):
    emmbed = discord.Embed(
        title='Help Me! - Bot Commands',
        description='**Commands with "\\\\" prefix :**\n\help\n\move @name Set number of times\n\stop\n\set channel1 channel2\n\\tah\n\n'
                    '**Slash Commands with "/" prefix :**\n/move\n/stop\n/help\n/tah',
        color=0x88FFF,
        timestamp=discord.utils.utcnow()
    )
    await ctx.response.send_message(embed=emmbed)
#--------- end help ---------


#--------- move ---------
@bot.tree.command(name='move', description='Move Some Member')
async def moveCommand(ctx, member:discord.Member,number : int):
    global  numberChannel1, numberChannel2,stop_loop,channel1,channel2  
    original_channel = member.voice.channel
    if  check == True :
        channel1 = bot.get_channel(numberChannel1)
        channel2 = bot.get_channel(numberChannel2)  
        for i in range(int(number)) :    
            if stop_loop == True:
                await ctx.channel.send("stop")
                await member.move_to(original_channel)
                stop_loop = False  
                break
            await member.move_to(channel1)
            await asyncio.sleep(0.5)
            await member.move_to(channel2)
            await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
            print(i+1,end=" ")
    
        await member.move_to(original_channel)
        await bot.change_presence(activity=discord.Game(status[0]))
    elif check == False :
        numberChannel1 = int(1213543702820163664) 
        numberChannel2 = int(1213543871926243379) 
        channel1 = bot.get_channel(numberChannel1)
        channel2 = bot.get_channel(numberChannel2)
        for i in range(int(number)) :    
            if stop_loop == True:
                await ctx.channel.send("stop")
                await member.move_to(original_channel)
                stop_loop = False  
                break
            await member.move_to(channel1)
            await asyncio.sleep(0.5)
            await member.move_to(channel2)
            await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
            print(i+1,end=" ")
    
        await member.move_to(original_channel)
        await bot.change_presence(activity=discord.Game(status[0]))
    else :
        await ctx.channel.send("Please set(\set) a room for poking or /help")
    return 


@bot.command()
async def move(ctx, member:discord.Member,number) :
    global  numberChannel1, numberChannel2,stop_loop,channel1,channel2  
    original_channel = member.voice.channel
    if  check == True :
        channel1 = bot.get_channel(numberChannel1)
        channel2 = bot.get_channel(numberChannel2)  
        for i in range(int(number)) :    
            if stop_loop == True:
                await ctx.channel.send("stop")
                await member.move_to(original_channel)
                stop_loop = False  
                break
            await member.move_to(channel1)
            await asyncio.sleep(0.5)
            await member.move_to(channel2)
            await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
            print(i+1,end=" ")
    
        await member.move_to(original_channel)
        await bot.change_presence(activity=discord.Game(status[0]))
    elif check == False :
        numberChannel1 = int(1213543702820163664) 
        numberChannel2 = int(1213543871926243379) 
        channel1 = bot.get_channel(numberChannel1)
        channel2 = bot.get_channel(numberChannel2)
        for i in range(int(number)) :    
            if stop_loop == True:
                await ctx.channel.send("stop")
                await member.move_to(original_channel)
                stop_loop = False  
                break
            await member.move_to(channel1)
            await asyncio.sleep(0.5)
            await member.move_to(channel2)
            await bot.change_presence(activity=discord.Game(status[1])) #bot status when move some person
            print(i+1,end=" ")
    
        await member.move_to(original_channel)
        await bot.change_presence(activity=discord.Game(status[0]))
    else :
        await ctx.channel.send("Please set(\set) a room for poking or /help")
        
    return 
#--------- end move ---------


#--------- call tah ---------
@bot.command(aliases=['tah'])
async def callTah(ctx, member: discord.Member = None):
    tahId = 577053817674268673  # User ID as an integer
    tahMember = ctx.guild.get_member(tahId)  # Fetch the Member object
    tah = tahMember.name #discord name
    if tahMember is None:
        await ctx.send(f"{tah} is not in this server.")
        return
    
    if ctx.author.voice and ctx.author.voice.channel:
        targetChannel = ctx.author.voice.channel 
    else:
        await ctx.send("You must be in the voice room")
        return

    if tahMember.voice and tahMember.voice.channel == targetChannel:
        await ctx.send(f"{tah} is already in your room.")
        return

    if tahMember and tahMember.voice:
        await tahMember.move_to(targetChannel)
        await ctx.send(f"call {tah} to room {targetChannel.name}")
    else:
        await ctx.send(f"{tah if tahMember else {tah}} not in voice channel")

@bot.tree.command(name='tah', description='Call cheetah to your room')
async def callTah(ctx: discord.Interaction):
    tahId = 577053817674268673  # User ID as an integer
    tahMember = ctx.guild.get_member(tahId)  # Fetch the Member object

    if tahMember is None:
        await ctx.response.send_message("User with the specified ID is not in this server.")
        return

    tah = tahMember.name  # Discord name

    if ctx.user.voice and ctx.user.voice.channel:
        targetChannel = ctx.user.voice.channel
    else:
        await ctx.response.send_message("You must be in a voice channel to call someone.")
        return

    if tahMember.voice and tahMember.voice.channel == targetChannel:
        await ctx.response.send_message(f"{tah} is already in your room.")
        return

    if tahMember.voice:
        try:
            await tahMember.move_to(targetChannel)
            await ctx.response.send_message(f"Called {tah} to room {targetChannel.name}.")
        except Exception as e:
            await ctx.response.send_message(f"Failed to move {tah}: {str(e)}")
    else:
        await ctx.response.send_message(f"{tah} is not currently in a voice channel.")
#--------- end call tah ---------


#--------- stop ---------
@bot.command()
async def stop(ctx):
    global stop_loop
    stop_loop = True

@bot.tree.command(name='stop', description='Stop Move Some Member')
async def stop(ctx):
    global stop_loop
    stop_loop = True
#--------- end stop ---------


  
server_on()
bot.run(TOKEN)



