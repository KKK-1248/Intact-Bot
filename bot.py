import discord
from discord.ext import commands, tasks
from motor import motor_asyncio
import os
from itertools import cycle
import logging
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
logging.basicConfig(level=logging.INFO)

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

    cluster.close()
    return prefix

intents=discord.Intents().all()
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    help_command=None
)

COGS = []
COGS.extend(['config', 'checks'])
for file in os.listdir("./cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        COGS.append(f"cogs.{file[:-3]}")
for file in os.listdir("./music_cogs/"):
    if file.endswith(".py") and not file.startswith("_"):
        COGS.append(f"music_cogs.{file[:-3]}")

presence = cycle([
    discord.Activity(type=discord.ActivityType.playing, name=f"on {len(bot.guilds)} servers"),
    discord.Activity(type=discord.ActivityType.listening, name= f".help"),
    discord.Activity(type=discord.ActivityType.listening, name="Chetan sing on stage(help me)")
])

#-----------------------START OF THE BOT-----------------------#
@bot.event
async def on_ready():
    change_pr.start()
    print("Bot is online")
    print(f"Logged in as {bot.user.name}")
    print("_______________")
    print(f"discord.py Version: v{discord.__version__}")
    print("_______________")

#ERROR HANDLER
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, discord.errors.NotFound):
        pass
    else:
        await ctx.send('{}'.format(str(error)))

@tasks.loop(seconds=20)
async def change_pr():
    await bot.change_presence(activity=next(presence))

@bot.command()
@commands.is_owner()
async def ch_pr(ctx, mode=None):
    if mode == '0':
        change_pr.stop()
        await bot.change_presence(activity=None)
        await ctx.send("Presence Stopped")
    
    elif mode == '1':
        await ctx.send("Presence Started")
        await change_pr.start()
    
    else:
        await ctx.send("Please Select a appropriate Mode and retry")
    

#RELOAD COMMANDS
@bot.command()
@commands.is_owner()
async def reload(ctx):
    try:
        unload_ext()
        load_ext()
    except Exception as error:
        await ctx.send(f"**Reload Extensions** Failed. Check console/log for errors")
        print(error)
        return
    
    await ctx.send("Reload Extensions command completed")

#LOAD THE COGS ON STARTUP
def load_ext():
    print("Loading all cogs...")
    [bot.load_extension(ext) for ext in COGS]
def unload_ext():
    print("Unloading all cogs...")
    [bot.unload_extension(ext) for ext in COGS]

load_ext()
cluster.close()
keep_alive()
bot.run(os.environ.get('TOKEN'))