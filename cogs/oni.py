
# Importing Libraries
import disnake
from disnake import Webhook
from disnake.ext import commands
import aiohttp
from PIL import Image
import config
import io




bot_ = commands.Bot(
    command_prefix=config.prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True,
    owner_ids=config.owner_ids
)

# WebHook : Server name
ServerNames = {
    10: 'test'
}

# Channels IDs : Webhooks 
servers = {
    1:[10],
    1028823443556278383:[],
    0:[],
    0:[],
    0:[],
}

# Here is going to be the main cog for alpha oni
# worked on by akira and mikey

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
            print("if")
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

            for removeKey in toRemoveServer:
                if removeKey in ServerNames.keys():
                    ServerNames.pop(removeKey)
            print(servers)
            print(ServerNames)
            embed = disnake.Embed(title=f"Server has been removed :D", color=disnake.Color.random())
            await inter.send(content=None, embed=embed)
        except Exception as e:
            embed = disnake.Embed(title="Error", description=f"An error occurred while updating the bot! {e}", color=config.Error())
            await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(oni(bot))

