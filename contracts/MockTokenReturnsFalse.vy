# @version 0.3.10
"""
Mock ERC20 token that returns False instead of reverting on failure.
This token is used to test the vault contract's ability to handle
non-standard ERC20 tokens.
"""

balances: public(HashMap[address, uint256])
allowances: public(HashMap[address, HashMap[address, uint256]])
force_fail: public(bool)

@external
def __init__():
    self.balances[msg.sender] = 1000 * 10**18
    self.force_fail = False

@view
@external
def balanceOf(account: address) -> uint256:
    return self.balances[account]

@external
def set_force_fail(fail: bool):
    self.force_fail = fail

@external
def transfer(to: address, amount: uint256) -> bool:
    if self.force_fail:
        return False
    if self.balances[msg.sender] < amount:
        return False
    self.balances[msg.sender] -= amount
    self.balances[to] += amount
    return True

@external
def transferFrom(sender: address, to: address, amount: uint256) -> bool:
    if self.force_fail:
        return False
    if self.allowances[sender][msg.sender] < amount or self.balances[sender] < amount:
        return False
    self.allowances[sender][msg.sender] -= amount
    self.balances[sender] -= amount
    self.balances[to] += amount
    return True

@external
def approve(spender: address, amount: uint256) -> bool:
    self.allowances[msg.sender][spender] = amount
    return True

@external
def drain(target: address):
    self.balances[target] = 0
