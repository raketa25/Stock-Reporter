#!/usr/bin/env python3
"""
AI Automated Stock Report Generator
A comprehensive tool for generating professional stock analysis reports with AI insights.
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import openai
from typing import Dict, List, Optional, Tuple
import logging
import time
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class StockData:
    """Data class to hold stock information"""
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    market_cap: float
    pe_ratio: float
    eps: float
    dividend_yield: float
    volume: int
    fifty_two_week_high: float
    fifty_two_week_low: float
    sector: str
    industry: str
    beta: float
    book_value: float
    price_to_book: float

class APIConfig:
    """Configuration class for API keys and endpoints"""
    
    def __init__(self):
        # =============================================================================
        # API KEYS - REPLACE WITH YOUR ACTUAL API KEYS
        # =============================================================================
        
        # Alpha Vantage API (Free: 5 calls/minute, 500/day)
        # Get your free key at: https://www.alphavantage.co/support/#api-key
        self.ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY_HERE"
        
        # Financial Modeling Prep API (Free: 250 calls/day)
        # Get your free key at: https://financialmodelingprep.com/developer/docs
        self.FMP_API_KEY = "YOUR_FMP_API_KEY_HERE"
        
        # Polygon.io API (Free: 5 calls/minute)
        # Get your free key at: https://polygon.io/
        self.POLYGON_API_KEY = "YOUR_POLYGON_API_KEY_HERE"
        
        # News API (Free: 1000 requests/month)
        # Get your free key at: https://newsapi.org/
        self.NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"
        
        # OpenAI API (for AI analysis)
        # Get your key at: https://platform.openai.com/api-keys
        self.OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
        
        # Quandl API (Optional - for additional financial data)
        # Get your free key at: https://www.quandl.com/
        self.QUANDL_API_KEY = "YOUR_QUANDL_API_KEY_HERE"
        
        # =============================================================================
        # API ENDPOINTS
        # =============================================================================
        self.ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
        self.FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
        self.POLYGON_BASE_URL = "https://api.polygon.io/v2"
        self.NEWS_API_BASE_URL = "https://newsapi.org/v2"
        self.QUANDL_BASE_URL = "https://www.quandl.com/api/v3"

class StockDataCollector:
    """Collects stock data from multiple APIs"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        openai.api_key = config.OPENAI_API_KEY
    
    def get_stock_data(self, symbol: str) -> Optional[StockData]:
        """Collect comprehensive stock data from multiple sources"""
        try:
            logger.info(f"Fetching data for {symbol}")
            
            # Primary data from Yahoo Finance (free and reliable)
            yf_data = self._get_yahoo_finance_data(symbol)
            
            # Additional data from other APIs
            av_data = self._get_alpha_vantage_data(symbol)
            fmp_data = self._get_fmp_data(symbol)
            
            # Combine data sources
            stock_data = self._combine_stock_data(symbol, yf_data, av_data, fmp_data)
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def _get_yahoo_finance_data(self, symbol: str) -> Dict:
        """Get data from Yahoo Finance using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1y")
            
            return {
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0) * 100,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'eps': info.get('trailingEps', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'volume': info.get('regularMarketVolume', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'beta': info.get('beta', 0),
                'book_value': info.get('bookValue', 0),
                'price_to_book': info.get('priceToBook', 0),
                'name': info.get('longName', symbol),
                'historical_data': hist
            }
        except Exception as e:
            logger.error(f"Yahoo Finance error for {symbol}: {e}")
            return {}
    
    def _get_alpha_vantage_data(self, symbol: str) -> Dict:
        """Get data from Alpha Vantage API"""
        try:
            if self.config.ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_API_KEY_HERE":
                return {}
            
            # Global Quote endpoint
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.config.ALPHA_VANTAGE_API_KEY
            }
            
            response = requests.get(self.config.ALPHA_VANTAGE_BASE_URL, params=params)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': float(quote.get('10. change percent', '0%').replace('%', '')),
                    'volume': int(quote.get('06. volume', 0))
                }
            
            time.sleep(12)  # Alpha Vantage rate limit: 5 calls per minute
            return {}
            
        except Exception as e:
            logger.error(f"Alpha Vantage error for {symbol}: {e}")
            return {}
    
    def _get_fmp_data(self, symbol: str) -> Dict:
        """Get data from Financial Modeling Prep API"""
        try:
            if self.config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
                return {}
            
            # Company profile
            profile_url = f"{self.config.FMP_BASE_URL}/profile/{symbol}?apikey={self.config.FMP_API_KEY}"
            profile_response = requests.get(profile_url)
            profile_data = profile_response.json()
            
            # Financial ratios
            ratios_url = f"{self.config.FMP_BASE_URL}/ratios/{symbol}?apikey={self.config.FMP_API_KEY}"
            ratios_response = requests.get(ratios_url)
            ratios_data = ratios_response.json()
            
            result = {}
            if profile_data and len(profile_data) > 0:
                profile = profile_data[0]
                result.update({
                    'market_cap': profile.get('mktCap', 0),
                    'sector': profile.get('sector', 'Unknown'),
                    'industry': profile.get('industry', 'Unknown'),
                    'beta': profile.get('beta', 0),
                    'name': profile.get('companyName', symbol)
                })
            
            if ratios_data and len(ratios_data) > 0:
                ratios = ratios_data[0]
                result.update({
                    'pe_ratio': ratios.get('priceEarningsRatio', 0),
                    'price_to_book': ratios.get('priceToBookRatio', 0),
                    'dividend_yield': ratios.get('dividendYield', 0) * 100
                })
            
            return result
            
        except Exception as e:
            logger.error(f"FMP error for {symbol}: {e}")
            return {}
    
    def _combine_stock_data(self, symbol: str, yf_data: Dict, av_data: Dict, fmp_data: Dict) -> StockData:
        """Combine data from multiple sources, prioritizing most reliable sources"""
        
        # Priority order: Yahoo Finance > FMP > Alpha Vantage
        def get_value(key: str, default=0):
            return yf_data.get(key, fmp_data.get(key, av_data.get(key, default)))
        
        return StockData(
            symbol=symbol,
            name=get_value('name', symbol),
            price=get_value('price', 0),
            change=get_value('change', 0),
            change_percent=get_value('change_percent', 0),
            market_cap=get_value('market_cap', 0),
            pe_ratio=get_value('pe_ratio', 0),
            eps=get_value('eps', 0),
            dividend_yield=get_value('dividend_yield', 0),
            volume=get_value('volume', 0),
            fifty_two_week_high=get_value('fifty_two_week_high', 0),
            fifty_two_week_low=get_value('fifty_two_week_low', 0),
            sector=get_value('sector', 'Unknown'),
            industry=get_value('industry', 'Unknown'),
            beta=get_value('beta', 0),
            book_value=get_value('book_value', 0),
            price_to_book=get_value('price_to_book', 0)
        )
    
    def get_news_data(self, symbol: str, company_name: str) -> List[Dict]:
        """Get recent news for the stock"""
        try:
            if self.config.NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
                return self._get_mock_news(symbol)
            
            params = {
                'q': f'{symbol} OR "{company_name}"',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'language': 'en',
                'apiKey': self.config.NEWS_API_KEY
            }
            
            response = requests.get(f"{self.config.NEWS_API_BASE_URL}/everything", params=params)
            data = response.json()
            
            if data.get('status') == 'ok':
                return [
                    {
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'publishedAt': article['publishedAt'],
                        'source': article['source']['name']
                    }
                    for article in data.get('articles', [])[:5]
                ]
            
            return self._get_mock_news(symbol)
            
        except Exception as e:
            logger.error(f"News API error for {symbol}: {e}")
            return self._get_mock_news(symbol)
    
    def _get_mock_news(self, symbol: str) -> List[Dict]:
        """Generate mock news data when API is not available"""
        return [
            {
                'title': f'{symbol} reports strong quarterly earnings',
                'description': 'Company beats analyst expectations with robust revenue growth',
                'url': '#',
                'publishedAt': datetime.now().isoformat(),
                'source': 'Financial News'
            },
            {
                'title': f'{symbol} announces strategic partnership',
                'description': 'New collaboration expected to drive future growth',
                'url': '#',
                'publishedAt': (datetime.now() - timedelta(days=1)).isoformat(),
                'source': 'Business Wire'
            },
            {
                'title': f'Analysts upgrade {symbol} price target',
                'description': 'Multiple analysts raise price targets following strong performance',
                'url': '#',
                'publishedAt': (datetime.now() - timedelta(days=2)).isoformat(),
                'source': 'Market Watch'
            }
        ]
    
    def get_competitor_data(self, sector: str, exclude_symbol: str) -> List[Dict]:
        """Get competitor data for comparison"""
        # This would typically come from a sector classification API
        # For now, we'll use predefined competitor lists
        competitors = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
            'Healthcare': ['JNJ', 'PFE', 'UNH', 'MRK', 'ABBV'],
            'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'Consumer Cyclical': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE'],
            'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG']
        }
        
        sector_stocks = competitors.get(sector, ['SPY'])  # Default to S&P 500 if sector not found
        competitor_symbols = [s for s in sector_stocks if s != exclude_symbol][:3]
        
        competitor_data = []
        for comp_symbol in competitor_symbols:
            try:
                ticker = yf.Ticker(comp_symbol)
                info = ticker.info
                competitor_data.append({
                    'symbol': comp_symbol,
                    'name': info.get('longName', comp_symbol),
                    'price': info.get('currentPrice', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'market_cap': info.get('marketCap', 0)
                })
            except:
                continue
        
        return competitor_data

class AIAnalyzer:
    """AI-powered analysis using OpenAI GPT"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        if config.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
            openai.api_key = config.OPENAI_API_KEY
    
    def generate_analysis(self, stock_data: StockData, news_data: List[Dict], competitor_data: List[Dict]) -> str:
        """Generate AI-powered stock analysis"""
        try:
            if self.config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
                return self._generate_mock_analysis(stock_data)
            
            # Prepare context for AI
            context = f"""
            Stock: {stock_data.name} ({stock_data.symbol})
            Current Price: ${stock_data.price:.2f}
            Change: {stock_data.change_percent:.2f}%
            Market Cap: ${stock_data.market_cap:,.0f}
            P/E Ratio: {stock_data.pe_ratio:.1f}
            Sector: {stock_data.sector}
            
            Recent News Headlines:
            {chr(10).join([f"- {news['title']}" for news in news_data[:3]])}
            
            Competitors:
            {chr(10).join([f"- {comp['name']} (P/E: {comp['pe_ratio']:.1f})" for comp in competitor_data])}
            """
            
            prompt = f"""
            As a financial analyst, provide a comprehensive analysis of this stock based on the following data:
            
            {context}
            
            Please provide:
            1. Investment thesis (2-3 sentences)
            2. Key strengths and risks
            3. Valuation assessment
            4. Recommendation (Buy/Hold/Sell) with rationale
            
            Keep the analysis professional and balanced.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._generate_mock_analysis(stock_data)
    
    def _generate_mock_analysis(self, stock_data: StockData) -> str:
        """Generate mock analysis when OpenAI API is not available"""
        performance = "positive momentum" if stock_data.change_percent > 0 else "recent weakness"
        valuation = "attractively valued" if stock_data.pe_ratio < 20 else "premium valuation" if stock_data.pe_ratio > 30 else "fairly valued"
        
        return f"""
        Investment Thesis: {stock_data.name} demonstrates {performance} with current trading indicating {valuation} relative to sector peers. The company's position in the {stock_data.sector} sector provides both opportunities and challenges in the current market environment.
        
        Key Strengths: Strong market capitalization of ${stock_data.market_cap/1e9:.1f}B positions the company well for continued growth. The current P/E ratio of {stock_data.pe_ratio:.1f} suggests reasonable valuation metrics.
        
        Key Risks: Market volatility and sector-specific headwinds remain primary concerns. Beta of {stock_data.beta:.2f} indicates correlation with broader market movements.
        
        Valuation Assessment: Based on fundamental metrics, the stock appears {valuation} at current levels. Price-to-book ratio of {stock_data.price_to_book:.2f} supports this assessment.
        
        Recommendation: HOLD - Continue monitoring for entry opportunities while maintaining current positions. Consider dollar-cost averaging for long-term investors.
        """

class ReportGenerator:
    """Generates PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        )
        
        self.metric_style = ParagraphStyle(
            'MetricStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
    
    def generate_report(self, stock_data: StockData, news_data: List[Dict], 
                       competitor_data: List[Dict], ai_analysis: str, output_path: str):
        """Generate complete PDF report"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch)
            story = []
            
            # Title
            story.append(Paragraph(f"{stock_data.name} ({stock_data.symbol})", self.title_style))
            story.append(Paragraph(f"Stock Analysis Report - {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", self.heading_style))
            summary_text = f"""
            {stock_data.name} is currently trading at ${stock_data.price:.2f}, showing a 
            {stock_data.change_percent:+.2f}% change. The company operates in the {stock_data.sector} 
            sector with a market capitalization of ${stock_data.market_cap/1e9:.1f} billion.
            """
            story.append(Paragraph(summary_text, self.styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Key Metrics Table
            story.append(Paragraph("Key Financial Metrics", self.heading_style))
            metrics_data = [
                ['Metric', 'Value'],
                ['Current Price', f'${stock_data.price:.2f}'],
                ['Price Change', f'{stock_data.change_percent:+.2f}%'],
                ['Market Cap', f'${stock_data.market_cap/1e9:.1f}B'],
                ['P/E Ratio', f'{stock_data.pe_ratio:.1f}'],
                ['EPS', f'${stock_data.eps:.2f}'],
                ['Dividend Yield', f'{stock_data.dividend_yield:.2f}%'],
                ['Beta', f'{stock_data.beta:.2f}'],
                ['52-Week High', f'${stock_data.fifty_two_week_high:.2f}'],
                ['52-Week Low', f'${stock_data.fifty_two_week_low:.2f}']
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 20))
            
            # Recent News
            story.append(Paragraph("Recent News & Developments", self.heading_style))
            for news in news_data[:3]:
                story.append(Paragraph(f"• <b>{news['title']}</b>", self.styles['Normal']))
                if news['description']:
                    story.append(Paragraph(f"  {news['description'][:100]}...", self.styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 12))
            
            # Competitive Analysis
            if competitor_data:
                story.append(Paragraph("Competitive Landscape", self.heading_style))
                story.append(Paragraph(f"Key competitors in the {stock_data.sector} sector:", self.styles['Normal']))
                
                comp_data = [['Company', 'Symbol', 'Price', 'P/E Ratio', 'Market Cap']]
                for comp in competitor_data:
                    comp_data.append([
                        comp['name'][:20] + "..." if len(comp['name']) > 20 else comp['name'],
                        comp['symbol'],
                        f"${comp['price']:.2f}",
                        f"{comp['pe_ratio']:.1f}" if comp['pe_ratio'] else "N/A",
                        f"${comp['market_cap']/1e9:.1f}B" if comp['market_cap'] else "N/A"
                    ])
                
                comp_table = Table(comp_data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
                comp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(comp_table)
                story.append(Spacer(1, 20))
            
            # AI Analysis
            story.append(Paragraph("AI-Powered Analysis", self.heading_style))
            story.append(Paragraph(ai_analysis, self.styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Footer
            story.append(Spacer(1, 30))
            story.append(Paragraph("Disclaimer: This report is for informational purposes only and should not be considered as investment advice.", 
                                 self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            logger.info(f"Report generated successfully: {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

class StockReportApp:
    """Main application class"""
    
    def __init__(self):
        self.config = APIConfig()
        self.data_collector = StockDataCollector(self.config)
        self.ai_analyzer = AIAnalyzer(self.config)
        self.report_generator = ReportGenerator()
    
    def generate_monthly_report(self, symbol: str, output_dir: str = "reports") -> str:
        """Generate a complete monthly stock report"""
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            logger.info(f"Starting report generation for {symbol}")
            
            # Collect stock data
            stock_data = self.data_collector.get_stock_data(symbol)
            if not stock_data:
                raise ValueError(f"Could not fetch data for symbol: {symbol}")
            
            # Get news data
            news_data = self.data_collector.get_news_data(symbol, stock_data.name)
            
            # Get competitor data
            competitor_data = self.data_collector.get_competitor_data(stock_data.sector, symbol)
            
            # Generate AI analysis
            ai_analysis = self.ai_analyzer.generate_analysis(stock_data, news_data, competitor_data)
            
            # Generate report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"{symbol}_report_{timestamp}.pdf")
            
            self.report_generator.generate_report(
                stock_data, news_data, competitor_data, ai_analysis, output_path
            )
            
            logger.info(f"Report completed successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating report for {symbol}: {e}")
            raise
    
    def generate_batch_reports(self, symbols: List[str], output_dir: str = "reports") -> List[str]:
        """Generate reports for multiple stocks"""
        report_paths = []
        
        for symbol in symbols:
            try:
                report_path = self.generate_monthly_report(symbol, output_dir)
                report_paths.append(report_path)
                
                # Add delay between requests to respect API rate limits
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to generate report for {symbol}: {e}")
                continue
        
        return report_paths

def main():
    """Main function to demonstrate usage"""
    
    # Initialize the application
    app = StockReportApp()
    
    # Example: Generate single report
    try:
        symbol = "AAPL"  # Change this to any stock symbol
        print(f"Generating report for {symbol}...")
        
        report_path = app.generate_monthly_report(symbol)
        print(f"Report generated successfully: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example: Generate batch reports
    try:
        symbols = ["AAPL", "MSFT", "GOOGL"]  # Add more symbols as needed
        print(f"Generating batch reports for {symbols}...")
        
        report_paths = app.generate_batch_reports(symbols)
        print(f"Generated {len(report_paths)} reports:")
        for path in report_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"Batch processing error: {e}")

if __name__ == "__main__":
    main()

# =============================================================================
# ADVANCED FEATURES AND UTILITIES
# =============================================================================

class TechnicalAnalyzer:
    """Technical analysis calculations"""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, window: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50
    
    @staticmethod
    def calculate_moving_averages(prices: pd.Series) -> Dict[str, float]:
        """Calculate various moving averages"""
        return {
            'sma_20': prices.rolling(20).mean().iloc[-1] if len(prices) >= 20 else prices.mean(),
            'sma_50': prices.rolling(50).mean().iloc[-1] if len(prices) >= 50 else prices.mean(),
            'sma_200': prices.rolling(200).mean().iloc[-1] if len(prices) >= 200 else prices.mean(),
        }
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, window: int = 20, std_dev: int = 2) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window).mean()
        std = prices.rolling(window).std()
        
        return {
            'upper_band': (sma + (std * std_dev)).iloc[-1] if len(prices) >= window else prices.iloc[-1] * 1.02,
            'middle_band': sma.iloc[-1] if len(prices) >= window else prices.mean(),
            'lower_band': (sma - (std * std_dev)).iloc[-1] if len(prices) >= window else prices.iloc[-1] * 0.98
        }

class ESGAnalyzer:
    """ESG (Environmental, Social, Governance) analysis"""
    
    def __init__(self, config: APIConfig):
        self.config = config
    
    def get_esg_score(self, symbol: str) -> Dict[str, any]:
        """Get ESG score and ratings (mock implementation)"""
        # In production, this would connect to ESG data providers like:
        # - Sustainalytics API
        # - MSCI ESG API
        # - Refinitiv ESG API
        
        # Mock ESG data
        import random
        return {
            'overall_score': round(random.uniform(60, 90), 1),
            'environmental': round(random.uniform(50, 95), 1),
            'social': round(random.uniform(55, 90), 1),
            'governance': round(random.uniform(65, 95), 1),
            'controversy_score': round(random.uniform(1, 5), 1),
            'rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B'])
        }

class PortfolioManager:
    """Portfolio tracking and management"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.portfolio_file = "portfolio.json"
    
    def load_portfolio(self) -> Dict:
        """Load portfolio from file"""
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        return {"stocks": {}, "cash": 100000, "created": datetime.now().isoformat()}
    
    def save_portfolio(self, portfolio: Dict):
        """Save portfolio to file"""
        with open(self.portfolio_file, 'w') as f:
            json.dump(portfolio, f, indent=2)
    
    def add_stock(self, symbol: str, shares: int, purchase_price: float):
        """Add stock to portfolio"""
        portfolio = self.load_portfolio()
        
        if symbol in portfolio["stocks"]:
            # Update existing position
            existing = portfolio["stocks"][symbol]
            total_shares = existing["shares"] + shares
            avg_price = ((existing["shares"] * existing["avg_price"]) + 
                        (shares * purchase_price)) / total_shares
            
            portfolio["stocks"][symbol] = {
                "shares": total_shares,
                "avg_price": avg_price,
                "last_updated": datetime.now().isoformat()
            }
        else:
            # New position
            portfolio["stocks"][symbol] = {
                "shares": shares,
                "avg_price": purchase_price,
                "last_updated": datetime.now().isoformat()
            }
        
        # Update cash
        portfolio["cash"] -= shares * purchase_price
        self.save_portfolio(portfolio)
    
    def generate_portfolio_report(self, output_dir: str = "reports") -> str:
        """Generate comprehensive portfolio report"""
        portfolio = self.load_portfolio()
        
        if not portfolio["stocks"]:
            raise ValueError("Portfolio is empty")
        
        app = StockReportApp()
        
        # Collect current data for all stocks
        portfolio_data = []
        total_value = 0
        total_cost = 0
        
        for symbol, position in portfolio["stocks"].items():
            try:
                stock_data = app.data_collector.get_stock_data(symbol)
                if stock_data:
                    current_value = position["shares"] * stock_data.price
                    cost_basis = position["shares"] * position["avg_price"]
                    gain_loss = current_value - cost_basis
                    gain_loss_pct = (gain_loss / cost_basis) * 100
                    
                    portfolio_data.append({
                        "symbol": symbol,
                        "name": stock_data.name,
                        "shares": position["shares"],
                        "avg_price": position["avg_price"],
                        "current_price": stock_data.price,
                        "current_value": current_value,
                        "cost_basis": cost_basis,
                        "gain_loss": gain_loss,
                        "gain_loss_pct": gain_loss_pct
                    })
                    
                    total_value += current_value
                    total_cost += cost_basis
                    
            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")
        
        # Generate portfolio PDF report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"portfolio_report_{timestamp}.pdf")
        
        self._generate_portfolio_pdf(portfolio_data, total_value, total_cost, 
                                   portfolio["cash"], output_path)
        
        return output_path
    
    def _generate_portfolio_pdf(self, portfolio_data: List[Dict], total_value: float, 
                               total_cost: float, cash: float, output_path: str):
        """Generate portfolio PDF report"""
        doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                   fontSize=24, spaceAfter=30, textColor=colors.darkblue, 
                                   alignment=TA_CENTER)
        story.append(Paragraph("Portfolio Performance Report", title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary
        total_gain_loss = total_value - total_cost
        total_gain_loss_pct = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Portfolio Value', f'${total_value:,.2f}'],
            ['Total Cost Basis', f'${total_cost:,.2f}'],
            ['Cash Position', f'${cash:,.2f}'],
            ['Total Gain/Loss', f'${total_gain_loss:,.2f}'],
            ['Total Return %', f'{total_gain_loss_pct:+.2f}%']
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Individual positions
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], 
                                     fontSize=16, spaceAfter=12, textColor=colors.darkblue)
        story.append(Paragraph("Individual Positions", heading_style))
        
        position_data = [['Symbol', 'Shares', 'Avg Price', 'Current Price', 'Value', 'Gain/Loss', 'Return %']]
        
        for position in portfolio_data:
            color = colors.green if position['gain_loss'] >= 0 else colors.red
            position_data.append([
                position['symbol'],
                f"{position['shares']:,}",
                f"${position['avg_price']:.2f}",
                f"${position['current_price']:.2f}",
                f"${position['current_value']:,.2f}",
                f"${position['gain_loss']:,.2f}",
                f"{position['gain_loss_pct']:+.2f}%"
            ])
        
        position_table = Table(position_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 
                                                       0.8*inch, 1.2*inch, 1.2*inch, 1*inch])
        position_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(position_table)
        doc.build(story)

