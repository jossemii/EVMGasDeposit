import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware

def deploy_contract(w3, contract_interface):
    # Contratos de iniciación e implementación
    deploy_contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Obtener hash de transacción del contrato implementado
    tx_hash = deploy_contract.constructor().transact()

    # Obtenga el recibo tx para obtener la dirección del contrato
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    return tx_receipt.contractAddress

def generate():
    w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print('Is connected to the network: ', w3.isConnected())


    w3.eth.defaultAccount = '0xeA9942Da750Bb2Dc7DE63B8Fa4C73b31Cb92FE7e'
    contract_address = deploy_contract(
        w3 = w3,
        contract_interface={
            'abi': open('dist/abi.json', 'r').read(),
            'bin': open('dist/bytecode', 'rb').read()
        }
    )

    print(contract_address)


generate()