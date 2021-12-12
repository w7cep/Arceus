import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
import asyncio

bot_channel = 891852099653083186
talk_channels = [891852099653083186, 912538929713000478, 886404612335226891]

# you can have as many levels as you like
level = ["Youngster", "Challenger", "Ranger"] #you'll have to create roles (aka the levels) and put them here. So if my roles were Level 1, Level 2, and Level 3, then I'll use this
levelnum = [10,20,30]

cluster = MongoClient("mongodb+srv://W7CEP:Hudsongene0106@cluster2.5tx6k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

collection_name = cluster["leveling"]["levels"] #replace the database_name and the collection_name from MongoDB here.

#initiation
class Leveling(commands.Cog, name="Leveling"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Online!")

#gaining exp. It gains 1 exp but you can change it accordingly.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels: #to check if it's in the right channel
            stats = collection_name.find_one({"id":message.author.id}) #replace collection_name with your collection's name
            if not message.author.bot: #to check that it isn't levelling the bot up.
                if stats is None: #to check if they're registered
                    newuser = {"id" : message.author.id, "xp" : 0}
                    collection_name.insert_one(newuser) #replace collection_name with you collection's name; this is to insert the details into the database
                else: #means that they're registered
                    xp = stats["xp"] + 25 #increases xp by 1
                    collection_name.update_one({"id":message.author.id}, {"$set":{"xp":xp}}) #replace collection_name with your collection's name; is being ussed to update the databse
                    #to find what level the user's at
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Congrats! {message.author.mention}! You leveled up to **level: {lvl}**!") #sending an alert when the user levels up
                        #to check if they got a new role or not
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(nextcord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = nextcord.Embed(description=f"{message.author.mention}. New role: **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)
 
#to get rank
    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel: #to check if they're sending it in the right channel
            stats = collection_name.find_one({"id" : ctx.author.id}) #replace collection_name with your collection's name
            if stats is None: #checks if the user has send messages or not. If not then it send the message mentioned below
                embed = nextcord.Embed(description="You need to send messages to obtain a rank!")
                await ctx.channel.send(embed=embed)
            else: #if the user has send messages to the right channel(s)
                xp = stats["xp"]
                lvl = 0
                rank = 0
                totalxp = int(200*((1/2)*lvl))+xp
                while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20) #shows boxes (for visual effect)
                rankings = collection_name.find().sort("xp",-1) #replace collection_name with your collection's name
                for x in rankings: #to show what rank they are
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                #using this to send all the info
                embed = nextcord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name=f"Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.channel.send(embed=embed)
#Leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = collection_name.find().sort("xp",-1) #replace collection_name with your collection's name
            i = 1
            embed = nextcord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Leveling(bot))
