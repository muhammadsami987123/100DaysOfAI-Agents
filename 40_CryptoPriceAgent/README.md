# ₿ CryptoInsightsAgent - Day 40 of #100DaysOfAI-Agents

<div align="center">

![CryptoInsightsAgent Banner](https://img.shields.io/badge/CryptoInsightsAgent-Day%2040-blue?style=for-the-badge&logo=bitcoin&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?style=for-the-badge&logo=openai&logoColor=white)
![CoinGecko](https://img.shields.io/badge/CoinGecko-API-red?style=for-the-badge&logo=coingecko&logoColor=white)

**Your intelligent cryptocurrency assistant for real-time prices, portfolio tracking, and AI-powered market insights**

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [💼 Portfolio](#-portfolio-management) • [📈 Market Analysis](#-market-analysis) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is CryptoInsightsAgent?

CryptoInsightsAgent is a comprehensive cryptocurrency intelligence platform that combines real-time market data with AI-powered analysis to help you make informed investment decisions. Whether you're a seasoned trader, casual investor, or crypto enthusiast, this agent provides everything you need to track, analyze, and understand the cryptocurrency market.

### 🌟 Key Highlights

- **📈 Real-Time Prices**: Live cryptocurrency prices from CoinGecko API
- **💼 Portfolio Tracking**: Complete portfolio management with P&L calculations
- **🧠 AI Market Insights**: GPT-powered market analysis and trend identification
- **⚠️ Risk Analysis**: Automated risk assessment based on volatility metrics
- **🔍 Crypto Search**: Find and analyze any cryptocurrency by name or symbol
- **🌍 Multi-Currency**: Support for USD, EUR, GBP, JPY, INR, and more
- **⌨️ Rich CLI**: Beautiful command-line interface with tables and animations

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Real-Time Data**: Live cryptocurrency prices and market data
- ✅ **Portfolio Management**: Track investments with detailed P&L analysis
- ✅ **AI-Powered Insights**: Market sentiment and trend analysis using GPT
- ✅ **Risk Assessment**: Automated risk level calculation and recommendations
- ✅ **Interactive CLI**: Rich terminal interface with progress indicators
- ✅ **Multi-Currency Support**: Display prices in your preferred currency
- ✅ **Cryptocurrency Search**: Find any crypto by name, symbol, or ID

### 💼 Portfolio Features
- ✅ **Holdings Tracking**: Add, remove, and manage cryptocurrency holdings
- ✅ **P&L Calculations**: Real-time profit/loss with percentage changes
- ✅ **Performance Analytics**: Track investment performance over time
- ✅ **Risk Metrics**: Portfolio-wide risk assessment and analysis
- ✅ **Multi-Currency Portfolio**: Display portfolio in different currencies
- ✅ **Investment History**: Track purchase prices and investment amounts

### 📊 Market Analysis
- ✅ **Top Cryptocurrencies**: View top 10-100 cryptos by market cap
- ✅ **Price Movements**: 24-hour price changes with color-coded indicators
- ✅ **Market Cap Data**: Current market capitalization and rankings
- ✅ **Volatility Analysis**: Risk level assessment based on price movements
- ✅ **Trend Identification**: AI-powered market trend analysis
- ✅ **Sentiment Analysis**: Market sentiment based on price movements

### 🧠 AI-Powered Insights
- ✅ **Market Commentary**: Professional market analysis and commentary
- ✅ **Risk Recommendations**: AI-generated risk assessment and advice
- ✅ **Trend Analysis**: Identification of key market patterns and trends
- ✅ **Portfolio Optimization**: Suggestions for portfolio improvement
- ✅ **Market Sentiment**: Overall market sentiment and outlook
- ✅ **Investment Guidance**: Professional investment insights and recommendations

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **OpenAI API Key** (optional, for AI insights)
- **Internet connection** for real-time data

### ⚡ One-Click Installation

```bash
# Windows - Run the installer
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create virtual environment
# ✅ Install all dependencies
# ✅ Set up configuration files
# ✅ Create .env template
```

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 40_CryptoPriceAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment
echo OPENAI_API_KEY=your_api_key_here > .env
```

### 🎯 First Run

```bash
# Option 1: Interactive Mode (Recommended)
python main.py

# Option 2: Quick Price Lookup
python main.py bitcoin usd

# Option 3: Run Demo
python demo.py

# Option 4: Run Tests
python test_agent.py
```

### 🧪 Verify Installation

```bash
# Run the test suite
python test_agent.py

# Expected output:
# ✅ Configuration tests passed!
# ✅ Portfolio Manager tests passed!
# ✅ Risk Analyzer tests passed!
# ✅ CoinGecko Agent tests passed!
# ✅ Portfolio Calculations tests passed!
# 🎉 All tests passed successfully!
```

## 💼 Portfolio Management

### 📊 Adding Holdings

Track your cryptocurrency investments with detailed information:

```bash
python main.py
# Select option 2: Manage portfolio
# Add holding: bitcoin, 0.5, 45000
# Add holding: ethereum, 2.0, 3000
```

**Portfolio Features:**
- **Purchase Price Tracking**: Record your entry prices
- **Real-Time Valuation**: Current market value calculations
- **P&L Analysis**: Profit/loss with percentage changes
- **Performance Metrics**: Track investment performance
- **Risk Assessment**: Individual and portfolio risk analysis

### 📈 Portfolio Analytics

| Metric | Description | Example |
|--------|-------------|---------|
| **Total Value** | Current market value of all holdings | $15,750.00 |
| **Total Invested** | Original investment amount | $15,000.00 |
| **P&L** | Profit/Loss in absolute terms | +$750.00 |
| **P&L %** | Profit/Loss percentage | +5.0% |
| **Risk Level** | Overall portfolio risk assessment | Medium 🟡 |

### ⚠️ Risk Analysis

The agent provides comprehensive risk analysis:

- **Individual Risk**: Each cryptocurrency's risk level (Low/Medium/High)
- **Portfolio Risk**: Overall portfolio risk assessment
- **AI Analysis**: GPT-powered risk insights and recommendations
- **Risk Factors**: Identification of key risk factors
- **Volatility Metrics**: 24-hour price change analysis

## 📈 Market Analysis

### 🔍 Cryptocurrency Search

Find and analyze any cryptocurrency:

```bash
python main.py
# Select option 3: Search cryptocurrency
# Search for "ethereum" or "ETH"
# Get detailed information including:
# - Current price and 24h change
# - Market cap and ranking
# - Risk level assessment
```

### 📊 Top Cryptocurrencies

View the top cryptocurrencies by market cap:

```bash
python main.py
# Select option 1: Get crypto prices
# Choose number of cryptos (10-100)
# Select currency (USD, EUR, GBP, etc.)
```

**Market Data Includes:**
- **Real-Time Prices**: Current market prices
- **24h Changes**: Price movements with color coding
- **Market Cap**: Current market capitalization
- **Risk Levels**: Automatic risk assessment
- **Rankings**: Market cap rankings

### 🧠 AI Market Insights

When OpenAI API key is configured, get professional market analysis:

- **Market Sentiment**: Overall market outlook and sentiment
- **Trend Analysis**: Key market patterns and trends
- **Risk Assessment**: Professional risk analysis
- **Investment Guidance**: AI-generated recommendations
- **Market Commentary**: Professional market commentary

## 🎭 Examples & Usage

### 🌐 Interactive Mode

The main interface provides a comprehensive menu system:

1. **📈 Get Crypto Prices**: View top cryptocurrencies with real-time data
2. **💼 Manage Portfolio**: Add/remove holdings and track performance
3. **🔍 Search Cryptocurrency**: Find specific cryptocurrencies
4. **🚪 Exit**: Close the application

### 💻 Command Line Usage

Generate quick price lookups and analysis:

```bash
# 🚀 Basic price lookup
python main.py bitcoin usd

# 🌍 Multi-currency support
python main.py ethereum eur
python main.py cardano gbp
python main.py solana jpy

# 📊 Portfolio analysis
python main.py
# Navigate to portfolio management
# View current holdings and P&L
```

### 📚 Usage Examples

Here are some example workflows:

| Use Case | Command | Expected Output |
|----------|---------|----------------|
| **Price Check** | `python main.py bitcoin usd` | Current Bitcoin price in USD |
| **Portfolio Review** | Interactive mode → Portfolio | P&L analysis and risk assessment |
| **Market Research** | Interactive mode → Search | Detailed crypto information |
| **Market Overview** | Interactive mode → Prices | Top 10 cryptos with trends |

### 🎨 Advanced Features

**📊 Portfolio Analytics:**
- Real-time P&L calculations
- Performance tracking over time
- Risk level assessment
- Multi-currency support

**🧠 AI Insights:**
- Market sentiment analysis
- Trend identification
- Risk recommendations
- Investment guidance

**🔍 Search & Discovery:**
- Find cryptocurrencies by name or symbol
- Get detailed market information
- Risk level assessment
- Market cap and ranking data

## 🏗️ Project Architecture

### 📁 File Structure

```
40_CryptoPriceAgent/
├── 📄 main.py                   # Main CLI application with interactive menu
├── 🤖 crypto_agent.py           # Core agent classes and logic
├── ⚙️ config.py                 # Configuration and settings management
├── 📋 requirements.txt          # Python dependencies
├── 🧪 test_agent.py             # Comprehensive test suite
├── 🎬 demo.py                   # Interactive demo showcasing features
├── 📦 install.bat               # Windows installation script
├── 🚀 start.bat                 # Windows startup script
├── 📄 README.md                # This comprehensive documentation
├── 📄 env.example              # Environment variables template
├── 💾 portfolio.json           # Portfolio data storage (auto-created)
└── 💾 cache.json               # API response cache (auto-created)
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **AI Engine** | OpenAI GPT-4 | Market insights and analysis |
| **Data Source** | CoinGecko API | Real-time cryptocurrency data |
| **CLI Framework** | Typer + Rich | Interactive command-line interface |
| **Data Storage** | JSON + File System | Portfolio and cache persistence |
| **Configuration** | Python-dotenv | Environment variable management |

### 🎯 Key Components

#### 🤖 CoinGeckoAgent (`crypto_agent.py`)
- **Real-Time Data**: Fetches live cryptocurrency prices and market data
- **API Integration**: Handles CoinGecko API requests and responses
- **Error Handling**: Robust error handling and retry logic
- **Rate Limiting**: Respects API rate limits and timeouts

#### 🧠 OpenAIAgent (`crypto_agent.py`)
- **Market Analysis**: Generates AI-powered market insights
- **Risk Assessment**: Provides professional risk analysis
- **Trend Identification**: Identifies key market patterns
- **Investment Guidance**: Offers professional recommendations

#### 💼 PortfolioManager (`crypto_agent.py`)
- **Holdings Management**: Add, remove, and track cryptocurrency holdings
- **P&L Calculations**: Real-time profit/loss calculations
- **Performance Tracking**: Track investment performance over time
- **Multi-Currency Support**: Display portfolio in different currencies

#### ⚠️ RiskAnalyzer (`crypto_agent.py`)
- **Risk Calculation**: Calculate risk levels based on volatility
- **Portfolio Analysis**: Analyze overall portfolio risk
- **Risk Factors**: Identify key risk factors
- **Recommendations**: Provide risk-based recommendations

#### ⚙️ Configuration (`config.py`)
- **Settings Management**: Centralized configuration management
- **API Integration**: API key and endpoint configuration
- **Default Settings**: Default currencies and cryptocurrencies
- **Environment Variables**: Secure API key management

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get OpenAI API Key (Optional)**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-`)

**Step 2: Get CoinGecko API Key (Optional)**
1. Visit [CoinGecko API](https://www.coingecko.com/en/api)
2. Sign up for a free account
3. Navigate to API section
4. Copy your API key

**Step 3: Configure the Keys**

```bash
# Option 1: Environment Variables (Recommended)
# Windows
set OPENAI_API_KEY=sk-your_actual_api_key_here
set COINGECKO_API_KEY=your_coingecko_api_key_here

# Linux/Mac
export OPENAI_API_KEY=sk-your_actual_api_key_here
export COINGECKO_API_KEY=your_coingecko_api_key_here

# Option 2: .env File
echo OPENAI_API_KEY=sk-your_actual_api_key_here > .env
echo COINGECKO_API_KEY=your_coingecko_api_key_here >> .env
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize the application:

```python
# API Configuration
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
REQUEST_TIMEOUT_SECONDS = 10
COINGECKO_API_KEY = ""

# OpenAI Configuration
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-4o-mini"

# Default Settings
DEFAULT_CURRENCY = "usd"
DEFAULT_CRYPTOS = ["bitcoin", "ethereum", "binancecoin", "cardano", "solana"]

# Portfolio Settings
PORTFOLIO_CURRENCY = "usd"
```

### 🌍 Currency Configuration

The agent supports multiple currencies:

| Currency | Code | Symbol | Example |
|----------|------|--------|---------|
| **US Dollar** | `usd` | $ | $45,000.00 |
| **Euro** | `eur` | € | €42,000.00 |
| **British Pound** | `gbp` | £ | £35,000.00 |
| **Japanese Yen** | `jpy` | ¥ | ¥6,500,000 |
| **Indian Rupee** | `inr` | ₹ | ₹3,750,000 |
| **Canadian Dollar** | `cad` | C$ | C$60,000.00 |

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

Run the comprehensive test suite to verify everything is working:

```bash
python test_agent.py
```

**Test Coverage:**
- ✅ **Configuration**: Settings and environment variables
- ✅ **Portfolio Manager**: Holdings management and calculations
- ✅ **Risk Analyzer**: Risk level calculations and analysis
- ✅ **CoinGecko Agent**: API integration and data fetching
- ✅ **Portfolio Calculations**: P&L and performance calculations

### 🚀 Performance Testing

```bash
# Test real-time price fetching
python main.py bitcoin usd

# Test portfolio calculations
python main.py
# Navigate to portfolio management
# Add test holdings and verify calculations
```

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"API request failed"** | Network connectivity or API limits | Check internet connection and API key |
| **"Portfolio not found"** | Missing portfolio.json file | Run portfolio management to create file |
| **"OpenAI API error"** | Invalid or missing API key | Set OPENAI_API_KEY environment variable |
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Permission denied"** | File system permissions | Run with appropriate permissions |

### 📊 Performance Metrics

**Expected Performance:**
- **Price Fetching**: 1-3 seconds for top cryptocurrencies
- **Portfolio Calculations**: <1 second for typical portfolios
- **AI Insights**: 3-5 seconds for market analysis
- **Search Results**: 1-2 seconds for cryptocurrency search
- **Memory Usage**: <50MB typical

### 🔒 Security Considerations

- **API Key Security**: Never commit API keys to version control
- **Local Storage**: Portfolio data stored locally, not sent to external services
- **Input Validation**: All user inputs are sanitized and validated
- **Error Handling**: Sensitive information not exposed in error messages

## 💡 Best Practices & Tips

### 💼 Portfolio Management

**📊 Effective Portfolio Tracking:**
- **Record Purchase Prices**: Always record your entry prices for accurate P&L
- **Regular Updates**: Check portfolio regularly for performance tracking
- **Diversification**: Track multiple cryptocurrencies for risk management
- **Currency Consistency**: Use consistent currency for all holdings

**⚠️ Risk Management:**
- **Monitor Risk Levels**: Pay attention to individual and portfolio risk levels
- **AI Insights**: Use AI analysis for professional risk assessment
- **Volatility Tracking**: Monitor 24-hour price changes for volatility
- **Diversification**: Spread investments across different cryptocurrencies

### 📈 Market Analysis

**🔍 Effective Research:**
- **Use Search Feature**: Find specific cryptocurrencies quickly
- **Check Top Cryptos**: Monitor top cryptocurrencies for market trends
- **AI Insights**: Leverage AI analysis for market understanding
- **Risk Assessment**: Use risk levels for investment decisions

**📊 Data Interpretation:**
- **Price Changes**: Green for gains, red for losses
- **Risk Levels**: 🟢 Low, 🟡 Medium, 🔴 High risk
- **Market Cap**: Larger market cap = more established
- **24h Changes**: Short-term price movement indicators

### 🚀 Performance Optimization

**⚡ Faster Operations:**
- **Use Quick Lookup**: `python main.py bitcoin usd` for fast price checks
- **Cache Data**: API responses are cached for faster subsequent requests
- **Batch Operations**: Add multiple holdings at once
- **Efficient Search**: Use specific search terms for better results

**💾 Better Organization:**
- **Descriptive Holdings**: Use clear cryptocurrency IDs
- **Regular Backups**: Portfolio data is automatically saved
- **Export Data**: Use portfolio data for external analysis
- **Track Performance**: Monitor P&L over time

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Price Alerts** | 🔄 Planned | Set price alerts for specific cryptocurrencies |
| **Historical Data** | 🔄 Planned | View historical price charts and data |
| **Portfolio Charts** | 🔄 Planned | Visual portfolio performance charts |
| **Export Options** | 🔄 Planned | Export portfolio data to CSV/Excel |
| **Mobile App** | 🔄 Planned | Native mobile application |
| **Web Interface** | 🔄 Planned | Web-based user interface |
| **Advanced Analytics** | 🔄 Planned | Detailed portfolio analytics and insights |
| **Social Features** | 🔄 Planned | Share portfolio performance and insights |

### 🎯 Enhancement Ideas

- **Real-time Notifications**: Price alerts and portfolio notifications
- **Advanced Charts**: Interactive price and portfolio charts
- **Portfolio Optimization**: AI-powered portfolio rebalancing suggestions
- **News Integration**: Cryptocurrency news and market updates
- **Trading Integration**: Connect with cryptocurrency exchanges
- **Tax Reporting**: Generate tax reports for cryptocurrency investments
- **Advanced Risk Models**: More sophisticated risk assessment models
- **Portfolio Backtesting**: Historical portfolio performance analysis

## 🤝 Contributing

We welcome contributions to make CryptoInsightsAgent even better!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Features**: Add new cryptocurrency data sources
- **UI Improvements**: Enhance the command-line interface
- **Performance**: Optimize API calls and data processing
- **Documentation**: Improve guides and examples
- **Testing**: Add more test cases and scenarios
- **Bug Fixes**: Report and fix issues
- **API Integration**: Add support for more cryptocurrency APIs

### 📋 Contribution Guidelines

- Follow the existing code style and patterns
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass
- Be respectful and constructive in discussions

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Check this README and code comments
2. **🧪 Test Suite**: Run `python test_agent.py`
3. **🔍 Troubleshooting**: Review the troubleshooting section
4. **📊 Logs**: Check console output for error messages
5. **🌐 API Status**: Verify CoinGecko and OpenAI APIs are operational

### 🐛 Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, terminal
- **Error Messages**: Full error output and stack traces
- **Steps to Reproduce**: What you were doing when it happened
- **Expected vs Actual**: What you expected vs what happened
- **Configuration**: Your .env file (without API keys)

### 💬 Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Showcase**: Share your portfolio insights and market analysis

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **CoinGecko** for providing comprehensive cryptocurrency data
- **OpenAI** for providing the GPT-4 API for market insights
- **Python community** for amazing libraries and tools
- **All contributors** who help improve this project

### 🌟 Inspiration

This project was inspired by the need for accessible cryptocurrency tools that are:
- **Comprehensive**: Covering prices, portfolio, and analysis
- **Intelligent**: AI-powered insights and recommendations
- **User-Friendly**: Easy to use for all skill levels
- **Professional**: Providing institutional-quality analysis

---

<div align="center">

## 🎉 Ready to Start Trading?

**Transform your cryptocurrency investments with intelligent insights and real-time analysis!**

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [💼 Portfolio](#-portfolio-management) • [📈 Market Analysis](#-market-analysis) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 40 of 100 - Building the future of AI agents, one day at a time!*

</div>
