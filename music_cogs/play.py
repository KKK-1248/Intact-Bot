import discord
from discord.ext import commands

from discord import FFmpegOpusAudio
import youtube_dl
import urllib.parse, urllib.request, re

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    #'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }

class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("PLAYER COG is loaded")

    @commands.command()
    async def play(self, ctx, *, search=None):
        voice_state = ctx.author.voice
        if voice_state is None: #If user is in not in a vc
            return await ctx.send('You need to be in a voice channel to use this command')
        
        if search is None:
            await ctx.send("Please enter a song name or its youtube URL")
        else:
            await ctx.send("Searching youtube for the song ...")
            
            #-IF A LINK IS GIVEN-
            if search.startswith("http"):
                link_formats = [
                    "http://www.youtube.com/watch?v=",
                    "https://www.youtube.com/watch?v=",
                    "https://youtu.be/"
                ]
                url = None
                for a in link_formats:
                    if search.startswith(a):
                        url = search
                        break

                channel = ctx.message.author.voice.channel
                
                if ctx.voice_client is None: #If bot is not in a vc
                    voice = await channel.connect()
                else:
                    if channel.id == ctx.voice_client.channel.id:
                        voice = ctx.voice_client
                    else:
                        return await ctx.send("You are not in the same voice channel as the bot")

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    try:
                        info = ydl.extract_info(url, download=False)
                        url2 = info['formats'][0]['url']
                        source = await FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                    except:
                        await ctx.send("Invalid Youtube Link!")
                        return
                    voice.play(source)
            
            #-IF A SONG NAME IS GIVEN-
            else:
                #SEARCH YOUTUBE FOR AUDIO LINK
                query_string = urllib.parse.urlencode({'search_query': search})
                htm_content = urllib.request.urlopen(
                    'http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})',
                                            htm_content.read().decode())
                
                if search_results == []:
                    await ctx.send("No Such Song Found")
                    return

                song_result = 'http://www.youtube.com/watch?v=' + search_results[0]
                
                #PLAY THE LINK FOUND ABOVE
                channel = ctx.message.author.voice.channel
                url = song_result
                # url = "https://youtu.be/dQw4w9WgXcQ"
                
                if ctx.voice_client is None: #If bot is not in a vc
                    voice = await channel.connect()
                else:
                    if channel.id == ctx.voice_client.channel.id:
                        voice = ctx.voice_client
                    else:
                        return await ctx.send("You are not in the same voice channel as the bot")

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    source = await FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                    voice.play(source)

            musem=discord.Embed(title="Play Music", color=discord.Color.dark_green())
            musem.set_thumbnail(url=ctx.author.avatar_url)
            musem.add_field(name=f"Requested Song/Song URL: {search}", value=f"URL of the Song Found: {url}")
            musem.set_footer(text=f"Requested by @{ctx.author.name}")
            await ctx.send(embed=musem)

def setup(bot):
    bot.add_cog(PlayerCog(bot))