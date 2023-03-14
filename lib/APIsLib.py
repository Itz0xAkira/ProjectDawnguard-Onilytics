import requests
import config
import json

def LookUpCollection(name):
    url = "https://api.reservoir.tools/search/collections/v1?name="+ name +"&limit=1"
            
    headers = {
        "accept": "*/*",
        "x-api-key": config.reservoirAPI
    }
    
    response = requests.get(url, headers=headers)
    temp = json.loads(response.text)
    result = temp["collections"][0]["contract"]
    return result

def reservoir_get_collection_data(name):
    # this is from reservoir  API URL: https://docs.reservoir.tools/reference/
    
    url = "https://api.reservoir.tools/search/collections/v1?name="+ name +"&limit=1"
            
    headers = {
        "accept": "*/*",
        "x-api-key": config.reservoirAPI
    }
    
    response = requests.get(url, headers=headers)
    temp = json.loads(response.text)
    result = temp["collections"][0]
    return result
        
def NFTPORT_get_collection_data(address):
    url = "https://api.nftport.xyz/v0/nfts/" + address +"?chain=ethereum"

    headers = {
        "accept": "application/json",
        "Authorization": config.nftPortAPI
    }
    
    response = requests.get(url, headers=headers)
    msg = json.loads(response.text)
    return msg

def blockdaemon_get_collection_data(address):
    
    # this is from blockdaemon  API URL: https://blockdaemon.com/documentation/ubiquity-api/authentication/#x-api-key
    headers = {
    'X-API-Key': config.blockdaemonAPI,
    }

    response = requests.get('https://svc.blockdaemon.com/nft/v1/ethereum/mainnet/collection?contract_address='+ address +'', headers=headers)
    msg = json.loads(response.text)
    return msg
    
def getSales(address):
    url = "https://api.reservoir.tools/sales/v4?includeTokenMetadata=false&collection="+ address +"&limit=200"

    headers = {
        "accept": "*/*",
        "x-api-key": config.reservoirAPI
    }

    response = requests.get(url, headers=headers)
    msg = json.loads(response.text)
    return msg