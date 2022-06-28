# @version >=0.3.1


owner: address
gas_amount: uint256


@external
def __init__():
    self.owner = msg.sender
    self.gas_amount = 0

@external
@payable
def pay():
    self.gas_amount = 12