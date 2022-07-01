# @version >=0.3.1

owner: address
token_list: HashMap[ bytes32, uint256]

event NewSession:
    token: indexed(bytes32)
    gas_amount: uint256


@external
def __init__():
    self.owner = msg.sender
    # self.token_list[EMPTY_BYTES32] = empty(uint256) With uncommenting this line, the compiler raise vyper.exceptions.TypeCheckFailure: Hex node did not produce IR. vyper.ast.nodes.Hex.

@external
@payable
def add_gas(token: bytes32):
    self.token_list[token] += msg.value

    log NewSession(
            token,
            msg.value
        )

@external
@view
def get_gas(token: bytes32) -> uint256:
    return self.token_list[token]

@external
@view
def get_owner() -> address:
    return self.owner


@external
def transfer_property(new_owner: address):
    assert self.owner == msg.sender, "invalid owner address."
    self.owner = new_owner




@internal
def _refund_balance():
    send(self.owner, self.balance - 0)  

@external
def refund_balance():
    assert self.owner == msg.sender, "invalid owner address."
    self._refund_balance()