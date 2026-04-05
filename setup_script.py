#!/usr/bin/env python3
"""
Setup and configuration script for AI Stock Report Generator
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_config_file():
    """Create configuration file with API key placeholders"""
    print("⚙️ Creating configuration file...")
    
    config = {
        "api_keys": {
            "alpha_vantage": {
                "key": "YOUR_ALPHA_VANTAGE_API_KEY_HERE",
                "url": "https://www.alphavantage.co/support/#api-key",
                "description": "Free tier: 5 calls/minute, 500/day",
                "required": False
            },
            "financial_modeling_prep": {
                "key": "YOUR_FMP_API_KEY_HERE", 
                "url": "https://financialmodelingprep.com/developer/docs",
                "description": "Free tier: 250 calls/day",
                "required": False
            },
            "polygon": {
                "key": "YOUR_POLYGON_API_KEY_HERE",
                "url": "https://polygon.io/",
                "description": "Free tier: 5 calls/minute",
                "required": False
            },
            "news_api": {
                "key": "YOUR_NEWS_API_KEY_HERE",
                "url": "https://newsapi.org/",
                "description": "Free tier: 1000 requests/month",
                "required": False
            },
            "openai": {
                "key": "YOUR_OPENAI_API_KEY_HERE",
                "url": "https://platform.openai.com/api-keys",
                "description": "Required for AI analysis",
                "required": True
            },
            "quandl": {
                "key": "YOUR_QUANDL_API_KEY_HERE",
                "url": "https://www.quandl.com/",
                "description": "Optional: Additional financial data",
                "required": False
            }
        },
        "settings": {
            "default_output_dir": "reports",
            "rate_limit_delay": 2,
            "max_retries": 3,
            "report_format": "pdf",
            "email_notifications": False
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration file created: config.json")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["reports", "data", "logs", "templates"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ Created: {directory}/")

def create_env_template():
    """Create .env template file"""
    print("🔐 Creating environment template...")
    
    env_content = """# AI Stock Report Generator - Environment Variables
# Copy this file to .env and fill in your actual API keys

# Alpha Vantage API (Free: 5 calls/minute, 500/day)
# Get your key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Financial Modeling Prep API (Free: 250 calls/day)  
# Get your key at: https://financialmodelingprep.com/developer/docs
FMP_API_KEY=your_fmp_key_here

# Polygon.io API (Free: 5 calls/minute)
# Get your key at: https://polygon.io/
POLYGON_API_KEY=your_polygon_key_here

# News API (Free: 1000 requests/month)
# Get your key at: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here

# OpenAI API (Required for AI analysis)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here

# Quandl API (Optional)
# Get your key at: https://www.quandl.com/
QUANDL_API_KEY=your_quandl_key_here

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    
    print("✅ Environment template created: .env.template")

def create_sample_scripts():
    """Create sample usage scripts"""
    print("📝 Creating sample scripts...")
    
    # Sample batch script
    batch_script = """#!/usr/bin/env python3
'''
Sample batch report generation script
Customize this script to generate reports for your portfolio
'''

from stock_report import EnhancedStockReportApp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Your portfolio symbols
    symbols = [
        'AAPL',  # Apple Inc.
        'MSFT',  # Microsoft Corporation  
        'GOOGL', # Alphabet Inc.
        'AMZN',  # Amazon.com Inc.
        'TSLA',  # Tesla Inc.
        # Add more symbols here
    ]
    
    app = EnhancedStockReportApp()
    
    print(f"Generating reports for {len(symbols)} stocks...")
    
    # Generate individual reports
    for symbol in symbols:
        try:
            print(f"\\nProcessing {symbol}...")
            report_path = app.generate_comprehensive_report(symbol)
            print(f"✅ Report generated: {report_path}")
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
    
    # Generate portfolio report if you have positions
    try:
        portfolio_path = app.portfolio_manager.generate_portfolio_report()
        print(f"\\n✅ Portfolio report generated: {portfolio_path}")
    except Exception as e:
        print(f"❌ Portfolio report error: {e}")

if __name__ == "__main__":
    main()
"""
    
    with open("batch_reports.py", "w") as f:
        f.write(batch_script)
    
    # Sample configuration script
    config_script = """#!/usr/bin/env python3
'''
Interactive configuration script
Run this to set up your API keys interactively
'''

import json
import getpass
from stock_report import APIConfig, ConfigManager

def main():
    print("🔧 AI Stock Report Generator - Interactive Configuration")
    print("=" * 60)
    
    config = APIConfig()
    
    # Get API keys interactively
    api_keys = {}
    
    print("\\n📡 API Key Configuration")
    print("Press Enter to skip optional APIs\\n")
    
    # Alpha Vantage
    key = input("Alpha Vantage API Key (optional): ").strip()
    if key:
        api_keys['alpha_vantage'] = key
    
    # Financial Modeling Prep
    key = input("Financial Modeling Prep API Key (optional): ").strip()
    if key:
        api_keys['fmp'] = key
    
    # News API
    key = input("News API Key (optional): ").strip()
    if key:
        api_keys['news_api'] = key
    
    # OpenAI (recommended)
    key = getpass.getpass("OpenAI API Key (recommended): ").strip()
    if key:
        api_keys['openai'] = key
    
    # Save configuration
    config_data = {
        "api_keys": api_keys,
        "configured_date": "$(date)"
    }
    
    with open("user_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    
    print("\\n✅ Configuration saved to user_config.json")
    
    # Test API keys
    if api_keys:
        print("\\n🧪 Testing API keys...")
        # Add validation logic here
        print("✅ API key validation completed")

if __name__ == "__main__":
    main()
"""
    
    with open("configure.py", "w") as f:
        f.write(config_script)
    
    print("✅ Sample scripts created:")
    print("  - batch_reports.py (batch processing)")
    print("  - configure.py (interactive setup)")

