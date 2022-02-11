import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import aiohttp
import json
from motor import motor_asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

mongo_client_id = os.environ['mongo_client_id']
cluster = motor_asyncio.AsyncIOMotorClient(mongo_client_id)
config = cluster['discord']['guild-settings']

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_db(self):
        with open('json/RANKING_SYS.json', 'r') as f:
            return json.load(f)
    
    def save_db(self, new_data):
        with open('json/RANKING_SYS.json', 'w') as f:
            json.dump(new_data, f, indent=4)
        return
    
    def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            raise commands.NoPrivateMessage("You cant use this command in DMs")
        else:
            return True

    @commands.Cog.listener('on_message')
    async def levelling(self, message):
        if message.author.bot:
            return

        ban = ["lb", "levels", "ranks", "rankings", "ranking", "level", "lvl", "rank", "reload", "restart", "ban"]

        for x in ban:
            if x in message.content:
                return

        if isinstance(message.channel, discord.channel.DMChannel):
            return

        user = message.author
        guild = message.guild
        db = self.get_db()

        setting = await config.find_one({'guild_id': guild.id})
        
        if setting['Ranking_System'] is False:
            return

        try:
            base = db[str(guild.id)]
        except KeyError:
            db[guild.id] = {}
            self.save_db(db)
            print(f"New Guild Detected. Inserted guild {str(message.guild.name)} whose ID is '{message.guild.id}'")
            return

        try:
            stats = base[str(user.id)]
        except KeyError:
            db[str(guild.id)][user.id] = {
                'xp': 15,
                'level': 1,
                'name': str(user.name)
            }
            self.save_db(db)
            return

        #Get a EXP number to add for each msg
        xp_increase2 = random.randrange(5, 15)
        xp = stats["xp"] + xp_increase2

        db[str(guild.id)][str(user.id)]['xp'] = xp
        lvlb4up = stats["level"]

        #to find what level the user's at
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*lvl)):
                break
            lvl += 1

        if lvlb4up != lvl: #If user levels up
            db[str(guild.id)][str(user.id)]['level'] = lvl
            db[str(guild.id)][str(user.id)]['name'] = str(user.name)
            await message.channel.send(f"GG {message.author.mention}, you just levelled up to **level {lvl-1}**!")
            self.save_db(db)
            return
        
        self.save_db(db)
        cluster.close()


    @commands.command(aliases=["level", "lvl"])
    async def rank(self, ctx, user:discord.Member=None):

        if user is None:
            user = ctx.author

        # if user.id==ctx.bot.id:
        #     await ctx.send("Bots can't have ranks or levels")
        #     return

        db = self.get_db()
        
        try:
            stats = db[str(ctx.guild.id)][str(user.id)]
        except KeyError:
            await ctx.reply("The person doesn't have a rank yet in this server. Keep talking to get a rank")
            return

        lvl = stats['level']

        if lvl == 1:
            await ctx.reply("The person doesn't have a rank yet in this server. Keep talking to get a rank")
            return

        rank = 0
        xp = stats['xp']
        xp = xp - ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
        xp_cap = int(200 * ((1 / 2) * lvl))

        rankings = db[str(ctx.guild.id)]
        leaderboard_dict = {}
        total = []

        for x in list(rankings):
            experience_points = rankings[str(x)]['xp']
            user_id = int(x)
            leaderboard_dict[experience_points] = user_id
            total.append(experience_points)
        
        total = sorted(total,reverse=True)

        for amt in total:
            rank += 1
            id_ = leaderboard_dict[amt]
            if user.id == id_:
                break
        
        card = await self.get_rank_card(member=user, level=lvl-1, rank=rank, final_xp=xp_cap, xp=xp)

        await ctx.send(file=card)

    @commands.command(aliases=["lb", "levels", "ranks", "rankings", "ranking"])
    async def leaderboard(self, ctx):
        db = self.get_db()
        
        try:
            base = db[str(ctx.guild.id)]
        except:
            await ctx.reply("No one has a rank in this server yet. Start talking to create ranks")
            return

        leadem = discord.Embed(title="Leader Board:",
                            description="The top 10 ranked members in this server",
                            color=discord.Color.green())
        leaderboard = {}
        total=[]
        
        for user in list(base):
            user_id = int(user)
            total_amt = base[str(user)]['xp']
            leaderboard[total_amt] = user_id
            total.append(total_amt)
    
        total = sorted(total, reverse=True)

        index = 1
        x=10
        for amt in total:
            idOfUser = leaderboard[amt]
            member = self.bot.get_user(idOfUser)
            
            if member not in ctx.guild.members:
                continue

            lvl = base[str(member.id)]['level']
            if lvl != 1:
                leadem.add_field(name=f"Rank #{index} - **{member}**", value=f"Total XP: **{amt}**\nLevel: **{lvl-1}**", inline=False)
            
            if index == x:
                break
            else:
                index += 1

        leadem.set_footer(text=f"Requested by @{ctx.author.name}")
        await ctx.send(embed=leadem)
    

    # IMAGE CREATION STARTS HERE
    async def get_rank_card(self, member, level, rank, final_xp, xp):
        user_avatar_image = str(member.avatar_url_as(format='png', size=512))
        async with aiohttp.ClientSession() as session:
            async with session.get(user_avatar_image) as resp:
                avatar_bytes = BytesIO(await resp.read())

        img = Image.open('media/rank-card-template.jpg')
        logo = Image.open(avatar_bytes).resize((200, 200))

        big_size = (logo.size[0] * 3, logo.size[1] * 3)
        mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        mask = mask.resize(logo.size, Image.ANTIALIAS)
        logo.putalpha(mask)

        ##############################
        img.paste(logo, (20, 20), mask=logo)

        # Black Circle
        draw = ImageDraw.Draw(img, 'RGB')
        draw.ellipse((152, 152, 208, 208), fill='#000')

        # Placing offline or Online Status
        status = str(member.status)
        if status == 'online':
            draw.ellipse((155, 155, 205, 205), fill='#43B581')

        elif status == 'offline':
            draw.ellipse((155, 155, 205, 205), fill='#808080')
            draw.ellipse((165, 165, 195, 195), fill='#000000')

        elif status == 'dnd':
            draw.ellipse((155, 155, 205, 205), fill='#F04747')

        elif status == 'idle':
            draw.ellipse((155, 155, 205, 205), fill='#FAA719')

        # Working with fonts
        bar_color = '#8fce00'  # Green
        name_color = '#11ebf2'  # Light Blue

        big_font = ImageFont.FreeTypeFont('fonts/ABeeZee-Regular.otf', 60)
        medium_font = ImageFont.FreeTypeFont('fonts/ABeeZee-Regular.otf', 40)
        small_font = ImageFont.FreeTypeFont('fonts/ABeeZee-Regular.otf', 30)

        text_size = draw.textsize(f"{level}", font=big_font)
        offset_x = 1000 - 15 - text_size[0]
        offset_y = 5
        draw.text((offset_x, offset_y), f"{level}", font=big_font, fill=bar_color)
        text_size = draw.textsize('LEVEL', font=small_font)

        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "LEVEL", font=small_font, fill=bar_color)

        # Placing Rank Text (right upper part)
        text_size = draw.textsize(f"#{rank}", font=big_font)
        offset_x -= 15 + text_size[0]
        offset_y = 8
        draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff")

        text_size = draw.textsize("RANK", font=small_font)
        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "RANK", font=small_font, fill="#fff")

        # Placing Progress Bar
        # Background Bar
        bar_offset_x = logo.size[0] + 20 + 100
        bar_offset_y = 160
        bar_offset_x_1 = 1000 - 50
        bar_offset_y_1 = 200
        circle_size = bar_offset_y_1 - bar_offset_y

        # Progress bar rect greyer one
        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
        # Placing circle in progress bar

        # Left circle
        draw.ellipse((
                    bar_offset_x - circle_size // 2,
                    bar_offset_y,
                    bar_offset_x + circle_size // 2,
                    bar_offset_y + circle_size
                    ), fill="#727175")

        # Right Circle
        draw.ellipse((
                    bar_offset_x_1 - circle_size // 2,
                    bar_offset_y,
                    bar_offset_x_1 + circle_size // 2,
                    bar_offset_y_1
                    ), fill="#727175")

        # Filling Progress Bar

        bar_length = bar_offset_x_1 - bar_offset_x
        # Calculating of length
        # Bar Percentage (final_xp - current_xp)/final_xp

        # Some variables
        progress = (final_xp - xp) * 100 / final_xp
        progress = 100 - progress
        progress_bar_length = round(bar_length * progress / 100)
        bar_offset_x_1 = bar_offset_x + progress_bar_length

        # Drawing Rectangle
        # draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#11ebf2")
        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill=bar_color)
        # Left circle
        draw.ellipse(
            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y + circle_size),
            fill=bar_color)
        # Right Circle
        draw.ellipse((bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1),
                    fill=bar_color)

        def convert_int(integer):
            integer = round(integer / 1000, 2)
            return f'{integer}K'

        # Drawing Xp Text
        text = f"/ {convert_int(final_xp)} XP"
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x = bar_offset_x_1 - xp_text_size[0]
        xp_offset_x = 830
        xp_offset_y = bar_offset_y - xp_text_size[1] - 10
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#727175")

        text = f'{convert_int(xp)} '
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x -= xp_text_size[0]
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#fff")

        # Placing User Name
        text = member.name
        text_size = draw.textsize(text, font=medium_font)
        text_offset_x = bar_offset_x - 10
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=medium_font, fill=name_color)

        # Placing Discriminator
        text = f'#{member.discriminator}'
        text_offset_x += text_size[0] + 10
        text_size = draw.textsize(text, font=small_font)
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=small_font, fill="#727175")

        bg_img = Image.new('RGB', (1060, 300))
        bg_img.paste(img, (30, 30))

        with BytesIO() as image_binary:
            bg_img.save(image_binary, "PNG")
            image_binary.seek(0)
            card = discord.File(fp=image_binary, filename='rank_card.png')

        return card

def setup(bot):
    bot.add_cog(Ranking(bot))
    cluster.close()