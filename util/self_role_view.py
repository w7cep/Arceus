import config
import nextcord
from util.role_view import RoleView
from utils.utils import custom_id

VIEW_NAME = "SelfRoleView"


class SelfRoleView(RoleView):
	def __init__(self):
		super().__init__(required_roles=[config.MEMBER_ROLE_ID])

	@nextcord.ui.button(
		label="TradeCord",
		emoji="🌀",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.TRADECORD_ROLE_ID),
	)
	async def tradecord_button(self, button, interaction):
		await self.handle_click(button, interaction)
		
	@nextcord.ui.button(
		label="Giveaway Ping",
		emoji="🎉",
		style=nextcord.ButtonStyle.blurple,
		# set custom id to be the bot name : the class name : the role id
		custom_id=custom_id(VIEW_NAME, config.GIVEAWAY_PING_ROLE_ID),
	)
	async def giveaway_ping_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Sword",
		emoji="⚔",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.SWORD_ROLE_ID),
	)
	async def sword_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Shield",
		emoji="🛡",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.SHIELD_ROLE_ID),
	)
	async def shield_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Male",
		emoji="🚹",
		style=nextcord.ButtonStyle.blurple,
		# set custom id to be the bot name : the class name : the role id
		custom_id=custom_id(VIEW_NAME, config.MALE_ROLE_ID),
	)
	async def male_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Female",
		emoji="🚺",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.FEMALE_ROLE_ID),
	)
	async def female_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Other",
		emoji="🚻",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.OTHER_ROLE_ID),
	)
	async def other_button(self, button, interaction):
		await self.handle_click(button, interaction) 
