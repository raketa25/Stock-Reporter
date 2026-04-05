# Stock-Reporter

This is a simple AI Stock Reporter with Python, Docker and more ...

# AI Stock Report Generator - Local Setup Guide

## 🖥️ Windows Setup Guide

### Prerequisites Check

First, verify you have the required software:

#### 1. Check Python Installation

```cmd
# Open Command Prompt (Windows key + R, type 'cmd', press Enter)
python --version
# Should show Python 3.8 or higher

# If Python is not installed, download from: https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation
```

#### 2. Check pip (Python package manager)

```cmd
pip --version
# Should show pip version
```

#### 3. Install Git (if not already installed)

- Download from: https://git-scm.com/download/win
- Use default installation options

### Step-by-Step Installation

#### 1. Create Project Directory

```cmd
# Open Command Prompt as Administrator (right-click cmd -> Run as administrator)
# Navigate to your desired directory (e.g., Desktop)
cd C:\Users\%USERNAME%\Desktop

# Create project folder
mkdir ai-stock-reports
cd ai-stock-reports
```

#### 2. Download Project Files

```cmd
# If you have the files in a zip, extract them here
# Otherwise, create the files manually by copying the code from the artifacts

# Create the main files:
# - Copy stock_report.py content to a new file
# - Copy requirements.txt content to a new file
# - Copy setup.py content to a new file
```

#### 3. Set Up Virtual Environment

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Your prompt should now show (venv) at the beginning
```

#### 4. Install Dependencies

```cmd
# Make sure virtual environment is activated (should see (venv) in prompt)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# If you get any errors, install packages individually:
pip install requests pandas yfinance reportlab matplotlib seaborn openai python-dateutil beautifulsoup4 lxml numpy scipy
```

#### 5. Run Setup Script

```cmd
python setup.py
```

#### 6. Configure API Keys

```cmd
# Copy the environment template
copy .env.template .env

# Edit the .env file with your API keys
# Use Notepad or any text editor:
notepad .env

# Add your API keys (at minimum, add an OpenAI key for AI analysis):
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
```

#### 7. Test Installation

```cmd
# Validate API configuration
python stock_report.py validate

# Generate your first report (works with Yahoo Finance, no API key needed)
python stock_report.py report --symbol AAPL

# Check if PDF was generated
dir reports
```

### Windows-Specific Troubleshooting

#### Issue: "python is not recognized"

**Solution:**

```cmd
# Add Python to PATH manually
# 1. Find Python installation directory (usually C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python3x)
# 2. Add to PATH:
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts
```

#### Issue: Permission denied errors

**Solution:**

```cmd
# Run Command Prompt as Administrator
# Right-click on Command Prompt -> "Run as administrator"
```

#### Issue: SSL certificate errors

**Solution:**

```cmd
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Issue: Microsoft Visual C++ build tools required

**Solution:**

- Download and install Microsoft Visual C++ Build Tools
- Or install Visual Studio Community (free)

---

## 🍎 macOS Setup Guide

### Prerequisites Check

#### 1. Check Python Installation

```bash
# Open Terminal (Command + Space, type 'Terminal', press Enter)
python3 --version
# Should show Python 3.8 or higher

# If not installed, install via Homebrew (recommended):
# First install Homebrew if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python:
brew install python
```

#### 2. Check pip

```bash
pip3 --version
```

#### 3. Install Git (usually pre-installed)

```bash
git --version
# If not installed: brew install git
```

### Step-by-Step Installation

#### 1. Create Project Directory

```bash
# Open Terminal
# Navigate to your desired directory
cd ~/Desktop

# Create project folder
mkdir ai-stock-reports
cd ai-stock-reports
```

#### 2. Download Project Files

```bash
# Create the necessary files
# You can use any text editor like nano, vim, or VS Code

# Create main Python file
nano stock_report.py
# Paste the stock_report.py content, then save (Ctrl+X, Y, Enter)

# Create requirements file
nano requirements.txt
# Paste the requirements.txt content, then save

# Create setup file
nano setup.py
# Paste the setup.py content, then save
```

#### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv stock-venv

# Activate virtual environment
source stock-venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

#### 4. Install Dependencies

```bash
# Make sure virtual environment is activated
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# If you encounter issues, try:
pip3 install -r requirements.txt

# For M1/M2 Macs, you might need:
pip install --no-deps -r requirements.txt
```

#### 5. Run Setup Script

```bash
python setup.py
```

#### 6. Configure API Keys

```bash
# Copy the environment template
cp .env.template .env

# Edit the .env file (using nano or your preferred editor)
nano .env

# Add your API keys:
# Press 'i' to enter insert mode in nano
# Add your keys, then press Esc, type ':wq', press Enter to save

# Or use VS Code if you have it:
code .env
```

#### 7. Test Installation

```bash
# Validate API configuration
python stock_report.py validate

# Generate your first report
python stock_report.py report --symbol AAPL

# Check if PDF was generated
ls -la reports/
```

### macOS-Specific Troubleshooting

#### Issue: Command Line Tools required

**Solution:**

