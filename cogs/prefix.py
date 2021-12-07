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


class Prefix(commands.Cog, name="Prefix"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        description="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.has_role('Bot Manager')
    async def prefix(self, ctx, *, prefix="py."):
        await self.bot.pf.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(
            f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!"
        )

    @commands.command(
        name="deleteprefix", aliases=["dp"], description="Delete your guilds prefix!"
    )
    @commands.guild_only()
    @commands.has_role('Bot Manager')
    async def deleteprefix(self, ctx):
        await self.bot.pf.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")

def setup(bot: commands.Bot):
    bot.add_cog(Prefix(bot))
