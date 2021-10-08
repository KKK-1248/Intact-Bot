import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("UTILITIES COG is loaded")

    @commands.command()
    async def serverinfo(self, ctx):
        desc = ctx.guild.description
        if desc:
            embed = discord.Embed(title=ctx.guild.name + " Server Information",description=desc,color=discord.Color.green())
        else:
            embed = discord.Embed(title=ctx.guild.name + " Server Information",color=discord.Color.green())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Server Name", value=ctx.guild.name)
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Server ID", value=ctx.guild.id)
        embed.add_field(name="Region", value=ctx.guild.region)

        totc = ctx.guild.member_count
        botc = len([bot_user for bot_user in ctx.guild.members if bot_user.bot])
        memc = totc-botc
        embed.add_field(name="Member Count", value=f"Total Members: {totc}\nHumans: {memc}\nBots: {botc}")
        
        embed.add_field(name="Server Boosts", value=f"Level: {ctx.guild.premium_tier}\nBoosts: {ctx.guild.premium_subscription_count}\nBoosters: {len(ctx.guild.premium_subscribers)}")
        embed.add_field(name="Roles:", value=len(ctx.guild.roles))
        channel = len(ctx.guild.channels)
        vc = len(ctx.guild.voice_channels)
        cat = len(ctx.guild.categories)
        banner = ctx.guild.banner_url
        icon = ctx.guild.icon_url
        info = f"Verification Level: {ctx.guild.verification_level}"
        if banner:
            info += f"\n[Banner]({banner})"
        if icon:
            info += f"\n[Icon]({icon})"
        embed.add_field(name="Channels:", value=f"Categories: {cat}\nText: {channel}\nVoice: {vc}")
        embed.add_field(name="Other Infos:", value=info)
        await ctx.send(embed=embed)

    @commands.command(aliases=["avatar"])
    async def av(self, ctx, *, avamember : discord.Member=None):
        embed77 = discord.Embed(title="The user's pfp is:", color=discord.Color.green())
        if avamember == None:
            avt=ctx.author.avatar_url
            embed77.set_image(url=avt)
        else:
            avt = avamember.avatar_url
            embed77.set_image(url=avt)
        await ctx.send(embed=embed77)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"I have a latency of **{round(self.bot.latency * 1000, 1)}** ms")
  
def setup(bot):
    bot.add_cog(Utilities(bot))