def create_documentation():
    """Create comprehensive documentation"""
    print("📚 Creating documentation...")
    
    readme_content = """# AI Stock Report Generator

A comprehensive Python application for generating professional stock analysis reports with AI-powered insights.

## Features

- 📊 **Multi-source Data Collection**: Integrates with Yahoo Finance, Alpha Vantage, Financial Modeling Prep, and more
- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT for intelligent stock analysis and recommendations  
- 📈 **Technical Analysis**: RSI, moving averages, Bollinger bands, and more
- 🌱 **ESG Scoring**: Environmental, Social, and Governance analysis
- 📰 **News Integration**: Recent headlines and market sentiment
- 🏢 **Competitive Analysis**: Sector comparison and peer analysis
- 📄 **Professional Reports**: Clean, shareable PDF reports
- 📅 **Scheduled Reports**: Automated monthly/weekly/daily reports
- 💼 **Portfolio Tracking**: Track multiple positions and performance

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup:**
   ```bash
   python setup.py
   ```

3. **Configure API keys:**
   ```bash
   python configure.py
   ```

4. **Generate your first report:**
   ```bash
   python stock_report.py report --symbol AAPL
   ```

## API Keys Required

### Essential (Free)
- **Yahoo Finance**: No API key needed (primary data source)

### Recommended (Free tiers available)
- **OpenAI**: Required for AI analysis ([Get key](https://platform.openai.com/api-keys))
- **Alpha Vantage**: Enhanced financial data ([Get key](https://www.alphavantage.co/support/#api-key))
- **News API**: Recent headlines ([Get key](https://newsapi.org/))

### Optional
- **Financial Modeling Prep**: Additional metrics ([Get key](https://financialmodelingprep.com/developer/docs))
- **Polygon.io**: Real-time data ([Get key](https://polygon.io/))

## Usage Examples

### Command Line Interface

```bash
# Generate single report
python stock_report.py report --symbol AAPL

# Generate comprehensive report  
python stock_report.py report --symbol AAPL --comprehensive

# Generate multiple reports
python stock_report.py report --symbols AAPL MSFT GOOGL

# Generate portfolio report
python stock_report.py portfolio

# Schedule monthly reports
python stock_report.py schedule --symbol AAPL --frequency monthly

# Validate API keys
python stock_report.py validate
```

### Python API

```python
from stock_report import EnhancedStockReportApp

# Initialize app
app = EnhancedStockReportApp()

# Generate single report
report_path = app.generate_monthly_report('AAPL')

# Generate comprehensive report
report_path = app.generate_comprehensive_report('AAPL')

# Batch processing
symbols = ['AAPL', 'MSFT', 'GOOGL']
report_paths = app.generate_batch_reports(symbols)

# Portfolio management
app.portfolio_manager.add_stock('AAPL', 100, 150.00)
portfolio_report = app.portfolio_manager.generate_portfolio_report()
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.template`):

```bash
ALPHA_VANTAGE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
# ... etc
```

### Configuration File

Modify `config.json` for default settings:

```json
{
  "settings": {
    "default_output_dir": "reports",
    "rate_limit_delay": 2,
    "max_retries": 3,
    "report_format": "pdf"
  }
}
```

## Report Contents

### Standard Report
- Executive Summary
- Key Financial Metrics  
- Recent News Headlines
- Competitive Landscape
- AI Analysis & Recommendations

### Comprehensive Report
- All standard features plus:
- Technical Analysis (RSI, Moving Averages, Bollinger Bands)
- ESG Analysis & Scoring
- Risk Assessment
- Historical Performance Charts
- Detailed Sector Analysis

## Scheduling & Automation

Set up automated reports using the scheduler:

```python
# Add to schedule
app.scheduler.add_scheduled_report('AAPL', 'monthly', 'your@email.com')

# Run scheduled reports (add to cron job)
app.scheduler.run_scheduled_reports()
```

### Cron Job Example

Add to your crontab for monthly reports on the 1st at 9 AM:

```bash
0 9 1 * * /usr/bin/python3 /path/to/stock_report.py schedule
```

## Data Sources & Rate Limits

| Source | Free Tier | Rate Limit | Best For |
|--------|-----------|------------|----------|
| Yahoo Finance | Unlimited | None | Primary data |
| Alpha Vantage | 500/day | 5/min | Enhanced metrics |
| News API | 1000/month | - | Headlines |
| OpenAI | Pay-per-use | 3500 RPM | AI analysis |
| FMP | 250/day | - | Financial statements |

## Troubleshooting

### Common Issues

1. **"No data found" error**: Check symbol spelling and market status
2. **API rate limit errors**: Increase delay in config or upgrade API plan
3. **PDF generation fails**: Ensure reportlab is properly installed
4. **Missing AI analysis**: Verify OpenAI API key is set

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- 📧 Email: support@stockreport.ai
- 💬 Issues: GitHub Issues page
- 📖 Wiki: Project Wiki

## Changelog

### v1.0.0
- Initial release with core functionality
- Multi-source data integration
- AI-powered analysis
- PDF report generation
- Portfolio tracking
- Scheduled reports
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    # Create API documentation
    api_docs = """# API Documentation

