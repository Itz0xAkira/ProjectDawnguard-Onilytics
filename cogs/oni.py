
# Importing Libraries
import disnake
from disnake.ext import commands
import os
import aiohttp
import base64
import time
from PIL import Image
from io import BytesIO
import random
import json
import config


# Here is going to be the main cog for alpha oni

class oni(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded Cog Oni')


    # Command template
    @commands.slash_command(name="bitcoin", description="Get the current price of Bitcoin!")
    async def bitcoin(inter):
        try:
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            async with aiohttp.request("GET", url) as response:
                text = await response.text()
                value = json.loads(text)["bpi"]["USD"]["rate"]
                embed = disnake.Embed(title=f"Bitcoin Price", description=f"Current bitcoin price: ${value}", color=disnake.Color.random())
                embed.set_footer(text=f'Requested by {inter.author}', icon_url=inter.author.avatar.url)
                await inter.send(embed=embed)
        except Exception as e:
            print(f"Error sending bitcoin command: {e}")
            await inter.send(embed=errors.create_error_embed(f"Error sending bitcoin command: {e}"))
            

def setup(bot):
    bot.add_cog(oni(bot))
