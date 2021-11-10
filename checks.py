from discord.ext import commands
import json

class NotInWhiteListError(commands.CheckFailure):
    pass

def inBlacklist(blacklisted_members):
    async def inner_check(ctx):
        if ctx.author.id not in blacklisted_members:
            raise NotInWhiteListError("You're blacklisted from using the bot!")
        
        return True
    return commands.check(inner_check)

class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        with open("json/IDs.json", "r") as file:
            checkData = json.load(file)
        bannedIDs = checkData['blacklist']

        commands = self.bot.walk_commands()
        for cmd in commands:
            try:
                @cmd.before_invoke
                async def ban_ids(self, ctx):
                    if ctx.author.id in bannedIDs:
                        raise NotInWhiteListError("You have been banned from using the bot")
            
            except TypeError:
                @cmd.before_invoke
                async def ban_ids(ctx):
                    if ctx.author.id in bannedIDs:
                        raise NotInWhiteListError("You have been banned from using the bot")

def setup(bot):
    bot.add_cog(Checks(bot))