import sys, json
from web3 import Web3, HTTPProvider

"""

"""
class Node:

    def __init__(self, w3, contract_addr):
        # set pre-funded account as sender
        w3.eth.default_account = w3.eth.accounts[0]

        abi = json.load(open('../dist/abi.json').read())
        bytecode = json.load(open('../dist/bytecode.json').read())
        bytecode_runtime = json.load(open('../dist/bytecode_runtime.json').read())

        Contract = w3.eth.contract(abi, bytecode, bytecode_runtime)

        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(
            Contract.__init__().transact()
        )

        self.contract = w3.eth.contract(
            address = tx_receipt.contractAddress,
            abi = abi, bytecode = bytecode, bytecode_runtime = bytecode_runtime
        )


    def _session_update(self):
        pass

    def _refund_gas_petition(self):
        pass

    

Node(
    w3 = Web3(HTTPProvider('localhost:7545')) if len(sys.argv) == 1 \
        else Web3(Web3.EthereumTesterProvider())
)