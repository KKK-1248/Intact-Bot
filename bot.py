import discord
from discord.ext import commands
from motor import motor_asyncio
import os, sys, asyncio, random
import logging
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#GET THE PREFIX FROM MONGODB
mongo_client_id = os.environ['mongo_client_id']
cluster = motor_asyncio.AsyncIOMotorClient(mongo_client_id)
config = cluster['discord']['guild-settings']
default_prefix = '.'

async def get_prefix(bot, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return default_prefix

    guild = await config.find_one({'guild_id': message.guild.id})
    if guild is None:
        prefix = default_prefix
    else:
        prefix = guild['prefix']

    return prefix

#BOT INSTANCE
TOKEN = os.environ['TOKEN']
intents=discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
bot.remove_command('help')

#-----------------------START OF THE BOT-----------------------#
@bot.event
async def on_ready():
    print("Bot is online")
    print(f"Logged in as {bot.user.name}")
    print("_______________")
    print(f"discord.py Version: v{discord.__version__}")
    print("_______________")
    log = bot.get_channel(898470803195195392)
    await log.send("<@869162661382868992> Bot Startup Initiated")

#CHANGE THE STATUS
async def ch_pr():
    await bot.wait_until_ready()
    statuses_playing=[f"on {len(bot.guilds)} servers", "Visual Studio Code"]
    statuses_listening=["Immortals on Spotify", "Counting Stars on Spotify"]
    while not bot.is_closed():
        status1 = random.choice(statuses_playing)
        status2 = random.choice(statuses_listening)
        await bot.change_presence(activity=discord.Game(name=status1))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name= f".help"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status2))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name= f".help"))
        await asyncio.sleep(15)

async def monitor_chaos():
    await bot.wait_until_ready()
    while not bot.is_closed():
        log = await bot.fetch_channel(898470803195195392)
        await log.send("Bot is online as of now")
        await asyncio.sleep(600)

#ERROR HANDLER
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, discord.errors.NotFound):
        pass
    else:
        await ctx.send('{}'.format(str(error)))

#RELOAD COMMANDS
@bot.command()
@commands.is_owner()
async def reload(ctx):
    for file in os.listdir("./cogs/"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{file[:-3]}")
                bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                await ctx.send(f"Failed to reload the following cog:- *{file}*")
                print(e)
    
    for file in os.listdir("./intact_cogs/"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"intact_cogs.{file[:-3]}")
                bot.load_extension(f"intact_cogs.{file[:-3]}")
            except Exception as e:
                await ctx.send(f"Failed to reload the following cog:- *{file}*")
                print(e)

    await ctx.send("Cog Reload command completed")

@bot.command()
@commands.is_owner()
async def mureload(ctx):
    for file in os.listdir("./music_cogs/"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"music_cogs.{file[:-3]}")
                bot.load_extension(f"music_cogs.{file[:-3]}")
            except Exception as e:
                await ctx.send(f"Failed to reload the following cog:- *{file}*")
                print(e)
            
    await ctx.send("Cog Reload command completed")

#RESTART THE BOT
@bot.command()
@commands.is_owner()
async def restart(ctx):
    try:
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        await ctx.send("Unable to restart. An error occurred. Error:\n```py\n{}\n```".format(e))

#LOAD THE COGS ON STARTUP
bot.load_extension('config')
for file in os.listdir("./intact_cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"intact_cogs.{file[:-3]}")
for file in os.listdir("./cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")
for file in os.listdir("./music_cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"music_cogs.{file[:-3]}")

#LOOPS
bot.loop.create_task(ch_pr())
bot.loop.create_task(monitor_chaos())
#RUN
keep_alive()
bot.run(TOKEN)