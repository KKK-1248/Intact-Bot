import discord
from discord.ext import commands

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
        msg = "```"
        for a in guilds:
            msg+= str(f"\n{a.id} - {a}\n")
        msg += "```"
        await ctx.send(msg)
    
    @commands.command(aliases=["guildcount"])
    @commands.is_owner()
    async def guild_count(self, ctx):
        if str(ctx.guild.id) not in ids:
            return

        guilds = len(self.bot.guilds)
        await ctx.send(f"The Bot is currently is on **{guilds} servers**")
    
    @commands.command()
    @commands.is_owner()
    async def leave_guild(self, ctx, id:discord.Guild):
        guild = self.bot.get_guild(id)
        guild.leave()
    
    @commands.command()
    async def truth(self, ctx):
        if ctx.message.author.id == 760482926663172138:#chetan id
            await ctx.send("You Suck!!!")
        else:
            await ctx.send("You dont suck")
    
    @commands.command()
    async def uptime(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Owner(bot))