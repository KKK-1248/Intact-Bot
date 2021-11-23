import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import asyncio
import random

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("FUN_COMMANDS COG is loaded")

    def killer(self, author, mention):
        kill_list=[
                f"{mention} stubbed their toe so hard they died",#1
                f"{mention} died because of stupidity",#2
                f"{mention} died because of their stench",#3
                f"{mention} saw themself in a mirror and died due to their ugliness",#4
                f"{mention} died because they ate their own poop",#5
                f"{mention} was killed by the police for being a idiot",#6
                f"{mention} commited suicide because even Rick Astley gave them up",#7
                f"{mention} was killed by Mahatma Gandhi because they were annoying enough to make him forget the concept of non-violence",#8
                f"{mention} died because they realised that they were a ghost",#9
                f"{mention} thought they can fly and jumped from a 30 story building",#10
                f"{mention} wanted to build a ikea shelf, but they were so dumb they built a guillotine and hanged themselfs on it",#11
                f"{author} killed {mention} with a frying pan",#12
                f"{mention} died after smelling {author}'s fart"#13
                ]
        return kill_list

    @commands.command()
    async def kill(self, ctx, member:discord.Member=None):
        if member == None or member == ctx.author:
            await ctx.send("OK, you are dead. Now ping someone else to kill")
            return
        
        kill_list = self.killer(
            author=ctx.author.mention,
            mention=member.mention
        )

        if member == self.bot.user:
            await ctx.send("I dont wanna commit suicide")
        else:
            await ctx.send(random.choice(kill_list))
    
    @commands.command()
    async def spotify(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                
                embed = discord.Embed(
                    title = f"{member.name}'s Spotify Activity",
                    description = f"Listening to **{activity.title}**",
                    color = discord.Colour.random()
                )

                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist, inline=False)
                embed.add_field(name="Album", value=activity.album, inline=False)
                minutes, seconds = divmod(int(activity.duration.seconds), 60)
                song_duration = f'{minutes}:{seconds} minutes'
                embed.add_field(name="Duration of the Song", value=song_duration, inline=False)
                embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=embed)
                return
        
        await ctx.send("The member is not listening to spotify")
    
    @commands.command(aliases=["heck"])
    async def hack(self, ctx, user: discord.Member = None, *, virus: str = "trojan"):
        if user is None:
            await ctx.send("You need to mention someone to hack them you dummy!")
            return

        msg = f"``[▓                    ] / {virus}-virus.exe Packing files.``"
        heck = await ctx.send(msg)
        list = [
            f"``[▓▓▓                    ] / {virus}-virus.exe Packing files.``",
            f"``[▓▓▓▓▓▓▓                ] - {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {virus}-virus.exe Packing files..``",
            f"``Successfully downloaded {virus}-virus.exe``",
            "``Injecting virus.   |``",
            "``Injecting virus..  /``",
            "``Injecting virus... -``",
            f"``Successfully Injected {virus}-virus.exe into {user.name}``\n\nThe totally real and dangerous hack is complete *winks*",
            ]
        for i in list:
            await asyncio.sleep(1)
            await heck.edit(content=i)

    @commands.command()
    async def wanted(self, ctx, user: discord.Member=None):
        if user==None:
            user=ctx.author
        
        wanted = Image.open("media/wanted.jpg")
        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((177, 177))

        wanted.paste(pfp, ((120, 212)))
        with BytesIO() as image_binary:
            wanted.save(image_binary, "PNG")
            image_binary.seek(0)
            img = discord.File(fp=image_binary, filename='wanted.png')

        await ctx.send(file=img)

def setup(bot):
    bot.add_cog(Fun_Commands(bot))