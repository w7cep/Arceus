#This Code Is Under The MPL-2.0 License
import asyncio
import datetime
import json
import random
from difflib import get_close_matches
import nextcord.errors
from nextcord.ext.commands import MissingPermissions
import nextcord
from nextcord.colour import Color
from nextcord.components import Button
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ui.view import View
from nextcord.ext import commands
import json
import random
import asyncio
from difflib import get_close_matches

PREFIX = ">"
BOT_USER_ID = "909159653315842060"
ban_msg = [
    "flew to close to the radar and got banned",
    "messed up bad and got banned",
    "has been struck by the BAN HAMMER",
    "annoyed some staff and got banned",
    "wanted to see what would happen if you broke rules and got banned",
    "tried to dodge the ban hammer :rofl:",
    "was blown up by Creeper",
    "was killed by [Intentional Game Design]",
    "tried to swim in lava",
    "experienced kinetic energy",
    "drowned",
    "hit the ground too hard",
    "was squashed by a falling anvil",
    "was squished too much",
    "fell out of the world",
    "went up in flames",
    "went off with a bang",
    "was struck by lightning",
    "discovered the floor was lava",
]


kick_msg = [
    "got booted and got kicked?",
    "got kicked, imagine getting kicked...",
    "got kicked... I ran out of jokes",
]


class BanConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()

class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)  # gets a member object
        # can change into any permission
        permission = argument.guild_permissions.manage_messages
        if not permission:  # checks if user has the permission
            return argument  # returns user object
        else:
            # tells user that target is a staff member
            raise commands.BadArgument("You cannot punish other staff members")

class MuteConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()

