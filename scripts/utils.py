import asyncio
import time

async def log_loop(event_filter, poll_interval: int, event_name: str, opt, w3, contract):
    while True:
        for event in event_filter.get_new_entries():
            receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
            result = getattr(contract.events, event_name).processReceipt(receipt)
            opt(args = result[0]['args'])
            time.sleep(poll_interval)

def catch_event(contractAddress, w3, contract, event_name, opt):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(
                    event_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress}),
                    pool_interval = 2, event_name = event_name, opt = opt, w3 = w3, contract = contract
                )))
    finally:
        # close loop to free up system resources
        loop.close()