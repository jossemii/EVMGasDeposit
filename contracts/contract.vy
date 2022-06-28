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

event RefundGasPetition:
    session_id: uint256


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
def set_balance_refundable(session_id: uint256, balance_refundable: uint256):
    assert self.owner == msg.sender, "invalid owner address."
    self.session_list[session_id].balance_refundable = balance_refundable


# Requiere que el nodo le de el valor de gas que le quedó. 
#  Por lo tanto, necesita ejecutarse en varios bloques.
@internal
def _refund_gas(session_id: uint256):
    assert self.session_list[session_id].balance_refundable > 0, "nothing for refund."
    assert self.balance >= self.session_list[session_id].balance_refundable, "can't refund the gas. insuficient liquidity on contract."
    send(
        self.session_list[session_id].client, 
        self.session_list[session_id].balance_refundable
    )
    self.session_list[session_id].gas_amount = 0
    self.session_list[session_id].balance_refundable = 0
    log SessionUpdated(
            session_id,
            self.session_list[session_id].gas_amount
        )


@external
def refund_gas(session_id: uint256):
    assert self.session_list[session_id].client == msg.sender, "invalid client."
    log RefundGasPetition(session_id)
    self._refund_gas(session_id)


@external
def shutdown_contract():
    assert self.owner == msg.sender, "invalid owner address."
    for i in range(0, 1): # self.session_list: TODO
        self._refund_gas(i)  # TODO tardará 2*numero_sesiones, ya que el método espera.
    self._refund_balance()