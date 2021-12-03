import nextcord
from nextcord.ext import commands


class Channel(commands.Cog, name="Channel"):
    """Channel Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, amount=5):
        """Purge a number of messages in a channel"""
        if amount is None:
            await ctx.send("Please specify a number of messages to purge")
        else:
            await ctx.channel.purge(limit=amount + 1)
            embed = nextcord.Embed(
                title=f"{ctx.author.name} purged: {ctx.channel.name}",
                description=f"{amount} messages were cleared",
            )
            await ctx.channel.trigger_typing()
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="clean")
    @commands.has_permissions(manage_channels=True)
    async def clean(self, ctx):
        """Cleans the chat of the bot's messages."""
        def is_me(m):
            return m.author == self.bot.user
        await ctx.channel.trigger_typing()
        await ctx.message.channel.purge(limit=100, check=is_me)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def ch(self, ctx):
        """Channel mod commands"""
        await ctx.channel.trigger_typing()
        await ctx.send("Invalid sub-command passed")

    @ch.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, channel: nextcord.TextChannel = None):
        "Lock the channel."
        if channel == None:
            channel = ctx.message.channel
        await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=False)
        await ctx.channel.trigger_typing()
        await channel.send(f"{channel.mention} has been locked 🔒")

    @ch.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, channel: nextcord.TextChannel = None):
        """Unlock the channel."""
        if channel == None:
            channel = ctx.message.channel
        await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=None, read_messages=None, view_channel=False)
        await ctx.channel.trigger_typing()
        await channel.send(f"{channel.mention} has been unlocked 🔓")

    @ch.command(name="stats")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def stats(self, ctx):
        """
        Sends a nice fancy embed with some channel stats
        """
        channel = ctx.channel
        embed = nextcord.Embed(
            title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}",
                         icon_url=ctx.author.avatar.url)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        embed.add_field(name="Channel Guild",
                        value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic",
                        value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Channel Position",
                        value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay",
                        value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is nsfw?",
                        value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?",
                        value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time",
                        value=channel.created_at, inline=False)
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        #!FIX: #3 embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        """Create new channels and categories.
        ($$new category @role "name of category")
        ($$new channel @role "name of channel")
        """
        await ctx.channel.trigger_typing()
        await ctx.send("Invalid sub-command passed.")

    @new.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: nextcord.Role, *, name):
        """Create a new category."""
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            role: nextcord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.channel.trigger_typing()
        await ctx.send(f"Hey dude, I made {category.name} for ya!")

    @new.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: nextcord.Role, *, name):
        """Create a new channel."""
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            role: nextcord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=self.bot.get_channel(8907541406363549716))
        await ctx.channel.trigger_typing()
        await ctx.send(f"Hey dude, I made {channel.name} for ya!")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def delete(self, ctx):
        """Delete channels and categories.
        ($$delete category @role "name of category")
        ($$delete channel @role "name of channel")
        """
        await ctx.channel.trigger_typing()
        await ctx.send("Invalid sub-command passed.")

    @delete.command(name='category')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _category(self, ctx, category: nextcord.CategoryChannel, *, reason=None):
        """Delete a category."""
        await category.delete(reason=reason)
        await ctx.channel.trigger_typing()
        await ctx.send(f"Hey man! I deleted {category.name} for ya!")

    @delete.command(name='channel')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _channel(self, ctx, channel: nextcord.TextChannel = None, *, reason=None):
        """Delete a channel."""
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.channel.trigger_typing()
        await ctx.send(f"Hey man! I deleted {channel.name} for ya!")

def setup(bot: commands.Bot):
    bot.add_cog(Channel(bot))
