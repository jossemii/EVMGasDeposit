import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware

def deploy_contract(w3, contract_interface, private_key):
    # Contratos de iniciación e implementación
    deploy_contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Obtener hash de transacción del contrato implementado
    tx_hash = deploy_contract.constructor().transact()

    # Obtenga el recibo tx para obtener la dirección del contrato
    tx_receipt = w3.eth.get_transaction_receipt(tx_hash)

    return tx_receipt.contractAddress

def generate():
    w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print('Is connected to the network: ', w3.isConnected())

    
    private_key = '1b1810de121878360861aa25096eae02e259af680bc48305acf56456e2cff24c'
    if (w3.eth.account.privateKeyToAccount(private_key).address == '0xeA9942Da750Bb2Dc7DE63B8Fa4C73b31Cb92FE7e'):
        print('Private key is correct')

    w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key).address
    contract_address = deploy_contract(
        w3 = w3,
        contract_interface={
            'abi': open('simple_dist/abi.json', 'r').read(),
            'bin': bytes(open('simple_dist/bytecode', 'r').read(), 'utf-8')
        },
        private_key=private_key
    )

    print(contract_address)


generate()