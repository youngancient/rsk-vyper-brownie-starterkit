<img src="./rootstock-banner.png" alt="RSK Logo" style="width:100%; height: auto;" />

# RSK Vyper + Ape Framework Starter Kit on Replit

The only zero-setup Vyper + Ape environment on Replit. Compile, test, and deploy highly secure Vyper 0.4.3 contracts to Rootstock testnet effortlessly.

## Features

- ✅ **Ape Framework + Vyper 0.4.3 auto-configured**
- ✅ **Rootstock testnet/mainnet** networks configured
- ✅ **Secure example contracts**:
  - `ERC20.vy` - Fully EIP-20 compliant Token (including self-transfers) with safe math inherently supported by Vyper.
  - `Vault.vy` - Vault with inflation attack protection (virtual shares) & mathematically proven owner withdrawal safety constraints.
- ✅ **Comprehensive test suite** using Pytest and native Ape Framework snap-shooting
- ✅ **One-click deploy & verify** scripts
- ✅ **Solidity → Vyper migration** cheat-sheet

## 📋 Prerequisites

### For Replit:
- No manual setup needed! Dependencies automatically bootstrap on your first 'Run' via the `.replit` bootloader natively.

### For Local Development:
- Python 3.8+ (Python 3.12 recommended)
- pip (Python package manager)

## 🚀 Quick Start

### On Replit:

1. **Fork this Repl** or create a new one from this template
2. **Click "Run"** - Ape will automatically compile the contracts
3. **Import your Deployment Account** (if deploying):
   ```bash
   ape accounts import default
   ```
4. **Deploy**: Run the CLI native deployer:
   ```bash
   ape run deploy --network rootstock:testnet
   ```

⚠️ **Educational only. Not audited. Do NOT deploy to mainnet without an external audit.**

### Local Setup:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/youngancient/rsk-vyper-brownie-starterkit.git
   cd rsk-vyper-brownie-starterkit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Node endpoints & Account keystores:**
   Create a `.env` file in the project root for custom node RPCs (optional):
   ```bash
   # .env file content
   # WARNING: Public nodes have rate limits! Use dedicated RPCs for production scale.
   # Ape Framework natively scans for these specialized environment variables to override the config RPCs dynamically!
   APE_ROOTSTOCK_TESTNET_URI=https://public-node.testnet.rsk.co
   APE_ROOTSTOCK_MAINNET_URI=https://public-node.rsk.co
   ```
   
   **Initialize your Ape Account Keystore with your private key natively:**
   ```bash
   ape accounts import default
   ```

4. **Compile contracts:**
   ```bash
   ape compile
   ```

5. **Run tests:**
   ```bash
   ape test
   ```

## 📁 Project Structure

```
.
├── contracts/              # Vyper 0.4.3 contracts
│   ├── ERC20.vy           # Secure ERC20 token implementation
│   └── Vault.vy           # Anti-inflation Vault contract
├── scripts/               # Deployment scripts
│   ├── deploy.py          # Deploy contracts
│   ├── verify.py          # Verify contracts
│   └── analyze.py         # Analyze structure
├── tests/                 # Test files
│   ├── conftest.py        # Pytest & Ape fixtures
│   ├── test_erc20.py      # ERC20 tests
│   └── test_vault.py      # Vault tests
├── ape-config.yaml        # Ape Framework config
├── .gitignore             
├── .env.example           # sample for .env
├── requirements.txt       # Python dependencies (eth-ape, ape-vyper)
├── replit.nix             # Replit Nix config
├── .replit                # Replit run config
├── pytest.ini             # Pytest config
├── SECURITY.md            # Security docs
├── MIGRATION.md           # Solidity → Vyper cheat-sheet
├── TESTING_GUIDE.md       # Comprehensive testing guide
└── README.md              # This file
```

## 🔧 Configuration

### Ape Configuration

Networks are configured in `ape-config.yaml`:

- **Rootstock Testnet**: Chain ID 31
- **Rootstock Mainnet**: Chain ID 30

### Environment Variables & Accounts

Create a `.env` file to map dedicated Node infrastructures securely (optional):

```env
# WARNING: Public nodes have rate limits! Replace with dedicated RPCs for production scale:
# Ape Framework natively scans for these specialized environment variables to override the config RPCs dynamically!
APE_ROOTSTOCK_TESTNET_URI=https://my-alchemy-testnet...
APE_ROOTSTOCK_MAINNET_URI=https://my-alchemy-mainnet...
```

