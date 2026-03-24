# @version 0.3.10
"""
Mock ERC20 token that returns False instead of reverting on failure.
"""

balances: public(HashMap[address, uint256])
allowances: public(HashMap[address, HashMap[address, uint256]])

@external
def __init__():
    self.balances[msg.sender] = 1000 * 10**18

@external
def transfer(to: address, amount: uint256) -> bool:
    if self.balances[msg.sender] < amount:
        return False
    self.balances[msg.sender] -= amount
    self.balances[to] += amount
    return True

@external
def transferFrom(sender: address, to: address, amount: uint256) -> bool:
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
