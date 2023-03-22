import io

import aiohttp
# Importing Libraries
import disnake
from lib.DisLib import *
from disnake import Webhook
from PIL import Image



class oni(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded Cog Oni')        
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != message.author.bot:
            if message.channel.id in list(servers.keys()):
                for i in list(servers[message.channel.id]):
                    print(list(servers[message.channel.id]))
                    attach = message.attachments
                    sentembed = message.embeds
                    if attach:
                        for attachment in attach:
                            fp = io.BytesIO()
                            await attachment.save(fp)
                            async with aiohttp.ClientSession() as session:
                                print(i)
                                webhook = Webhook.from_url(i, session=session)
                                await webhook.send(message.clean_content, file=disnake.File(fp, filename=attachment.filename), username='Onilytics',embeds=sentembed)
                    else:
                        async with aiohttp.ClientSession() as session:
                            print(i)
                            webhook = Webhook.from_url(i, session=session)
                            await webhook.send(message.clean_content, username='Onilytics',embeds=sentembed)
                            
                        
            
    @commands.slash_command(name="collection", description="Shows collection's data")
    async def collection(inter, collection_name):
        try:
            await inter.response.defer()
            await inter.send(embed= data(collection_name,inter.author, inter.author.avatar)[0] ,components=[
            disnake.ui.Button(label="Discord", style=disnake.ButtonStyle.primary, url = data(collection_name,inter.author, inter.author.avatar)[1]["collection"]['meta']["discord_url"]),
            disnake.ui.Button(label="Twitter", style=disnake.ButtonStyle.primary, url = "https://twitter.com/" + data(collection_name,inter.author, inter.author.avatar)[1]["collection"]['meta']["twitter_username"]),
            disnake.ui.Button(label="Etherscan", style=disnake.ButtonStyle.primary, url = "https://etherscan.io/address/" + data(collection_name,inter.author, inter.author.avatar)[2]["contract"]),
        ],)
            
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occurred while Fetching the data! {e}", color=config.Error())
            await inter.send(embed=embed)

    @commands.slash_command(name="collection_test", description="Shows collection's data")
    async def collection_test(inter, collection_name):
        await inter.response.defer()
        await inter.send(embed= data(collection_name,inter.author, inter.author.avatar))
            
    @commands.slash_command(name="sales", description="Shows collection's data")
    async def sales(inter, collection_name):
        try:
            await inter.response.defer()
            await inter.send(disnake.File(Sales(collection_name), filename='plot.jpg'))
            
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occurred while Fetching the data! {e}", color=config.Error())
            await inter.send(embed=embed)       
    
    
    
    @commands.slash_command(name="send_alpha", description="Shows collection's data")
    async def sendAlpha(inter, entry_point1, stop_loss, short_hold, mid_hold, long_hold, timeshort, timemid, timelong, collection_name, _description):
        try:
            await inter.response.defer()
            await inter.send(embed= CreateEmbed(inter.author, inter.author.avatar, entry_point1, stop_loss, short_hold, timeshort, mid_hold, timemid, long_hold, timelong, collection_name, _description)[0],components=[
            disnake.ui.Button(label="Blur", style=disnake.ButtonStyle.primary, url = "https://blur.io/collection/" + data(collection_name,inter.author, inter.author.avatar)[2]["contract"]),
            disnake.ui.Button(label="Etherscan", style=disnake.ButtonStyle.primary, url = "https://etherscan.io/address/" + data(collection_name,inter.author, inter.author.avatar)[2]["contract"]),
        ])
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occurred while Fetching the data! {e}", color=config.Error())
            await inter.send(embed=embed)

    # Command template
    @commands.slash_command(name="addserver", description="it adds a server to the list of the server to ")
    async def addserver(inter, server_name, source_channel, webhook):
        try:
            ServerNames[webhook] = server_name
            servers[int(source_channel)].append(webhook)
            print(servers)
            print(ServerNames)
            embed = disnake.Embed(title=f"Server is added :D", color=disnake.Color.random())
            await inter.send(content=None, embed=embed)
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occured while updating the bot! {e}", color=config.Error())
            await inter.send(embed=embed)

    @commands.slash_command(name="refresh", description="it adds a server to the list of the server to ")
    async def refresh(inter):
        try:
            # WebHook : Server name
            ServerNames = getWebhooks()

            # Channels IDs : Webhooks 
            servers = getChannels()
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occured while updating the bot! {e}", color=config.Error())
            await inter.send(embed=embed)

    @commands.slash_command(name="remove_server", description="it adds a server to the list of the server to ")
    async def remove_server(inter, server_name):
        try:
            toRemoveServer = []
            for key, val in ServerNames.items():
                if val == server_name:
                    toRemoveServer.append(key);
                
            for key, val in servers.items():
                for removeKey in toRemoveServer:
                    if removeKey in val:
                        val.remove(removeKey)
                        ## Remove webhook from channel

            for removeKey in toRemoveServer:
                if removeKey in ServerNames.keys():
                    ServerNames.pop(removeKey)
                     ## Delete webhook
                     
            print(servers)
            print(ServerNames)
            embed = disnake.Embed(title=f"Server has been removed :D", color=disnake.Color.random())
            await inter.send(content=None, embed=embed)
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occurred while updating the bot! {e}", color=config.Error())
            await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(oni(bot))
