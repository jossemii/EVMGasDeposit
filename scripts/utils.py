import asyncio
import time

def catch_event(contractAddress, w3, contract, event):
    def handle_event(event, event_name):
        receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
        result = getattr(contract.events, event_name).processReceipt(receipt)
        print(result[0]['args'])

    async def log_loop(event_filter, poll_interval, event_name):
        while True:
            for event in event_filter.get_new_entries():
                handle_event(event, event_name)
                time.sleep(poll_interval)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(
                    w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
                    , 2, event_name=event
                )))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()