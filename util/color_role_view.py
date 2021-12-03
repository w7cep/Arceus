import config
import nextcord
from util.role_view import RoleView
from utils.utils import custom_id

VIEW_NAME = "ColorRoleView"


class ColorRoleView(RoleView):
	def __init__(self):
		super().__init__(required_roles=[config.MEMBER_ROLE_ID])

	@nextcord.ui.button(
		label="Orange",
		emoji="🟠",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.ORANGE_ROLE_ID),
	)
	async def orange_button(self, button, interaction):
		await self.handle_click(button, interaction)
		
	@nextcord.ui.button(
		label="Yellow",
		emoji="🟡",
		style=nextcord.ButtonStyle.blurple,
		# set custom id to be the bot name : the class name : the role id
		custom_id=custom_id(VIEW_NAME, config.YELLOW_ROLE_ID),
	)
	async def yellow_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Green",
		emoji="🟢",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.GREEN_ROLE_ID),
	)
	async def green_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Blue",
		emoji="🔵",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.BLUE_ROLE_ID),
	)
	async def blue_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Purple",
		emoji="🟣",
		style=nextcord.ButtonStyle.blurple,
		# set custom id to be the bot name : the class name : the role id
		custom_id=custom_id(VIEW_NAME, config.PURPLE_ROLE_ID),
	)
	async def purple_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="Brown",
		emoji="🟤",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.BROWN_ROLE_ID),
	)
	async def brown_button(self, button, interaction):
		await self.handle_click(button, interaction)

	@nextcord.ui.button(
		label="White",
		emoji="⚪",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.WHITE_ROLE_ID),
	)
	async def white_button(self, button, interaction):
		await self.handle_click(button, interaction)
  
	@nextcord.ui.button(
		label="Maroon",
		emoji="🔴",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.MAROON_ROLE_ID),
	)
	async def maroon_button(self, button, interaction):
		await self.handle_click(button, interaction) 
