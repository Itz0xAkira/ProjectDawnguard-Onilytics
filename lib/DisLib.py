import disnake
from disnake.ext import commands
from lib.APIsLib import *
from lib.dbDriver import *
import config
import datetime
import matplotlib.pyplot as plt
import numpy as np
import datetime
from hampel import hampel
import pandas as pd
import io
import urllib, base64

from PIL import Image

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
libDir = parent + "/lib/"
sys.path.append(libDir)
sys.path.append(parent)

bot = commands.Bot(
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
    timestamps = []
    for i in range(len(json)):
        res = json[i]["sales"]
        for j in range(len(res)):
            timestamps.append(TimeStamp_to_Date(res[j]["timestamp"]))
    return timestamps


def EthPrice(json):
    EthPrice = []
    for i in range(len(json)):
        res = json[i]["sales"]
        for j in range(len(res)):
            EthPrice.append(res[j]["price"]["amount"]["decimal"])
    return EthPrice
    
def SendListings(name):
    address = LookUpCollection(name)
    listings = listing(address)

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
    embed.add_field(name="Volume", value=" " + str(int(res["allTimeVolume"])) + " ETH", inline=True)
    embed.add_field(name="Floor Price", value= " " + str(res["floorAskPrice"]) + " ETH               ", inline=True)
    verValue = res["openseaVerificationStatus"]
    if verValue == "verified":
        embed.add_field(name="Verified", value=":white_check_mark:", inline=True)
    else: 
        embed.add_field(name="Verified", value="❌", inline=True)
    
    
    return embed, block, res, nftPort


def CreateEmbed(author,avatar, collection_name, _description, entry_point1, stop_loss, short_hold, TimeShort, mid_hold, TimeMid, long_hold, TimeLong):
    
    res = reservoir_get_collection_data(collection_name)
    nftPort = NFTPORT_get_collection_data(res["contract"])
    
    
    embed = disnake.Embed(
    title= res["name"] ,
    description= _description,
    color=disnake.Colour.green(),
    )
    embed.set_author(
        name= author,
        icon_url= avatar
    )
    embed.set_footer(
        text="Powered by Project Dawnguard.",
        icon_url="https://iili.io/H0uvi6g.jpg",
    )

    embed.set_thumbnail(url= avatar)
    embed.set_image(url=nftPort["contract"]['metadata']["banner_url"])
    
    embed.add_field(name="Entry Point ", value= entry_point1, inline=True)
    embed.add_field(name="Stop Loss", value= stop_loss, inline=True)
    embed.add_field(name="Floor Price", value= " " + str(res["floorAskPrice"]) + " ETH               ", inline=True)
    embed.add_field(name=" 🚀  ***Exit Points***", value= "", inline=False)
    embed.add_field(name="Short Term", value= short_hold + " Eth \n" + TimeShort, inline=True)
    embed.add_field(name="Mid term", value= mid_hold + " Eth \n" + TimeMid, inline=True)
    embed.add_field(name="Long Term", value= long_hold + " Eth \n" + TimeLong , inline=True)
    
    
    
    return embed, res, nftPort

def Sales(name):
    res = LookUpCollection(name)
    salesData = getSalesBySize(res)
    TimeStamps = SalesTime(salesData) #this hold the list of date obj for the X axis 
    eth = EthPrice(salesData) #this is for the list of the prices for each obj in TimeStamps list Should go on the Y axis
    x = TimeStamps
    y = remove_outlier_hampel(eth)
    

    # yMin = min(i for i in y if i is not None) - 0.2
    # yMax =  max(i for i in y if i is not None) + 0.2
    yMin = np.nanmin(y)-0.5
    yMax =  np.nanmin(y)+1.5


    # Create the scatter plot
    fig, ax = plt.subplots(figsize = (15,5))
    ax.set_ylim([yMin, yMax])
    
    scatter = ax.scatter(x, y, color ='#b33939',edgecolors="#ff5252")
    
    #Changes the timestamps to Dates
    # date_labels = [date.strftime('%b %d') for date in x] # convert dates to "Mar 03", "Mar 04", etc.
    
    plt.grid(axis='y', linestyle='--')
        
    #xlabel Timemstamps
    MD = []
    for i in range(6,-2,-1):
            _now = datetime.date.today() - datetime.timedelta(days=i)
            n_md = _now.strftime('%b %d')
            MD.append(n_md)
 
    # Add labels and title
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(MD)
    ax.xaxis.label.set_backgroundcolor("white")
    csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Helvetica'}
    plt.ylabel('Price(ETH)', style = 'italic',color="white")
    plt.title('Sales', fontweight = 'bold',color="white", fontname ="sans-serif", fontsize = 30)
    plt.xticks(rotation = 45, color = "white")
    plt.yticks(color = "white")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    
    
    #add Dawnguard logo
    bg_ax = fig.add_axes(rect=[-0.05,0.75,0.2,0.2], zorder=-1)
    bg_ax.axis('off')


    #Set inner graph color
    ax.set_facecolor((1, 1, 0, 0))
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    image = Image.open(buf)
    image = image.convert('RGB')
    image.save(buf, format='JPEG', quality=50)
    buf.seek(0)


    
    return buf

def getSalesBySize(res,limit=1000,size=20,startingFromToken=None):
    if  size < 1:
        return None
    
    salesList = list()
    nextPageToken = startingFromToken
    for i in range(size):
        if(size == 1 or i == 0 or nextPageToken is None):
            current = getSales(res,limit=limit)
            salesList.append(current)
            nextPageToken = salesList[0]["nextPageToken"]
        else:
            current = getSales(res,continuationToken=nextPageToken,limit=limit)
            salesList.append(current)
            nextPageToken = salesList[len(salesList) - 1]["nextPageToken"]

        if nextPageToken is None:
            break

    return salesList


def remove_outlier_hampel(data):
    time_series = pd.Series(data)
    # Outlier detection with Hampel filter
    # Returns the Outlier indices
    # For more outliers
    # outlier_indices = hampel(ts = time_series, window_size = 3) 
    outlier_indices = hampel(ts = time_series, window_size = 4, n=2)


    time_series[time_series.index.isin(outlier_indices)] = None
    # time_series = time_series.mask(outlier_indices, other=None)
    # time_series = time_series.where(pd.notnull(time_series), None)
    # time_series.loc[outlier_indices] = np.nan
    # time_series[outlier_indices] = None

    # Drop Outliers indices from Series
    filtered_d = time_series.tolist()
    return filtered_d