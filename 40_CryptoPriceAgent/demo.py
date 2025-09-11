#!/usr/bin/env python3
"""
Demo script for CryptoInsightsAgent
Shows the agent's capabilities with sample data
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crypto_agent import CoinGeckoAgent, OpenAIAgent, PortfolioManager, RiskAnalyzer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

console = Console()


def demo_crypto_prices():
    """Demo cryptocurrency price display"""
    console.print(Panel("📈 Cryptocurrency Prices Demo", style="cyan"))
    
    # Sample crypto data
    sample_cryptos = [
        {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 114217.00,
            "price_change_percentage_24h": 2.42,
            "market_cap": 2250000000000,
            "market_cap_rank": 1
        },
        {
            "id": "ethereum",
            "name": "Ethereum",
            "symbol": "eth",
            "current_price": 3845.50,
            "price_change_percentage_24h": -1.25,
            "market_cap": 462000000000,
            "market_cap_rank": 2
        },
        {
            "id": "binancecoin",
            "name": "BNB",
            "symbol": "bnb",
            "current_price": 715.20,
            "price_change_percentage_24h": 5.67,
            "market_cap": 108000000000,
            "market_cap_rank": 3
        }
    ]
    
    # Display in table format
    table = Table(title="Top Cryptocurrencies (Demo Data)")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Name", style="magenta", width=15)
    table.add_column("Symbol", style="blue", width=8)
    table.add_column("Price", style="green", width=12)
    table.add_column("24h Change", style="yellow", width=12)
    table.add_column("Market Cap", style="white", width=15)
    table.add_column("Risk", style="red", width=8)
    
    for crypto in sample_cryptos:
        rank = crypto.get('market_cap_rank', 'N/A')
        name = crypto.get('name', 'Unknown')
        symbol = crypto.get('symbol', '').upper()
        price = crypto.get('current_price', 0)
        change_24h = crypto.get('price_change_percentage_24h', 0)
        market_cap = crypto.get('market_cap', 0)
        
        # Calculate risk level
        risk_level, risk_emoji = RiskAnalyzer.calculate_risk_level(change_24h)
        
        # Format currency and percentage
        price_str = f"${price:,.2f}"
        change_str = f"+{change_24h:.2f}%" if change_24h > 0 else f"{change_24h:.2f}%"
        market_cap_str = f"${market_cap / 1e9:.1f}B"
        
        table.add_row(
            str(rank),
            name,
            symbol,
            price_str,
            change_str,
            market_cap_str,
            f"{risk_emoji} {risk_level}"
        )
    
    console.print(table)


def demo_portfolio():
    """Demo portfolio tracking"""
    console.print(Panel("💼 Portfolio Tracking Demo", style="cyan"))
    
    # Create sample portfolio data
    sample_portfolio = {
        "total_value": 15750.00,
        "total_invested": 15000.00,
        "pnl": 750.00,
        "pnl_percentage": 5.0,
        "holdings": {
            "bitcoin": {
                "amount": 0.1,
                "current_price": 114217.00,
                "current_value": 11421.70,
                "invested": 10000.00,
                "pnl": 1421.70,
                "pnl_percentage": 14.22
            },
            "ethereum": {
                "amount": 1.0,
                "current_price": 3845.50,
                "current_value": 3845.50,
                "invested": 4000.00,
                "pnl": -154.50,
                "pnl_percentage": -3.86
            },
            "binancecoin": {
                "amount": 5.0,
                "current_price": 715.20,
                "current_value": 3576.00,
                "invested": 1000.00,
                "pnl": 2576.00,
                "pnl_percentage": 257.60
            }
        }
    }
    
    # Portfolio summary
    summary_md = f"""
### 📊 Portfolio Summary

- **Total Value**: ${sample_portfolio['total_value']:,.2f}
- **Total Invested**: ${sample_portfolio['total_invested']:,.2f}
- **P&L**: ${sample_portfolio['pnl']:,.2f} (+{sample_portfolio['pnl_percentage']:.1f}%)

