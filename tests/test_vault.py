"""
Test suite for Vault contract

Tests include:
- Basic deposit/withdraw functionality
- Virtual shares inflation attack protection
- Emergency withdraw state updates
- Multi-user scenarios
"""

import pytest
from ape import project, accounts, networks, config, reverts

def get_event(tx, event_name):
    for log in tx.events:
        if getattr(log, 'event_name', getattr(log, 'name', '')) == event_name:
            return log
    return None



# Virtual shares constants (must match contract)
VIRTUAL_SHARES = 1000000000  # 1e9
VIRTUAL_ASSETS = 1  # 1 wei


@pytest.mark.unit
def test_vault_deployment(vault, token, deployer):
    """
    Test vault deployment
    """
    assert vault.token() == token.address
    assert vault.owner() == deployer
    assert vault.totalShares() == 0
    assert vault.totalAssets() == 0


@pytest.mark.unit
def test_first_deposit(vault, token, approved_vault_user1):
    """
    Test first deposit with virtual shares
    """
    amount = 100 * 10**18
    
    initial_balance = token.balanceOf(approved_vault_user1)
    initial_vault_balance = token.balanceOf(vault.address)
    
    tx = vault.deposit(amount, sender=approved_vault_user1)
    
    # Token transfer succeeded
    assert token.balanceOf(approved_vault_user1) == initial_balance - amount
    assert token.balanceOf(vault.address) == initial_vault_balance + amount
    
    # Shares calculated with virtual offset
    # shares = (amount * (0 + VIRTUAL_SHARES)) / (0 + VIRTUAL_ASSETS)
    expected_shares = (amount * VIRTUAL_SHARES) // VIRTUAL_ASSETS
    assert vault.shares(approved_vault_user1) == expected_shares
    assert vault.totalShares() == expected_shares
    assert vault.totalAssets() == amount
    
    # Check event
    assert get_event(tx, "Deposit") is not None
    assert getattr(get_event(tx, "Deposit"), "depositor") == approved_vault_user1
    assert getattr(get_event(tx, "Deposit"), "amount") == amount


@pytest.mark.unit
def test_subsequent_deposit_multi_user(vault, token, deployer, approved_vault_user1, approved_vault_user2):
    """
    Test deposit after initial deposit with different users
    """
    # First deposit by user1
    amount1 = 100 * 10**18
    vault.deposit(amount1, sender=approved_vault_user1)
    
    shares_after_first = vault.totalShares()
    assets_after_first = vault.totalAssets()
    
    # Second deposit by user2
    amount2 = 50 * 10**18
    vault.deposit(amount2, sender=approved_vault_user2)
    
    # User2 should receive proportional shares with virtual offset
    expected_shares = (amount2 * (shares_after_first + VIRTUAL_SHARES)) // (assets_after_first + VIRTUAL_ASSETS)
    assert vault.shares(approved_vault_user2) == expected_shares
    
    # Total should be updated
    assert vault.totalShares() == shares_after_first + expected_shares
    assert vault.totalAssets() == assets_after_first + amount2


@pytest.mark.unit
def test_deposit_zero_amount(vault, approved_vault_user1):
    """
    Test deposit with zero amount
    """
    with reverts("Amount must be greater than 0"):
        vault.deposit(0, sender=approved_vault_user1)


@pytest.mark.unit
def test_deposit_insufficient_allowance(vault, token, user1, deployer):
    """
    Test deposit without approval
    """
    amount = 100 * 10**18
    token.transfer(user1, amount, sender=deployer)
    # Don't approve
    
    with reverts():
        vault.deposit(amount, sender=user1)


