import discord
from discord.ext import commands

class IntermissionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("INTERMISSION COG is loaded")

    @commands.command()
    async def pause(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None: #If user is in not in a vc
            return await ctx.send('You need to be in a voice channel to use this command')

        voice = ctx.voice_client
        if voice is None: #If bot is not in a vc
            await ctx.send("The bot is not in a voice channel right now")
        elif voice.is_playing():
            if ctx.message.author.voice.channel.id == voice.channel.id:
                voice.pause()
                await ctx.send("The currently playing song has been paused. Use resume command to resume")
            else:
                await ctx.send('You are not in the same voice channel as the bot')
        else:
            await ctx.send("There is no song being played right now")
    
    @commands.command()
    async def resume(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None: #If user is in not in a vc
            return await ctx.send('You need to be in a voice channel to use this command')

        voice = ctx.voice_client
        if voice is None: #If bot is not in a vc
            await ctx.send("The bot is not in a voice channel right now")
        elif voice.is_paused():
            if ctx.message.author.voice.channel.id == voice.channel.id:
                voice.resume()
                await ctx.send("Resuming paused song")
            else:
                await ctx.send('You are not in the same voice channel as the bot')
        else:
            await ctx.send("There is no paused song right now")

    @commands.command()
    async def stop(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None: #If user is in not in a vc
            return await ctx.send('You need to be in a voice channel to use this command')

        voice = ctx.voice_client
        if voice is None: #If bot is not in a vc
            await ctx.send("The bot is not in a voice channel right now")
        elif voice.is_playing():
            if ctx.message.author.voice.channel.id == voice.channel.id:
                voice.stop()
                await ctx.send("The currently playing song has been stopped")
            else:
                await ctx.send('You are not in the same voice channel as the bot')
        else:
            await ctx.send("There is no song being played right now")

def setup(bot):
    bot.add_cog(IntermissionCog(bot))