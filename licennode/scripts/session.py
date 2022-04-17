import json
from web3 import Web3, HTTPProvider

class Session:
    
    def __init__(self, w3, contract_addr, initial_gas_amount):
        self.contract = w3.eth.contract(
                address=contract_addr, 
                abi=json.load(open('dist/abi.json').read())
            )
        
        tx_id = self.contract.functions.init_session().transfer(w3.eth.accounts[1], initial_gas_amount).transact()
        self.session_id = tx_id.data
        self.gas = initial_gas_amount - tx_id.gas_used*tx_id.wei
        


Session(
    w3 = Web3(HTTPProvider('localhost:7545')),
    contract_addr = ''
)