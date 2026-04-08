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
3. **Set environment variables** (if deploying):
   - `PRIVATE_KEY` - Your wallet private key
4. **Deploy**: Click "Deploy" button or run:
   ```bash
   ape run scripts/deploy --network rootstock-testnet
   ```

⚠️ **Educational only. Not audited. Do NOT deploy to mainnet without an external audit.**

### Local Setup:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rsk-vyper-brownie-starterkit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root with:
   ```bash
   # .env file content
   PRIVATE_KEY=your_private_key_here
   # WARNING: Public nodes have rate limits! Replace with dedicated RPCs for scale:
   RSK_TESTNET_RPC=https://public-node.testnet.rsk.co
   RSK_MAINNET_RPC=https://public-node.rsk.co
   ```
   **WARNING:** Never commit your `.env` file to version control!

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

### Environment Variables

Create a `.env` file following the `.env.example` (or set in Replit Secrets):

```env
PRIVATE_KEY=your_private_key_here
# WARNING: Public nodes have rate limits! Replace with dedicated RPCs for scale:
RSK_TESTNET_RPC=https://public-node.testnet.rsk.co
RSK_MAINNET_RPC=https://public-node.rsk.co
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
ape run scripts/deploy --network rootstock-testnet
```

### Deploy to Mainnet

```bash
ape run scripts/deploy --network rootstock-mainnet
```

Deployment addresses are actively captured within Ape's ecosystem tracking algorithms.

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
ape run scripts/<script_name> --network <network>
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

- **Testing:** The software has not undergone testing of any kind, and its functionality, accuracy, reliability, and suitability for any purpose are not guaranteed.
- **Use at Your Own Risk:** The user assumes all risks associated with the use of this software. The author(s) of this software shall not be held liable for any damages, including but not limited to direct, indirect, incidental, special, consequential, or punitive damages arising out of the use of or inability to use this software, even if advised of the possibility of such damages.
- **No Liability:** The author(s) of this software are not liable for any loss or damage, including without limitation, any loss of profits, business interruption, loss of information or data, or other pecuniary loss arising out of the use of or inability to use this software.
- **Sole Responsibility:** The user acknowledges that they are solely responsible for the outcome of the use of this software, including any decisions made or actions taken based on the software's output or functionality.
- **No Endorsement:** Mention of any specific product, service, or organization does not constitute or imply endorsement by the author(s) of this software.
- **Modification and Distribution:** This software may be modified and distributed under the terms of the license provided with the software. By modifying or distributing this software, you agree to be bound by the terms of the license.
- **Assumption of Risk:** By using this software, the user acknowledges and agrees that they have read, understood, and accepted the terms of this disclaimer and assumes all risks associated with the use of this software.