```bash
xcode-select --install
```

#### Issue: Permission issues with pip

**Solution:**

```bash
# Use --user flag
pip install --user -r requirements.txt

# Or fix permissions:
sudo chown -R $(whoami) /usr/local/lib/python3.x/site-packages
```

#### Issue: M1/M2 Mac compatibility issues

**Solution:**

```bash
# Install Rosetta 2 if needed
softwareupdate --install-rosetta

# Use conda instead of pip for some packages
brew install miniconda
conda install numpy pandas matplotlib

# Then install remaining packages with pip
pip install -r requirements.txt
```

#### Issue: SSL certificate verification failed

**Solution:**

```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Or bypass SSL (temporary):
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## 🔑 Getting API Keys (Required for Full Functionality)

### 1. OpenAI API Key (Recommended - Required for AI Analysis)

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key and add to your `.env` file:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 2. Alpha Vantage API Key (Free - Enhanced Financial Data)

1. Go to https://www.alphavantage.co/support/#api-key
2. Enter your email and get free API key
3. Add to `.env`:
   ```
   ALPHA_VANTAGE_API_KEY=XXXXXXXXXXXXXXXX
   ```

### 3. News API Key (Free - Recent Headlines)

1. Go to https://newsapi.org/register
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `.env`:
   ```
   NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 4. Financial Modeling Prep (Optional - Additional Metrics)

1. Go to https://financialmodelingprep.com/developer/docs
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env`:
   ```
   FMP_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🚀 Quick Start Commands

Once everything is set up, you can use these commands:

### Basic Usage

```bash
# Windows
python stock_report.py report --symbol AAPL

# macOS
python stock_report.py report --symbol AAPL
```

### Advanced Usage

```bash
# Generate comprehensive report
python stock_report.py report --symbol AAPL --comprehensive

# Generate multiple reports
python stock_report.py report --symbols AAPL MSFT GOOGL

# Validate your API keys
python stock_report.py validate

# Portfolio management
python stock_report.py portfolio
```

---

## 📁 Project Structure After Setup

```
ai-stock-reports/
├── venv/                     # Virtual environment
├── reports/                  # Generated PDF reports
├── data/                     # Cached data
├── logs/                     # Application logs
├── stock_report.py           # Main application
├── requirements.txt          # Dependencies
├── setup.py                  # Setup script
├── .env                      # Your API keys (keep private!)
├── .env.template             # Template for API keys
├── config.json               # Application configuration
└── README.md                 # Documentation
```

---

## 🎯 Testing Your Setup

### 1. Basic Test (No API Keys Required)

```bash
# This should work immediately using Yahoo Finance
python stock_report.py report --symbol AAPL
```

### 2. API Key Validation

```bash
# Check which APIs are working
python stock_report.py validate
```

### 3. Comprehensive Test (Requires OpenAI API Key)

```bash
# Generate full report with AI analysis
python stock_report.py report --symbol AAPL --comprehensive
```

---

## 🔧 Common Issues and Solutions

### Issue: Import errors

**Windows:**

```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall problematic packages
pip uninstall reportlab
pip install reportlab
```

**macOS:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall problematic packages
pip uninstall reportlab
pip install reportlab
```

### Issue: PDF generation fails

**Solution for both platforms:**

```bash
# Install additional dependencies
pip install pillow

# For macOS, might need:
brew install freetype
```

### Issue: Memory errors during report generation

**Solution:**

```bash
# Reduce batch size or add swap space
# Check available memory:

# Windows:
wmic computersystem get TotalPhysicalMemory

# macOS:
sysctl hw.memsize
```

---

## 📞 Getting Help

### Check Logs

**Windows:**

```cmd
type logs\stock_report.log
```

**macOS:**

```bash
cat logs/stock_report.log
```

### Enable Debug Mode

```bash
# Set environment variable for detailed logging
# Windows:
set LOG_LEVEL=DEBUG

# macOS:
export LOG_LEVEL=DEBUG

# Then run your command
python stock_report.py report --symbol AAPL
```

### Community Support

- Check the README.md for detailed documentation
- Run the test suite: `python test_suite.py test`
- Validate your setup: `python stock_report.py validate`

---

## 🎉 Next Steps

Once you have everything working:

1. **Generate your first comprehensive report:**

   ```bash
   python stock_report.py report --symbol AAPL --comprehensive
   ```

2. **Set up portfolio tracking:**

   ```python
   # Add stocks to your portfolio
   python -c "
   from stock_report import EnhancedStockReportApp
   app = EnhancedStockReportApp()
   app.portfolio_manager.add_stock('AAPL', 100, 150.00)
   app.portfolio_manager.add_stock('MSFT', 50, 300.00)
   print('Portfolio updated!')
   "
   ```

3. **Schedule monthly reports:**

   ```bash
   python stock_report.py schedule --symbol AAPL --frequency monthly
   ```

4. **Explore batch processing:**
   ```bash
   python stock_report.py report --symbols AAPL MSFT GOOGL AMZN TSLA
   ```

You're now ready to generate professional stock reports with AI-powered insights! 🚀
