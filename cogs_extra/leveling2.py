import math
import aiosqlite
import asyncio
import nextcord
from nextcord.ext import commands

# should be fixed


bot.multiplier = 1

async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")

class Leveling2(commands.Cog, name="Leveling2"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(message):
        if not message.author.bot:
            cursor = await bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

            if cursor.rowcount == 0:
                await bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                cur = await bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                data = await cur.fetchone()
                exp = data[0]
                lvl = math.sqrt(exp) / bot.multiplier
        
                if lvl.is_integer():
                    await message.channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")

            await bot.db.commit()

        await bot.process_commands(message)

    @commands.command()
    async def stats(ctx, member: nextcord.Member=None):
        if member is None: member = ctx.author

    # get user exp
        async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
            data = await cursor.fetchone()
            exp = data[0]

        # calculate rank
        async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            rank = 1
            async for value in cursor:
                if exp < value[0]:
                    rank += 1

        lvl = int(math.sqrt(exp)//bot.multiplier)

        current_lvl_exp = (bot.multiplier*(lvl))**2
        next_lvl_exp = (bot.multiplier*((lvl+1)))**2

        lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

        embed = nextcord.Embed(title=f"Stats for {member.name}", colour=nextcord.Colour.gold())
        embed.add_field(name="Level", value=str(lvl))
        embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
        embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
        embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

        await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(ctx): 
        buttons = {}
        for i in range(1, 6):
            buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10

        embed = nextcord.Embed(title=f"Leaderboard Page {current}", description="", colour=nextcord.Colour.gold())
        msg = await ctx.send(embed=embed)

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            if current != previous_page:
                embed.title = f"Leaderboard Page {current}"
                embed.description = ""

                async with bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                    index = entries_per_page*(current-1)

                    async for entry in cursor:
                        index += 1
                        member_id, exp = entry
                        member = ctx.guild.get_member(member_id)
                        embed.description += f"{index}) {member.mention} : {exp}\n"

                    await msg.edit(embed=embed)

            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            else:
                previous_page = current
                await msg.remove_reaction(reaction.emoji, ctx.author)
                current = buttons[reaction.emoji]

    commands.loop.create_task(initialize())

def setup(bot: commands.Bot):
    bot.add_cog(Leveling2(bot))
