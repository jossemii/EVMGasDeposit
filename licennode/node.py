import json
from web3 import Web3, HTTPProvider

class Node:

    def __init__(self, w3, contract_addr):
        self.contract = w3.eth.contract(
                address=contract_addr, 
                abi=json.load(open('dist/abi.json').read())
            )

    def _session_update(self):
        pass

    def _refund_gas_petition(self):
        pass

    



Node(
    w3 = Web3(HTTPProvider('localhost:7545')),
    contract_addr = ''
)