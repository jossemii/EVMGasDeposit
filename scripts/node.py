import sys, json, time
from utils import catch_event
from web3 import Web3, HTTPProvider

class Node:

    def __init__(self, w3, contract_addr):
        self.w3 = w3
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

        self.sessions = {}

        # Contract events.

        # Update Session Event.
        catch_event(
            contractAddress = tx_receipt.contractAddress,
            w3 = w3,
            contract = self.contract,
            event_name = 'SessionUpdated',
            opt = lambda args: self.sessions.update({ args['session_id']: args['gas_amount'] })
        )

        # Refund Gas Event.
        catch_event(
            contractAddress = tx_receipt.contractAddress,
            w3 = w3,
            contract = self.contract,
            event_name = 'RefundGas',
            opt = lambda args: self.w3.eth.wait_for_transaction_receipt(
                                    self.contract.functions.set_balance_refundable(
                                        session_id = args['session_id'],
                                        balance_refundable = self.sessions[args['session_id']] - gas_amount_consumed(args['session_id'])
                                    ).transact()
                                )
        )

    def transfer_property(self, new_owner):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.transfer_property(
                new_owner = new_owner
            ).transact()
        )

    def shutdown_contract(self):
        self.w3.eth.wait_for_transaction_receipt(
            self.contract.functions.shutdown_contract().transact()
        )



    

Node(
    w3 = Web3(HTTPProvider('localhost:7545')) if len(sys.argv) == 1 \
        else Web3(Web3.EthereumTesterProvider())
)