import discord
from discord.ext import commands
import requests


class Intact_1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.command()
    async def truth(self, ctx):
        if ctx.message.author.id == 760482926663172138:#chetan id
            await ctx.send("You Suck!!!")
        else:
            await ctx.send("You dont suck")

    @commands.command()
    async def status(self, ctx):
        await ctx.send("Your status is **{}**".format(str(ctx.author.status)))

    @commands.command()
    async def anime(self, ctx, *, anime_character_name):
        try:
            reqcont = requests.get(f"https://www.animecharactersdatabase.com/api_series_characters.php?character_q={anime_character_name}")
            
            # No results
            if reqcont.content==-1 or reqcont.content=='-1':
                await ctx.send("No results found. Maybe there is a typo in what you typed?")
                return
            
            try:
                reqcont = reqcont.json()
            except Exception as e:
                # Please enable this line only while you are developing and not when deplying
                await ctx.send(reqcont.content)
                await ctx.send(f"Unable to turn the data to json format: {e}")
                return

            curent_info = reqcont["search_results"][0]

            # Creting the embed and sending it
            embed=discord.Embed(title="Anime Character Info", description=f"Anime Character '{anime_character_name.capitalize()}' Info'", color=0x00f549)
            embed.set_thumbnail(url=f"{curent_info['anime_image']}")
            embed.set_image(url=f"{curent_info['character_image']}")
            embed.add_field(name="Anime Name", value=f"{curent_info['anime_name']}", inline=False)
            embed.add_field(name="Name", value=f"{curent_info['name']}", inline=False)
            embed.add_field(name="Gender", value=f"{curent_info['gender']}", inline=False)
            embed.add_field(name="Description", value=f"{curent_info['desc']}", inline=False)
            embed.set_footer(text=f"Requested by @{ctx.author.name}")
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error has occured:\n```{e}```")

def setup(bot):
    bot.add_cog(Intact_1(bot))