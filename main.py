import discord
from discord.ext import commands
import re
from dotenv import load_dotenv
import os



load_dotenv()

def getColor(color_input):
    if re.match(r'^#(?:[0-9a-fA-F]{6})$', color_input):
        return discord.Colour(int(color_input[1:], 16))  # Convert hex to int
    return "INVALID COLOR"

# Intents to allow role management
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.message_content = True

# Create an instance of the Bot client
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command()
async def roleColor(ctx,color:str):
    author = ctx.author
    top_role = ctx.author.top_role
    color = getColor(color)
    if color == "INVALID COLOR":
        await ctx.send("Invalid color code. Please enter a valid color code.")

    else:
        #print([role.name for role in author.roles])
        if ['@everyone'] == [role.name for role in author.roles] or top_role.name == "Server Booster":
            try:
                new_role = await ctx.guild.create_role(name=f"{author} color", color=color)
                await ctx.send(f"Role '{new_role.name}' created successfully with color {new_role.color}.")
                try:
                    await author.add_roles(new_role)
                    if "Server Booster" in [role.name for role in author.roles]:
                        booster_role = discord.utils.get(ctx.guild.roles, name="Server Booster")
                        await new_role.edit(position=booster_role.position + 1)
                    await ctx.send(f"Role '{author} color' has been assigned to {author.mention}.")
                except discord.Forbidden:
                    await ctx.send("I do not have permission to assign this role.")
                except discord.HTTPException:
                    await ctx.send("Failed to assign role. Please try again.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to create roles.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to create the role: {e}")

        else:
            try:
                await top_role.edit(colour = color)
                await ctx.send("Role color has been updated!")
            except discord.Forbidden:
                await ctx.send("I don't have permission to edit this role.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to update the role color: {e}")



# Run the bot with your token
bot.run(os.getenv("token").strip())
