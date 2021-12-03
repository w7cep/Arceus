from nextcord.ext import commands, tasks
import nextcord
import datetime
import nextcord.errors
from nextcord.ext.commands import MissingPermissions

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

class Block(commands.Cog, name="Block"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
    bot.add_cog(Block(bot))