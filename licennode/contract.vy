# @version >=0.2.4 <0.3.0

SESSION_ID_DIGITS: constant(uint256) = 16
SESSION_ID_MODULUS: constant(uint256) = 10 ** SESSION_ID_DIGITS

struct Session:
    client: address
    gas_amount: uint256

owner: address
sessionList: HashMap[ uint256, Session]

event SessionUpdated:
    session_id: uint256
    gas_amount: uint256

event RefundGasPetition:
    session_id: uint256


@internal
@pure
def _generate_session_id(_client: address) -> uint256:
    return bitwise_xor(
                convert(sha256(_client), uint256),
                block.timestamp
            ) % SESSION_ID_MODULUS


@external
def __init__():
    self.owner = msg.sender


@external
def transfer_property(new_owner: address):
    assert self.owner == msg.sender, "invalid owner address."
    self.owner = new_owner


@external
def refund_balance():
    assert self.owner == msg.sender, "invalid owner address."
    send(self.owner, self.balance)


@external
@payable
def init_session(client: address) -> uint256:
    session_id: uint256 = self._generate_session_id(client)
    self.sessionList[session_id] = Session({
        client: client,
        gas_amount: msg.value
    })

    log SessionUpdated(
            session_id,
            self.sessionList[session_id].gas_amount
        )
    return session_id


@external
@payable
def increase_gas(session_id: uint256):
    assert self.sessionList[session_id].client == msg.sender, "invalid client."
    self.sessionList[session_id].gas_amount += msg.value
    
    log SessionUpdated(
            session_id,
            self.sessionList[session_id].gas_amount
        )


@external
def transfer_gas(from_session_id: uint256, to_session_id: uint256, gas_amount: uint256):
    assert self.sessionList[from_session_id].client == msg.sender, "invalid client."
    assert self.sessionList[from_session_id].gas_amount >= gas_amount, "insuficient gas on session."
    self.sessionList[from_session_id].gas_amount -= gas_amount
    self.sessionList[to_session_id].gas_amount += gas_amount


# TODO, estos dos métodos se deben de estudiar mejor.
@external
def add_balance_refundable(session_id: uint256, balance_refundable: uint256):
    assert self.owner == msg.sender, "invalid owner address."
    self.sessionList[session_id].balance_refundable = balance_refundable


# Requiere que el nodo le de el valor de gas que le quedó. 
#  Por lo tanto, necesita ejecutarse en varios bloques.
@external
def refundGas(session_id: uint256):
    assert self.sessionList[session_id].client == msg.sender, "invalid client."
    log RefundGas(session_id)

    assert self.sessionList[session_id].balance_refundable > 0, "can't refund the gas."
    send(
        self.sessionList[session_id].client, 
        self.sessionList[session_id].balance_refundable
    )
    self.sessionList[session_id].gas_amount = 0
    self.sessionList[session_id].balance_refundable = 0
    log SessionUpdated(
            session_id,
            self.sessionList[session_id].gas_amount
        )
