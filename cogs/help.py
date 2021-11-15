import discord
from discord.ext import commands

class Help(commands.Cog, name="help_hide"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("HELP COG is loaded")

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        helpem= discord.Embed(color=discord.Color.purple())
        helpem.set_author(name="HELP")

        helpem.add_field(name='\u200b', value="**FUN**", inline=False)
        helpem.add_field(name="`kill`", value="Your personal hitman")
        helpem.add_field(name="`meme`", value="Sends a random meme")
        helpem.add_field(name="`wanted`", value="Makes the user/mentioned wanted")

        helpem.add_field(name='\u200b', value="**MODERATION**", inline=False)
        helpem.add_field(name="`purge`", value="Deletes the specified amount of messages")
        helpem.add_field(name="`setpreifx`", value="Set a custom prefix for this server. Administrator permission required")

        helpem.add_field(name='\u200b', value="**MISC**", inline=False)
        helpem.add_field(name="`snipe`", value="Shows the recently deleted message")
        helpem.add_field(name="`img/image/pic/picture`", value="Search google for images using this command")
        helpem.add_field(name="`yt`", value="Search youtube using this command")
        helpem.add_field(name="`wiki/wikipedia`", value="Search wikipedia using this command")
        helpem.add_field(name="`serverinfo`", value="Shows the server info")
        helpem.add_field(name="`membercount`", value="Member count of this server")
        helpem.add_field(name="`av`", value="Shows your/mentioned member's pfp")
        helpem.add_field(name="`say`", value="Says whatever you say")
        helpem.add_field(name="`t/trans/translate`", value="Translates whatever is given with the command to English")
        helpem.add_field(name="`ping`", value="Shows the bot's ping")

        helpem.add_field(name='\u200b', value="**MUSIC COMMANDS**", inline=False)
        helpem.add_field(name="`help music`", value="Shows commands for playing music")
        await ctx.send(embed=helpem)

    @help.command()
    async def music(self, ctx):
        musichelp = discord.Embed(color=discord.Color.purple())
        musichelp.set_author(name="MUSIC COMMANDS HELP")
        musichelp.add_field(name="`play`", value="Plays the requested song")
        musichelp.add_field(name="`stop`", value="Stops the currently playing song")
        musichelp.add_field(name="`pause`", value="Pauses the currently playing song")
        musichelp.add_field(name="`resume`", value="Resumes the paused song")
        musichelp.add_field(name="`dc/disconnect`", value="Disconnect the bot from the vc")
        musichelp.add_field(name="`leave`", value="Disconnect the bot from the vc without joining it(admins only)")

        musichelp.add_field(name='\u200b',value="**Please note that all commands except the leave command require the user to be in a voice channel**", inline=False)
        await ctx.send(embed=musichelp)
    
    @commands.command()
    @commands.is_owner()
    async def help_own(self, ctx):
        ownem= discord.Embed(color=discord.Color.blurple())
        ownem.set_author(name="Developer Help")

        ownem.add_field(name="`guild(s)/g`", value="Shows the servers the bot is in. Might not always work. A bit buggy/messy")
        ownem.add_field(name="`truth`", value="Roasts Cherry")

        ownem.add_field(name='\u200b', value="**DONT MESS WITH THESE ONES**", inline=False)
        ownem.add_field(name="`delete_all_keys`", value="DELETES ALL THE KEYS IN THE DATABASE")
        ownem.add_field(name="`reload`", value="Reloads all the cogs")
        ownem.add_field(name="`mureload`", value="Reloads all the music cogs")
        ownem.add_field(name="`load`", value="Loads new cogs")
        await ctx.send(embed=ownem)

    
def setup(bot):
    bot.add_cog(Help(bot))