import json
import web3, sys, os
from web3 import Web3
from hashlib import sha256
import sys
from web3.middleware import geth_poa_middleware

class DeployContract:
    def __init__(self, abi, bin, private_key, w3):
        self.w3 = w3
        self.abi = abi # Your contract ABI code
        self.bin = bin # Your contract ByteCode 
        self.priv = private_key
        self.pub = w3.eth.account.privateKeyToAccount(private_key).address

    def deploy(self):
        print("Deploying contract...")
        method = self.w3.eth.contract(
                        abi=self.abi, 
                        bytecode=self.bin
                    ).constructor()

        try:
            transaction = method.buildTransaction({
                'from': self.pub,
                'gasPrice': self.w3.eth.gasPrice,
                'gas': method.estimateGas(),
                'nonce': self.w3.eth.getTransactionCount(self.pub),
                'chainId': json.load(open('scripts/provider.json'))['chain_id'],
            })
        except Exception as e: print('Error: ',e); sys.exit(1)

        print("Signing transaction...")

        # Sign the transaction using your private key
        signed = self.w3.eth.account.signTransaction(transaction, self.priv)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        print("Waiting for transaction to finish...")
        transaction_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

def generate(private_key, public_key=None):
    DIR = 'dist'
    w3 = Web3(Web3.HTTPProvider(json.load(open('scripts/provider.json'))['node_provider_uri']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print('Is connected to the network: ', w3.isConnected())

    if public_key and (w3.eth.account.privateKeyToAccount(private_key).address == public_key):
        print('Private key is correct')

    w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key).address

    deployment = DeployContract(
        abi = open(DIR+'/abi.json', 'r').read(),
        bin = open(DIR+'/bytecode', 'rb').read(),
        private_key = private_key,
        w3 = w3
    )
    contract = deployment.deploy()

    print(contract)


if __name__ == '__main__':
    try:
        os.system('rm -rf dist')
    except: pass
    try:
        os.system('mkdir dist')
    except: pass
    contract = sys.argv[1] if len(sys.argv) > 1 else 'contract'
    os.system('vyper contracts/'+contract+'.vy >> dist/bytecode')
    os.system('vyper -f abi contracts/'+contract+'.vy >> dist/abi.json')

    # Read keys.json
    with open('scripts/keys.json', 'r') as f:
        keys = json.load(f)
    generate(
        private_key = keys['private_key'],
        public_key = keys['public_key']
    )