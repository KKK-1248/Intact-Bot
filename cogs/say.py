import discord
from discord.ext import commands
from better_profanity import profanity
import aiohttp
from io import BytesIO

class Wb_Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("WEBHOOK SAY COG is loaded")
    
    @commands.command()
    async def say(self, ctx, *, txt=None):
        if txt is None:
            return

        if profanity.contains_profanity(txt):
            await ctx.send("I can't use bad words!")
            return

        if "--c" in txt:
            txt = txt.split("--c")
            channel = self.bot.get_channel(int(txt[1]))
            txt = txt[0]
        else:
            channel = ctx.channel
            try:
                await ctx.message.delete()
            except discord.errors.NotFound:
                pass

        allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True)
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name = self.bot.user.name)
        
        if webhook is None:
            user_avatar_image = str(self.bot.user.avatar_url_as(format='png', size=512))
            async with aiohttp.ClientSession() as session:
                async with session.get(user_avatar_image) as resp:
                    avatar_bytes = BytesIO(await resp.read())
                webhook = await channel.create_webhook(name = self.bot.user.name, avatar=avatar_bytes.read())

        await webhook.send(
            txt,
            username = ctx.author.name,
            avatar_url = ctx.author.avatar_url,
            allowed_mentions=allowed_mentions
        )

def setup(bot):
    bot.add_cog(Wb_Say(bot))