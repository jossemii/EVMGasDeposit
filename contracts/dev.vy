# @version >=0.3.1

SESSION_ID_DIGITS: constant(uint256) = 16
SESSION_ID_MODULUS: constant(uint256) = 10 ** SESSION_ID_DIGITS

struct Session:
    client: address
    gas_amount: uint256
    balance_refundable: uint256

owner: address
session_list: HashMap[ uint256, Session]

event SessionUpdated:
    session_id: uint256
    gas_amount: uint256

@internal
def _generate_session_id(_client: address) -> uint256:
    return bitwise_xor(
                convert(_client, uint256),
                block.timestamp
            ) % SESSION_ID_MODULUS


@external
def __init__():
    self.owner = msg.sender


@external
@payable
def init_session() -> uint256:
    session_id: uint256 = self._generate_session_id(msg.sender)
    self.session_list[session_id] = Session({
        client: msg.sender,
        gas_amount: msg.value,
        balance_refundable: 0
    })

    log SessionUpdated(
            session_id,
            self.session_list[session_id].gas_amount
        )
    return session_id