import discord
from discord.ext import commands

class Intact_1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def truth(self, ctx):
        if ctx.message.author.id == 760482926663172138:#chetan id
            await ctx.send("You Suck!!!")
        else:
            await ctx.send("You dont suck")

    @commands.command()
    async def status(self, ctx):
        await ctx.send("Your status is **{}**".format(str(ctx.author.status)))

def setup(bot):
    bot.add_cog(Intact_1(bot))