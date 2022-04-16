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


@internal
@pure
def _generateSessionId(_client: address) -> uint256:
    return bitwise_xor(
                convert(sha256(_client), uint256),
                block.timestamp
            ) % SESSION_ID_MODULUS


@external
def __init__():
    self.owner = msg.sender


@external
def transfer_property(new_owner: address):
    assert self.owner == msg.sender
    self.owner = new_owner


@external
@payable
def modifySession(session_id: uint256):
    assert self.sessionList[session_id].client == msg.sender, "invalid client."
    self.sessionList[session_id].gas_amount += msg.value
    
    log SessionUpdated(
            session_id,
            self.sessionList[session_id].gas_amount
        )


@external
@payable
def initSession(client: address) -> uint256:
    session_id: uint256 = self._generateSessionId(client)
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
@view
def getSessionGasAmount(session_id: uint256) -> uint256:
    return self.sessionList[uint256].gas_amount