@pytest.mark.unit
def test_withdraw(vault, token, approved_vault_user1):
    """
    Test withdraw functionality
    """
    # First deposit
    deposit_amount = 100 * 10**18
    vault.deposit(deposit_amount, sender=approved_vault_user1)
    
    shares = vault.shares(approved_vault_user1)
    initial_balance = token.balanceOf(approved_vault_user1)
    initial_vault_balance = token.balanceOf(vault.address)
    
    # Withdraw half of shares
    withdraw_shares = shares // 2
    tx = vault.withdraw(withdraw_shares, sender=approved_vault_user1)
    
    assert vault.shares(approved_vault_user1) == shares - withdraw_shares
    assert token.balanceOf(approved_vault_user1) > initial_balance
    assert token.balanceOf(vault.address) < initial_vault_balance
    
    # Check event
    assert get_event(tx, "Withdraw") is not None
    assert getattr(get_event(tx, "Withdraw"), "withdrawer") == approved_vault_user1
    assert getattr(get_event(tx, "Withdraw"), "shares") == withdraw_shares


@pytest.mark.unit
def test_withdraw_all(vault, token, approved_vault_user1):
    """
    Test withdrawAll functionality
    """
    # Deposit
    deposit_amount = 100 * 10**18
    vault.deposit(deposit_amount, sender=approved_vault_user1)
    
    shares = vault.shares(approved_vault_user1)
    assert shares > 0
    
    initial_balance = token.balanceOf(approved_vault_user1)
    
    # Withdraw all
    tx = vault.withdrawAll(sender=approved_vault_user1)
    
    assert vault.shares(approved_vault_user1) == 0
    assert vault.totalShares() == 0
    assert vault.totalAssets() == 0
    assert token.balanceOf(approved_vault_user1) > initial_balance


@pytest.mark.unit
def test_withdraw_insufficient_shares(vault, user1):
    """
    Test withdraw with insufficient shares
    """
    with reverts("Insufficient shares"):
        vault.withdraw(1, sender=user1)


@pytest.mark.unit
def test_withdraw_zero_shares(vault, approved_vault_user1):
    """
    Test withdraw with zero shares
    """
    with reverts("Shares must be greater than 0"):
        vault.withdraw(0, sender=approved_vault_user1)


@pytest.mark.unit
def test_convert_to_shares(vault, token, approved_vault_user1):
    """
    Test convertToShares function with virtual offset
    """
    # Before any deposits, uses virtual offset
    test_amount = 100 * 10**18
    expected_before = (test_amount * VIRTUAL_SHARES) // VIRTUAL_ASSETS
    assert vault.convertToShares(test_amount) == expected_before
    
    # After deposit
    deposit_amount = 100 * 10**18
    vault.deposit(deposit_amount, sender=approved_vault_user1)
    
    # Should calculate with virtual offset
    assets = 50 * 10**18
    total_shares_with_virtual = vault.totalShares() + VIRTUAL_SHARES
    total_assets_with_virtual = vault.totalAssets() + VIRTUAL_ASSETS
    expected_shares = (assets * total_shares_with_virtual) // total_assets_with_virtual
    assert vault.convertToShares(assets) == expected_shares


@pytest.mark.unit
def test_convert_to_assets(vault, token, approved_vault_user1):
    """
    Test convertToAssets function with virtual offset
    """
    # Before any deposits
    test_shares = 100 * 10**18
    expected_before = (test_shares * VIRTUAL_ASSETS) // VIRTUAL_SHARES
    assert vault.convertToAssets(test_shares) == expected_before
    
    # After deposit
    deposit_amount = 100 * 10**18
    vault.deposit(deposit_amount, sender=approved_vault_user1)
    
    shares = vault.shares(approved_vault_user1)
    total_shares_with_virtual = vault.totalShares() + VIRTUAL_SHARES
    total_assets_with_virtual = vault.totalAssets() + VIRTUAL_ASSETS
    expected_assets = (shares * total_assets_with_virtual) // total_shares_with_virtual
    assert vault.convertToAssets(shares) == expected_assets


