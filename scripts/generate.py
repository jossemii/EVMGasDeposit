import web3, sys, os
from web3 import Web3
from web3.middleware import geth_poa_middleware

class DeployContract:
    def __init__(self, abi, bin, private_key, w3):
        self.w3 = w3
        self.abi = abi # Your contract ABI code
        self.bin = bin # Your contract ByteCode 
        self.priv = private_key
        self.pub = w3.eth.account.privateKeyToAccount(private_key).address

    def deploy(self):
        instance = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)
        # hacky .. but it works :D
        tx_data = instance.constructor().__dict__.get('data_in_transaction')
        transaction = {
            'from': self.pub, # Only 'from' address, don't insert 'to' address
            'value': 0, # Add how many ethers you'll transfer during the deploy
            'gas': 2000000, # Trying to make it dynamic ..
            'gasPrice': self.w3.eth.gasPrice, # Get Gas Price
            'nonce': self.w3.eth.getTransactionCount(self.pub), # Get Nonce
            'data': tx_data, # Here is the data sent through the network,
            'chainId': 43113,
        }
        # Sign the transaction using your private key
        signed = self.w3.eth.account.signTransaction(transaction, self.priv)
        #print(signed.rawTransaction)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        return tx_hash.hex()

def generate(DIR):
    w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print('Is connected to the network: ', w3.isConnected())

    
    private_key = '1b1810de121878360861aa25096eae02e259af680bc48305acf56456e2cff24c'
    if (w3.eth.account.privateKeyToAccount(private_key).address == '0xeA9942Da750Bb2Dc7DE63B8Fa4C73b31Cb92FE7e'):
        print('Private key is correct')

    w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key).address

    deployment = DeployContract(
        abi = open(DIR+'/abi.json', 'r').read(),
        bin = bytes(open(DIR+'/bytecode', 'r').read(), 'utf-8'),
        private_key = private_key,
        w3 = w3
    )
    contract = deployment.deploy()

    print(contract)


if __name__ == '__main__':
    os.system('mkdir dist')
    os.system('vyper contracts/'+sys.argv[1]+'.vy >> dist/bytecode')
    os.system('vyper -f abi contracts/'+sys.argv[1]+'.vy >> dist/abi.json')
    generate(DIR='dist')
    os.system('rm -rf dist')