class ScheduledReportManager:
    """Manages scheduled report generation"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.schedule_file = "schedule.json"
    
    def add_scheduled_report(self, symbol: str, frequency: str, email: str = None):
        """Add a stock to scheduled reporting"""
        schedule = self.load_schedule()
        
        schedule[symbol] = {
            "frequency": frequency,  # 'daily', 'weekly', 'monthly'
            "email": email,
            "last_generated": None,
            "active": True
        }
        
        self.save_schedule(schedule)
    
    def load_schedule(self) -> Dict:
        """Load schedule from file"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_schedule(self, schedule: Dict):
        """Save schedule to file"""
        with open(self.schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)
    
    def run_scheduled_reports(self):
        """Run all scheduled reports that are due"""
        schedule = self.load_schedule()
        app = StockReportApp()
        
        for symbol, config in schedule.items():
            if not config["active"]:
                continue
            
            # Check if report is due
            if self._is_report_due(config):
                try:
                    logger.info(f"Generating scheduled report for {symbol}")
                    report_path = app.generate_monthly_report(symbol)
                    
                    # Update last generated time
                    config["last_generated"] = datetime.now().isoformat()
                    schedule[symbol] = config
                    self.save_schedule(schedule)
                    
                    # Send email if configured
                    if config.get("email"):
                        self._send_email_report(config["email"], symbol, report_path)
                    
                    logger.info(f"Scheduled report completed for {symbol}")
                    
                except Exception as e:
                    logger.error(f"Error in scheduled report for {symbol}: {e}")
    
    def _is_report_due(self, config: Dict) -> bool:
        """Check if a report is due based on frequency"""
        if not config.get("last_generated"):
            return True
        
        last_gen = datetime.fromisoformat(config["last_generated"])
        now = datetime.now()
        
        if config["frequency"] == "daily":
            return (now - last_gen).days >= 1
        elif config["frequency"] == "weekly":
            return (now - last_gen).days >= 7
        elif config["frequency"] == "monthly":
            return (now - last_gen).days >= 30
        
        return False
    
    def _send_email_report(self, email: str, symbol: str, report_path: str):
        """Send email with report (requires email configuration)"""
        # This would require email configuration (SMTP settings)
        # For now, just log the action
        logger.info(f"Would send report {report_path} for {symbol} to {email}")

