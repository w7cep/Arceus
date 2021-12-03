import nextcord

class Dropdown(nextcord.ui.Select):
	def __init__(self):
		selectOptions = [
			nextcord.SelectOption(label="Python", description="python is cool"),
			nextcord.SelectOption(label="jave", description="java is old"),
			nextcord.SelectOption(label="French", description="if you put le infront of a word it becomes french. change my mind")
		]
		super().__init__(placeholder='Select your language', min_values=1, max_values=1, options=selectOptions)
  
	async def callback(self, interaction: nextcord.Interaction):
		if self.values[0] == "python":
			return await interaction.response.send_message('python is pretty cool ngl')
		await interaction.response.send_message(f'you chose {self.values[0]}')
  
class DropdownView(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(Dropdown())