import discord
import random
from discord.ext import commands

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
        if member==None:
            await ctx.send("Please mention the persion you want to kill")

        elif len(ctx.message.mentions) == 1:
            kill_list = self.killer(author=ctx.author.mention, mention=member.mention)

            if self.bot.user in ctx.message.mentions:
                await ctx.send("I dont wanna commit suicide")
            elif ctx.message.author in ctx.message.mentions:
                await ctx.send("OK, you are dead. Now ping someone else to kill")
            else:
                await ctx.send(random.choice(kill_list))
        
        else:
            await ctx.send("Whoa there! I am not omni-man or superman to kill more than one person at a time")

def setup(bot):
    bot.add_cog(Fun_Commands(bot))