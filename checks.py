import discord
from discord.ext import commands
import json

class NotInWhiteList(commands.CheckFailure):
    pass

def in_blacklist(blacklisted_members):
    async def inner_check(ctx):
        if ctx.author.id not in blacklisted_members:
            raise NotInWhiteList("You're blacklisted from using the bot!")
        
        return True
    return commands.check(inner_check)

class Checks(commands.Cogs):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def blacklist(self, message):
        with open("json/IDs.json", "r") as file:
            checkData = json.load(file)
        bannedIDs = checkData['blacklist']

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            if message.author.id in bannedIDs:
                await message.channel.send("You have been banned from using the bot")
            else:
                await self.bot.process_commands(message)
        else:
            pass

def setup(bot):
    bot.add_cog(Checks(bot))