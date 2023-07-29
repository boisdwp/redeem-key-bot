import datetime
from datetime import date
import requests, json, random
import nextcord
import time
from nextcord.ext import commands
from nextcord import SlashOption
from random import choice
import cooldowns

white = nextcord.Color.from_rgb(88, 101, 242) # Use any rgb colour code idc
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

bot = Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

channeltogenid = str(12345678910) # Generation channel ID
name = "Generator name" # Self Explanatory
generationlogschannelid = int(12345678910) # Generation Logs channel ID

special_codes_file = "special_codes.txt"  # Path to the notepad list of special codes

def read_special_codes():
    with open(special_codes_file, "r") as file:
        return file.read().splitlines()

def write_special_codes(codes):
    with open(special_codes_file, "w") as file:
        file.write("\n".join(codes))

restricted_channel_id = 12345678910  # Replace this with the allowed channel ID

@bot.slash_command(name="redeem", description="Redeem a special role using a text code.")
async def redeem(interaction: nextcord.Interaction, code: str):
    if interaction.channel.id != restricted_channel_id:
        embed = nextcord.Embed(
            title="Wrong Channel",
            description=f"If you want to redeem the code, please use the command in <#{restricted_channel_id}>.",
            color=white,
        )
        await interaction.send(embed=embed)
        return

    codes = read_special_codes()

    if code.lower() in [c.lower() for c in codes]:
        user = interaction.user
        role_id = 12345678910  # Replace this with the role ID that should be given to users who redeem the code
        role = interaction.guild.get_role(role_id)

        if role:
            if role in user.roles:
                embed = nextcord.Embed(
                    title="Role Given",
                    description="Sorry, but you already have the role. If this is a mistake, please message one of the staff members.",
                    color=white,
                )
                await interaction.send(embed=embed)
            else:
                await user.add_roles(role, reason="Redeemed special role")

                # Remove the redeemed code from the list
                codes = [c for c in codes if c.lower() != code.lower()]
                write_special_codes(codes)

                # Sending the embed
                embed = nextcord.Embed(
                    title="Special Role Redeemed!",
                    description=f"Thank you for buying our Generator. {role.name}",
                    color=white,
                )
                embed.set_image(
                    url="YOUR-IMAGE-URL"
                )  # Replace with the actual image URL you want to use
                await interaction.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="Invalid Key", description=f"Please message a staff for a new key if you bought it."
            )
            await interaction.send(embed=embed)
    else:
        await interaction.send("If you are messing with the bot, this will be a 1 Hour Timeout.")

try:
    bot.run("DISCORD_BOT_TOKEN") # https://discord.com/developers/applications
except Exception as error:
    print(error)
