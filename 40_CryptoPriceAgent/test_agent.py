#!/usr/bin/env python3
"""
Test script for CryptoInsightsAgent
Tests basic functionality without requiring API keys
"""

import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from crypto_agent import CoinGeckoAgent, OpenAIAgent, PortfolioManager, RiskAnalyzer
    from config import get_default_currency, get_default_cryptos
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the 40_CryptoPriceAgent directory")
    sys.exit(1)


def test_portfolio_manager():
    """Test portfolio management functionality"""
    print("🧪 Testing Portfolio Manager...")
    
    # Create a test portfolio manager
    portfolio_manager = PortfolioManager()
    
    # Test adding holdings
    success = portfolio_manager.add_holding("bitcoin", 0.5, 45000)
    assert success, "Failed to add bitcoin holding"
    
    success = portfolio_manager.add_holding("ethereum", 2.0, 3000)
    assert success, "Failed to add ethereum holding"
    
    # Test getting portfolio
    portfolio = portfolio_manager.get_portfolio()
    assert "bitcoin" in portfolio["holdings"], "Bitcoin not in portfolio"
    assert "ethereum" in portfolio["holdings"], "Ethereum not in portfolio"
    
    # Test removing holdings
    success = portfolio_manager.remove_holding("bitcoin", 0.1)
    assert success, "Failed to remove partial bitcoin holding"
    
    # Check remaining amount
    remaining = portfolio_manager.get_portfolio()["holdings"]["bitcoin"]["amount"]
    assert remaining == 0.4, f"Expected 0.4 bitcoin, got {remaining}"
    
    print("✅ Portfolio Manager tests passed!")


def test_risk_analyzer():
    """Test risk analysis functionality"""
    print("🧪 Testing Risk Analyzer...")
    
    # Test individual crypto risk calculation
    risk_level, risk_emoji = RiskAnalyzer.calculate_risk_level(2.5)
    assert risk_level == "Low", f"Expected Low risk, got {risk_level}"
    assert risk_emoji == "🟢", f"Expected green emoji, got {risk_emoji}"
    
    risk_level, risk_emoji = RiskAnalyzer.calculate_risk_level(8.0)
    assert risk_level == "Medium", f"Expected Medium risk, got {risk_level}"
    assert risk_emoji == "🟡", f"Expected yellow emoji, got {risk_emoji}"
    
    risk_level, risk_emoji = RiskAnalyzer.calculate_risk_level(20.0)
    assert risk_level == "High", f"Expected High risk, got {risk_level}"
    assert risk_emoji == "🔴", f"Expected red emoji, got {risk_emoji}"
    
    # Test portfolio risk analysis
    test_portfolio = {
        "holdings": {
            "bitcoin": {"pnl_percentage": 15.0},
            "ethereum": {"pnl_percentage": -25.0},
            "cardano": {"pnl_percentage": 5.0}
        }
    }
    
    risk_analysis = RiskAnalyzer.analyze_portfolio_risk(test_portfolio)
    assert "risk_level" in risk_analysis, "Risk analysis missing risk_level"
    assert "risk_emoji" in risk_analysis, "Risk analysis missing risk_emoji"
    assert "factors" in risk_analysis, "Risk analysis missing factors"
    
    print("✅ Risk Analyzer tests passed!")


@patch('crypto_agent.requests.get')
def test_coingecko_agent_mock(mock_get):
    """Test CoinGecko agent with mocked responses"""
    print("🧪 Testing CoinGecko Agent (mocked)...")
    
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 45000,
            "price_change_percentage_24h": 2.5,
            "market_cap": 850000000000,
            "market_cap_rank": 1
        }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    # Test the agent
    agent = CoinGeckoAgent()
    cryptos = agent.get_top_cryptos(1, "usd")
    
    assert len(cryptos) == 1, f"Expected 1 crypto, got {len(cryptos)}"
    assert cryptos[0]["id"] == "bitcoin", f"Expected bitcoin, got {cryptos[0]['id']}"
    
    print("✅ CoinGecko Agent tests passed!")


def test_config():
    """Test configuration functionality"""
    print("🧪 Testing Configuration...")
    
    # Test default values
    currency = get_default_currency()
    assert currency == "usd", f"Expected usd, got {currency}"
    
    cryptos = get_default_cryptos()
    assert isinstance(cryptos, list), "Default cryptos should be a list"
    assert len(cryptos) > 0, "Default cryptos should not be empty"
    assert "bitcoin" in cryptos, "Bitcoin should be in default cryptos"
    
    print("✅ Configuration tests passed!")


def test_portfolio_calculations():
    """Test portfolio value calculations with mock data"""
    print("🧪 Testing Portfolio Calculations...")
    
    # Create portfolio manager
    portfolio_manager = PortfolioManager()
    
    # Clear any existing holdings first
    portfolio_manager.portfolio["holdings"] = {}
    
    # Add test holdings
    portfolio_manager.add_holding("bitcoin", 0.5, 40000)  # Invested: $20,000
    portfolio_manager.add_holding("ethereum", 2.0, 2500)  # Invested: $5,000
    
    # Mock the crypto agent for price fetching
    with patch.object(CoinGeckoAgent, 'get_crypto_prices') as mock_prices:
        mock_prices.return_value = {
            "bitcoin": {"usd": 45000},  # Current price higher
            "ethereum": {"usd": 2000}   # Current price lower
        }
        
        # Calculate portfolio value
        portfolio_value = portfolio_manager.get_portfolio_value(CoinGeckoAgent(), "usd")
        
        # Verify calculations
        assert portfolio_value["total_invested"] == 25000, f"Expected $25,000 invested, got ${portfolio_value['total_invested']}"
        assert portfolio_value["total_value"] == 26500, f"Expected $26,500 value, got ${portfolio_value['total_value']}"
        assert portfolio_value["pnl"] == 1500, f"Expected $1,500 P&L, got ${portfolio_value['pnl']}"
        assert abs(portfolio_value["pnl_percentage"] - 6.0) < 0.1, f"Expected ~6% P&L, got {portfolio_value['pnl_percentage']}%"
        
        # Check individual holdings
        btc_holding = portfolio_value["holdings"]["bitcoin"]
        assert btc_holding["current_value"] == 22500, f"Expected $22,500 BTC value, got ${btc_holding['current_value']}"
        assert btc_holding["pnl"] == 2500, f"Expected $2,500 BTC P&L, got ${btc_holding['pnl']}"
        
        eth_holding = portfolio_value["holdings"]["ethereum"]
        assert eth_holding["current_value"] == 4000, f"Expected $4,000 ETH value, got ${eth_holding['current_value']}"
        assert eth_holding["pnl"] == -1000, f"Expected -$1,000 ETH P&L, got ${eth_holding['pnl']}"
    
    print("✅ Portfolio Calculations tests passed!")


def cleanup_test_files():
    """Clean up test files"""
    print("🧹 Cleaning up test files...")
    
    test_files = ["portfolio.json", "cache.json"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")
    
    print("✅ Cleanup completed!")


def main():
    """Run all tests"""
    print("🚀 Starting CryptoInsightsAgent Tests...")
    print("=" * 50)
    
    try:
        test_config()
        test_portfolio_manager()
        test_risk_analyzer()
        test_coingecko_agent_mock()
        test_portfolio_calculations()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        print("\nThe CryptoInsightsAgent is working correctly!")
        print("You can now run the main application with: python main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        cleanup_test_files()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
