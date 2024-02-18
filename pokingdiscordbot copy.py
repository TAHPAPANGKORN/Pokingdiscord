import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from myserver import server
import os

bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())

TOKEN = os.environ.get('token')

stop_loop = False

@bot.event
async def on_ready():
    print("Online!!")
    channel = bot.get_channel(682225304991039573)
    await channel.send("Now Online!!")
@bot.command()
async def on_ready(ctx):
    await ctx.send("online")

@bot.command()
async def move(ctx, member:discord.Member,number) :
    channel1 = bot.get_channel(927827825598267392)
    channel2 = bot.get_channel(927827898298167367)
    original_channel = member.voice.channel
    global stop_loop
    for i in range(int(number)) :
        if stop_loop:
            await ctx.send("stop")
            await member.move_to(original_channel)
            stop_loop = False  
            break
        await member.move_to(channel1)
        await asyncio.sleep(0.5)
        await member.move_to(channel2)
        print(i+1)
    await member.move_to(original_channel)
    
@bot.command()
async def stop(ctx):
    global stop_loop
    stop_loop = True

  
server_on():
bot.run(TOKEN)


# @bot.event
# async def on_member_join(member):
#     channel = bot.get_channel(1208761379146829907)
#     text = f"welcom to the sever {member.mention}!"
#     await channel.send(text)

# @bot.event
# async def on_member_remove(member):
#     channel = bot.get_channel(1208761379146829907)
#     text = f"see you again {member.mention}!"
    
#     await channel.send(text)
# @bot.event
# async def on_message(message):
#     mes = message.content
#     if mes == 'hi' :
#         await message.channel.send("hi i here tah")
#     await bot.process_commands(message)

# @bot.command()
# async def hi(ctx):
#     await ctx.channel.send("test1")
