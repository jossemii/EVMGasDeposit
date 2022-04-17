from web3 import Web3, HTTPProvider

def node(w3):
    #contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi']) 
    print ("Latest Avalanche block number" , w3.eth.blockNumber)



node(
    w3 = Web3(HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
)