import os
import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

CHANNELS_COLLECTION_NAME = u'channels'
WEBHOOKS_COLLECTION_NAME = u'webhooks'

folderPath = os.path.dirname(os.path.realpath(__file__))
fileName = "discord-database-pd-firebase-adminsdk-cm68h-0cae30ba85.json"
certificatePath = folderPath + "/" + fileName

cred = credentials.Certificate(certificatePath)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

## Production Tip: Change CHANNELS_COLLECTION_NAME to the production name (e.g: channels)

def addWebhook(channelId, webhookUrl, serverName):
    webhooksCollectionRef = db.collection(WEBHOOKS_COLLECTION_NAME)
    channelsCollectionRef = db.collection(CHANNELS_COLLECTION_NAME)
    channelDocRef = channelsCollectionRef.document(str(channelId))
    channelDoc = channelDocRef.get()
    encodedWebhookId = encode_message(webhookUrl)
    targetWebhookRef = webhooksCollectionRef.document(encodedWebhookId)
    if(not targetWebhookRef.get().exists):
        targetWebhookRef.set({
            "serverName": serverName,
            "webhookUrl": webhookUrl
        })

    if(channelDoc.exists):
        channel = channelDoc.to_dict()
        webhooksList = channel["webhooks"]
        for webhook in webhooksList:
            if webhook == encodedWebhookId:
                return

        webhooksList.append(encodedWebhookId)
        channelDocRef.update({
            "webhooks": webhooksList
        })
    else:
        newChannel = {
                "webhooks": [encodedWebhookId]
        }
        channelDocRef.set(newChannel)

def deleteChannel(channelId):
    channelsCollectionRef = db.collection(CHANNELS_COLLECTION_NAME)
    channelDocRef = channelsCollectionRef.document(channelId)
    channelDoc = channelDocRef.get()

    if(channelDoc.exists):
        channelDocRef.delete()
    else:
        print("[deleteChannelId] Referenced channel doesn't exist!")
        
def deleteWebhook(webhookUrl):
    webhooksCollectionRef = db.collection(WEBHOOKS_COLLECTION_NAME)
    encodedWebhookId = encode_message(webhookUrl)
    webhookDocRef = webhooksCollectionRef.document(encodedWebhookId)
    webhookDoc = webhookDocRef.get()

    if(webhookDoc.exists):
        webhookDocRef.delete()
    else:
        print("[deleteWebhook] Referenced channel doesn't exist!")


def deleteWebhookByServername(serverName):
    webhookCollectionRef = db.collection(WEBHOOKS_COLLECTION_NAME)
    webhookRef = webhookCollectionRef.where("serverName","==", serverName)
    webhooksRefs = webhookRef.get()
    for hookRef in webhooksRefs:
        hook = hookRef.to_dict()
        deleteWebhook(hook["webhookUrl"])


def removeWebhook(channelId, webhookUrl):
    channelsCollectionRef = db.collection(CHANNELS_COLLECTION_NAME)
    channelDocRef = channelsCollectionRef.document(channelId)
    channelDoc = channelDocRef.get()
    encodedWebhookId = encode_message(webhookUrl)

    if(channelDoc.exists):
        channel = channelDoc.to_dict()
        webhooksList = channel["webhooks"]
        filteredList = []
        for webhook in webhooksList:
            if not webhook == encodedWebhookId:
                print(webhook, " - ", encodedWebhookId)
                filteredList.append(webhook)
        channelDocRef.update({
            "webhooks": filteredList
        })
    else:
        print("[removeWebhook] Referenced channel doesn't exist!")


def getChannel(channelId):
        collectionRef = db.collection(CHANNELS_COLLECTION_NAME)
        channelDocRef = collectionRef.document(channelId)
        channelDoc = channelDocRef.get()
        if(not channelDoc.exists):
            return None
        channel = channelDoc.to_dict()
        for i in range(0,len(channel["webhooks"])):
            channel["webhooks"][i] = decode_message(channel["webhooks"][i])
        return channel


def getChannels():
    channels = {}
    channelsCollectionRef = db.collection(CHANNELS_COLLECTION_NAME)
    for channel in channelsCollectionRef.stream():
        channels[channel.id] = getChannel(channel.id)["webhooks"]
    return channels

def getWebhook(webhookUrl):
        collectionRef = db.collection(WEBHOOKS_COLLECTION_NAME)
        encodedWebhookId = encode_message(webhookUrl)
        webhookDocRef = collectionRef.document(encodedWebhookId)
        webhookDoc = webhookDocRef.get()
        if(not webhookDoc.exists):
            return None
        return webhookDoc.to_dict()

def getWebhooks():
    webhooks = {}
    webhookCollectionRef = db.collection(WEBHOOKS_COLLECTION_NAME)
    for hook in webhookCollectionRef.stream():
        webhook = getWebhook(decode_message(hook.id))
        webhooks[webhook["webhookUrl"]] = webhook["serverName"]
    return webhooks

def getServerNames():
    webhooks = getWebhooks()
    serverNames = []
    for hook in webhooks.items():
        serverNames.append(hook[1])
    return serverNames

def encode_message(message):   
    message_ascii_encoded = message.encode('ascii')
    message_b64_encoded = base64.b64encode(message_ascii_encoded)
    return message_b64_encoded.decode('ascii')

def decode_message(message):
    message_ascii_encoded = message.encode('ascii')
    message_b64_decoded = base64.b64decode(message_ascii_encoded)
    return message_b64_decoded.decode('ascii')
