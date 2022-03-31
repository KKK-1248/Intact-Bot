import discord
from discord.ext import commands
from googleapiclient.discovery import build
from googletrans import Translator, LANGUAGES
import wikipedia
from dotenv import load_dotenv
from better_profanity import profanity
import warnings, os, random

load_dotenv()
api_key = os.environ['google_project_API_Key']
engine_id = os.environ['cse_id']
translator = Translator(service_urls=['translate.googleapis.com'])

class Search_web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("SEARCH_WEB COG is loaded")
    
    #Translate command
    @commands.command(aliases=['t', 'translate'])
    async def trans(self, ctx, *, translate_need=None):
        if translate_need==None:
            await ctx.send("Please type what you want to translate along with the command")
            return

        words = translator.translate(translate_need)
        lang = LANGUAGES[words.src].upper()
        await ctx.send(f"{words.text.capitalize()}\nLanguage Detected: **{lang}**")

    #Image Search
    @commands.command(aliases=["pic", "picture", "img", "photo"])
    async def image(self, ctx, *, pic_search=None):
        if pic_search==None:
            await ctx.send("Please enter what image you want to search for")
            return
        
        if profanity.contains_profanity(pic_search):
            white_lister = pic_search.lower()
            white_list = ["hit", "kill", "suck"]
            if white_lister in white_list:
                pass
            else:
                await ctx.send("You cannot use banned words!")
                return

        try:
            randit = random.randint(0, 4)
            resource = build("customsearch", "v1", developerKey=api_key).cse()
            result = resource.list(q=f"{pic_search}", cx=engine_id, searchType="image").execute()
            url = result["items"][randit]["link"]

            picem = discord.Embed(title=f"**__{pic_search}__**", url=url, colour = discord.Color.orange())
            picem.set_author(name="Image Search")
            picem.set_image(url=url)
            picem.set_footer(text=f"Searched by @{ctx.author.name}",
                            icon_url=ctx.author.avatar_url)
            await ctx.send(embed=picem)
        except:
            await ctx.send("Image not found")

    #Youtube search
    @commands.command(aliases=["youtube"])
    async def yt(self, ctx, *, search=None):
        await ctx.send('**Note: This command is deprecated**')

    #Wikipedia search
    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, search_query=None):
        if search_query == None:
            return await ctx.send("Please search for something")
        
        warnings.catch_warnings()
        warnings.simplefilter("ignore")
        await ctx.send('Searching Wikipedia ...')
        wikiem = discord.Embed(color=discord.Color.green())
        
        try:
            results = wikipedia.summary(search_query, sentences=3, auto_suggest=False, redirect=True)
            wikiem.set_author(name="According to Wikipedia")
        except:
            wikiem.set_author(name="Cant find it on wikipedia")
            results = "No data found. Check for typos"

        wikiem.add_field(name=search_query, value=results)
        wikiem.set_footer(text=f"Requested by @{ctx.message.author.name}")
        await ctx.send(embed=wikiem)

def setup(bot):
    bot.add_cog(Search_web(bot))