@pytest.mark.unit
def test_ownership_transfer(vault, deployer, user1):
    """
    Test ownership transfer
    """
    assert vault.owner() == deployer
    
    tx = vault.transferOwnership(user1, sender=deployer)
    
    assert vault.owner() == user1
    
    # Check event
    assert get_event(tx, "OwnershipTransferred") is not None
    assert getattr(get_event(tx, "OwnershipTransferred"), "previous_owner") == deployer
    assert getattr(get_event(tx, "OwnershipTransferred"), "new_owner") == user1


@pytest.mark.unit
def test_ownership_transfer_only_owner(vault, user1, user2):
    """
    Test ownership transfer by non-owner
    """
    with reverts("Only owner"):
        vault.transferOwnership(user2, sender=user1)


@pytest.mark.unit
def test_ownership_transfer_invalid_address(vault, deployer):
    """
    Test ownership transfer to zero address
    """
    import ape
    with reverts("Invalid address"):
        vault.transferOwnership("0x0000000000000000000000000000000000000000", sender=deployer)


@pytest.mark.unit
def test_emergency_withdraw_updates_state(vault, token, deployer, approved_vault_user1):
    """
    Test emergency withdraw properly updates totalAssets and totalShares
    """
    deposit_amount = 100 * 10**18
    vault.deposit(deposit_amount, sender=approved_vault_user1)
    
    owner_deposit = 100 * 10**18
    token.transfer(deployer, owner_deposit, sender=deployer)
    token.approve(vault.address, owner_deposit, sender=deployer)
    vault.deposit(owner_deposit, sender=deployer)
    
    initial_total_assets = vault.totalAssets()
    initial_total_shares = vault.totalShares()
    owner_initial_shares = vault.shares(deployer)
    vault_balance = token.balanceOf(vault.address)
    owner_balance = token.balanceOf(deployer)
    
    emergency_amount = 50 * 10**18
    tx = vault.emergencyWithdraw(emergency_amount, sender=deployer)
    
    # Token balances updated
    assert token.balanceOf(vault.address) == vault_balance - emergency_amount
    assert token.balanceOf(deployer) == owner_balance + emergency_amount
    
    # CRITICAL: totalAssets and totalShares should be updated
    assert vault.totalAssets() == initial_total_assets - emergency_amount
    assert vault.totalShares() < initial_total_shares
    assert vault.shares(deployer) < owner_initial_shares
    
    # Check event
    assert get_event(tx, "EmergencyWithdraw") is not None


@pytest.mark.unit
def test_emergency_withdraw_only_owner(vault, user1):
    """
    Test emergency withdraw by non-owner
    """
    with reverts("Only owner"):
        vault.emergencyWithdraw(1, sender=user1)


@pytest.mark.integration
def test_inflation_attack_protection(vault, token, deployer, user1, user2):
    """
    Test that vault is protected against inflation attacks
    
    Attack scenario (without protection):
    1. Attacker deposits 1 wei
    2. Attacker sends large amount directly to contract
    3. Victim deposits, gets 0 shares due to rounding
    4. Attacker withdraws all
    
    With virtual shares, this attack is not profitable
    """
    # Setup attacker (user1) and victim (user2)
    attacker = user1
    victim = user2
    
    attacker_amount = 1000 * 10**18
    victim_amount = 100 * 10**18
    
    token.transfer(attacker, attacker_amount, sender=deployer)
    token.transfer(victim, victim_amount, sender=deployer)
    
    token.approve(vault.address, attacker_amount, sender=attacker)
    token.approve(vault.address, victim_amount, sender=victim)
    
    # Attacker makes first deposit of 1 wei
    vault.deposit(1, sender=attacker)
    attacker_shares_initial = vault.shares(attacker)
    
    # Attacker sends tokens directly to vault (donation)
    donation_amount = 1000 * 10**18 - 1
    token.transfer(vault.address, donation_amount, sender=attacker)
    
    # Victim deposits - with virtual shares, they should still get meaningful shares
    vault.deposit(victim_amount, sender=victim)
    victim_shares = vault.shares(victim)
    
    # CRITICAL: Victim should have received shares (> 0)
    assert victim_shares > 0, "Victim should receive shares due to virtual share protection"
    
    # Victim should be able to withdraw their funds
    vault.withdrawAll(sender=victim)
    victim_final_balance = token.balanceOf(victim)
    
    # Victim should recover most of their deposit
    # (may lose small amount due to attacker's donation, but not everything)
    assert victim_final_balance > 0, "Victim should recover funds"


