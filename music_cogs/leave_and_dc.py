import discord
from discord.ext import commands

class DisconnectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("DISCONNECT COG is loaded")
    
    @commands.command(pass_context=True, aliases=["disconnect"])
    async def dc(self,ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            return await ctx.send('You need to be in a voice channel to use this command')

        voice = ctx.voice_client
        if voice: # If the bot is in a vc
            if ctx.message.author.voice.channel.id == voice.channel.id:
                await voice.disconnect()
                await ctx.send('Bot left voice channel')
            else:
                await ctx.send("You are not in the same voice channel as the bot")
        else:
            await ctx.send("I'm not in the voice channel to disconnect")

    @commands.command(pass_context=True)
    #@commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        voice = ctx.voice_client
        if voice: # If the bot is in a voice channel
            await voice.disconnect()
            await ctx.send('Bot left cuz a mod/admin wanted it to leave')
        else:
            await ctx.send("I'm not in a voice channel, use the join command to make me join")

def setup(bot):
    bot.add_cog(DisconnectCog(bot))