from discord.ext import commands
from replit import db

ids = [
    "877865875607285760",
    "884282015590002739",
    "845323793894866954",
    "869499359459442688" #The 3 musketeers
]

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["guild", "g"])
    @commands.is_owner()
    async def guilds(self, ctx):
        if str(ctx.guild.id) not in ids:
            return

        guilds = self.bot.guilds
        for a in guilds:
            await ctx.send(f"```{a.id} - {a}```")
  
    @commands.command()
    @commands.is_owner()
    async def keys(self, ctx):
        keys = db.keys()
        await ctx.send(keys)
    
    @commands.command()
    @commands.is_owner()
    async def delete_all_keys(self, ctx):
        db.clear()
        await ctx.reply("ALL REPLIT KEYS ARE DELETED")

def setup(bot):
    bot.add_cog(Owner(bot))