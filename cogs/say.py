import discord
from discord.ext import commands
from better_profanity import profanity

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

        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

        if profanity.contains_profanity(txt):
            await ctx.send("You cannot use banned words!")
            return

        if "--" in txt:
            txt = txt.split("--")
            channel = self.client.get_channel(int(txt[1]))
            txt = txt[0]
        else:
            channel = ctx.channel

        send_auth = f"\n\n- **@{ctx.author.name}**"
        send = txt + send_auth
    
        allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False)
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name = self.bot.user.name)
        if webhook is None:
            with open("media/bot_avatar.jpg", "rb") as wbavatar:
                webhook = await channel.create_webhook(name = self.bot.user.name, avatar=wbavatar.read())

        await webhook.send(send,
                        username = self.bot.user.name,
                        avatar_url = self.bot.user.avatar_url,
                        allowed_mentions=allowed_mentions)

def setup(bot):
    bot.add_cog(Wb_Say(bot))