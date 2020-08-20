from flask import Flask, render_template, request, redirect, g, url_for
from flask_bootstrap import Bootstrap
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import pprint
import json

url = "https://ropsten.infura.io/v3/8db3e633846f4c7e8d02c53a00253acc"
w3 =  Web3(HTTPProvider(url))

print(f"connection : {w3.isConnected()}")

abiJsonFile = open('./static/abi.json','r')
contract_abi = abiJsonFile.read()
contract_address = w3.toChecksumAddress("0x2D7337ed0BC0B9aE1574A3061D453Dc00BBf56A6")

contract = w3.eth.contract(address = contract_address, abi = contract_abi)

print(contract.all_functions())
print("Owner Account : "+contract.functions.owner().call())

owner_pub_key = "0xbAE6e58D470195BeE55b22872d76B342d0e6BF25"
owner_pri_key = "C59C333E99DDEDB9C8E46653B9A8D606A110074678DB2C8206B08A29E0F39944"

def saveInBlockchain(jsonString):
    
    transaction = contract.functions.dealsMade(jsonString).buildTransaction({
        'gas': 1000000,
        'gasPrice': Web3.toWei('1', 'gwei'),
        'from': owner_pub_key,
        'nonce': w3.eth.getTransactionCount(owner_pub_key)
    })


    ###############################EXECUTED################################
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=owner_pri_key)
    tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #############################################################
    tx_hash = w3.toHex(tx)
    print("tx_hash = "+tx_hash)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("\n\nTransaction receipt mined:")
    pprint.pprint(dict(receipt))
    print("\n\nWas transaction successful?")
    status = receipt['status']
    pprint.pprint(status)

    return "status"


def getPaperTrail():




    numOfDeals = contract.functions.numberOfDeals().call()
    print(f"\nNo. of registered users : {numOfDeals}")

    paperTrail = []
    
    for i in range(numOfDeals):
        dealData = json.loads(contract.functions.dealsMadeList(i).call())
        
        for deal in dealData:
            paperTrail.append(deal)


        
        
    print(paperTrail)

    return paperTrail