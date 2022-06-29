import sys, json
from web3 import Web3, HTTPProvider, geth_poa_middleware

class Session:

    def __init__(self, w3, contract_addr):
        self.w3 = w3
        # set pre-funded account as sender
        w3.eth.default_account = w3.eth.accounts[0]

        abi = json.load(open('../dist/abi.json').read())
        bytecode = json.load(open('../dist/bytecode.json').read())
        bytecode_runtime = json.load(open('../dist/bytecode_runtime.json').read())

        self.wallet = w3.eth.accounts[0]

        self.contract = w3.eth.contract(
            address = contract_addr,
            abi = abi, bytecode = bytecode, bytecode_runtime = bytecode_runtime
        )

        self.session_id = self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.init_session().transact()
        )

    def refund_gas(self):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.refund_gas(
                from_session_id = self.session_id,
            ).transact()
        )


w3 = Web3(HTTPProvider(json.load(open('provider.json'))['node_provider_uri']))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
Session(
    w3 = w3,
    contract_addr = json.load(open('provider.json').read())['contract_addr']
)