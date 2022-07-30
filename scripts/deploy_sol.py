import json
import shutil
import web3, sys, os
from web3 import Web3
import sys
from web3.middleware import geth_poa_middleware
from solcx import compile_source

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
                    ).constructor(52)

        print("Building transaction...")
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
        print('Parity factor -> ',self.w3.eth.contract(
            address = Web3.toChecksumAddress(transaction_receipt.contractAddress),
            abi = self.abi, 
            bytecode = self.bin          
        ).functions.get_parity_factor().call())

def compile_solidity_code() -> tuple:
    compiled_sol = compile_source(
        open('contracts/sol/contract.sol', 'r').read(),
        output_values = ['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()
    print(f'Contract ID: {contract_id}')
    return contract_interface['abi'], contract_interface['bin']

def generate(private_key, public_key=None):
    DIR = 'dist'
    w3 = Web3(Web3.HTTPProvider(json.load(open('scripts/provider.json'))['node_provider_uri']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print('Is connected to the network: ', w3.isConnected())

    if public_key and (w3.eth.account.privateKeyToAccount(private_key).address == public_key):
        print('Private key is correct')

    w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key).address
    
    abi, bin = compile_solidity_code()

    deployment = DeployContract(
        abi = abi,
        bin = bin,
        private_key = private_key,
        w3 = w3
    )
    deployment.deploy()

    # Delete all content of dist folder
    for file in os.listdir(DIR):
        file_path = os.path.join(DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    print('Saving contract to file...')
    with open(f'dist/abi.json', 'w') as f:
        f.write(json.dumps(abi))
    with open(f'dist/bytecode', 'w') as f:
        f.write(bin)
    print('Done!')


if __name__ == '__main__':
    # Read keys.json
    with open('scripts/keys.json', 'r') as f:
        keys = json.load(f)
    generate(
        private_key = keys['private_key'],
        public_key = keys['public_key']
    )