# 🚀 AI Stock Report Generator - Complete Setup Instructions

## 📋 What You'll Get After Setup

✅ **Professional PDF Stock Reports** with:

- Executive summary and key metrics (P/E, Market Cap, EPS)
- AI-powered analysis and recommendations
- Technical indicators (RSI, Moving Averages)
- Recent news and competitive analysis
- Performance charts and risk assessment

✅ **Multiple Data Sources**:

- Yahoo Finance (free, no API key needed)
- Alpha Vantage, News API, OpenAI (free tiers available)
- Financial Modeling Prep, Polygon.io (optional)

✅ **Advanced Features**:

- Portfolio tracking and performance reports
- Scheduled automated reports
- Batch processing for multiple stocks
- Command-line interface

---

## 🖥️ WINDOWS SETUP (5 Minutes)

### Step 1: Download and Install Python

1. Go to https://python.org/downloads/
2. Download Python 3.11 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

### Step 2: Create Project Folder

```cmd
# Open Command Prompt (Windows key + R, type 'cmd', press Enter)
cd Desktop
mkdir ai-stock-reports
cd ai-stock-reports
```

### Step 3: Copy Project Files

**Create these files in your `ai-stock-reports` folder:**

#### File 1: `interactive_setup.py`

```python
# Copy the entire interactive_setup.py
# Save as: interactive_setup.py
```

#### File 2: `requirements.txt`

```txt
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
```

#### File 3: `stock_report.py`

```python
# set the entire stock_report.py code in the same path
# This is the 2000+ line main application
# Save as: stock_report.py
```

### Step 4: Run Automated Setup

```cmd
python interactive_setup.py
```

### Step 5: First Test

```cmd
# Activate virtual environment
venv\Scripts\activate

# Generate your first report
python stock_report.py report --symbol AAPL

# Check if PDF was created
dir reports
```

---

## 🍎 macOS SETUP (5 Minutes)

### Step 1: Install Prerequisites

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Verify installation
python3 --version
```

### Step 2: Create Project Folder

```bash
# Open Terminal (Command + Space, type 'Terminal')
cd ~/Desktop
mkdir ai-stock-reports
cd ai-stock-reports
```

### Step 3: Copy Project Files

**Create these files in your `ai-stock-reports` folder:**

#### Using nano editor:

```bash
# Create setup script
nano interactive_setup.py
# Paste the interactive_setup.py code, then press Ctrl+X, Y, Enter

# Create requirements
nano requirements.txt
# Paste the requirements.txt content, then save

# Create main application
nano stock_report.py
# Paste the stock_report.py code, then save
```

#### Or using VS Code (if installed):

```bash
code interactive_setup.py    # Paste content and save
code requirements.txt        # Paste content and save
code stock_report.py         # Paste content and save
```

### Step 4: Run Automated Setup

```bash
python3 interactive_setup.py
```

### Step 5: First Test

```bash
# Activate virtual environment
source venv/bin/activate

# Generate your first report
python stock_report.py report --symbol AAPL

# Check if PDF was created
ls -la reports/
```

---

## 🔑 API KEYS SETUP (Optional but Recommended)

### Free API Keys (Recommended):

#### 1. OpenAI API (For AI Analysis) - $5 free credit

1. Go to https://platform.openai.com/api-keys
2. Sign up/login and create API key
3. Add to `.env` file:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### 2. Alpha Vantage (Enhanced Data) - Free

1. Go to https://www.alphavantage.co/support/#api-key
2. Enter email to get free key
3. Add to `.env` file:
   ```
   ALPHA_VANTAGE_API_KEY=XXXXXXXXXXXXXXXX
   ```

#### 3. News API (Headlines) - Free

1. Go to https://newsapi.org/register
2. Sign up for free account
3. Add to `.env` file:
   ```
   NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🚀 USAGE EXAMPLES

### Basic Commands

```bash
# Windows: venv\Scripts\activate
# macOS: source venv/bin/activate

# Generate single report
python stock_report.py report --symbol AAPL

# Generate comprehensive report (needs OpenAI API)
python stock_report.py report --symbol AAPL --comprehensive

# Generate multiple reports
python stock_report.py report --symbols AAPL MSFT GOOGL AMZN TSLA

# Validate your API keys
python stock_report.py validate

# Portfolio management
python stock_report.py portfolio
```

### Advanced Features

