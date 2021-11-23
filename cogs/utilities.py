import discord
from discord.ext import commands
import asyncio

snipe_message_author = {}
snipe_message_content = {}
es_before = {}
es_after = {}
es_author = {}

class Utilities(commands.Cog):
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
        print("UTILITIES COG is loaded")
    
    @commands.Cog.listener("on_message_delete")
    async def ghostPing(self, message):
        if message.author.id == self.bot.user.id:
            return

        if len(message.mentions) == 0:
            return
        else:
            ghostping = discord.Embed(title=f'GHOSTPING', timestamp=message.created_at)
            ghostping.add_field(name='**Sender of the Message:**', value=f'{message.author}', inline=False)
            ghostping.add_field(name='**Message:**', value=f'{message.content}', inline=False)
            # ghostping.set_thumbnail(
            #     url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXtzZMvleC8FG1ExS4PyhFUm9kS4BGVlsTYw&usqp=CAU')
            try:
                await message.channel.send(embed=ghostping)
            except discord.Forbidden:
                try:
                    await message.author.send(embed=ghostping)
                except discord.Forbidden:
                    return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        snipe_message_author[message.channel.id] = message.author.name
        snipe_message_content[message.channel.id] = message.content

        await asyncio.sleep(600)

        snipe_message_author.pop(message.channel.id, None)
        snipe_message_content.pop(message.channel.id, None)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        es_before[str(before.channel.id)] = before.content
        es_after[str(before.channel.id)] = after.content
        es_author[str(before.channel.id)] = before.author.name

        await asyncio.sleep(600)

        es_before.pop(before.channel.id, None)
        es_after.pop(before.channel.id, None)
        es_author.pop(before.channel.id, None)

    @commands.command()
    @commands.is_owner()
    async def snipe_check(self, ctx):
        msg = str(f'''```
Deleted Snipe :-
    snipe msgs = {snipe_message_content}
    snipe authors = {snipe_message_author}

Edit Snipe :-
    es_before = {es_before}
    es_after = {es_after}
    es_author = {es_author}```
        ''')
        await ctx.send(msg)
    
    @commands.command(name = 'snipe')
    async def snipe(self, ctx):
        try:
            em = discord.Embed(title = f"Last deleted message in #{ctx.channel.name}", description = snipe_message_content[ctx.channel.id])
            em.set_footer(text = f"This message was sent by {snipe_message_author[ctx.channel.id]}")
            await ctx.send(embed = em)
        except:
            await ctx.send(f"There are no recently deleted messages in #{ctx.channel.name}")
    
    @commands.command(aliases=['es', 'e_snipe'])
    async def edit_snipe(self, ctx):
        try:
            old_msg = es_before[str(ctx.channel.id)]
            new_msg = es_after[str(ctx.channel.id)]
            author = es_author[str(ctx.channel.id)]
            
            em = discord.Embed(title = f"Last edited message in #{ctx.channel.name}", description = f"**Old Message:** {old_msg}\n**New Message:** {new_msg}")
            em.set_footer(text = f"This message was sent by {author}")
            await ctx.send(embed = em)
        except:
            await ctx.send(f"There are no recently edited messages in #{ctx.channel.name}")

    @commands.command()
    async def serverinfo(self, ctx):
        desc = ctx.guild.description
        totc = ctx.guild.member_count
        botc = len([bot_user for bot_user in ctx.guild.members if bot_user.bot])
        memc = totc-botc
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

        if desc:
            embed = discord.Embed(title=ctx.guild.name + " Server Information",description=desc,color=discord.Color.green())
        else:
            embed = discord.Embed(title=ctx.guild.name + " Server Information",color=discord.Color.green())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Server Name", value=ctx.guild.name)
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Server ID", value=ctx.guild.id)
        embed.add_field(name="Member Count", value=f"Total Members: {totc}\nHumans: {memc}\nBots: {botc}")
        embed.add_field(name="Roles:", value=len(ctx.guild.roles))

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
    async def membercount(self, ctx):
        bot_count = len([bot_user for bot_user in ctx.guild.members if bot_user.bot])
        mem_count = int(ctx.guild.member_count)-bot_count
        await ctx.send(f"There are currently **{mem_count}** humans and **{bot_count}** bots in this server")

    @commands.command(pass_context=True, aliases=["clear", "delete"])
    @commands.has_permissions(manage_permissions=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send(f'Cleared by {ctx.author.mention}')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"I have a latency of **{round(self.bot.latency * 1000, 1)}** ms")

def setup(bot):
    bot.add_cog(Utilities(bot))