Alternatively, Ape allows you to completely bypass configuration and ad-hoc deploy to ANY custom endpoint natively via the CLI string:
```bash
ape run deploy --network https://rpc.my-custom-node.com
```

**Next, securely bind your account private key natively to Ape:**
```bash
ape accounts import default --use-private-key
```

## Contracts

### ERC20.vy

Standard ERC20 token implementation with:
- Full ERC20 integration & Interface adherence
- Fully supports self-transfers (EIP-20 compendious)
- Automatic overflow/underflow protection intrinsic to Vyper 0.4.x

### Vault.vy

Highly secure deposit/withdraw vault with:
- Strict 1:1 proportional withdrawal guarantees preventing Rug-Pull vulnerabilities
- Share-based withdrawal system mitigating inflation attacks

## Testing

### Run All Tests

```bash
ape test
```

### Run Specific Test File

```bash
ape test tests/test_erc20.py
ape test tests/test_vault.py
```

### Test Markers

```bash
# Run only unit tests
ape test -m unit

# Run only integration tests
ape test -m integration
```

## Deployment

### Deploy to Testnet

```bash
ape run deploy --network rootstock:testnet
```

### Deploy to Mainnet

```bash
ape run deploy --network rootstock:mainnet
```

### Verify Contracts

To natively verify your deployed smart contracts on the Rootstock Blockscout explorers, run the included verification script:

```bash
ape run verify --network rootstock:testnet
```

The script will automatically detect the dynamic addresses securely captured within Ape's ecosystem `deployments/` architecture and evaluate their live validation status! 

*(Note: Currently, the verification script is an instructional assistant that fetches validation status and outputs the direct Blockscout GUI portals to paste your Vyper code manually!)*

## 📚 Documentation

### Migration Guide
See `MIGRATION.md` for a comprehensive Solidity → Vyper 0.4.3 migration cheat-sheet.

### Security
See `SECURITY.md` for security best practices and analysis tools.

## 🛠️ Development

### Compile Contracts

```bash
ape compile
```

### Open Ape Console

```bash
ape console
```

### Run Scripts

```bash
ape run <script_name> --network <network>
```

## 🌐 Rootstock Networks

### Testnet
- **Chain ID**: 31
- **RPC**: https://public-node.testnet.rsk.co
- **Explorer**: https://rootstock-testnet.blockscout.com/
- **Faucet**: https://faucet.rsk.co/

### Mainnet
- **Chain ID**: 30
- **RPC**: https://public-node.rsk.co
- **Explorer**: https://rootstock.blockscout.com/

## Dependencies

- **eth-ape** - Core Development framework (Successor to Ape Framework)
- **ape-vyper** - Vyper plugin natively compiling 0.4.3 environments
- **python-dotenv** - Environment variables parameter parsing

## License

This project is open source and available under the MIT License.

## Resources

- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Ape Framework Documentation](https://docs.apeworx.io/ape/stable/)
- [Rootstock Documentation](https://developers.rsk.co/)
- [Replit Documentation](https://docs.replit.com/)

# Disclaimer

The software provided in this GitHub repository is offered "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement.

- **Testing:** While this software includes a comprehensive Pytest test suite, its functionality, accuracy, reliability, and suitability for production or any specific purpose are not guaranteed.
- **Use at Your Own Risk:** The user assumes all risks associated with the use of this software. The author(s) of this software shall not be held liable for any damages, including but not limited to direct, indirect, incidental, special, consequential, or punitive damages arising out of the use of or inability to use this software, even if advised of the possibility of such damages.
- **No Liability:** The author(s) of this software are not liable for any loss or damage, including without limitation, any loss of profits, business interruption, loss of information or data, or other pecuniary loss arising out of the use of or inability to use this software.
- **Sole Responsibility:** The user acknowledges that they are solely responsible for the outcome of the use of this software, including any decisions made or actions taken based on the software's output or functionality.
- **No Endorsement:** Mention of any specific product, service, or organization does not constitute or imply endorsement by the author(s) of this software.
- **Modification and Distribution:** This software may be modified and distributed under the terms of the license provided with the software. By modifying or distributing this software, you agree to be bound by the terms of the license.
- **Assumption of Risk:** By using this software, the user acknowledges and agrees that they have read, understood, and accepted the terms of this disclaimer and assumes all risks associated with the use of this software.
