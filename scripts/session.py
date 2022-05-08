import sys, json, time
from utils import catch_event
from web3 import Web3, HTTPProvider

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

    def increase_gas(self, amount):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.increase_gas(
                session_id = self.session_id
            ).transact({"from": self.wallet, "value": amount})
        )

    def transfer_gas(self, amount, to):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.transfer_gas(
                from_session_id = self.session_id,
                to_session_id = to,
                gas_amount = amount
            ).transact()
        )

    def refund_gas(self):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.refund_gas(
                from_session_id = self.session_id,
            ).transact()
        )



Session(
    w3 = Web3(HTTPProvider('localhost:7545')) if len(sys.argv) == 1 \
        else Web3(Web3.EthereumTesterProvider())
)