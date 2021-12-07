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


class Testing(commands.Cog, name="Testing"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="botmanager", description="Gives Bot Manager role to a Member."
    )
    @commands.has_permissions(administrator=True)
    async def botmanager(self, ctx, member: nextcord.Member = None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Bot Manager Error", description="Member to give Bot Manager role to - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Bot Manager Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Bot Manager Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Bot ManagerError",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Bot Manager Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        BotManagerRole = nextcord.utils.get(guild.roles, name="Bot Manager")
        if member.id in [ctx.author.id, self.bot.user.id]:
            em3 = nextcord.Embed(
                title="Bot Manager Error",
                description="You cannot give yourself or the bot this role!",
            )
            return await ctx.send(embed=em3)
        if not BotManagerRole:
            BotManagerRole = await guild.create_role(name="Bot Manager")
            await ctx.send("No Bot Manager role found. Creating Bot Manager role...")
            '''for channel in guild.channels:
                await channel.set_permissions(
                    BotManagerRole,
                    view_channel=True
                )'''

        embed = nextcord.Embed(
            title="We hav a new Bot Manager!",
            description=f"{member.mention} is now a Bot Manager!",
            colour=nextcord.Colour.green(),
        )
        await ctx.send(embed=embed)
        await member.add_roles(BotManagerRole)
        await member.send(
            f"You have been granted __Admin__ access to: **Arceus**"
        )
        return

def setup(bot: commands.Bot):
    bot.add_cog(Testing(bot))
