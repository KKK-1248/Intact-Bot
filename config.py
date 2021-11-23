import discord
from discord.ext import commands, tasks
from motor import motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client_id = os.environ['mongo_client_id']
cluster = motor_asyncio.AsyncIOMotorClient(mongo_client_id)
config = cluster['discord']['guild-settings']
default_prefix = '.'

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("SETTINGS ARE LOADED")
    
    @tasks.loop(minutes=10)
    async def make_sure_stays_alive(self):
        channel = self.bot.get_channel(898470803195195392)
        await channel.send("BOT IS ALIVE")

    @commands.Cog.listener("on_message")
    async def start_life(self, message):
        msg = "<@869162661382868992> Bot Startup Initiated"
        if message.content == msg:
            await self.make_sure_stays_alive.start()

    #DEFAULT SETTINGS MANAGEMENT
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log_one = self.bot.get_channel(896029961528438806)
        guild_db = await config.find_one({'guild_id': guild.id})
        
        if guild_db is not None:
            await log_one.send(f"```OLD GUILD Detected\nGuild Name: {guild.name}\nGuild ID: {guild.id}```")
            return

        new_guild = {
            'guild_id': guild.id,
            'guild_name': guild.name,
            'prefix': default_prefix,
            'Ranking_System': True
        }
        await config.insert_one(new_guild)
        await log_one.send(f"```New Guild Detected\nGuild Name: {guild.name}\nGuild ID: {guild.id}\nMember Count: {guild.member_count}```")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log_one = self.bot.get_channel(896029961528438806)
        await config.delete_one({'guild_id': guild.id})
        await log_one.send(f"```Bot left guild\nGuild Name: {guild.name}```")


    #SET NEW PREFIXES
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix=None):
        if prefix is None:
            await ctx.send('Please enter the new prefix along with the command!')
            return

        guild = {'guild_id': ctx.guild.id}
        await config.update_one(guild, {"$set":{"prefix": prefix, "guild_name": str(ctx.guild.name)}})
        await ctx.send(f'Prefix changed to: {prefix}')

def setup(bot):
    bot.add_cog(Settings(bot))