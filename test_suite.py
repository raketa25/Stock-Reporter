#!/usr/bin/env python3
"""
Comprehensive test suite for AI Stock Report Generator
"""

import unittest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

# Import our modules (assuming they're in the same directory)
try:
    from stock_report import (
        StockData, APIConfig, StockDataCollector, AIAnalyzer, 
        ReportGenerator, StockReportApp, EnhancedStockReportApp,
        TechnicalAnalyzer, ESGAnalyzer, PortfolioManager
    )
except ImportError:
    print("Warning: Could not import stock_report modules. Ensure stock_report.py is in the same directory.")


class TestStockData(unittest.TestCase):
    """Test StockData dataclass"""
    
    def test_stock_data_creation(self):
        """Test creating StockData object"""
        stock = StockData(
            symbol="AAPL",
            name="Apple Inc.",
            price=150.0,
            change=2.5,
            change_percent=1.7,
            market_cap=2500000000000,
            pe_ratio=25.5,
            eps=6.0,
            dividend_yield=0.6,
            volume=50000000,
            fifty_two_week_high=180.0,
            fifty_two_week_low=120.0,
            sector="Technology",
            industry="Consumer Electronics",
            beta=1.2,
            book_value=4.0,
            price_to_book=37.5
        )
        
        self.assertEqual(stock.symbol, "AAPL")
        self.assertEqual(stock.name, "Apple Inc.")
        self.assertEqual(stock.price, 150.0)


class TestAPIConfig(unittest.TestCase):
    """Test API configuration"""
    
    def test_api_config_initialization(self):
        """Test APIConfig initialization"""
        config = APIConfig()
        
        # Check that placeholders are set
        self.assertIn("YOUR_", config.ALPHA_VANTAGE_API_KEY)
        self.assertIn("YOUR_", config.OPENAI_API_KEY)
        
        # Check URLs are set
        self.assertTrue(config.ALPHA_VANTAGE_BASE_URL.startswith("https://"))
        self.assertTrue(config.FMP_BASE_URL.startswith("https://"))


class TestStockDataCollector(unittest.TestCase):
    """Test data collection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = APIConfig()
        self.collector = StockDataCollector(self.config)
    
    @patch('yfinance.Ticker')
    def test_yahoo_finance_data_collection(self, mock_ticker):
        """Test Yahoo Finance data collection"""
        # Mock yfinance response
        mock_info = {
            'currentPrice': 150.0,
            'regularMarketChange': 2.5,
            'regularMarketChangePercent': 0.017,
            'marketCap': 2500000000000,
            'trailingPE': 25.5,
            'trailingEps': 6.0,
            'dividendYield': 0.006,
            'regularMarketVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'beta': 1.2,
            'bookValue': 4.0,
            'priceToBook': 37.5,
            'longName': 'Apple Inc.'
        }
        
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = mock_info
        mock_ticker_instance.history.return_value = pd.DataFrame({
            'Close': [145, 147, 149, 150]
        })
        mock_ticker.return_value = mock_ticker_instance
        
        # Test data collection
        result = self.collector._get_yahoo_finance_data('AAPL')
        
        self.assertEqual(result['price'], 150.0)
        self.assertEqual(result['name'], 'Apple Inc.')
        self.assertEqual(result['sector'], 'Technology')
    
    def test_combine_stock_data(self):
        """Test data combination from multiple sources"""
        yf_data = {
            'price': 150.0,
            'name': 'Apple Inc.',
            'pe_ratio': 25.5
        }
        
        fmp_data = {
            'market_cap': 2500000000000,
            'pe_ratio': 25.0  # Different value to test priority
        }
        
        av_data = {
            'volume': 50000000
        }
        
        stock_data = self.collector._combine_stock_data('AAPL', yf_data, av_data, fmp_data)
        
        # Yahoo Finance should have priority
        self.assertEqual(stock_data.pe_ratio, 25.5)
        self.assertEqual(stock_data.price, 150.0)
        self.assertEqual(stock_data.market_cap, 2500000000000)


class TestTechnicalAnalyzer(unittest.TestCase):
    """Test technical analysis calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.prices = pd.Series([100, 102, 98, 105, 103, 107, 104, 108, 106, 110])
    
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        rsi = TechnicalAnalyzer.calculate_rsi(self.prices, window=4)
        
        # RSI should be between 0 and 100
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
    
    def test_moving_averages(self):
        """Test moving average calculations"""
        mas = TechnicalAnalyzer.calculate_moving_averages(self.prices)
        
        self.assertIn('sma_20', mas)
        self.assertGreater(mas['sma_20'], 0)
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        bb = TechnicalAnalyzer.calculate_bollinger_bands(self.prices, window=5)
        
        self.assertIn('upper_band', bb)
        self.assertIn('middle_band', bb)
        self.assertIn('lower_band', bb)
        
        # Upper band should be higher than lower band
        self.assertGreater(bb['upper_band'], bb['lower_band'])


