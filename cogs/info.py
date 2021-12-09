import nextcord
from nextcord.ext import commands
import platform
from util.help_command import NewHelpCommand
from datetime import datetime

class Info(commands.Cog, name="Info"):
    """Information commands"""

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.bot = bot

    @commands.command()
    async def vscode(self, ctx):
        em = nextcord.Embed(
            title="__**VS Code Online**__",
            description="Click [here](https://vscode.dev) to open the VS Code Online.",
            color=nextcord.Color.dark_green(),
            timestamp=datetime.now(),
            )
        em.set_image(url="https://cdn.discordapp.com/attachments/909167663496966175/918234042812493854/unknown.png")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/862327803964817438/907116113970741328/21035.jpg")
        await ctx.send(embed=em)

    @commands.command(name="botstats")
    async def botstats(self, ctx):
        """A useful command that displays bot statistics."""
        pythonVersion = platform.python_version()
        dpyVersion = nextcord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        version = "v1.1.0"
        developer = "<@741118153299591240>"
        embed = nextcord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="Useful stats.",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )
        embed.add_field(name="Bot Version:", value=version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="nextcord Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value=developer)

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
        embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.set_author(name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

    @commands.command(name="wiki")
    @commands.guild_only()
    async def wiki(self, ctx, msg):
        """Get info from wikipedia."""
        url: str = f"https://wikipedia.org/wiki/{msg}"
        await ctx.channel.trigger_typing()
        await ctx.send(f"Here : {url}")

    @commands.command(name="emoji")
    @commands.guild_only()
    async def emoji(self, ctx, emoji: nextcord.Emoji = None):
        """Display information about an emoji in the server."""
        if not emoji:
                    await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

        try:
                    emoji = await emoji.guild.fetch_emoji(emoji.id)
        except nextcord.NotFound:
                    await ctx.channel.trigger_typing()
                    await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **General:**
        **- Name:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]({emoji.url})
        **- Author:** {emoji.user.name}
        **- Time Created:** {creation_time}
        **- Usable by:** {can_use_emoji}

        **Other:**
        **- Animated:** {is_animated}
        **- Managed:** {is_managed}
        **- Requires Colons:** {requires_colons}
        **- Guild Name:** {emoji.guild.name}
        **- Guild Id:** {emoji.guild.id}
        """

        embed = nextcord.Embed(
        title=f"**Emoji Information for:** `{emoji.name}`",
        description=description,
        colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.set_author(name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)


# setup functions for bot
def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
