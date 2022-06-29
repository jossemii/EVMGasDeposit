import sys, json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class Session:

    def __init__(self, w3, contract_addr, private_key):
        self.w3 = w3
        self.priv = private_key
        self.pub = w3.eth.account.privateKeyToAccount(private_key).address

        self.contract = w3.eth.contract(
            address = contract_addr,
            abi = json.load(open('dist/abi.json')), 
            bytecode = open('dist/bytecode', 'rb').read()
        )


        tx_data = self.contract.functions.initi_session().__dict__.get('data_in_transaction')
        transaction = {
            'from': self.pub, # Only 'from' address, don't insert 'to' address
            'value': 0, # Add how many ethers you'll transfer during the deploy
            'gas': 2000000, # Trying to make it dynamic ..
            'gasPrice': self.w3.eth.gasPrice, # Get Gas Price
            'nonce': self.w3.eth.getTransactionCount(self.pub), # Get Nonce
            'data': tx_data, # Here is the data sent through the network,
            'chainId': json.load(open('scripts/provider.json'))['chain_id'],
        }
        # Sign the transaction using your private key
        signed = self.w3.eth.account.signTransaction(transaction, self.priv)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)

        print('Initi session tx_hash: ', tx_hash.hex())
        self.session_id = self.contract.events.session_initiated().processReceipt(self.w3.eth.waitForTransactionReceipt(tx_hash))['args']['session_id']
        print('session_id -> ', self.session_id)


    def refund_gas(self):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.refund_gas(
                from_session_id = self.session_id,
            ).transact()
        )


if __name__ == '__main__':
    w3 = Web3(HTTPProvider(json.load(open('scripts/provider.json'))['node_provider_uri']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    Session(
        w3 = w3,
        contract_addr = json.load(open('scripts/provider.json'))['contract_addr'],
        private_key = json.load(open('scripts/keys.json'))['private_key']
    )