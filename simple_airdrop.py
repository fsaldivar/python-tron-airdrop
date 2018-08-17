import json
import requests
import base58
import time

SELF_ADDRESS = ""
PK = ""
TOKEN_NAME = ""

def hexTRONAddress(address):
  return base58.b58decode_check(address.encode()).encode("hex")

def base58TRONAddress(address):
  return base58.b58encode_check(str(bytearray.fromhex(address)))

def broadcastTxnJSON(data):
  # Sign Data
  data_dict = json.loads(data)
  sign_dict = {'transaction':data_dict, 'privateKey':PK}
  post_data = json.dumps(sign_dict, separators=(',',':'))
  r = requests.post("http://127.0.0.1:8090/wallet/gettransactionsign", data=post_data)

  # Broadcast Signed Transaction Data
  r = requests.post("http://127.0.0.1:8090/wallet/broadcasttransaction", data=r.content)
  return r.content

def generateAssetTransferTxn(giftAddress):
  post_dict = {'owner_address':hexTRONAddress(SELF_ADDRESS), 'to_address':hexTRONAddress(giftAddress), 'asset_name':TOKEN_NAME.encode("hex"), 'amount':1}
  post_data = json.dumps(post_dict, separators=(',',':'))
  r = requests.post("http://127.0.0.1:8090/wallet/transferasset", data=post_data)
  return r.content

def main_airdrop_all():
  currentPage = 0
  total_accounts = 1

  print "Airdropping to ALL accounts"
  while (total_accounts - currentPage > 0):
    print "Processing accounts starting from: " + str(currentPage)
    r = requests.get("https://api.tronscan.org/api/account?limit=100&start="+str(currentPage))
    account_data = json.loads(r.content)
    total_accounts = account_data['total']
    account_objects = account_data['data']

    for account in account_data['data']:
      if account['address'] != SELF_ADDRESS:
        # Send Tokens
        broadcastTxnJSON(generateAssetTransferTxn(account['address']))
        time.sleep(.05)
    currentPage += 100
  print "Done!"

main_airdrop_all()
