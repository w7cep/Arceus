import nextcord
from nextcord.ext import commands
import utils.json_loader as jl
from utils import checks
import inspect
import datetime
from collections import Counter
import asyncio
import os
import random
import traceback


class Blacklist(commands.Cog, name="Blacklist"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="blacklist", description="Blacklist a user from the bot", usage="<user>"
    )
    @commands.has_role('Bot Manager')
    async def blacklist(self, ctx, user: nextcord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        self.bot.blacklisted_users.append(user.id)
        data = jl.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        jl.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

    @commands.command(
        name="unblacklist",
        description="Unblacklist a user from the bot",
        usage="<user>",
    )
    @commands.has_role('Bot Manager')
    async def unblacklist(self, ctx, user: nextcord.Member):
        """
        Unblacklist someone from the bot
        """
        self.bot.blacklisted_users.remove(user.id)
        data = jl.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        jl.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

def setup(bot: commands.Bot):
    bot.add_cog(Blacklist(bot))
