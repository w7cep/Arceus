import nextcord
from nextcord.ext import commands
import platform

class Support(commands.Cog, name="Support"):
    """Displays help information for commands and cogs"""

    def __init__(self, bot: commands.Bot):
        self.__bot = bot


    @commands.command(name="support")
    async def support(self, ctx, *, reason = None):
        """Command to get support from the Admins."""
        guild = ctx.guild
        user = ctx.author
        amount2 = 1
        await ctx.channel.purge(limit=amount2)
        channel = await guild.create_text_channel(f'Ticket {user}')
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
        perms = channel.overwrites_for(user)
        await channel.set_permissions(user, view_channel=not perms.view_channel)
        await channel.set_permissions(user, read_message_history=not perms.read_message_history)
        await channel.set_permissions(user, send_messages=not perms.send_messages)
        await ctx.channel.trigger_typing()
        await channel.send(f"{user.mention}")
        embed = nextcord.Embed(title=f"{user} requested support.", description= "Either an admin or support staff will be with you shortly...", color=0x00ff00)
        embed.add_field(name="Reason", value=f"``{reason}``")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.set_author(name="Frogadier", icon_url="https://cdn.discordapp.com/attachments/891852099653083186/904941718200283146/Frogadier_Avatar.png")
        await ctx.channel.trigger_typing()
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def ticket(self, ctx):
        """Create a ticket."""
        name2 = 'Tickets'
        role = int(915137514061316116)
        guild = ctx.guild
        user = ctx.author
        amount2 = 1
        await ctx.channel.purge(limit=amount2)
        category = nextcord.utils.get(ctx.guild.categories, name=name2)
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            role: nextcord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(f'Ticket {user}', overwrites=overwrites, category=category)
        await ctx.channel.trigger_typing()
        await ctx.send(f"Hey dude, I made {channel.name} for ya!")

# setup functions for bot
def setup(bot: commands.Bot):
    bot.add_cog(Support(bot))
