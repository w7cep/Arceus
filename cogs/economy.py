# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHOENIX - P.Sai Keerthan Reddy

# These are basic codes/commands used for Economy Bot !!!
# make sure to read the instructions in README.md file !!!


import nextcord
from nextcord.ext import commands
import asyncio
from pymongo import MongoClient
import random
auth_url = "mongodb+srv://W7CEP:Hudsongene0106@cluster2.5tx6k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

main_shop = [
    {"name":"Watch","price":100,"description":"Time"},
    {"name":"Laptop","price":1000,"description":"Work"},
    {"name":"PC","price":10000,"description":"Gaming"},
    {"name":"Ferrari","price":99999,"description":"Sports Car"}
]



async def open_bank(user):
    cluster = MongoClient(auth_url)
    db = cluster["Arceus"]

    cursor = db["Arceus_economy"]

    try:
        post = {"_id": user.id, "wallet": 0, "bank": 5000} # You can add as many columns as you can in this list !!!

        cursor.insert_one(post)

    except:
        pass


async def get_bank_data(user):
    cluster = MongoClient(auth_url)
    db = cluster["Arceus"]

    cursor = db["Arceus_economy"]

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
    db = cluster["Arceus"]

    cursor = db["Arceus_economy"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

class Economy(commands.Cog, name="Economy"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def slots(self, ctx, amount = None):
        await open_bank(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        users = await get_bank_data(ctx.author)

        wallet_amt = users[0]

        amount = int(amount)
        amt = 2*amount

        if amount > wallet_amt:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        final = []
        for i in range(3):
            a = random.choice(['X','O','Q'])

            final.append(a)

        await ctx.send(str(final))

        if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
            await update_bank(ctx.author,amt)
            await ctx.send(f'You won : {amt}) | {ctx.author.mention}')
        else:
            await update_bank(ctx.author,-1*amount)
            await ctx.send(f'You lose : {amt} | {ctx.author.mention}')


    @commands.command(aliases=['rb'])
    async def rob(self, ctx, member : nextcord.Member):
        await open_bank(ctx.author)
        await open_bank(member)

        users = await get_bank_data(member)

        wallet_amt = users[0]

        if wallet_amt < 100:
            await ctx.send('It is useless to rob him :(')
            return

        earning = random.randrange(0,wallet_amt)

        await update_bank(ctx.author,+1*earning)
        await update_bank(member,-1*earning, 'bank')
        await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')

    @commands.command(aliases=['sm'])
    async def send(self, ctx, member : nextcord.Member, amount = None):
        await open_bank(ctx.author)
        await open_bank(member)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        user = ctx.author
        users = await get_bank_data(user)

        bank_amt = users[1]

        bal = await update_bank(ctx.author)
        if amount == 'all':
            amount = bank_amt

        amount = int(amount)

        if amount > bank_amt:
            await ctx.send(f"{user.mention} You don't have that enough money!")
            return
        if amount < 0:
            await ctx.send(f"{user.mention} enter a valid amount !")
            return

        await update_bank(ctx.author,-1*amount,'bank')
        await update_bank(member,amount,'bank')
        await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')

    @commands.command()
    async def beg(self, ctx):
        await open_bank(ctx.author)
        user = ctx.author

        users = await get_bank_data(user)

        earnings = random.randrange(101)

        await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

        await update_bank(user, +1 * earnings)


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

    """@commands.command()
    async def shop(self, ctx):
        em = nextcord.Embed(title = "Shop")

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")

        await ctx.send(embed = em)

    @commands.command()
    async def buy(self, ctx, item,amount = 1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return

        await ctx.send(f"You just bought {amount} {item}")

    @commands.command()
    async def bag(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = nextcord.Embed(title = "Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name = name, value = amount)

        await ctx.send(embed = em)

    async def buy_this(user, item_name,amount):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await get_bank_data()

        bal = await update_bank(user)

        if bal[0]<cost:
            return [False,2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1
            if t == None:
                obj = {"item":item_name , "amount" : amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"] = [obj]

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await update_bank(user,cost*-1,"wallet")

        return [True,"Worked"]

    @commands.command()
    async def sell(self, ctx, item, amount = 1):
        await open_account(ctx.author)

        res = await sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold {amount} {item}.")

    async def sell_this(self, user, item_name, amount,price = None):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price==None:
                    price = 0.7* item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await get_bank_data()

        bal = await update_bank(user)

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False,2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1
            if t == None:
                return [False,3]
        except:
            return [False,3]

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await update_bank(user,cost,"wallet")

        return [True,"Worked"]"""

def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))

