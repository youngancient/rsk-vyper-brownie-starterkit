"""
Deployment script for ERC20 and Vault contracts
Usage: brownie run scripts/deploy --network rootstock-testnet
"""

from brownie import ERC20, Vault, accounts, network, config
import json
from pathlib import Path


def get_account():
    """
    Get account from private key or use local account
    """
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def get_tx_params(account):
    """
    Generate transaction parameters, forcing legacy gas for Rootstock
    """
    params = {"from": account}
    # RSK requires legacy Type 0 transactions. 0.06 gwei is a safe default.
    if "rootstock" in network.show_active():
        params["gas_price"] = "0.065 gwei" 
        params["required_confs"] = 1  # Wait for 1 RSK block confirmation (~30 secs)
    return params

def save_deployment_info(contract_name, contract_address, network_name):
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
        "tx_hash": None  # Can be added if needed
    }
    
    with open(deployment_file, "w") as f:
        json.dump(deployments, f, indent=2)
    
    print(f"✅ Deployment info saved to {deployment_file}")


def deploy_erc20():
    """
    Deploy ERC20 token contract
    """
    print("=" * 60)
    print("Deploying ERC20 Token...")
    print("=" * 60)
    
    account = get_account()
    tx_params = get_tx_params(account)
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
    print(f"Network: {network.show_active()}")
    
    # Deploy
    token = ERC20.deploy(
        name,
        symbol,
        decimals,
        initial_supply,
        tx_params
    )
    
    print(f"\n✅ ERC20 Token deployed at: {token.address}")
    print(f"Transaction: {token.tx.txid if hasattr(token.tx, 'txid') else 'N/A'}")
    
    # Save deployment info
    save_deployment_info("ERC20", token.address, network.show_active())
    
    return token


def deploy_vault(token_address):
    """
    Deploy Vault contract
    """
    print("\n" + "=" * 60)
    print("Deploying Vault...")
    print("=" * 60)
    
    account = get_account()
    tx_params = get_tx_params(account)

    print(f"Token Address: {token_address}")
    print(f"Deploying from: {account.address}")
    print(f"Network: {network.show_active()}")
    
    # Deploy
    vault = Vault.deploy(
        token_address,
        tx_params
    )
    
    print(f"\n✅ Vault deployed at: {vault.address}")
    print(f"Transaction: {vault.tx.txid if hasattr(vault.tx, 'txid') else 'N/A'}")
    
    # Save deployment info
    save_deployment_info("Vault", vault.address, network.show_active())
    
    return vault


def main():
    """
    Main deployment function
    """
    print("\n🚀 Starting Deployment Process")
    print(f"Network: {network.show_active()}")
    print("=" * 60)
    
    # Deploy ERC20
    token = deploy_erc20()
    
    # Deploy Vault
    vault = deploy_vault(token.address)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Deployment Summary")
    print("=" * 60)
    print(f"Network: {network.show_active()}")
    print(f"ERC20 Token: {token.address}")
    print(f"Vault: {vault.address}")
    print("=" * 60)
    print("\n✅ Deployment complete!")
    print("\nNext steps:")
    print("1. Verify contracts: brownie run scripts/verify --network <network>")
    print("2. Check deployments/<network>.json for addresses")
    print("=" * 60)