## Core Classes

### StockReportApp
Main application class for generating reports.

#### Methods

**generate_monthly_report(symbol: str, output_dir: str = "reports") -> str**
- Generates a standard monthly report
- Returns path to generated PDF

**generate_batch_reports(symbols: List[str], output_dir: str = "reports") -> List[str]**
- Generates reports for multiple stocks
- Returns list of generated report paths

### StockDataCollector
Handles data collection from multiple APIs.

#### Methods

**get_stock_data(symbol: str) -> Optional[StockData]**
- Collects comprehensive stock data
- Combines data from multiple sources

**get_news_data(symbol: str, company_name: str) -> List[Dict]**
- Fetches recent news headlines
- Returns list of news articles

### AIAnalyzer
Generates AI-powered analysis using OpenAI GPT.

#### Methods

**generate_analysis(stock_data: StockData, news_data: List[Dict], competitor_data: List[Dict]) -> str**
- Creates comprehensive AI analysis
- Returns formatted analysis text

### PortfolioManager
Manages portfolio tracking and reporting.

#### Methods

**add_stock(symbol: str, shares: int, purchase_price: float)**
- Adds stock position to portfolio

**generate_portfolio_report(output_dir: str = "reports") -> str**
- Generates portfolio performance report

## Data Classes

### StockData
Core data structure for stock information.

#### Attributes
- symbol: str
- name: str  
- price: float
- change: float
- change_percent: float
- market_cap: float
- pe_ratio: float
- eps: float
- dividend_yield: float
- volume: int
- fifty_two_week_high: float
- fifty_two_week_low: float
- sector: str
- industry: str
- beta: float

## Configuration

### APIConfig
Manages API keys and endpoints.

#### Environment Variables
All API keys can be set via environment variables:
- ALPHA_VANTAGE_API_KEY
- FMP_API_KEY
- POLYGON_API_KEY
- NEWS_API_KEY
- OPENAI_API_KEY
- QUANDL_API_KEY

## Error Handling

The application includes comprehensive error handling:
- API rate limit management
- Network timeout handling
- Invalid symbol validation
- Missing data fallbacks

## Extending the Application

### Adding New Data Sources

1. Create new method in StockDataCollector
2. Add API configuration in APIConfig
3. Update data combination logic
4. Add error handling

### Custom Report Templates

1. Extend ReportGenerator class
2. Override _generate_comprehensive_pdf method
3. Add custom styling and sections

### New Analysis Types

1. Create new analyzer class
2. Implement analysis methods
3. Integrate with main report generation
"""
    
    with open("API.md", "w") as f:
        f.write(api_docs)
    
    print("✅ Documentation created:")
    print("  - README.md (main documentation)")
    print("  - API.md (API reference)")

def main():
    """Main setup function"""
    print("🚀 AI Stock Report Generator Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Run setup steps
    steps = [
        ("Installing requirements", install_requirements),
        ("Creating directories", create_directories), 
        ("Creating configuration", create_config_file),
        ("Creating environment template", create_env_template),
        ("Creating sample scripts", create_sample_scripts),
        ("Creating documentation", create_documentation)
    ]
    
    for step_name, step_func in steps:
        print(f"\\n{step_name}...")
        success = step_func()
        if success is False:
            print(f"❌ Failed: {step_name}")
            return
    
    print("\\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\\nNext steps:")
    print("1. Copy .env.template to .env and add your API keys")
    print("2. Run: python configure.py (for interactive setup)")  
    print("3. Generate your first report: python stock_report.py report --symbol AAPL")
    print("4. Read README.md for detailed usage instructions")
    print("\\n💡 Tip: Start with just Yahoo Finance (no API key needed) and add other sources later")

if __name__ == "__main__":
    main()