class Moderation(commands.Cog, name="Moderation"):
    """Moderation commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.command(name="ban", description="Bans the member from your server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Can not ban yourself, trust me I woulda ages ago",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banMsg = random.choice(ban_msg)
        banEmbed = nextcord.Embed(
            title="Ban Success", description=f"{member.mention} {banMsg}"
        )
        banEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=banEmbed)
        await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        await member.ban(reason=reason)

    @commands.command(description="Unbans a member from your server by ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        em = nextcord.Embed(title="Unban Success", description="Unbanned user :D")
        await ctx.send(embed=em)

    @commands.command(name="kick", description="Kicks the member from your server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Kick Error", description="Member to kick - Not Found"
            )
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                title="Kick Error",
                description="I require the ``Kick Members`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Kick Error",
                description="You sadly can not kick your self",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        kickMsg = random.choice(kick_msg)
        kickEmbed = nextcord.Embed(
            title="Kick Success", description=f"{member.mention} {kickMsg}"
        )
        kickEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=kickEmbed)
        await member.send(f"You got kicked in **{guild}** | Reason: **{reason}**")
        await member.kick(reason=reason)

    @commands.command(name="tempban", description="bans a member indefinitely.")
    @commands.has_permissions(manage_messages=True)
    async def tempban(
        self, ctx, member: nextcord.Member = None, time=None, *, reason=None
    ):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Tempban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Tempban Error", description="Don't bother, i've tried"
            )
            return await ctx.send(embed=em5)
        if time == None:
            em2 = nextcord.Embed(
                title="Tempban Error", description="Time to ban - Not Found"
            )
            return await ctx.send(embed=em2)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Tempmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Tempmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)

        if not time == None:
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            tempban = int(time[0]) * time_convert[time[-1]]
            embed = nextcord.Embed(
                title="Tempban Success",
                description=f"{member.mention} was banned ",
                colour=nextcord.Colour.red(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Duration", value=time)
            await ctx.send(embed=embed)
            await member.ban(reason=reason)
            await member.send(
                f"You have been banned from: **{guild.name}** | Reason: **{reason}** | Time: **{time}**"
            )
            if not time == None:
                await asyncio.sleep(tempban)
                await ctx.guild.unban(member)
                await member.send(f"You have been unbanned from **{guild}**")
            return

    @commands.command(name="tempmute", description="Mutes a member indefinitely.")
    @commands.has_permissions(manage_messages=True)
    async def tempmute(
        self, ctx, member: nextcord.Member = None, time=None, *, reason=None
    ):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Tempmute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Tempmute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        if time == None:
            em2 = nextcord.Embed(
                title="Tempmute Error", description="Time to mute - Not Found"
            )
            return await ctx.send(embed=em2)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Tempmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Tempmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Muted role too high to give to a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        if not time == None:
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            tempmute = int(time[0]) * time_convert[time[-1]]
            embed = nextcord.Embed(
                title="Tempmute Success",
                description=f"{member.mention} was muted ",
                colour=nextcord.Colour.blue(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Duration", value=time)
            await ctx.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(
                f"You have been muted from: **{guild.name}** | Reason: **{reason}** | Time: **{time}**"
            )
            if not time == None:
                await asyncio.sleep(tempmute)
                await member.remove_roles(mutedRole)
                await member.send(f"You have been unmuted from **{guild}**")
            return

    @commands.command(
        name="mute", description="Mutes a member for a specific amount of time."
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Mute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Mute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Mute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Mute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if member.id in [ctx.author.id, self.bot.user.id]:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="You cannot warn yourself or the bot!",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    add_reactions=False,
                )

        embed = nextcord.Embed(
            title="Mute Success",
            description=f"{member.mention} was muted ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been muted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(name="unmute", description="Unmutes a muted member.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Unmute Error", description="Member to unmute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Unmute Error", description="wHat?"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Unmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Unmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Muted role too high to remove from a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        embed = nextcord.Embed(
            title="Unmute Success",
            description=f"{member.mention} was unmuted ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.remove_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been unmuted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(
        name="modmute", description="Mutes a member for a specific amount of time."
    )
    @commands.has_permissions(manage_messages=True)
    async def modmute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild

        if member == None:
            em1 = nextcord.Embed(
                title="Mute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Mute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Mute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Mute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)

        em = nextcord.Embed(
        title="Are you sure?",
        description="This is a very risky command only to be used in important situations such as, `NSFW or NSFLPosting` or `Raid on the Server`. Only use this command if no admin is online or responding. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
        )
        view = MuteConfirm()
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command has been Timed Out, please try again.")
        elif view.value:
            mutedRole = nextcord.utils.get(guild.roles, name="Muted")
            if member.id in [ctx.author.id, self.bot.user.id]:
                em3 = nextcord.Embed(
                title="Mute Error",
                description="You cannot warn yourself or the bot!",
            )
                return await ctx.send(embed=em3)
            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")
                await ctx.send("No mute role found. Creating mute role...")
                for channel in guild.channels:
                    await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    add_reactions=False,
                    )

            embed = nextcord.Embed(
                title="Mute Success",
                description=f"{member.mention} was muted ",
                colour=nextcord.Colour.blue(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            await ctx.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(
                f"You have been muted from: **{guild.name}** | Reason: **{reason}**"
            )
            return
        else:
            banEmbed = nextcord.Embed(
                title="Ban Cancelled",
                description="Lets pretend like this never happened them :I",
                )
            await ctx.author.send(embed=banEmbed)

    @commands.command(description="Modbans the member.")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def modban(self, ctx, member: nextcord.Member = None, *, reason=None):
        if reason is None:
            reason = f"{ctx.author.name} modbanned {member.name}"
        else:
            reason = (f"{ctx.author.name} modbanned {member.name} for the reason of {reason}")
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Can not ban yourself, trust me I woulda ages ago",
            )
            return await ctx.send(embed=embed69)
        em = nextcord.Embed(
            title="Are you sure?",
            description="This is a very risky command only to be used in important situations such as, `NSFW or NSFLPosting` or `Raid on the Server`. Only use this command if no admin is online or responding. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
        )
        view = BanConfirm()
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command has been Timed Out, please try again.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                title="Ban Success", description=f"{member.mention} {banMsg}"
            )
            banEmbed.add_field(name="Reason", value=reason)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                title="Ban Cancelled",
                description="Lets pretend like this never happened them :I",
            )
            await ctx.author.send(embed=banEmbed)

    @commands.command(name="block")
    @commands.has_permissions(manage_messages=True)
    async def _block(self, ctx, *, user: Sinner = None, channel: nextcord.TextChannel = None, reason=None):
        """Block a user from the channel."""
        if not user:  # checks if there is user
            return await ctx.send("You must specify a user")
        if channel == None:
            channel = ctx.channel
        if reason == None:
            reason = "no reason"
        # sets permissions for current channel
        await channel.set_permissions(user, send_messages=False, view_channel=True, read_message_history=True)
        await ctx.channel.trigger_typing()
        await channel.send(f"🚫{user.mention} has been blocked in {channel.mention} 🚫 for {reason}")

    @commands.command(name="unblock")
    @commands.has_permissions(manage_messages=True)
    async def _unblock(self, ctx, user: Sinner = None, channel: nextcord.TextChannel = None, reason=None):
        """Unblock a user from the channel."""
        if not user:  # checks if there is user
            return await ctx.send("You must specify a user")
        if channel == None:
            channel = ctx.channel

        # sets permissions for current channel
        await channel.set_permissions(user, send_messages=None, view_channel=None, read_message_history=None)
        await ctx.channel.trigger_typing()
        await channel.send(f"✅{user.mention} has been unblocked in {channel.mention}✅")

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
