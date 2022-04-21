import time

def catch_event(contractAddress, w3, contract, event):
    def handle_event(event):
        receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
        result = contract.events.{event}.processReceipt(receipt)
        print(result[0]['args'])

    def log_loop(event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                handle_event(event)
                time.sleep(poll_interval)

    block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
    log_loop(block_filter, 2)