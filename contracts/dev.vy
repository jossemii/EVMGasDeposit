# @version >=0.3.1


owner: address
gas_amount: uint256


@internal
def _convert_to_uint256(amount: uint256) -> uint256:
    return amount

@external
def __init__():
    self.owner = msg.sender
    self.gas_amount = self._convert_to_uint256(msg.gas)

@external
@payable
def add_direct_gas_amount():
    self.gas_amount = self._convert_to_uint256(0)
