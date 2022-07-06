import json
from time import sleep
from utils import catch_event
from hashlib import sha256
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class Provider:

    def __init__(self, w3, contract_addr, private_key):
        self.w3 = w3
        self.priv = private_key
        self.pub = w3.eth.account.privateKeyToAccount(private_key).address

        self.contract = w3.eth.contract(
            address = Web3.toChecksumAddress(contract_addr),
            abi = json.load(open('dist/abi.json')), 
            bytecode = open('dist/bytecode', 'rb').read()
        )

        print('Init session on contract:', contract_addr)

        self.sessions = {}


        # Update Session Event.
        catch_event(
            contractAddress = Web3.toChecksumAddress(contract_addr),
            w3 = w3,
            contract = self.contract,
            event_name = 'NewSession',
            opt = lambda args: self.__new_session(
                        token = args['token'], 
                        amount = args['gas_amount']
                    )
        )

    def __new_session(self, token, amount):
        print('New session:', token, amount)
        if token not in self.sessions:
            self.sessions[token] = amount
        else:
            self.sessions[token] += amount
            
        print('\n')
        print(self.sessions)


    def transfer_property(self, new_owner):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.transfer_property(
                new_owner = new_owner
            ).transact()
        )


if __name__ == '__main__':
    w3 = Web3(HTTPProvider(json.load(open('scripts/provider.json'))['node_provider_uri']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    Provider(
        w3 = w3,
        contract_addr = json.load(open('scripts/provider.json'))['contract_addr'],
        private_key = json.load(open('scripts/keys.json'))['private_key']
    )