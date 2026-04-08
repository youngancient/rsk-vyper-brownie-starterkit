"""
Deployment script for ERC20 and Vault contracts
Usage: ape run scripts/deploy --network rootstock-testnet
"""

from ape import project, accounts, networks, config, reverts
import json
import click
from pathlib import Path


def get_account():
    """
    Get account from private key or use local account
    """
    if networks.active_provider.network.name in ["development", "local", "hardhat"]:
        return accounts.test_accounts[0]
    else:
        import os
        alias = os.environ.get("APE_ACCOUNT_ALIAS", "default")
        return accounts.load(alias)


def get_tx_hash(contract):
    if hasattr(contract, 'txn_hash') and contract.txn_hash:
        return contract.txn_hash
    if hasattr(contract, 'receipt') and hasattr(contract.receipt, 'txn_hash') and contract.receipt.txn_hash:
        return contract.receipt.txn_hash
    if hasattr(contract, 'tx') and hasattr(contract.tx, 'txid') and contract.tx.txid:
        return contract.tx.txid
    return "N/A"

def save_deployment_info(contract_name, contract_address, network_name, tx_hash=None):
    """
    Save deployment information to file
    """
    deployment_dir = Path("deployments")
    deployment_dir.mkdir(exist_ok=True)
    
    deployment_file = deployment_dir / f"{network_name}.json"
    
    if deployment_file.exists():
        with open(deployment_file, "r") as f:
            deployments = json.load(f)
    else:
        deployments = {}
    
    deployments[contract_name] = {
        "address": contract_address,
        "network": network_name,
        "tx_hash": tx_hash
    }
    
    with open(deployment_file, "w") as f:
        json.dump(deployments, f, indent=2)
    
    print(f"✅ Deployment info saved to {deployment_file}")


def deploy_erc20(account):
    """
    Deploy ERC20 token contract
    """
    print("=" * 60)
    print("Deploying ERC20 Token...")
    print("=" * 60)
    
    # Token parameters
    name = "Rootstock Starter Token"
    symbol = "RST"
    decimals = 18
    initial_supply = 10_000_000 * 10**decimals  # 10 million tokens
    
    print(f"Name: {name}")
    print(f"Symbol: {symbol}")
    print(f"Decimals: {decimals}")
    print(f"Initial Supply: {initial_supply / 10**decimals:,.0f} {symbol}")
    print(f"Deploying from: {account.address}")
    print(f"Network: {networks.active_provider.network.name}")
    
    # Deploy
    token = account.deploy(project.ERC20, name, symbol, decimals, initial_supply)
    
    print(f"\n✅ ERC20 Token deployed at: {token.address}")
    print(f"Transaction: {get_tx_hash(token)}")
    
    # Save deployment info
    save_deployment_info("ERC20", token.address, networks.active_provider.network.name, get_tx_hash(token))
    
    return token


def deploy_vault(account, token_address):
    """
    Deploy Vault contract
    """
    print("\n" + "=" * 60)
    print("Deploying Vault...")
    print("=" * 60)
    

    print(f"Token Address: {token_address}")
    print(f"Deploying from: {account.address}")
    print(f"Network: {networks.active_provider.network.name}")
    
    # Deploy
    vault = account.deploy(project.Vault, token_address)
    
    print(f"\n✅ Vault deployed at: {vault.address}")
    print(f"Transaction: {get_tx_hash(vault)}")
    
    # Save deployment info
    save_deployment_info("Vault", vault.address, networks.active_provider.network.name, get_tx_hash(vault))
    
    return vault


def main():
    """
    Main deployment function
    """
    print("\n🚀 Starting Deployment Process")
    print(f"Network: {networks.active_provider.network.name}")
    print("=" * 60)
    
    if "mainnet" in networks.active_provider.network.name.lower():
        if not click.confirm("⚠️  DANGER: You are deploying to MAINNET! Are you sure you want to proceed?"):
            print("Deployment cancelled.")
            return
    
    
    account = get_account()
    # Deploy ERC20
    token = deploy_erc20(account)
    
    # Deploy Vault
    vault = deploy_vault(account, token.address)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Deployment Summary")
    print("=" * 60)
    print(f"Network: {networks.active_provider.network.name}")
    print(f"ERC20 Token: {token.address}")
    print(f"Vault: {vault.address}")
    print("=" * 60)
    print("\n✅ Deployment complete!")
    print("\nNext steps:")
    print("1. Verify contracts: ape run scripts/verify --network <network>")
    print("2. Check deployments/<network>.json for addresses")
    print("=" * 60)

