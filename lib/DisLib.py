import disnake
from disnake.ext import commands
from lib.APIsLib import *
from lib.dbDriver import *
import config
import datetime
import matplotlib.pyplot as plt


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

def TimeStamp_to_Date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object

def SalesTime(json):
    res = json["sales"]
    timestamps = []
    for i in range(len(res)):
        timestamps.append(TimeStamp_to_Date(res[i]["timestamp"]))
    return timestamps


def EthPrice(json):
    res = json["sales"]
    EthPrice = []
    for i in range(len(res)):
        EthPrice.append(res[i]["price"]["amount"]["decimal"])
    print(EthPrice)
    return EthPrice
    

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
    TimeStamps = SalesTime(sales) #this hold the list of date obj for the X axis 
    eth = EthPrice(sales) #this is for the list of the prices for each obj in TimeStamps list Should go on the Y axis
    
    
    x = TimeStamps
    y = eth

    #plt.rcParams.update({'font.size': 6})


    # Create the scatter plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, color ='blue')
    date_labels = [date.strftime('%b %d') for date in x] # convert dates to "Mar 03", "Mar 04", etc.
    
    MD = []
    for i in range(8,-1,-1):
        _now = datetime.date.today() - datetime.timedelta(days=i)
        n_md = _now.strftime('%b %d')
        MD.append(n_md)

    
    #Timestamps alt
    # for i in date_labels:
    #     if i not in MD:
    #         MD.insert(0,i)
    #     else:
    #         MD.append('')
    
    #Turn grid on
    ax.grid()
    
    # Add labels and title
    ax.set_xticklabels(MD)
    plt.ylabel('Price(ETH)', style = 'italic')
    plt.title('Sales', fontweight = 'bold')
    plt.xticks(rotation = 45)

    #Set inner graph color
    ax.set_facecolor('lightgrey')
    
    # Display the plot and outer graph color
    plt.savefig('Sales_Graph.png',facecolor='white')
    
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
    
    return embed