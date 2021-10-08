import discord
import asyncio
from discord.ext import commands

snipe_message_author = {}
snipe_message_content = {}

class Server_related(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    #This is a event
    @commands.Cog.listener()
    async def on_ready(self):
        print("SERVER_RELATED COG is loaded")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        await asyncio.sleep(600)
        snipe_message_author.pop(message.channel.id, None)
        snipe_message_content.pop(message.channel.id, None)

    @commands.command(name = 'snipe')
    async def snipe(self, ctx):
        channel = ctx.channel
        try:
            em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
            em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
            await ctx.send(embed = em)
        except:
            await ctx.send(f"There are no recently deleted messages in #{channel.name}")

    @commands.command()
    async def membercount(self, ctx):
        bot_count = len([bot_user for bot_user in ctx.guild.members if bot_user.bot])
        await ctx.send(f"There are currently **{str(ctx.guild.member_count)}** humans and **{bot_count}** bots in this server")

    @commands.command(pass_context=True, aliases=["clear", "delete"])
    @commands.has_permissions(manage_permissions=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send(f'Cleared by {ctx.author.mention}')

def setup(bot):
    bot.add_cog(Server_related(bot))