class TestESGAnalyzer(unittest.TestCase):
    """Test ESG analysis"""
    
    def setUp(self):
        """Set up ESG analyzer"""
        self.config = APIConfig()
        self.esg_analyzer = ESGAnalyzer(self.config)
    
    def test_esg_score_generation(self):
        """Test ESG score generation"""
        esg_data = self.esg_analyzer.get_esg_score('AAPL')
        
        # Check all required fields are present
        required_fields = ['overall_score', 'environmental', 'social', 'governance', 'controversy_score', 'rating']
        for field in required_fields:
            self.assertIn(field, esg_data)
        
        # Check score ranges
        self.assertGreaterEqual(esg_data['overall_score'], 0)
        self.assertLessEqual(esg_data['overall_score'], 100)


class TestPortfolioManager(unittest.TestCase):
    """Test portfolio management functionality"""
    
    def setUp(self):
        """Set up portfolio manager with temporary file"""
        self.config = APIConfig()
        self.temp_dir = tempfile.mkdtemp()
        self.portfolio_manager = PortfolioManager(self.config)
        self.portfolio_manager.portfolio_file = os.path.join(self.temp_dir, "test_portfolio.json")
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_stock(self):
        """Test adding stock to portfolio"""
        self.portfolio_manager.add_stock('AAPL', 100, 150.0)
        
        portfolio = self.portfolio_manager.load_portfolio()
        
        self.assertIn('AAPL', portfolio['stocks'])
        self.assertEqual(portfolio['stocks']['AAPL']['shares'], 100)
        self.assertEqual(portfolio['stocks']['AAPL']['avg_price'], 150.0)
    
    def test_portfolio_persistence(self):
        """Test portfolio saves and loads correctly"""
        # Add stock
        self.portfolio_manager.add_stock('AAPL', 100, 150.0)
        
        # Create new portfolio manager with same file
        new_manager = PortfolioManager(self.config)
        new_manager.portfolio_file = self.portfolio_manager.portfolio_file
        
        portfolio = new_manager.load_portfolio()
        self.assertIn('AAPL', portfolio['stocks'])


class TestReportGenerator(unittest.TestCase):
    """Test PDF report generation"""
    
    def setUp(self):
        """Set up report generator and test data"""
        self.generator = ReportGenerator()
        self.temp_dir = tempfile.mkdtemp()
        
        self.stock_data = StockData(
            symbol="AAPL",
            name="Apple Inc.",
            price=150.0,
            change=2.5,
            change_percent=1.7,
            market_cap=2500000000000,
            pe_ratio=25.5,
            eps=6.0,
            dividend_yield=0.6,
            volume=50000000,
            fifty_two_week_high=180.0,
            fifty_two_week_low=120.0,
            sector="Technology",
            industry="Consumer Electronics",
            beta=1.2,
            book_value=4.0,
            price_to_book=37.5
        )
        
        self.news_data = [
            {
                'title': 'Apple reports strong earnings',
                'description': 'Company beats expectations',
                'url': 'https://example.com',
                'publishedAt': datetime.now().isoformat(),
                'source': 'TechNews'
            }
        ]
        
        self.competitor_data = [
            {
                'symbol': 'MSFT',
                'name': 'Microsoft Corporation',
                'price': 300.0,
                'pe_ratio': 28.0,
                'market_cap': 2200000000000
            }
        ]
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_report_generation(self):
        """Test PDF report generation"""
        output_path = os.path.join(self.temp_dir, "test_report.pdf")
        ai_analysis = "This is a test analysis of the stock."
        
        # Should not raise an exception
        self.generator.generate_report(
            self.stock_data,
            self.news_data,
            self.competitor_data,
            ai_analysis,
            output_path
        )
        
        # Check file was created
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)


