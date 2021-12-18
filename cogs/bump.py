import nextcord
from nextcord import Embed
from nextcord.ext import commands
import config
from better_profanity import profanity
from datetime import datetime
import asyncio
profanity.load_censor_words_from_file("./data/profanity.txt")

class Bump(commands.Cog, name="Bump"):
    """Test commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        '''self.bot_reminder.start()'''

    '''@tasks.loop(hours=4)  # you can even use hours and minutes
    async def bot_reminder(self):
        print("Sending SysBot reminder message")
        channel = self.bot.get_channel(843271842931933224)
        await channel.send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")

    @bot_reminder.before_loop
    async def before_bot_reminder(self):
        print('waiting...')
        await self.bot.wait_until_ready()'''

    @commands.Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.now()-m.created_at).seconds < 60)

        if message.content == "!d bump":
            bump = nextcord.Embed(
                title=f"Thank you for the bump {message.author}",
                description="That was a good bumping!\nI will remind you in 2 hours for another!\nuse `.remindme` to get the <@&881596772143759400> role!")
            await message.channel.send(embed=bump)
            await asyncio.sleep(7200)
            await message.channel.send("<@&881596772143759400> I'm ready for another good bumping!")
        #7200 seconds = 2 hours


    @commands.command()
    @commands.has_permissions()
    @commands.guild_only()
    async def remindme(self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None):
        member = ctx.author
        role = ctx.guild.get_role(881596772143759400)

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

def setup(bot: commands.Bot):
    bot.add_cog(Bump(bot))