class ConfigManager:
    """Manages application configuration and API key validation"""
    
    @staticmethod
    def validate_api_keys(config: APIConfig) -> Dict[str, bool]:
        """Validate API keys by making test requests"""
        results = {}
        
        # Test Alpha Vantage
        if config.ALPHA_VANTAGE_API_KEY != "YOUR_ALPHA_VANTAGE_API_KEY_HERE":
            try:
                params = {
                    'function': 'GLOBAL_QUOTE',
                    'symbol': 'AAPL',
                    'apikey': config.ALPHA_VANTAGE_API_KEY
                }
                response = requests.get(config.ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
                results['alpha_vantage'] = response.status_code == 200 and 'Global Quote' in response.json()
            except:
                results['alpha_vantage'] = False
        else:
            results['alpha_vantage'] = False
        
        # Test FMP
        if config.FMP_API_KEY != "YOUR_FMP_API_KEY_HERE":
            try:
                url = f"{config.FMP_BASE_URL}/profile/AAPL?apikey={config.FMP_API_KEY}"
                response = requests.get(url, timeout=10)
                results['fmp'] = response.status_code == 200 and isinstance(response.json(), list)
            except:
                results['fmp'] = False
        else:
            results['fmp'] = False
        
        # Test News API
        if config.NEWS_API_KEY != "YOUR_NEWS_API_KEY_HERE":
            try:
                params = {
                    'q': 'AAPL',
                    'apiKey': config.NEWS_API_KEY
                }
                response = requests.get(f"{config.NEWS_API_BASE_URL}/everything", params=params, timeout=10)
                results['news_api'] = response.status_code == 200 and response.json().get('status') == 'ok'
            except:
                results['news_api'] = False
        else:
            results['news_api'] = False
        
        # Test OpenAI
        if config.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
            try:
                openai.api_key = config.OPENAI_API_KEY
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                results['openai'] = True
            except:
                results['openai'] = False
        else:
            results['openai'] = False
        
        return results

# =============================================================================
# ENHANCED MAIN APPLICATION WITH ALL FEATURES
# =============================================================================

class EnhancedStockReportApp(StockReportApp):
    """Enhanced version with all advanced features"""
    
    def __init__(self):
        super().__init__()
        self.technical_analyzer = TechnicalAnalyzer()
        self.esg_analyzer = ESGAnalyzer(self.config)
        self.portfolio_manager = PortfolioManager(self.config)
        self.scheduler = ScheduledReportManager(self.config)
    
    def generate_comprehensive_report(self, symbol: str, output_dir: str = "reports") -> str:
        """Generate the most comprehensive report possible"""
        try:
            # Create output directory
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            logger.info(f"Starting comprehensive report generation for {symbol}")
            
            # Collect all data
            stock_data = self.data_collector.get_stock_data(symbol)
            if not stock_data:
                raise ValueError(f"Could not fetch data for symbol: {symbol}")
            
            # Get historical data for technical analysis
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(period="1y")
            
            # Technical analysis
            technical_data = {}
            if not hist_data.empty:
                prices = hist_data['Close']
                technical_data = {
                    'rsi': self.technical_analyzer.calculate_rsi(prices),
                    'moving_averages': self.technical_analyzer.calculate_moving_averages(prices),
                    'bollinger_bands': self.technical_analyzer.calculate_bollinger_bands(prices)
                }
            
            # ESG data
            esg_data = self.esg_analyzer.get_esg_score(symbol)
            
            # Other data
            news_data = self.data_collector.get_news_data(symbol, stock_data.name)
            competitor_data = self.data_collector.get_competitor_data(stock_data.sector, symbol)
            ai_analysis = self.ai_analyzer.generate_analysis(stock_data, news_data, competitor_data)
            
            # Generate enhanced report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"{symbol}_comprehensive_report_{timestamp}.pdf")
            
            self._generate_comprehensive_pdf(
                stock_data, news_data, competitor_data, ai_analysis,
                technical_data, esg_data, output_path
            )
            
            logger.info(f"Comprehensive report completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report for {symbol}: {e}")
            raise
    
    def _generate_comprehensive_pdf(self, stock_data: StockData, news_data: List[Dict],
                                  competitor_data: List[Dict], ai_analysis: str,
                                  technical_data: Dict, esg_data: Dict, output_path: str):
        """Generate comprehensive PDF with all features"""
        doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Title page
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                   fontSize=28, spaceAfter=30, textColor=colors.darkblue,
                                   alignment=TA_CENTER)
        
        story.append(Paragraph(f"{stock_data.name} ({stock_data.symbol})", title_style))
        story.append(Paragraph("Comprehensive Stock Analysis Report", styles['Heading2']))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 50))
        
        # Table of contents
        story.append(Paragraph("Table of Contents", styles['Heading2']))
        toc_items = [
            "1. Executive Summary",
            "2. Financial Metrics",
            "3. Technical Analysis",
            "4. ESG Analysis",
            "5. Competitive Landscape",
            "6. Recent News & Developments",
            "7. AI-Powered Analysis",
            "8. Risk Assessment",
            "9. Investment Recommendation"
        ]
        
        for item in toc_items:
            story.append(Paragraph(item, styles['Normal']))
        
        story.append(PageBreak())
        
        # Call parent's report generation for basic content
        self.report_generator.generate_report(stock_data, news_data, competitor_data, ai_analysis, 
                                            output_path.replace('.pdf', '_temp.pdf'))
        
        # Add technical analysis section
        if technical_data:
            story.append(Paragraph("Technical Analysis", styles['Heading2']))
            
            if 'rsi' in technical_data:
                rsi_interpretation = "Oversold" if technical_data['rsi'] < 30 else "Overbought" if technical_data['rsi'] > 70 else "Neutral"
                story.append(Paragraph(f"RSI (14-day): {technical_data['rsi']:.1f} - {rsi_interpretation}", styles['Normal']))
            
            if 'moving_averages' in technical_data:
                ma_data = technical_data['moving_averages']
                story.append(Paragraph(f"Moving Averages:", styles['Normal']))
                story.append(Paragraph(f"  • 20-day SMA: ${ma_data.get('sma_20', 0):.2f}", styles['Normal']))
                story.append(Paragraph(f"  • 50-day SMA: ${ma_data.get('sma_50', 0):.2f}", styles['Normal']))
                story.append(Paragraph(f"  • 200-day SMA: ${ma_data.get('sma_200', 0):.2f}", styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        # Add ESG section
        if esg_data:
            story.append(Paragraph("ESG Analysis", styles['Heading2']))
            story.append(Paragraph(f"Overall ESG Score: {esg_data['overall_score']}/100 (Rating: {esg_data['rating']})", styles['Normal']))
            story.append(Paragraph(f"Environmental Score: {esg_data['environmental']}/100", styles['Normal']))
            story.append(Paragraph(f"Social Score: {esg_data['social']}/100", styles['Normal']))
            story.append(Paragraph(f"Governance Score: {esg_data['governance']}/100", styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(story)
        
        # Clean up temp file
        temp_file = output_path.replace('.pdf', '_temp.pdf')
        if os.path.exists(temp_file):
            os.remove(temp_file)

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def create_cli():
    """Create command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Stock Report Generator')
    parser.add_argument('command', choices=['report', 'portfolio', 'schedule', 'validate'], 
                       help='Command to execute')
    parser.add_argument('--symbol', '-s', help='Stock symbol (e.g., AAPL)')
    parser.add_argument('--symbols', nargs='+', help='Multiple stock symbols')
    parser.add_argument('--output', '-o', default='reports', help='Output directory')
    parser.add_argument('--comprehensive', '-c', action='store_true', 
                       help='Generate comprehensive report')
    parser.add_argument('--email', help='Email address for scheduled reports')
    parser.add_argument('--frequency', choices=['daily', 'weekly', 'monthly'], 
                       default='monthly', help='Report frequency')
    
    return parser

def main_cli():
    """Main CLI function"""
    parser = create_cli()
    args = parser.parse_args()
    
    app = EnhancedStockReportApp()
    
    try:
        if args.command == 'report':
            if args.symbol:
                if args.comprehensive:
                    report_path = app.generate_comprehensive_report(args.symbol, args.output)
                else:
                    report_path = app.generate_monthly_report(args.symbol, args.output)
                print(f"Report generated: {report_path}")
            
            elif args.symbols:
                report_paths = app.generate_batch_reports(args.symbols, args.output)
                print(f"Generated {len(report_paths)} reports:")
                for path in report_paths:
                    print(f"  - {path}")
            
            else:
                print("Error: Please specify --symbol or --symbols")
        
        elif args.command == 'portfolio':
            report_path = app.portfolio_manager.generate_portfolio_report(args.output)
            print(f"Portfolio report generated: {report_path}")
        
        elif args.command == 'schedule':
            if args.symbol and args.frequency:
                app.scheduler.add_scheduled_report(args.symbol, args.frequency, args.email)
                print(f"Added {args.symbol} to {args.frequency} schedule")
            else:
                # Run scheduled reports
                app.scheduler.run_scheduled_reports()
                print("Scheduled reports completed")
        
        elif args.command == 'validate':
            results = ConfigManager.validate_api_keys(app.config)
            print("API Key Validation Results:")
            for service, status in results.items():
                status_text = "✓ Valid" if status else "✗ Invalid/Missing"
                print(f"  {service}: {status_text}")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

# =============================================================================
# INSTALLATION REQUIREMENTS
# =============================================================================
"""
To install all required packages, run:

pip install -r requirements.txt

Where requirements.txt contains:
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

For additional data sources, also install:
pip install quandl
pip install alpha_vantage
pip install polygon-api-client

Usage Examples:
===============

1. Generate single report:
   python stock_report.py report --symbol AAPL

2. Generate comprehensive report:
   python stock_report.py report --symbol AAPL --comprehensive

3. Generate batch reports:
   python stock_report.py report --symbols AAPL MSFT GOOGL

4. Generate portfolio report:
   python stock_report.py portfolio

5. Add stock to schedule:
   python stock_report.py schedule --symbol AAPL --frequency monthly --email user@example.com

6. Run scheduled reports:
   python stock_report.py schedule

7. Validate API keys:
   python stock_report.py validate

Environment Variables (Alternative to hardcoding):
================================================
You can also set API keys as environment variables:

export ALPHA_VANTAGE_API_KEY="your_key_here"
export FMP_API_KEY="your_key_here"
export NEWS_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
export POLYGON_API_KEY="your_key_here"

Then modify the APIConfig class to read from environment variables:
self.ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'YOUR_ALPHA_VANTAGE_API_KEY_HERE')
"""

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sys.exit(main_cli())
    else:
        main()