class TestAIAnalyzer(unittest.TestCase):
    """Test AI analysis functionality"""
    
    def setUp(self):
        """Set up AI analyzer"""
        self.config = APIConfig()
        self.analyzer = AIAnalyzer(self.config)
        
        self.stock_data = StockData(
            symbol="AAPL",
            name="Apple Inc.",
            price=150.0,
            change=2.5,
            change_percent=1.7,
            market_cap=2500000000000,
            pe_ratio=25.5,
            eps=6.0,
            dividend_yield=0.6,
            volume=50000000,
            fifty_two_week_high=180.0,
            fifty_two_week_low=120.0,
            sector="Technology",
            industry="Consumer Electronics",
            beta=1.2,
            book_value=4.0,
            price_to_book=37.5
        )
    
    def test_mock_analysis_generation(self):
        """Test mock analysis generation (when OpenAI API not available)"""
        analysis = self.analyzer._generate_mock_analysis(self.stock_data)
        
        self.assertIsInstance(analysis, str)
        self.assertGreater(len(analysis), 100)  # Should be substantial
        self.assertIn('AAPL', analysis)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete application"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.app = StockReportApp()
    
    def tearDown(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('stock_report.StockDataCollector.get_stock_data')
    @patch('stock_report.StockDataCollector.get_news_data')
    @patch('stock_report.StockDataCollector.get_competitor_data')
    def test_end_to_end_report_generation(self, mock_competitors, mock_news, mock_stock_data):
        """Test complete report generation flow"""
        # Mock the data
        mock_stock_data.return_value = StockData(
            symbol="AAPL", name="Apple Inc.", price=150.0, change=2.5,
            change_percent=1.7, market_cap=2500000000000, pe_ratio=25.5,
            eps=6.0, dividend_yield=0.6, volume=50000000,
            fifty_two_week_high=180.0, fifty_two_week_low=120.0,
            sector="Technology", industry="Consumer Electronics",
            beta=1.2, book_value=4.0, price_to_book=37.5
        )
        
        mock_news.return_value = [
            {'title': 'Test news', 'description': 'Test description',
             'url': 'https://test.com', 'publishedAt': datetime.now().isoformat(),
             'source': 'Test Source'}
        ]
        
        mock_competitors.return_value = [
            {'symbol': 'MSFT', 'name': 'Microsoft', 'price': 300.0,
             'pe_ratio': 28.0, 'market_cap': 2200000000000}
        ]
        
        # Generate report
        report_path = self.app.generate_monthly_report('AAPL', self.temp_dir)
        
        # Verify report was created
        self.assertTrue(os.path.exists(report_path))
        self.assertGreater(os.path.getsize(report_path), 0)


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance(unittest.TestCase):
    """Performance and load tests"""
    
    def test_batch_processing_performance(self):
        """Test performance of batch processing"""
        import time
        
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        app = StockReportApp()
        
        start_time = time.time()
        
        # Mock the data collection to avoid API calls
        with patch.object(app.data_collector, 'get_stock_data') as mock_get_data:
            mock_get_data.return_value = StockData(
                symbol="TEST", name="Test Company", price=100.0, change=1.0,
                change_percent=1.0, market_cap=1000000000, pe_ratio=20.0,
                eps=5.0, dividend_yield=2.0, volume=1000000,
                fifty_two_week_high=120.0, fifty_two_week_low=80.0,
                sector="Technology", industry="Software", beta=1.0,
                book_value=50.0, price_to_book=2.0
            )
            
            with patch.object(app.data_collector, 'get_news_data') as mock_news:
                mock_news.return_value = []
                
                with patch.object(app.data_collector, 'get_competitor_data') as mock_comp:
                    mock_comp.return_value = []
                    
                    with tempfile.TemporaryDirectory() as temp_dir:
                        report_paths = app.generate_batch_reports(symbols, temp_dir)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should process 3 stocks in reasonable time (< 30 seconds with mocking)
        self.assertLess(processing_time, 30)
        self.assertEqual(len(report_paths), len(symbols))


# =============================================================================
# TEST UTILITIES
# =============================================================================

class TestUtilities:
    """Utility functions for testing"""
    
    @staticmethod
    def create_mock_stock_data(symbol="TEST"):
        """Create mock stock data for testing"""
        return StockData(
            symbol=symbol,
            name=f"{symbol} Corporation",
            price=100.0,
            change=1.0,
            change_percent=1.0,
            market_cap=1000000000,
            pe_ratio=20.0,
            eps=5.0,
            dividend_yield=2.0,
            volume=1000000,
            fifty_two_week_high=120.0,
            fifty_two_week_low=80.0,
            sector="Technology",
            industry="Software",
            beta=1.0,
            book_value=50.0,
            price_to_book=2.0
        )
    
    @staticmethod
    def create_test_config():
        """Create test configuration"""
        config = APIConfig()
        # Override with test values
        config.ALPHA_VANTAGE_API_KEY = "test_key"
        return config


# =============================================================================
# TEST RUNNER AND MAIN
# =============================================================================

def run_all_tests():
    """Run all tests and generate report"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestStockData,
        TestAPIConfig,
        TestStockDataCollector,
        TestTechnicalAnalyzer,
        TestESGAnalyzer,
        TestPortfolioManager,
        TestReportGenerator,
        TestAIAnalyzer,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


# =============================================================================
# DEPLOYMENT GUIDE
# =============================================================================

DEPLOYMENT_GUIDE = """
# AI Stock Report Generator - Deployment Guide

## Local Development Setup

### 1. Environment Setup
```bash
# Clone/download the project
git clone <repository_url>
cd ai-stock-report-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py
```

### 2. Configuration
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys
nano .env

# Test configuration
python configure.py
python stock_report.py validate
```

### 3. First Report
```bash
# Generate test report (works with Yahoo Finance only)
python stock_report.py report --symbol AAPL

# Generate comprehensive report (requires OpenAI API)
python stock_report.py report --symbol AAPL --comprehensive
```

## Production Deployment Options

### Option 1: VPS/Server Deployment

#### Requirements
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- 2GB RAM minimum
- 10GB storage

#### Steps
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Clone project
git clone <repository_url>
cd ai-stock-report-generator

# Setup application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py

# Configure environment
cp .env.template .env
# Edit .env with your API keys

# Test installation
python stock_report.py validate
```

#### Systemd Service (for scheduled reports)
```bash
# Create service file
sudo nano /etc/systemd/system/stock-reports.service

# Add content:
[Unit]
Description=Stock Report Generator
After=network.target

[Service]
Type=oneshot
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-stock-report-generator
Environment=PATH=/home/ubuntu/ai-stock-report-generator/venv/bin
ExecStart=/home/ubuntu/ai-stock-report-generator/venv/bin/python stock_report.py schedule

[Install]
WantedBy=multi-user.target

# Create timer for monthly execution
sudo nano /etc/systemd/system/stock-reports.timer

# Add content:
[Unit]
Description=Run Stock Reports Monthly
Requires=stock-reports.service

[Timer]
OnCalendar=monthly
Persistent=true

[Install]
WantedBy=timers.target

# Enable and start
sudo systemctl enable stock-reports.timer
sudo systemctl start stock-reports.timer
```

### Option 2: Docker Deployment

#### Single Container
```bash
# Build image
docker build -t stock-report-generator .

# Run with mounted volumes
docker run -d \\
  --name stock-reports \\
  -v $(pwd)/reports:/app/reports \\
  -v $(pwd)/.env:/app/.env:ro \\
  stock-report-generator

# Execute reports
docker exec stock-reports python stock_report.py report --symbol AAPL
```

#### Docker Compose (Recommended)
```bash
# Start services
docker-compose up -d

# Generate reports
docker-compose run stock-report-generator python stock_report.py report --symbol AAPL

# Scheduled execution (add to cron)
0 9 1 * * cd /path/to/project && docker-compose run --rm stock-report-generator python stock_report.py schedule
```

### Option 3: Cloud Deployment

#### AWS Lambda
```bash
# Install serverless framework
npm install -g serverless
npm install serverless-python-requirements

# Create serverless.yml
service: stock-report-generator

provider:
  name: aws
  runtime: python3.8
  timeout: 900
  environment:
    OPENAI_API_KEY: ${env:OPENAI_API_KEY}
    # ... other API keys

functions:
  generateReport:
    handler: lambda_handler.generate_report
    events:
      - schedule: cron(0 9 1 * ? *)  # Monthly on 1st at 9 AM

plugins:
  - serverless-python-requirements

# Deploy
serverless deploy
```

#### Google Cloud Functions
```bash
# Deploy function
gcloud functions deploy stock-report-generator \\
  --runtime python39 \\
  --trigger-http \\
  --memory 2GB \\
  --timeout 540s \\
  --set-env-vars OPENAI_API_KEY=${OPENAI_API_KEY}

# Schedule with Cloud Scheduler
gcloud scheduler jobs create http monthly-reports \\
  --schedule="0 9 1 * *" \\
  --uri=https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/stock-report-generator \\
  --http-method=POST
```

#### Azure Functions
```bash
# Create function app
func init StockReportGenerator --python
cd StockReportGenerator

# Add function
func new --name GenerateReport --template "Timer trigger"

# Deploy
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

## Monitoring and Maintenance

### Log Monitoring
```bash
# Check application logs
tail -f logs/stock_report.log

# Docker logs
docker-compose logs -f stock-report-generator

# Systemd logs
sudo journalctl -u stock-reports.service -f
```

### Health Checks
```bash
# API validation
python stock_report.py validate

# Generate test report
python stock_report.py report --symbol AAPL --output test_reports

# Check disk space
df -h reports/
```

### Backup Strategy
```bash
# Backup reports
tar -czf reports_backup_$(date +%Y%m%d).tar.gz reports/

# Backup configuration
cp config.json config_backup_$(date +%Y%m%d).json
cp .env .env_backup_$(date +%Y%m%d)

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backup/stock_reports_$DATE.tar.gz reports/ config.json
find /backup -name "stock_reports_*.tar.gz" -mtime +30 -delete
```

## Scaling Considerations

### High Volume Processing
- Use Redis for caching API responses
- Implement rate limiting and retries
- Consider database storage for historical data
- Use message queues for batch processing

### Multiple Users
- Add user authentication
- Implement multi-tenancy
- Use cloud storage for reports
- Add web interface

### Performance Optimization
- Cache competitor data
- Parallel processing for batch reports
- Optimize PDF generation
- Use CDN for report distribution

## Security Best Practices

### API Key Management
- Use environment variables or secrets management
- Rotate keys regularly
- Monitor API usage
- Implement key validation

### System Security
- Regular security updates
- Firewall configuration
- SSL/TLS for web interfaces
- Access logging

### Data Protection
- Encrypt sensitive data
- Secure report storage
- Regular backups
- GDPR compliance if applicable

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Increase delays, use multiple keys
2. **PDF Generation Errors**: Check ReportLab installation
3. **Memory Issues**: Reduce batch sizes, optimize data handling
4. **Permission Errors**: Check file permissions and user accounts

### Debug Mode
```bash
# Enable debug logging
export PYTHONPATH=.
export LOG_LEVEL=DEBUG
python stock_report.py report --symbol AAPL
```

### Performance Profiling
```bash
# Profile memory usage
python -m memory_profiler stock_report.py

# Profile execution time
python -m cProfile -o profile.stats stock_report.py
```

## Maintenance Schedule

### Daily
- Check log files for errors
- Monitor API usage
- Verify scheduled reports

### Weekly  
- Review generated reports
- Check disk space
- Update dependencies

### Monthly
- API key rotation
- System updates
- Backup verification
- Performance review

### Quarterly
- Security audit
- Feature updates
- Documentation updates
- User feedback review
"""

def print_deployment_guide():
    """Print the deployment guide"""
    print(DEPLOYMENT_GUIDE)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "deploy-guide":
            print_deployment_guide()
        elif sys.argv[1] == "test":
            success = run_all_tests()
            sys.exit(0 if success else 1)
        else:
            print("Usage: python test_suite.py [test|deploy-guide]")
    else:
        print("AI Stock Report Generator - Test Suite")
        print("="*50)
        print("Available commands:")
        print("  python test_suite.py test          - Run all tests")
        print("  python test_suite.py deploy-guide  - Show deployment guide")
        print("="*50)