```python
# Python API usage
from stock_report import EnhancedStockReportApp

app = EnhancedStockReportApp()

# Add stocks to portfolio
app.portfolio_manager.add_stock('AAPL', 100, 150.00)
app.portfolio_manager.add_stock('MSFT', 50, 300.00)

# Generate portfolio report
portfolio_report = app.portfolio_manager.generate_portfolio_report()

# Schedule monthly reports
app.scheduler.add_scheduled_report('AAPL', 'monthly', 'your@email.com')
```

---

## 🔧 TROUBLESHOOTING

### Windows Issues:

#### "python is not recognized"

```cmd
# Check if Python is in PATH
where python

# If not found, add manually:
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts
```

#### Permission denied

```cmd
# Run as Administrator
# Right-click Command Prompt -> "Run as administrator"
```

#### SSL certificate errors

```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### macOS Issues:

#### Permission issues

```bash
# Use --user flag
pip install --user -r requirements.txt

# Or fix permissions
sudo chown -R $(whoami) /usr/local/lib/python3.x/site-packages
```

#### M1/M2 Mac issues

```bash
# Install Rosetta 2
softwareupdate --install-rosetta

# Use conda for some packages
brew install miniconda
conda install numpy pandas matplotlib
pip install -r requirements.txt
```

#### Command Line Tools missing

```bash
xcode-select --install
```

---

## 📊 SAMPLE REPORT OUTPUT

After running `python stock_report.py report --symbol AAPL --comprehensive`, you'll get a PDF with:

```
Apple Inc. (AAPL) - Comprehensive Stock Analysis Report
Generated on December 08, 2024

EXECUTIVE SUMMARY
Apple Inc. is currently trading at $185.25, showing a +1.34% change.
The company operates in the Technology sector with a market
capitalization of $2.85 trillion.

KEY FINANCIAL METRICS
┌─────────────────┬──────────────┐
│ Current Price   │ $185.25     │
│ Market Cap      │ $2.85T      │
│ P/E Ratio       │ 28.5        │
│ EPS             │ $6.50       │
│ Dividend Yield  │ 0.52%       │
│ 52-Week High    │ $199.62     │
│ 52-Week Low     │ $164.08     │
└─────────────────┴──────────────┘

TECHNICAL ANALYSIS
• RSI (14-day): 65.2 - Neutral
• Moving Averages:
  - 20-day SMA: $182.45
  - 50-day SMA: $178.90
  - 200-day SMA: $171.25

RECENT NEWS & DEVELOPMENTS
• Apple reports strong quarterly earnings beat expectations
• New product launch drives investor confidence
• Strategic partnership announced with major corporation

AI-POWERED ANALYSIS
Investment Thesis: Apple demonstrates positive momentum with
current trading indicating reasonable valuation relative to
sector peers. The company's position in the Technology sector
provides both opportunities and challenges...

[Detailed analysis continues...]
```

---

## 🎯 QUICK START CHECKLIST

- [ ] Python 3.8+ installed with PATH configured
- [ ] Project folder created with all 3 main files
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] At least one API key configured (OpenAI recommended)
- [ ] First report generated successfully
- [ ] PDF found in `reports/` folder

---

## 💡 PRO TIPS

1. **Start Simple**: Use Yahoo Finance data first (no API key needed)
2. **Add OpenAI**: For AI analysis, get OpenAI API key ($5 free credit)
3. **Batch Processing**: Generate reports for your entire portfolio at once
4. **Scheduling**: Set up monthly automated reports
5. **Portfolio Tracking**: Track your positions and performance over time

---

## 📞 GETTING HELP

### Run Diagnostics

```bash
# Check your setup
python troubleshoot.py

# Test basic functionality
python test_basic.py

# Enable debug mode
# Windows: set LOG_LEVEL=DEBUG
# macOS: export LOG_LEVEL=DEBUG
python stock_report.py report --symbol AAPL
```

### Check Logs

```bash
# View application logs
# Windows: type logs\stock_report.log
# macOS: cat logs/stock_report.log
```

### Common Solutions

1. **Import Errors**: Ensure virtual environment is activated
2. **API Errors**: Check `.env` file and run `python stock_report.py validate`
3. **PDF Issues**: Install pillow: `pip install pillow`
4. **Network Issues**: Check internet connection and firewall

---

## 🚀 YOU'RE READY!

Once setup is complete, you can:

- Generate professional stock reports in seconds
- Track your portfolio performance
- Get AI-powered investment insights
- Automate monthly reporting
- Scale to analyze hundreds of stocks

**Generate your first report now:**

```bash
python stock_report.py report --symbol AAPL --comprehensive
```

The PDF will be saved in the `reports/` folder! 📄✨
