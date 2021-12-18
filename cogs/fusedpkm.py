import nextcord
from nextcord import Embed
from nextcord.ext import commands
import config
from better_profanity import profanity
from datetime import datetime
import asyncio
profanity.load_censor_words_from_file("./data/profanity.txt")

class FusedPkm(commands.Cog, name="FusedPkm"):
    """Test commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade kyurem-white"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade kyurem-black"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade necrozma-dusk-mane"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade necrozma-dawn-wings"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade calyrex-ice"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade calyrex-shadow"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    '''@commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Kyurem-White"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Kyurem-Black"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```\nKyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Necrozma-Dusk-Mane"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Necrozma-Dawn-Wings"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Calyrex-Ice"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("$trade Calyrex-Shadow"):
            await message.channel.send("You can't trade fused pokemon!")
            em = nextcord.Embed(title="Fused Pokémon can't be traded",description="```Kyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow```")
            em.set_footer(text="A complete list of unavailable trade can be found by typing .illegal")
            await message.channel.send(embed=em)'''


def setup(bot: commands.Bot):
    bot.add_cog(FusedPkm(bot))
