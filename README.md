# Vyper + Brownie Starter Kit on Replit

The only zero-setup Vyper + Brownie environment on Replit. Compile, test, and deploy Vyper contracts to Rootstock testnet entirely in the browser.

## 🎯 Features

- ✅ **Brownie + Vyper pre-installed** via Replit Nix
- ✅ **Rootstock testnet/mainnet** networks configured
- ✅ **Example contracts** with security features:
  - `ERC20.vy` - ERC20 token with zero-address validation & safe allowance functions
  - `Vault.vy` - Vault with inflation attack protection (virtual shares)
- ✅ **Comprehensive test suite** using Pytest
- ✅ **Slither static analysis** integration
- ✅ **One-click deploy & verify** scripts
- ✅ **Solidity → Vyper migration** cheat-sheet

## 📋 Prerequisites

### For Replit:
- No setup needed! Everything is pre-configured via `replit.nix`

### For Local Development:
- Python 3.8+ (Python 3.10 recommended)
- pip (Python package manager)

## 🚀 Quick Start

### On Replit:

1. **Fork this Repl** or create a new one from this template
2. **Click "Run"** - Brownie will compile the contracts
3. **Set environment variables** (if deploying):
   - `PRIVATE_KEY` - Your wallet private key
4. **Deploy**: Click "Deploy" button or run:
   ```bash
   brownie run scripts/deploy --network rootstock-testnet
   ```

### Local Setup:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vyper
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
   RSK_TESTNET_RPC=https://public-node.testnet.rsk.co
   RSK_MAINNET_RPC=https://public-node.rsk.co
   ```
   **WARNING:** Never commit your `.env` file to version control!

4. **Compile contracts:**
   ```bash
   brownie compile
   ```

5. **Register networks (first time only):**
   ```bash
   brownie networks add Ethereum rootstock-testnet host=https://public-node.testnet.rsk.co chainid=31
   brownie networks add Ethereum rootstock-mainnet host=https://public-node.rsk.co chainid=30
   ```

6. **Run tests:**
   ```bash
   brownie test
   ```

## 📁 Project Structure

```
.
├── contracts/              # Vyper contracts
│   ├── ERC20.vy           # ERC20 token implementation
│   └── Vault.vy           # Vault contract
├── scripts/               # Deployment scripts
│   ├── deploy.py          # Deploy contracts
│   ├── verify.py          # Verify contracts
│   ├── setup_networks.py  # Setup Rootstock 
├── tests/                 # Test files
│   ├── conftest.py        # Pytest fixtures
│   ├── test_erc20.py      # ERC20 tests
│   └── test_vault.py      # Vault tests
├── brownie-config.yaml    # Brownie config
├── .gitignore             
├── .env.example           # sample for .env
├── requirements.txt       # Python dependencies
├── replit.nix             # Replit Nix config
├── .replit                # Replit run config
├── pytest.ini             # Pytest config
├── SECURITY.md            # Security docs
├── MIGRATION.md           # Solidity → Vyper cheat-sheet
└── README.md              # This file
```

## 🔧 Configuration

### Brownie Configuration

Networks are configured in `brownie-config.yaml`:

- **Rootstock Testnet**: Chain ID 31
- **Rootstock Mainnet**: Chain ID 30

**First-time setup — Register networks with Brownie:**
```bash
brownie networks add Ethereum rootstock-testnet host=https://public-node.testnet.rsk.co chainid=31
brownie networks add Ethereum rootstock-mainnet host=https://public-node.rsk.co chainid=30
```

### Environment Variables

Create a `.env` file following the `.env.example` (or set in Replit Secrets):

```env
PRIVATE_KEY=your_private_key_here
RSK_TESTNET_RPC=https://public-node.testnet.rsk.co
RSK_MAINNET_RPC=https://public-node.rsk.co
```

## 📝 Contracts

### ERC20.vy

Standard ERC20 token implementation with:
- Full ERC20 interface compliance
- Checked arithmetic (automatic overflow/underflow protection)
- Transfer, approve, and transferFrom functions
- Events for all state changes

**Deployment Parameters:**
- Name: "Rootstock Starter Token"
- Symbol: "RST"
- Decimals: 18
- Initial Supply: 10,000,000 RST

### Vault.vy

Simple deposit/withdraw vault with:
- ERC20 token deposit functionality
- Share-based withdrawal system
- Proportional share calculation
- Owner access control
- Emergency withdraw function

**Features:**
- First deposit: 1:1 share ratio
- Subsequent deposits: Proportional to existing shares
- Withdraw by burning shares
- Owner can emergency withdraw

## 🧪 Testing

### Run All Tests

```bash
brownie test
```

### Run Specific Test File

```bash
brownie test tests/test_erc20.py
brownie test tests/test_vault.py
```

### Run with Coverage

```bash
brownie test --coverage
```

### Test Markers

```bash
# Run only unit tests
brownie test -m unit

# Run only integration tests
brownie test -m integration
```

## 🔒 Security Analysis

### Run Security Analysis

```bash
python scripts/analyze.py
```

This will:
1. Compile contracts with Vyper compiler (strict checks)
2. Run Slither static analysis (with Vyper limitations noted)

### Manual Security Review

See `SECURITY.md` for:
- Security checklist
- Known limitations
- Best practices
- Slither limitations with Vyper

**Note:** Slither has limited Vyper support. Always use:
- Vyper compiler's built-in strict checks
- Manual security review
- External audits for production

## 🚀 Deployment

### Setup Networks (First Time)

```bash
brownie run scripts/setup_networks
```

### Deploy to Testnet

```bash
brownie run scripts/deploy --network rootstock-testnet
```

### Deploy to Mainnet

```bash
brownie run scripts/deploy --network rootstock-mainnet
```

Deployment addresses are saved to `deployments/<network>.json`

### Verify Contracts

```bash
brownie run scripts/verify --network rootstock-testnet
```

**Note:** Automatic verification may require manual steps. See `scripts/verify.py` for instructions.

## 📚 Documentation

### Migration Guide

See `MIGRATION.md` for a comprehensive Solidity → Vyper migration cheat-sheet.

### Security

See `SECURITY.md` for security best practices and analysis tools.

## 🛠️ Development

### Compile Contracts

```bash
brownie compile
```

### Open Brownie Console

```bash
brownie console
```

### Run Scripts

```bash
brownie run scripts/<script_name> --network <network>
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

## 📦 Dependencies

- **eth-brownie** ==1.20.0 - Development framework
- **vyper** ==0.3.10 - Vyper compiler
- **pytest** ==4.1.0 - Testing framework
- **slither-analyzer** ==0.9.6 - Static analysis
- **python-dotenv** ==0.16.0 - Environment variables

## 🐛 Troubleshooting

### Compilation Errors

```bash
# Clear Brownie cache
brownie compile --all
```

### Network Connection Issues

- Check RPC endpoint in `brownie-config.yaml`
- Verify network is accessible
- Try alternative RPC endpoints

### Test Failures

```bash
# Run tests with verbose output
brownie test -v

# Run specific test
brownie test -k test_name
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Brownie Documentation](https://eth-brownie.readthedocs.io/)
- [Rootstock Documentation](https://developers.rsk.co/)
- [Replit Documentation](https://docs.replit.com/)

## ⚠️ Disclaimer

This is a starter kit for educational purposes. Always:
- Audit contracts before mainnet deployment
- Test thoroughly on testnets
- Follow security best practices
- Get professional security reviews

## 🙏 Acknowledgments

- Rootstock team for network support
- Vyper community
- Brownie framework developers

---

**Happy Building on Rootstock! 🚀**