@pytest.mark.integration
def test_full_workflow_multi_user(vault, token, deployer, user1, user2):
    """
    Integration test: Full deposit/withdraw workflow with multiple users
    """
    # Setup: Fund users
    amount1 = 1000 * 10**18
    amount2 = 500 * 10**18
    
    token.transfer(user1, amount1, sender=deployer)
    token.transfer(user2, amount2, sender=deployer)
    
    token.approve(vault.address, amount1, sender=user1)
    token.approve(vault.address, amount2, sender=user2)
    
    # User1 deposits
    vault.deposit(amount1, sender=user1)
    user1_shares = vault.shares(user1)
    assert user1_shares > 0
    
    # User2 deposits
    vault.deposit(amount2, sender=user2)
    user2_shares = vault.shares(user2)
    assert user2_shares > 0
    
    # Both users have different share amounts
    assert user1_shares != user2_shares
    
    # User1 withdraws half
    vault.withdraw(user1_shares // 2, sender=user1)
    assert vault.shares(user1) > 0
    
    # User2 withdraws all
    vault.withdrawAll(sender=user2)
    assert vault.shares(user2) == 0
    
    # User1 still has shares and assets remain
    assert vault.totalAssets() > 0
    assert vault.totalShares() > 0


@pytest.mark.unit
def test_very_small_deposit_shares(vault, token, deployer, approved_vault_user1, user2):
    """
    Test that very small deposits do not result in 0 shares 
    due to virtual offset calculation and safely execute.
    """
    amount1 = 1000 * 10**18
    vault.deposit(amount1, sender=approved_vault_user1)
    
    # User2 attempts a fractional dust deposit (1 wei)
    token.transfer(user2, 1, sender=deployer)
    token.approve(vault.address, 1, sender=user2)
    
    # Should succeed and grant >0 shares
    vault.deposit(1, sender=user2)
    assert vault.shares(user2) > 0


@pytest.mark.unit
def test_withdraw_after_emergencyWithdraw(vault, token, deployer, approved_vault_user1):
    """
    Test user withdrawal behavior after emergencyWithdraw
    """
    amount = 100 * 10**18
    vault.deposit(amount, sender=approved_vault_user1)
    
    owner_deposit = 100 * 10**18
    token.transfer(deployer, owner_deposit, sender=deployer)
    token.approve(vault.address, owner_deposit, sender=deployer)
    vault.deposit(owner_deposit, sender=deployer)
    
    # Owner emergency withdraws half the assets
    emergency_amount = 50 * 10**18
    vault.emergencyWithdraw(emergency_amount, sender=deployer)
    
    # User should still be able to withdraw remaining assets correctly
    tx = vault.withdrawAll(sender=approved_vault_user1)
    
    # They should get back exactly what they deposited
    assert getattr(get_event(tx, "Withdraw"), "amount") == 100 * 10**18


@pytest.mark.unit
def test_non_standard_erc20_returns_false(deployer, user1):
    """
    Test vault interaction with an ERC20 that returns False on failure
    """
    import ape
    # Assuming MockTokenReturnsFalse is compiled
    token = project.MockTokenReturnsFalse.deploy(sender=deployer)
    vault = deployer.deploy(project.Vault, token.address)
    
    # user1 has 0 tokens, the transferFrom inside deposit will return False
    token.approve(vault.address, 100, sender=user1)
    
    # Vault should catch the False return value and revert
    with reverts("Transfer failed"):
        vault.deposit(100, sender=user1)
        

@pytest.mark.unit
def test_non_standard_erc20_withdrawals_return_false(deployer, user1):
    """
    Test that withdraw, withdrawAll, and emergencyWithdraw revert if token transfer returns False
    """
    import ape
    token = project.MockTokenReturnsFalse.deploy(sender=deployer)
    vault = deployer.deploy(project.Vault, token.address)
    
    # Give user1 some tokens to deposit successfully
    amount = 100 * 10**18
    # We shouldn't use token.transfer here as it returns bool, but we can call it
    token.transfer(user1, amount, sender=deployer)
    token.approve(vault.address, amount, sender=user1)
    vault.deposit(amount, sender=user1)
    
    # Drain vault's token balance so that transfer returns False
    token.drain(vault.address, sender=deployer)
    
    with reverts("Transfer failed"):
        vault.withdraw(vault.shares(user1), sender=user1)

@pytest.mark.unit
def test_withdrawAll_erc20_returns_false(deployer, user1):
    import ape
    token = project.MockTokenReturnsFalse.deploy(sender=deployer)
    vault = deployer.deploy(project.Vault, token.address)
    amount = 100 * 10**18
    token.transfer(user1, amount, sender=deployer)
    token.approve(vault.address, amount, sender=user1)
    vault.deposit(amount, sender=user1)
    token.drain(vault.address, sender=deployer)
    with reverts("Transfer failed"):
        vault.withdrawAll(sender=user1)

@pytest.mark.unit
def test_emergencyWithdraw_erc20_returns_false(deployer, user1):
    import ape
    token = project.MockTokenReturnsFalse.deploy(sender=deployer)
    vault = deployer.deploy(project.Vault, token.address)
    amount = 100 * 10**18
    token.transfer(deployer, amount, sender=deployer)
    token.approve(vault.address, amount, sender=deployer)
    vault.deposit(amount, sender=deployer)
    token.drain(vault.address, sender=deployer)
    with reverts("Insufficient balance"):
        vault.emergencyWithdraw(amount, sender=deployer)

@pytest.mark.unit
def test_withdraw_amount_too_small(vault, token, deployer, user1):
    amount1 = 1000 * 10**18
    token.transfer(user1, amount1, sender=deployer)
    token.approve(vault.address, amount1, sender=user1)
    vault.deposit(amount1, sender=user1)
    with reverts("Withdrawal amount too small"):
        vault.withdraw(1, sender=user1)

@pytest.mark.unit
def test_withdrawAll_amount_too_small(vault, token, deployer, user1):
    amount1 = 1
    token.transfer(user1, amount1, sender=deployer)
    token.approve(vault.address, amount1, sender=user1)
    vault.deposit(amount1, sender=user1)
    token.approve(vault.address, amount1, sender=deployer)
    vault.deposit(amount1, sender=deployer)
    vault.emergencyWithdraw(1, sender=deployer)
    vault.withdrawAll(sender=user1)
    assert token.balanceOf(user1) == 1

@pytest.mark.unit
def test_emergencyWithdraw_more_than_tracked(vault, token, deployer):
    amount = 100 * 10**18
    token.transfer(vault.address, amount, sender=deployer)
    with reverts("Insufficient owner shares"):
        vault.emergencyWithdraw(amount, sender=deployer)

@pytest.mark.unit
def test_emergencyWithdraw_zero_amount(vault, deployer):
    with reverts("Amount must be greater than 0"):
        vault.emergencyWithdraw(0, sender=deployer)

@pytest.mark.unit
def test_emergencyWithdraw_insufficient_balance(vault, deployer):
    with reverts("Insufficient owner shares"):
        vault.emergencyWithdraw(100, sender=deployer)

@pytest.mark.unit
def test_withdrawAll_no_shares_to_withdraw(vault, user1):
    with reverts("No shares to withdraw"):
        vault.withdrawAll(sender=user1)
