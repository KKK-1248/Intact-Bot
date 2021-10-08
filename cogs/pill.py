import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

class Pillow_PIL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True
    
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
    bot.add_cog(Pillow_PIL(bot))