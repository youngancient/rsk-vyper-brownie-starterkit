"""
Verification script to test if the project setup is complete
Run this to verify all components are working correctly
"""

import subprocess
import sys
import os
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    path = Path(dirpath)
    if path.exists() and path.is_dir():
        print(f"✅ {description}: {dirpath}/")
        return True
    else:
        print(f"❌ {description}: {dirpath}/ - NOT FOUND")
        return False


def check_command(command, description):
    """Check if a command is available"""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {description}: {version}")
            return True
        else:
            print(f"❌ {description}: Command failed")
            return False
    except FileNotFoundError:
        print(f"❌ {description}: Not installed")
        return False
    except Exception as e:
        print(f"⚠️  {description}: Error checking - {e}")
        return False


def check_python_package(package, description):
    """Check if a Python package is installed"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = [line for line in result.stdout.split('\n') if line.startswith('Version:')]
            if version_line:
                version = version_line[0].split(':')[1].strip()
                print(f"✅ {description}: {package} (v{version})")
            else:
                print(f"✅ {description}: {package} (installed)")
            return True
        else:
            print(f"❌ {description}: {package} - NOT INSTALLED")
            return False
    except Exception as e:
        print(f"⚠️  {description}: Error checking - {e}")
        return False


def main():
    """Main verification function"""
    print("=" * 70)
    print("🔍 PROJECT SETUP VERIFICATION")
    print("=" * 70)
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    
    results = []
    
    print("\n📁 Checking Project Structure...")
    print("-" * 70)
    
    # Check directories
    results.append(check_directory_exists("contracts", "Contracts directory"))
    results.append(check_directory_exists("tests", "Tests directory"))
    results.append(check_directory_exists("scripts", "Scripts directory"))
    
    # Check contract files
    print("\n📄 Checking Contract Files...")
    print("-" * 70)
    results.append(check_file_exists("contracts/ERC20.vy", "ERC20 contract"))
    results.append(check_file_exists("contracts/Vault.vy", "Vault contract"))
    
    # Check test files
    print("\n🧪 Checking Test Files...")
    print("-" * 70)
    results.append(check_file_exists("tests/conftest.py", "Test fixtures"))
    results.append(check_file_exists("tests/test_erc20.py", "ERC20 tests"))
    results.append(check_file_exists("tests/test_vault.py", "Vault tests"))
    
    # Check script files
    print("\n📜 Checking Script Files...")
    print("-" * 70)
    results.append(check_file_exists("scripts/deploy.py", "Deploy script"))
    results.append(check_file_exists("scripts/verify.py", "Verify script"))
    results.append(check_file_exists("scripts/analyze.py", "Analyze script"))
    
    # Check configuration files
    print("\n⚙️  Checking Configuration Files...")
    print("-" * 70)
    results.append(check_file_exists("ape-config.yaml", "Ape config"))
    results.append(check_file_exists("requirements.txt", "Requirements file"))
    results.append(check_file_exists("pytest.ini", "Pytest config"))
    results.append(check_file_exists("replit.nix", "Replit Nix config"))
    results.append(check_file_exists(".replit", "Replit config"))
    results.append(check_file_exists(".gitignore", "Git ignore"))
    
    # Check documentation
    print("\n📚 Checking Documentation...")
    print("-" * 70)
    results.append(check_file_exists("README.md", "README"))
    results.append(check_file_exists("MIGRATION.md", "Migration guide"))
    results.append(check_file_exists("SECURITY.md", "Security docs"))
    
    # Check tools
    print("\n🛠️  Checking Installed Tools...")
    print("-" * 70)
    results.append(check_command(sys.executable, "Python"))
    results.append(check_command("pip", "pip"))
    
    # Check Python packages
    print("\n📦 Checking Python Packages...")
    print("-" * 70)
    results.append(check_python_package("eth-ape", "Ape framework"))
    results.append(check_python_package("vyper", "Vyper compiler"))
    results.append(check_python_package("pytest", "Pytest"))
    results.append(check_python_package("slither-analyzer", "Slither"))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"✅ Passed: {passed}/{total} ({percentage:.1f}%)")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED! Project setup is complete.")
        print("\n📋 Next Steps:")
        print("   1. Run: ape compile")
        print("   2. Run: ape test")
        print("   3. Run: ape run scripts/deploy --network rootstock-testnet")
    else:
        print("\n⚠️  SOME CHECKS FAILED. Please review the errors above.")
        print("\n📋 To fix:")
        print("   1. Install missing packages: pip install -r requirements.txt")
        print("   2. Verify all files are present")
        print("   3. Check file paths")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

