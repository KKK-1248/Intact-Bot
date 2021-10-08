import discord
from discord.ext import commands
from replit import db
import os

ids = [877865875607285760, 884282015590002739, 845323793894866954]

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.command(aliases=["guild", "g"])
    @commands.is_owner()
    async def guilds(self, ctx, *, server: discord.Guild=None):
        # if int(ctx.guild.id) not in ids:
        #     print(f"\nGuilds command used in {ctx.guild.name}\nUsed by {ctx.message.author.name} - {ctx.message.author.id}")
        #     return

        guilem = discord.Embed(title="Guilds", color=discord.Color.random())
        guilds = self.bot.guilds
        if server==None:
            guilem.set_thumbnail(url=self.bot.user.avatar_url)
            for a in guilds:
                id = a.id
                mc = a.member_count
                guilem.add_field(name=a, value=f"Server ID: **{id}**\nServer Member Count: **{mc}**", inline=False)
        
        else:
            id = server.id
            mc = server.member_count
            guilem.set_thumbnail(url=server.icon_url)
            guilem.add_field(name=server, value=f"Server ID: **{id}**\nServer Member Count: **{mc}**", inline=False)

        await ctx.send(embed=guilem)
  
    @commands.command()
    @commands.is_owner()
    async def keys(self, ctx):
        keys = db.keys()
        await ctx.send(keys)
        print(os.getenv("REPLIT_DB_URL"))
    
    @commands.command()
    @commands.is_owner()
    async def delete_all_keys(self, ctx):
        #await ctx.send("Are you sure you want to clear all the keys in the database??? Respond with yes(y)/no(n)")
        db.clear()
        await ctx.send("ALL KEYS ARE DELETED")
        keys = db.keys()
        await ctx.send(keys)

def setup(bot):
    bot.add_cog(Owner(bot))