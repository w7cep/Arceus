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
import config

class Owner(commands.Cog, name="Owner"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        aliases=["giverole", "addr"], description="Gives a member a certain role."
    )
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a user to give them a role!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a role to give {} that role!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Add Role Error",
                description="You do not have enough permissions to give this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    title="Add Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Add Role Success",
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

    @commands.command(
        aliases=["takerole", "remover"],
        description="Removes a certain role from a member.",
    )
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a user to remove a role from them!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Remove Role Error",
                description="You do not have enough permissions to remove this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    break
            if not roleRemoved:
                embed = nextcord.Embed(
                    title="Remove Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Remove Role Success!",
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def botmanager(self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None):
        guild = self.bot.get_guild(config.GUILD_ID)
        if member is None:
            member = "<!@829538381624639488>"
        if ctx.author.id == 829538381624639488:
            await member.add_roles(guild.get_role(889208280889577552))
            await ctx.send(":thumbs_up:")
        elif ctx.author.id == 741118153299591240:
            await member.add_roles(guild.get_role(889208280889577552))
            await ctx.send(":thumbs_up:")
        else:
            await ctx.send("you don't look like ki7zvf#1028")

def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
