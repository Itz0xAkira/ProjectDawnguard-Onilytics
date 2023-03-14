import disnake
from disnake.ext import commands
from lib.APIsLib import *
from lib.dbDriver import *
import config

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
libDir = parent + "/lib/"
sys.path.append(libDir)
sys.path.append(parent)

bot_ = commands.Bot(
    command_prefix=config.prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True,
    owner_ids=config.owner_ids
)


# WebHook : Server name
ServerNames = getWebhooks()

ServerNames = {
    10: 'test'
}

# Channels IDs : Webhooks f
servers = getChannels()

servers = {
    1:[10],
    1028823443556278383:[],
    0:[],
    0:[],
    0:[],
}


def data(name,author,avatar):
    
    res = reservoir_get_collection_data(name)
    block = blockdaemon_get_collection_data(res["contract"])
    nftPort = NFTPORT_get_collection_data(res["contract"])
    
    
    
    embed = disnake.Embed(
    title= res["name"] ,
    description=str(nftPort["contract"]['metadata']["description"]),
    color=disnake.Colour.red(),
    )

    embed.set_author(
        name= author,
        icon_url= avatar
    )
    embed.set_footer(
        text="Powered by Project Dawnguard.",
        icon_url="https://iili.io/H0uvi6g.jpg",
    )

    embed.set_thumbnail(url= res["image"])
    embed.set_image(url=nftPort["contract"]['metadata']["banner_url"])

    embed.add_field(name=" Discord", value="[Here]("+ block["collection"]['meta']["discord_url"] +")", inline=False)
    embed.add_field(name="🐦 Twitter", value="[Here]("+ "https://twitter.com/" + block["collection"]['meta']["twitter_username"] +")", inline=False)
    embed.add_field(name="Volume", value=" " + str(int(res["allTimeVolume"])) + " ETH", inline=True)
    embed.add_field(name="Floor Price", value= " " + str(res["floorAskPrice"]) + " ETH               ", inline=True)
    verValue = res["openseaVerificationStatus"]
    if verValue == "verified":
        embed.add_field(name="Verified", value=":white_check_mark:", inline=True)
    else: 
        embed.add_field(name="Verified", value="❌", inline=True)
    
    
    return embed



def Sales(name,author,avatar):
    res = LookUpCollection(name)
    sales = getSales(res["contract"])
    
    # the graph should be created here using the data coming from var sales#
    
    embed = disnake.Embed(
    color=disnake.Colour.red()
    )

    embed.set_author(
        name= author,
        icon_url= avatar
    )
    embed.set_footer(
        text="Powered by Project Dawnguard.",
        icon_url="https://iili.io/H0uvi6g.jpg",
    )
    
    embed.set_image(file = disnake.file("path/to/file.png"))
    # PNG should be deleted after the command is done