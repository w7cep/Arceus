import nextcord
from nextcord.ext import commands
import json
class Leveling(commands.Cog, name="Leveling"):
    """Test commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, user : nextcord.Member = None):
        if not user:
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'You areat level {lvl}!')
        else:
            id = user.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'{user} is at level {lvl}!')

    async def update_data(users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1

    async def add_experience(users, user, exp):
        users[f'{user.id}']['experience'] += exp

    async def level_up(users, user, message):
        with open('levels.json', 'r') as g:
            levels = json.load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1/8))
        if lvl_start < lvl_end:
            await message.channel.send(f'{user.mention} has leveled up!!! **LEVEL - {lvl_end}')
            users[f'{user.id}']['level'] = lvl_end

    @commands.Cog.listener()
    async def on_member_join(member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

    @commands.Cog.listener()
    async def on_message(message):
        if message.autho.bot == False:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await update_data(users, message.author)
            await add_experience(users, message.author, 1)
            await level_up(users, message.author, message)

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)

        await bot.process_commands(message)

def setup(bot: commands.Bot):
    bot.add_cog(Leveling(bot))
