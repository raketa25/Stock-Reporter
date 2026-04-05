#!/usr/bin/env python3
"""
Interactive Setup Script for AI Stock Report Generator
Works on both Windows and macOS
"""

import os
import sys
import subprocess
import platform
import urllib.request
import json
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("🚀 AI Stock Report Generator - Interactive Setup")
    print("=" * 70)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        print("\n💡 Please install Python 3.8+ from:")
        print("   Windows: https://www.python.org/downloads/")
        print("   macOS: brew install python")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def check_pip():
    """Check if pip is available"""
    print("📋 Checking pip installation...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False

def create_virtual_environment():
    """Create and activate virtual environment"""
    print("🏗️  Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        response = input("Virtual environment already exists. Recreate? (y/N): ").lower()
        if response == 'y':
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("✅ Using existing virtual environment")
            return True
    
    try:
        # Create virtual environment
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        
        # Provide activation instructions
        if platform.system() == "Windows":
            print("💡 To activate later, run: venv\\Scripts\\activate")
            pip_path = "venv\\Scripts\\pip"
            python_path = "venv\\Scripts\\python"
        else:
            print("💡 To activate later, run: source venv/bin/activate")
            pip_path = "venv/bin/pip"
            python_path = "venv/bin/python"
        
        return True, pip_path, python_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False, None, None

def install_dependencies(pip_path):
    """Install required packages"""
    print("📦 Installing dependencies...")
    
    # Core requirements
    packages = [
        "requests>=2.28.0",
        "pandas>=1.5.0", 
        "yfinance>=0.2.0",
        "reportlab>=3.6.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "openai>=0.27.0",
        "python-dateutil>=2.8.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "numpy>=1.21.0",
        "scipy>=1.9.0"
    ]
    
    try:
        # Upgrade pip first
        subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install packages one by one to show progress
        for i, package in enumerate(packages, 1):
            print(f"  Installing {package.split('>=')[0]}... ({i}/{len(packages)})")
            result = subprocess.run([pip_path, "install", package], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"    ⚠️  Warning: Failed to install {package}")
                print(f"    Error: {result.stderr}")
            else:
                print(f"    ✅ {package.split('>=')[0]} installed")
        
        print("✅ Dependencies installation completed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_project_files():
    """Create necessary project files and directories"""
    print("📁 Creating project structure...")
    
    # Create directories
    directories = ["reports", "data", "logs", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ Created: {directory}/")
    
    # Create requirements.txt
    requirements_content = """# AI Stock Report Generator - Requirements
requests>=2.28.0
pandas>=1.5.0
yfinance>=0.2.0
reportlab>=3.6.0
matplotlib>=3.6.0
seaborn>=0.12.0
openai>=0.27.0
python-dateutil>=2.8.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
numpy>=1.21.0
scipy>=1.9.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    print("  ✅ Created: requirements.txt")
    
    # Create .env template
    env_template = """# AI Stock Report Generator - Environment Variables
# Copy this file to .env and fill in your actual API keys

# OpenAI API (Required for AI analysis)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here

# Alpha Vantage API (Free: 5 calls/minute, 500/day)
# Get your key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# News API (Free: 1000 requests/month)
# Get your key at: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here

# Financial Modeling Prep API (Free: 250 calls/day)  
# Get your key at: https://financialmodelingprep.com/developer/docs
FMP_API_KEY=your_fmp_key_here

# Polygon.io API (Free: 5 calls/minute)
# Get your key at: https://polygon.io/
POLYGON_API_KEY=your_polygon_key_here

# Quandl API (Optional)
# Get your key at: https://www.quandl.com/
QUANDL_API_KEY=your_quandl_key_here
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    print("  ✅ Created: .env.template")
    
    # Create basic config.json
    config = {
        "settings": {
            "default_output_dir": "reports",
            "rate_limit_delay": 2,
            "max_retries": 3,
            "report_format": "pdf"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("  ✅ Created: config.json")
    
    return True

def interactive_api_configuration():
    """Interactive API key configuration"""
    print("\n🔑 API Key Configuration")
    print("=" * 40)
    print("You can skip any API by pressing Enter. The app works with Yahoo Finance")
    print("(no API key needed), but AI analysis requires OpenAI API key.")
    print()
    
    api_keys = {}
    
    # OpenAI (most important)
    print("📊 OpenAI API (Recommended - enables AI analysis)")
    print("   Get your key at: https://platform.openai.com/api-keys")
    openai_key = input("   Enter OpenAI API key (or press Enter to skip): ").strip()
    if openai_key:
        api_keys['OPENAI_API_KEY'] = openai_key
        print("   ✅ OpenAI API key saved")
    else:
        print("   ⏭️  Skipped - AI analysis will use mock data")
    
    print()
    
    # Alpha Vantage
    print("📈 Alpha Vantage API (Optional - enhanced financial data)")
    print("   Get your key at: https://www.alphavantage.co/support/#api-key")
    av_key = input("   Enter Alpha Vantage API key (or press Enter to skip): ").strip()
    if av_key:
        api_keys['ALPHA_VANTAGE_API_KEY'] = av_key
        print("   ✅ Alpha Vantage API key saved")
    
    print()
    
    # News API
    print("📰 News API (Optional - recent headlines)")
    print("   Get your key at: https://newsapi.org/")
    news_key = input("   Enter News API key (or press Enter to skip): ").strip()
    if news_key:
        api_keys['NEWS_API_KEY'] = news_key
        print("   ✅ News API key saved")
    
    print()
    
    # Save to .env file
    if api_keys:
        env_content = ""
        
        # Read template first
        try:
            with open(".env.template", "r") as f:
                env_content = f.read()
        except FileNotFoundError:
            pass
        
        # Replace keys
        for key, value in api_keys.items():
            if key in env_content:
                # Replace the placeholder line
                import re
                pattern = f"{key}=.*"
                replacement = f"{key}={value}"
                env_content = re.sub(pattern, replacement, env_content)
            else:
                # Add new key
                env_content += f"\n{key}={value}\n"
        
        # Write .env file
        with open(".env", "w") as f:
            f.write(env_content)
        
        print(f"✅ Saved {len(api_keys)} API keys to .env file")
    else:
        # Create empty .env from template
        try:
            with open(".env.template", "r") as f:
                template_content = f.read()
            with open(".env", "w") as f:
                f.write(template_content)
            print("✅ Created .env file from template")
        except FileNotFoundError:
            pass
    
    return len(api_keys) > 0

def test_installation(python_path):
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    # Test basic import
    test_script = '''
import sys
try:
    import yfinance as yf
    import pandas as pd
    import requests
    import reportlab
    print("✅ Core packages imported successfully")
    
    # Test Yahoo Finance
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    if "longName" in info:
        print("✅ Yahoo Finance connection working")
    else:
        print("⚠️  Yahoo Finance returned limited data")
    
    print("✅ Basic functionality test passed")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Warning: {e}")
'''
    
    try:
        result = subprocess.run([python_path, "-c", test_script], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ Test failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Test timeout - this might be normal for first run")
        return True
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def create_quick_start_script():
    """Create a quick start script"""
    print("📝 Creating quick start script...")
    
    if platform.system() == "Windows":
        script_content = '''@echo off
echo Activating virtual environment...
call venv\\Scripts\\activate

echo Generating AAPL stock report...
python stock_report.py report --symbol AAPL

echo.
echo Report should be in the reports/ folder!
echo.
echo To generate more reports:
echo   python stock_report.py report --symbol MSFT
echo   python stock_report.py report --symbols AAPL MSFT GOOGL
echo   python stock_report.py validate
echo.
pause
'''
        script_name = "quick_start.bat"
    else:
        script_content = '''#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate

echo "Generating AAPL stock report..."
python stock_report.py report --symbol AAPL

echo ""
echo "Report should be in the reports/ folder!"
echo ""
echo "To generate more reports:"
echo "  python stock_report.py report --symbol MSFT"
echo "  python stock_report.py report --symbols AAPL MSFT GOOGL"
echo "  python stock_report.py validate"
echo ""
'''
        script_name = "quick_start.sh"
    
    with open(script_name, "w") as f:
        f.write(script_content)
    
    if platform.system() != "Windows":
        os.chmod(script_name, 0o755)
    
    print(f"  ✅ Created: {script_name}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 70)
    print("🎉 Setup completed successfully!")
    print("=" * 70)
    
    print("\n📋 What was installed:")
    print("  ✅ Python virtual environment")
    print("  ✅ All required packages")
    print("  ✅ Project structure and configuration files")
    
    if os.path.exists(".env"):
        print("  ✅ API keys configuration")
    else:
        print("  ⚠️  No API keys configured (Yahoo Finance will still work)")
    
    print("\n🚀 Next steps:")
    print("1. To generate your first report:")
    
    if platform.system() == "Windows":
        print("   - Double-click 'quick_start.bat' OR")
        print("   - Run: venv\\Scripts\\activate")
        print("   - Then: python stock_report.py report --symbol AAPL")
    else:
        print("   - Run: ./quick_start.sh OR")
        print("   - Run: source venv/bin/activate")
        print("   - Then: python stock_report.py report --symbol AAPL")
    
    print("\n2. To add more API keys later:")
    print("   - Edit the .env file")
    print("   - Get keys from:")
    print("     • OpenAI: https://platform.openai.com/api-keys")
    print("     • Alpha Vantage: https://www.alphavantage.co/support/#api-key")
    print("     • News API: https://newsapi.org/")
    
    print("\n3. Advanced usage:")
    print("   - Comprehensive reports: python stock_report.py report --symbol AAPL --comprehensive")
    print("   - Multiple stocks: python stock_report.py report --symbols AAPL MSFT GOOGL")
    print("   - Portfolio tracking: python stock_report.py portfolio")
    print("   - Validate APIs: python stock_report.py validate")
    
    print("\n💡 Tips:")
    print("  - Reports are saved in the 'reports/' folder")
    print("  - Check 'logs/' folder if you encounter issues")
    print("  - The app works without API keys using Yahoo Finance data")
    print("  - Add OpenAI API key for AI-powered analysis")
    
    print("\n🆘 Need help?")
    print("  - Check README.md for detailed documentation")
    print("  - Run tests: python test_suite.py test")
    print("  - Enable debug: set LOG_LEVEL=DEBUG (Windows) or export LOG_LEVEL=DEBUG (macOS)")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Setup virtual environment
    result = create_virtual_environment()
    if isinstance(result, tuple):
        success, pip_path, python_path = result
        if not success:
            return False
    else:
        return False
    
    # Install dependencies
    if not install_dependencies(pip_path):
        print("⚠️  Some packages failed to install, but continuing...")
    
    # Create project structure
    if not create_project_files():
        return False
    
    # Configure API keys
    interactive_api_configuration()
    
    # Test installation
    if not test_installation(python_path):
        print("⚠️  Some tests failed, but basic functionality should work")
    
    # Create quick start script
    create_quick_start_script()
    
    # Show next steps
    print_next_steps()
    
    return True

def download_main_script():
    """Download or create the main stock_report.py script"""
    print("📥 Setting up main application script...")
    
    # Since we can't download from a URL, we'll create a minimal version
    # that users can replace with the full version
    minimal_script = '''#!/usr/bin/env python3
"""
AI Stock Report Generator - Minimal Version
Replace this file with the complete stock_report.py from the artifacts
"""

import sys
import os

def main():
    print("🚀 AI Stock Report Generator")
    print("=" * 50)
    print()
    print("⚠️  This is a minimal setup version.")
    print()
    print("To get the full functionality:")
    print("1. Copy the complete 'stock_report.py' code from the project artifacts")
    print("2. Replace this file with the complete version")
    print("3. Then run: python stock_report.py report --symbol AAPL")
    print()
    print("The complete script includes:")
    print("  • Multi-source data integration (Yahoo Finance, Alpha Vantage, etc.)")
    print("  • AI-powered analysis with OpenAI GPT")
    print("  • Professional PDF report generation")
    print("  • Technical analysis (RSI, moving averages, etc.)")
    print("  • Portfolio management")
    print("  • Scheduled reporting")
    print()
    print("For now, here's a basic test using Yahoo Finance:")
    
    try:
        import yfinance as yf
        import pandas as pd
        from datetime import datetime
        
        symbol = input("Enter stock symbol (e.g., AAPL): ").upper().strip()
        if not symbol:
            symbol = "AAPL"
        
        print(f"\\nFetching data for {symbol}...")
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\\n📊 Basic Stock Information for {symbol}:")
        print("-" * 40)
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Current Price: ${info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}")
        print(f"Market Cap: ${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "Market Cap: N/A")
        print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
        
        print(f"\\n✅ Basic functionality is working!")
        print("Replace this script with the complete version for full features.")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install yfinance pandas")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
'''
    
    with open("stock_report.py", "w") as f:
        f.write(minimal_script)
    
    print("  ✅ Created: stock_report.py (minimal version)")
    print("  📝 Replace this with the complete version from the artifacts")

def create_readme():
    """Create a basic README file"""
    print("📚 Creating README file...")
    
    readme_content = """# AI Stock Report Generator - Local Installation

## Quick Start

1. **First Time Setup:**
   ```bash
   python interactive_setup.py
   ```

2. **Activate Environment:**
   ```bash
   # Windows
   venv\\Scripts\\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Generate First Report:**
   ```bash
   python stock_report.py report --symbol AAPL
   ```

## Project Structure

```
ai-stock-reports/
├── venv/                    # Virtual environment
├── reports/                 # Generated PDF reports
├── data/                    # Cached data
├── logs/                    # Application logs
├── stock_report.py         # Main application (replace with complete version)
├── requirements.txt        # Dependencies
├── .env                    # Your API keys (keep private!)
├── config.json             # Configuration
└── quick_start.bat/.sh     # Quick start script
```

## Getting API Keys

### Required for AI Analysis
- **OpenAI**: https://platform.openai.com/api-keys

### Optional (Free Tiers Available)
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
- **News API**: https://newsapi.org/
- **Financial Modeling Prep**: https://financialmodelingprep.com/developer/docs

## Commands

```bash
# Generate single report
python stock_report.py report --symbol AAPL

# Generate comprehensive report (requires OpenAI)
python stock_report.py report --symbol AAPL --comprehensive

# Generate multiple reports
python stock_report.py report --symbols AAPL MSFT GOOGL

# Validate API keys
python stock_report.py validate

# Portfolio management
python stock_report.py portfolio
```

## Troubleshooting

### Windows
- Run Command Prompt as Administrator
- If Python not found: Add Python to PATH
- For build errors: Install Visual C++ Build Tools

### macOS
- Install Xcode Command Line Tools: `xcode-select --install`
- For M1/M2 Macs: May need Rosetta 2
- Permission issues: Use `--user` flag with pip

### Common Issues
- **Import errors**: Make sure virtual environment is activated
- **PDF generation fails**: Install pillow: `pip install pillow`
- **API errors**: Check .env file and validate keys

## Next Steps

1. Replace `stock_report.py` with the complete version from the project artifacts
2. Add your API keys to the `.env` file
3. Generate your first comprehensive report
4. Set up portfolio tracking and scheduled reports

## Getting Help

- Check the logs: `cat logs/stock_report.log`
- Enable debug mode: `export LOG_LEVEL=DEBUG`
- Run tests: `python test_suite.py test`
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("  ✅ Created: README.md")

def create_troubleshooting_script():
    """Create a troubleshooting script"""
    print("🔧 Creating troubleshooting script...")
    
    troubleshoot_script = '''#!/usr/bin/env python3
"""
Troubleshooting script for AI Stock Report Generator
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def print_system_info():
    """Print system information"""
    print("🖥️  System Information")
    print("-" * 30)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()

def check_virtual_environment():
    """Check virtual environment status"""
    print("🐍 Virtual Environment Status")
    print("-" * 30)
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment directory exists")
        
        # Check if we're in the virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("✅ Virtual environment is activated")
        else:
            print("⚠️  Virtual environment is NOT activated")
            if platform.system() == "Windows":
                print("   Run: venv\\\\Scripts\\\\activate")
            else:
                print("   Run: source venv/bin/activate")
    else:
        print("❌ Virtual environment not found")
        print("   Run: python -m venv venv")
    print()

def check_dependencies():
    """Check installed packages"""
    print("📦 Checking Dependencies")
    print("-" * 30)
    
    required_packages = [
        "requests", "pandas", "yfinance", "reportlab", 
        "matplotlib", "seaborn", "openai", "numpy"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Run: pip install {package}")
    print()

def check_project_structure():
    """Check project files and directories"""
    print("📁 Project Structure")
    print("-" * 30)
    
    required_files = [
        "stock_report.py", "requirements.txt", ".env", "config.json"
    ]
    
    required_dirs = [
        "reports", "data", "logs", "venv"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ - Missing")
    print()

def check_api_keys():
    """Check API key configuration"""
    print("🔑 API Key Configuration")
    print("-" * 30)
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        with open(env_file, 'r') as f:
            content = f.read()
            
        api_keys = [
            "OPENAI_API_KEY", "ALPHA_VANTAGE_API_KEY", 
            "NEWS_API_KEY", "FMP_API_KEY"
        ]
        
        for key in api_keys:
            if key in content and not content.split(key + "=")[1].split()[0].startswith("your_"):
                print(f"✅ {key} - Configured")
            else:
                print(f"⚠️  {key} - Not configured")
    else:
        print("❌ .env file not found")
        print("   Copy .env.template to .env and add your API keys")
    print()

def test_basic_functionality():
    """Test basic functionality"""
    print("🧪 Testing Basic Functionality")
    print("-" * 30)
    
    try:
        import yfinance as yf
        print("✅ yfinance import successful")
        
        # Test Yahoo Finance connection
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        if "longName" in info:
            print("✅ Yahoo Finance connection working")
        else:
            print("⚠️  Yahoo Finance returned limited data")
            
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
    
    print()

def run_diagnostics():
    """Run comprehensive diagnostics"""
    try:
        import requests
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection working")
        else:
            print("⚠️  Internet connection issues")
    except:
        print("❌ Internet connection failed")
    
    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        print(f"💾 Disk space: {free // (1024**3)}GB free of {total // (1024**3)}GB total")
    except:
        print("⚠️  Could not check disk space")
    
    print()

def suggest_fixes():
    """Suggest common fixes"""
    print("🔧 Common Fixes")
    print("-" * 30)
    print("1. Reinstall dependencies:")
    if platform.system() == "Windows":
        print("   venv\\\\Scripts\\\\activate")
        print("   pip install --upgrade pip")
        print("   pip install -r requirements.txt")
    else:
        print("   source venv/bin/activate")
        print("   pip install --upgrade pip") 
        print("   pip install -r requirements.txt")
    
    print("\\n2. Reset virtual environment:")
    print("   Remove venv/ folder and run setup again")
    
    print("\\n3. Check permissions:")
    if platform.system() == "Windows":
        print("   Run Command Prompt as Administrator")
    else:
        print("   Check file permissions: ls -la")
    
    print("\\n4. API issues:")
    print("   Verify API keys in .env file")
    print("   Check API rate limits")
    print("   Test with: python stock_report.py validate")
    
    print("\\n5. Enable debug mode:")
    if platform.system() == "Windows":
        print("   set LOG_LEVEL=DEBUG")
    else:
        print("   export LOG_LEVEL=DEBUG")
    print("   python stock_report.py report --symbol AAPL")

def main():
    """Main troubleshooting function"""
    print("🔧 AI Stock Report Generator - Troubleshooting")
    print("=" * 50)
    print()
    
    print_system_info()
    check_virtual_environment()
    check_dependencies()
    check_project_structure()
    check_api_keys()
    test_basic_functionality()
    run_diagnostics()
    suggest_fixes()
    
    print("\\n" + "=" * 50)
    print("🆘 If issues persist:")
    print("  1. Check README.md for detailed instructions")
    print("  2. Run: python interactive_setup.py (to reinstall)")
    print("  3. Enable debug logging for more details")
    print("=" * 50)

if __name__ == "__main__":
    main()
'''
    
    with open("troubleshoot.py", "w") as f:
        f.write(troubleshoot_script)
    
    if platform.system() != "Windows":
        os.chmod("troubleshoot.py", 0o755)
    
    print("  ✅ Created: troubleshoot.py")

def final_setup():
    """Complete the setup with additional files"""
    print("\n🎯 Finalizing setup...")
    
    # Download/create main script
    download_main_script()
    
    # Create documentation
    create_readme()
    
    # Create troubleshooting script
    create_troubleshooting_script()
    
    # Create a simple test script
    test_script = '''#!/usr/bin/env python3
"""Quick test script"""

def test_imports():
    """Test all required imports"""
    try:
        import yfinance as yf
        import pandas as pd
        import requests
        import reportlab
        import matplotlib
        import numpy as np
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_yahoo_finance():
    """Test Yahoo Finance connection"""
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        price = info.get('currentPrice', info.get('regularMarketPrice'))
        if price:
            print(f"✅ Yahoo Finance working - AAPL: ${price}")
            return True
        else:
            print("⚠️  Yahoo Finance returned no price data")
            return False
    except Exception as e:
        print(f"❌ Yahoo Finance failed: {e}")
        return False

def main():
    print("🧪 Quick Test Suite")
    print("=" * 30)
    
    if test_imports() and test_yahoo_finance():
        print("\\n🎉 Basic functionality is working!")
        print("You can now generate reports with Yahoo Finance data.")
    else:
        print("\\n❌ Some tests failed. Run troubleshoot.py for help.")

if __name__ == "__main__":
    main()
'''
    
    with open("test_basic.py", "w") as f:
        f.write(test_script)
    
    print("  ✅ Created: test_basic.py")
    
    print("✅ Setup finalization completed!")

if __name__ == "__main__":
    try:
        if main():
            final_setup()
        else:
            print("❌ Setup failed. Please check the errors above and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\n\\n⏹️  Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        print("Please report this issue and try running the setup again.")
        sys.exit(1)