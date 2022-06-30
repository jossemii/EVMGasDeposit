# @version >=0.3.1


struct Token:
    client: address     # last client address
    gas_amount: uint256     # total gas amount added to this token
    balance_refundable: uint256     # balance refundable to this token

owner: address
token_list: HashMap[ bytes32, Token]

event NewSession:
    token: bytes32
    gas_amount: uint256


event RefundGasPetition:
    token: bytes32


@internal
def _to_uint256(x: uint256) -> uint256:
    return x

def _to_bytes32(x: bytes32) -> bytes32:
    return x


@external
def __init__():
    self.owner = msg.sender
    self.token_list[self._to_bytes32(0)] = Token({
        client: msg.sender,
        gas_amount: self._to_uint256(0),
        balance_refundable: self._to_uint256(0)
    })


@external
@payable
def add_gas(token: bytes32) -> uint256:
    if token not in self.token_list:
        self.token_list[token] = Token({
            client: msg.sender,
            gas_amount: self._to_uint256(msg.value),
            balance_refundable: self._to_uint256(0)
        })
    else:
        self.token_list[token].gas_amount += self._to_uint256(msg.value)
        self.token_list[token].client = msg.sender

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



# REFUND GAS PETITION.

# TODO, estos dos métodos se deben de estudiar mejor.
@external
def set_balance_refundable(token: bytes32, balance_refundable: uint256):
    assert self.owner == msg.sender, "invalid owner address."
    self.token_list[token].balance_refundable = balance_refundable


# Requiere que el nodo le de el valor de gas que le quedó. 
#  Por lo tanto, necesita ejecutarse en varios bloques.
@internal
def _refund_gas(token: bytes32):
    assert self.token_list[token].balance_refundable > 0, "nothing for refund."
    assert self.balance >= self.token_list[token].balance_refundable, "can't refund the gas. insuficient liquidity on contract."
    send(
        self.token_list[token].client, 
        self.token_list[token].balance_refundable
    )
    self.token_list[token].gas_amount = 0
    self.token_list[token].balance_refundable = 0
    log SessionUpdated(
            token,
            self.token_list[token].gas_amount
        )


@external
def refund_gas(token: bytes32):
    assert self.token_list[token].client == msg.sender, "invalid client."
    log RefundGasPetition(token)
    self._refund_gas(token)


@external
def shutdown_contract():
    assert self.owner == msg.sender, "invalid owner address."
    for i in range(0, 1): # self.token_list: TODO
        self._refund_gas(i)  # TODO tardará 2*numero_sesiones, ya que el método espera.
    self._refund_balance()