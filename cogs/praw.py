import discord
from discord.ext import commands, tasks
import asyncpraw
import random
import os
from dotenv import load_dotenv

load_dotenv()
reddit = asyncpraw.Reddit(
    client_id = os.environ['r_client_ID'],
    client_secret = os.environ['r_client_secret'],
    user_agent =  os.environ['r_user_agent']
)

class Praw_Real(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("PRAW REAL COG is loaded")

#START OF PRAW MEMES COMMAND
    @tasks.loop(hours= 1)
    async def get_submissions(self):
        global all_subs
        all_subs = []

        subreddit = await reddit.subreddit("memes")
        top = subreddit.hot(limit=200)
        subreddit2 = await reddit.subreddit("dankmemes")
        top2 = subreddit2.top(limit=100)

        async for submission in top:
            all_subs.append(submission)
        async for sub in top2:
            all_subs.append(sub)
            
        print("____________________")
        print("SUBMISSIONS UPDATED")

    @commands.command(aliases=["memes"])
    async def meme(self, ctx):
        global all_subs
        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        
        embed = discord.Embed(title=f'__{name}__', colour=discord.Colour.random(), url=url)

        embed.set_image(url=url)
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text='Here is your meme!')
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=["apraw", "praw"])
    @commands.is_owner()
    async def asyncpraw(self, ctx):
        global all_subs
        await ctx.send(f"There are currently **{len(all_subs)}** submissions in `global all_subs`")

def setup(bot):
    bot.add_cog(Praw_Real(bot))
    Praw_Real.get_submissions.start(bot)
    print("\nReloading submissions")