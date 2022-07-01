# Thats not an error.

owner: address


@external
def __init__():
    self.owner = msg.sender


@external
@view
def get_owner() -> address:
    return self.owner