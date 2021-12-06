# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHOENIX - P.Sai Keerthan Reddy

# These are basic codes/commands used for Economy Bot !!!
# make sure to read the instructions in README.md file !!!


import nextcord
from nextcord.ext import commands
import asyncio
from pymongo import MongoClient

auth_url = "mongodb+srv://W7CEP:Hudsongene0106@cluster2.5tx6k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

main_shop = [
            {"name":"Watch","price":100,"description": "Time"},
            {"name":"Laptop","price":1000,"description": "Work"},
            {"name":"PC","price":10000,"description": "Gaming"}
            ]



async def open_bank(user):
    cluster = MongoClient(auth_url)
    db = cluster["Arceus-economy"]

    cursor = db["economy"]

    try:
        post = {"_id": user.id, "wallet": 0, "bank": 5000} # You can add as many columns as you can in this list !!!

        cursor.insert_one(post)

    except:
        pass


async def get_bank_data(user):
    cluster = MongoClient(auth_url)
    db = cluster["Arceus-economy"]

    cursor = db["economy"]

    user_data = cursor.find({"_id": user.id})

    cols = ["wallet", "bank"] # You can add as many columns as you can in this list !!!

    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data


async def update_bank(user, amount=0, mode="wallet"):
    cluster = MongoClient(auth_url)
    db = cluster["Arceus-economy"]

    cursor = db["economy"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

class Economy(commands.Cog, name="Economy"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    @commands.guild_only()
    async def balance(self, ctx):
        user = ctx.author

        await open_bank(user)

        users = await get_bank_data(user)

        wallet_amt = users[0]
        bank_amt = users[1]

        net_amt = int(wallet_amt + bank_amt)

        em = nextcord.Embed(
                title= f"{user.name}'s Balance",
                description= f"Wallet: {wallet_amt}\nBank: {bank_amt}\nTotal: {net_amt}",
                color=nextcord.Color(0x00ff00)
            )

        await ctx.send(embed=em)


    @commands.command(name="withdraw", aliases=["with"])
    @commands.guild_only()
    async def withdraw(self, ctx, *,amount= None):
        user = ctx.author
        await open_bank(user)

        users = await get_bank_data(user)

        bank_amt = users[1]

        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, +1*bank_amt)
            await update_bank(user, -1*bank_amt, "bank")
            await ctx.send(f"{user.mention} you withdrew **{bank_amt}** from your **Bank!**")

        amount = int(amount)

        if amount > bank_amt:
            await ctx.send(f"{user.mention} You don't have that enough money!")
            return

        if amount < 0:
            await ctx.send(f"{user.mention} enter a valid amount !")
            return

        await update_bank(user, +1 * amount)
        await update_bank(user, -1 * amount, "bank")

        await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")


    @commands.command(name="deposit", aliases=["dep"])
    @commands.guild_only()
    async def deposit(self, ctx, *, amount= None):
        user = ctx.author
        await open_bank(user)

        users = await get_bank_data(user)

        wallet_amt = users[0]

        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, -1*wallet_amt)
            await update_bank(user, +1*wallet_amt, "bank")
            await ctx.send(f"{user.mention} you deposited {wallet_amt} into your bank")

        amount = int(amount)

        if amount > wallet_amt:
            await ctx.send(f"{user.mention} You don't have that enough money!")
            return

        if amount < 0:
            await ctx.send(f"{user.mention} enter a valid amount !")
            return

        await update_bank(user, -1 * amount)
        await update_bank(user, +1 * amount, "bank")

        await ctx.send(f"{user.mention} you deposited **{amount}** into your **Bank!**")


    @commands.command(name="shop")
    async def shop(self, ctx):
        em = nextcord.Embed(title = "Shop")

        for item in main_shop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")
        await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))

