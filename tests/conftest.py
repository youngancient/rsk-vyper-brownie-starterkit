"""
Pytest configuration and fixtures for Brownie tests

FIXED: User fixtures now point to different accounts for proper multi-user testing
"""

import pytest
from ape import project, accounts, networks, config, reverts


@pytest.fixture(scope="session", autouse=True)
def setup_accounts():
    pass



@pytest.fixture(scope="module")
def deployer():
    """
    Deployer account (account 0)
    """
    return accounts.test_accounts[0]


@pytest.fixture(scope="module")
def user1():
    """
    First test user account (account 1)
    FIXED: Now uses accounts.test_accounts[1] instead of accounts.test_accounts[0]
    """
    return accounts.test_accounts[1]


@pytest.fixture(scope="module")
def user2():
    """
    Second test user account (account 2)
    FIXED: Now uses accounts.test_accounts[2] instead of accounts.test_accounts[0]
    """
    return accounts.test_accounts[2]


@pytest.fixture(scope="module")
def user3():
    """
    Third test user account (account 3)
    """
    return accounts.test_accounts[3]


@pytest.fixture(scope="function")
def token(deployer):
    """
    Deploy ERC20 token for testing
    """
    name = "Rootstock Starter Token"
    symbol = "RST"
    decimals = 18
    initial_supply = 10_000_000 * 10**decimals  # 10 million tokens
    
    token = deployer.deploy(project.ERC20, name, symbol, decimals, initial_supply)
    return token


@pytest.fixture(scope="function")
def vault(deployer, token):
    """
    Deploy Vault contract for testing
    """
    vault = deployer.deploy(project.Vault, token.address)
    return vault


@pytest.fixture(scope="function")
def funded_user1(user1, token, deployer):
    """
    User1 with token balance for testing
    Using function scope for clean state in each test
    """
    amount = 10000 * 10**18  # 10,000 tokens
    token.transfer(user1, amount, sender=deployer)
    return user1


@pytest.fixture(scope="function")
def funded_user2(user2, token, deployer):
    """
    User2 with token balance for testing
    """
    amount = 10000 * 10**18  # 10,000 tokens
    token.transfer(user2, amount, sender=deployer)
    return user2


@pytest.fixture(scope="function")
def approved_vault_user1(funded_user1, token, vault):
    """
    User1 with approved token allowance for vault
    """
    amount = 10000 * 10**18
    token.approve(vault.address, amount, sender=funded_user1)
    return funded_user1


@pytest.fixture(scope="function")
def approved_vault_user2(funded_user2, token, vault):
    """
    User2 with approved token allowance for vault
    """
    amount = 10000 * 10**18
    token.approve(vault.address, amount, sender=funded_user2)
    return funded_user2
