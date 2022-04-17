import web3

def deploy_contract(w3, contract_interface):
         # Contratos de iniciación e implementación
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
         # Obtener hash de transacción del contrato implementado
    tx_hash = contract.deploy(
        transaction={'from': w3.eth.accounts[1]}
    )
         # Obtenga el recibo tx para obtener la dirección del contrato
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']

def generate(w3):
    deploy_contract(w3=w3)
