import json
from web3 import Web3, HTTPProvider

def node(w3, contract_addr):
    w3.eth.get_block('latest')
    return
    contract = w3.eth.contract(
            address=contract_addr, 
            abi=json.load(open('dist/abi.json').read())
        )

    



node(
    w3 = Web3(HTTPProvider('localhost:7545')),
    contract_addr = ''
)