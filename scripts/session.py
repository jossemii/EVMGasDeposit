from hashlib import sha256
import json
from time import sleep
from utils import transact
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class Session:

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

        input_hash = sha256("192.168.1.16".encode('utf-8'))
        print('Input hash:', input_hash.hexdigest())

        input_bytes = sha256("192.168.1.16".encode('utf-8')).digest()
        print('Input:', str(input))

        tx_hash = transact(
            w3 = w3,
            method = self.contract.functions.add_gas(input_bytes),
            priv = self.priv,
            value = 20
        )
        print('Session tx_hash: ', tx_hash)

        response = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if response['status'] == 0:
            raise Exception('Session init failed ' + str(response))

        try:
            response = self.contract.functions.get_gas(input_bytes).call({'from': self.pub})
            print('Session gas: ', response)
        except: print('Session gas not found')

    def refund_gas(self):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.refund_gas(
                from_session_id = self.session_id,
            ).transact()
        )


if __name__ == '__main__':
    w3 = Web3(HTTPProvider(json.load(open('scripts/provider.json'))['node_provider_uri']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    while True:
        Session(
            w3 = w3,
            contract_addr = json.load(open('scripts/provider.json'))['contract_addr'],
            private_key = json.load(open('scripts/keys.json'))['private_key']
        )
        print('Session done')
        sleep(10)