🎉 **Portfolio is in profit!**
"""
    console.print(Panel(Markdown(summary_md), title="Portfolio Summary", border_style="green"))
    
    # Individual holdings table
    table = Table(title="Individual Holdings")
    table.add_column("Crypto", style="cyan", width=12)
    table.add_column("Amount", style="blue", width=12)
    table.add_column("Current Price", style="green", width=12)
    table.add_column("Current Value", style="white", width=12)
    table.add_column("Invested", style="yellow", width=12)
    table.add_column("P&L", style="red", width=12)
    
    for crypto_id, holding in sample_portfolio["holdings"].items():
        amount = holding["amount"]
        current_price = holding["current_price"]
        current_value = holding["current_value"]
        invested = holding["invested"]
        pnl = holding["pnl"]
        pnl_percentage = holding["pnl_percentage"]
        
        pnl_str = f"${pnl:,.2f} ({pnl_percentage:+.1f}%)"
        
        table.add_row(
            crypto_id.upper(),
            f"{amount:.6f}",
            f"${current_price:,.2f}",
            f"${current_value:,.2f}",
            f"${invested:,.2f}",
            pnl_str
        )
    
    console.print(table)


def demo_risk_analysis():
    """Demo risk analysis"""
    console.print(Panel("⚠️ Risk Analysis Demo", style="cyan"))
    
    # Sample portfolio for risk analysis
    sample_portfolio = {
        "holdings": {
            "bitcoin": {"pnl_percentage": 14.22},
            "ethereum": {"pnl_percentage": -3.86},
            "binancecoin": {"pnl_percentage": 257.60}
        }
    }
    
    # Perform risk analysis
    risk_analysis = RiskAnalyzer.analyze_portfolio_risk(sample_portfolio)
    
    risk_md = f"""
### ⚠️ Risk Analysis

- **Overall Risk Level**: {risk_analysis['risk_emoji']} {risk_analysis['risk_level']}
- **High Risk Holdings**: {risk_analysis['high_risk_count']}
- **Medium Risk Holdings**: {risk_analysis['medium_risk_count']}
- **Low Risk Holdings**: {risk_analysis['low_risk_count']}

**Key Risk Factors:**
- BNB: High volatility (257.6%)
- Bitcoin: Moderate volatility (14.2%)
- Ethereum: Low volatility (-3.9%)
"""
    console.print(Panel(Markdown(risk_md), title="Risk Analysis", border_style="yellow"))


def demo_market_insights():
    """Demo market insights (simulated)"""
    console.print(Panel("🧠 Market Insights Demo", style="cyan"))
    
    # Simulated AI insights
    insights_md = """
### 🧠 Market Insights

The cryptocurrency market is showing mixed signals today. Bitcoin continues its upward trajectory with a 2.4% gain, indicating strong institutional confidence. Ethereum faces slight pressure with a 1.3% decline, possibly due to network congestion concerns. BNB's impressive 5.7% surge suggests growing adoption of the Binance ecosystem.

**Key Trends:**
- Bitcoin dominance remains strong
- DeFi tokens showing resilience
- Altcoin season indicators mixed

**Risk Assessment:** Medium risk environment with selective opportunities in established cryptocurrencies.
"""
    console.print(Panel(Markdown(insights_md), title="AI Market Analysis", border_style="blue"))


def main():
    """Run the demo"""
    console.clear()
    console.print(Panel(
        "₿ CryptoInsightsAgent Demo",
        title="₿ CryptoInsightsAgent",
        subtitle="Real-Time Prices, Risk Analysis & Market Insights",
        border_style="cyan",
        expand=True,
    ))
    
    console.print("\nThis demo showcases the key features of CryptoInsightsAgent:")
    console.print("• Real-time cryptocurrency prices")
    console.print("• Portfolio tracking and P&L calculations")
    console.print("• Risk analysis based on volatility")
    console.print("• AI-powered market insights")
    console.print("• Interactive CLI interface")
    
    input("\nPress Enter to continue...")
    
    demo_crypto_prices()
    input("\nPress Enter to continue...")
    
    demo_portfolio()
    input("\nPress Enter to continue...")
    
    demo_risk_analysis()
    input("\nPress Enter to continue...")
    
    demo_market_insights()
    
    console.print("\n🎉 Demo completed!")
    console.print("\nTo use the full agent with real data:")
    console.print("1. Run: python main.py")
    console.print("2. Or: python main.py bitcoin usd")
    console.print("3. Configure OpenAI API key for AI insights")


if __name__ == "__main__":
    main()
