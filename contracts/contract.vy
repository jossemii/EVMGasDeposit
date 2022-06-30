# @version >=0.3.1

owner: address
token_list: HashMap[ bytes32, uint256]

event NewSession:
    token: bytes32
    gas_amount: uint256

event RefundGasPetition:
    token: bytes32


@internal
def _to_uint256(x: uint256) -> uint256:
    return x

@internal
def _to_bytes32(x: bytes32) -> bytes32:
    return x


@external
def __init__():
    self.owner = msg.sender
    self.token_list[EMPTY_BYTES32] = self._to_uint256(0)


@external
@payable
def add_gas(token: bytes32):
    self.token_list[token] += self._to_uint256(msg.value)

    log NewSession(
            token,
            self._to_uint256(msg.value)
        )



# TRANSFER PROPERTY OF THE CONTRACT.

@external
def transfer_property(new_owner: address):
    assert self.owner == msg.sender, "invalid owner address."
    self.owner = new_owner



# REFUND BALANCE TO THE OWNER.

@internal
def _refund_balance():
    send(self.owner, self.balance - 0)  # TODO debe de asegurarse de tener la liquidez suficiente por si los clientes quieren retirar gas. Podría haber una opcion en la sesion, que seleccione el cliente, en la que escoja si quiere tener una cobertura para retirar liquidez o no.


@external
def refund_balance():
    assert self.owner == msg.sender, "invalid owner address."
    self._refund_balance()