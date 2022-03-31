from discord.ext import commands

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
        bannedIDs = [
            # None yet. Just an empty list
        ]
        except_cmds = ["reload", "ch_pr"]

        commands = self.bot.walk_commands()
        for cmd in commands:
            if cmd.name not in except_cmds:
                @cmd.before_invoke
                async def ban_ids(self, ctx):
                    if ctx.author.id in bannedIDs:
                        raise NotInWhiteListError("You have been banned from using the bot")

def setup(bot):
    bot.add_cog(Checks(bot))