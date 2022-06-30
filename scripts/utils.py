import asyncio, time, json

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


def transact(
    w3, method, priv, value = 0, gas = 2000000, pub = None, input = None
) -> str:
        pub = w3.eth.account.privateKeyToAccount(priv).address if not pub else pub  # Not verify the correctness, 
                                                                                    #     pub param is only for skip that step.
        
        transaction = method(input).buildTransaction({'gasPrice': w3.eth.gasPrice}) if input \
            else method().buildTransaction({'gasPrice': w3.eth.gasPrice})
        transaction.update({
            'from': pub, # Only 'from' address, don't insert 'to' address
            'value': value, # Add how many ethers you'll transfer during the deploy
            'gas': gas, # Trying to make it dynamic ..
            'nonce': w3.eth.getTransactionCount(pub), # Get Nonce
            'chainId': json.load(open('scripts/provider.json'))['chain_id'],
        })
        # Sign the transaction using your private key
        signed = w3.eth.account.signTransaction(transaction, priv)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        return tx_hash.hex()