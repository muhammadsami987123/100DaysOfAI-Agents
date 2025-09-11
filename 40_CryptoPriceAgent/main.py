import sys
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

# Support running as a package and as a script
try:  # package-style imports
    from .crypto_agent import CoinGeckoAgent, OpenAIAgent, PortfolioManager, RiskAnalyzer
    from . import config
except Exception:  # script-style fallback
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from crypto_agent import CoinGeckoAgent, OpenAIAgent, PortfolioManager, RiskAnalyzer  # type: ignore
    import config  # type: ignore


app = typer.Typer(add_completion=False, help="CryptoInsightsAgent — Your Smart Cryptocurrency Assistant")
console = Console()


def _show_header() -> None:
    """Display the application header"""
    console.clear()
    console.print(Panel(
        "₿ CryptoInsightsAgent — Your Smart Cryptocurrency Assistant",
        title="₿ CryptoInsightsAgent",
        subtitle="Real-Time Prices, Risk Analysis & Market Insights",
        border_style="cyan",
        expand=True,
    ))


def _render_markdown_panel(text: str, title: str = "CryptoInsightsAgent") -> None:
    """Render markdown text in a panel"""
    renderable = Markdown(text or "(no data)")
    console.print(Panel(renderable, title=title, border_style="cyan", expand=True))


def _format_currency(amount: float, currency: str = "usd") -> str:
    """Format currency amount with appropriate symbol"""
    symbols = {
        "usd": "$",
        "eur": "€",
        "gbp": "£",
        "jpy": "¥",
        "inr": "₹",
        "cad": "C$",
        "aud": "A$"
    }
    symbol = symbols.get(currency.lower(), currency.upper() + " ")
    return f"{symbol}{amount:,.2f}"


def _format_percentage(value: float) -> str:
    """Format percentage with color coding"""
    if value > 0:
        return f"[green]+{value:.2f}%[/green]"
    elif value < 0:
        return f"[red]{value:.2f}%[/red]"
    else:
        return f"{value:.2f}%"


def _display_crypto_prices(crypto_data: List[Dict], currency: str = "usd") -> None:
    """Display cryptocurrency prices in a table"""
    if not crypto_data:
        _render_markdown_panel("### ❌ No data available", "Error")
        return
    
    table = Table(title=f"Top Cryptocurrencies (in {currency.upper()})")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Name", style="magenta", width=15)
    table.add_column("Symbol", style="blue", width=8)
    table.add_column("Price", style="green", width=12)
    table.add_column("24h Change", style="yellow", width=12)
    table.add_column("Market Cap", style="white", width=15)
    table.add_column("Risk", style="red", width=8)
    
    for crypto in crypto_data:
        rank = crypto.get('market_cap_rank', 'N/A')
        name = crypto.get('name', 'Unknown')
        symbol = crypto.get('symbol', '').upper()
        price = crypto.get('current_price', 0)
        change_24h = crypto.get('price_change_percentage_24h', 0)
        market_cap = crypto.get('market_cap', 0)
        
        # Calculate risk level
        risk_level, risk_emoji = RiskAnalyzer.calculate_risk_level(change_24h)
        
        table.add_row(
            str(rank),
            name,
            symbol,
            _format_currency(price, currency),
            _format_percentage(change_24h),
            _format_currency(market_cap / 1e9, currency) + "B" if market_cap > 1e9 else _format_currency(market_cap / 1e6, currency) + "M",
            f"{risk_emoji} {risk_level}"
        )
    
    console.print(table)


def _display_portfolio(portfolio_value: Dict, currency: str = "usd") -> None:
    """Display portfolio information"""
    if not portfolio_value.get("holdings"):
        _render_markdown_panel("### 📊 Portfolio is empty\n\nAdd some holdings to track your investments.", "Portfolio")
        return
    
    # Overall portfolio summary
    total_value = portfolio_value["total_value"]
    total_invested = portfolio_value["total_invested"]
    pnl = portfolio_value["pnl"]
    pnl_percentage = portfolio_value["pnl_percentage"]
    
    summary_md = f"""
### 📊 Portfolio Summary

- **Total Value**: {_format_currency(total_value, currency)}
- **Total Invested**: {_format_currency(total_invested, currency)}
- **P&L**: {_format_currency(pnl, currency)} ({_format_percentage(pnl_percentage)})
"""
    
    if pnl > 0:
        summary_md += "\n🎉 **Portfolio is in profit!**"
    elif pnl < 0:
        summary_md += "\n📉 **Portfolio is at a loss**"
    else:
        summary_md += "\n➖ **Portfolio is at break-even**"
    
    _render_markdown_panel(summary_md, "Portfolio Summary")
    
    # Individual holdings table
    table = Table(title="Individual Holdings")
    table.add_column("Crypto", style="cyan", width=12)
    table.add_column("Amount", style="blue", width=12)
    table.add_column("Current Price", style="green", width=12)
    table.add_column("Current Value", style="white", width=12)
    table.add_column("Invested", style="yellow", width=12)
    table.add_column("P&L", style="red", width=12)
    
    for crypto_id, holding in portfolio_value["holdings"].items():
        amount = holding["amount"]
        current_price = holding["current_price"]
        current_value = holding["current_value"]
        invested = holding["invested"]
        pnl = holding["pnl"]
        pnl_percentage = holding["pnl_percentage"]
        
        table.add_row(
            crypto_id.upper(),
            f"{amount:.6f}",
            _format_currency(current_price, currency),
            _format_currency(current_value, currency),
            _format_currency(invested, currency),
            f"{_format_currency(pnl, currency)} ({_format_percentage(pnl_percentage)})"
        )
    
    console.print(table)


def _get_crypto_prices_interactive() -> None:
    """Interactive function to get crypto prices"""
    crypto_agent = CoinGeckoAgent()
    
    console.print("\n[bold]📈 Get Cryptocurrency Prices[/bold]")
    
    # Get number of cryptos to display
    limit = Prompt.ask("Number of top cryptos to display", default="10")
    try:
        limit = int(limit)
        if limit <= 0 or limit > 100:
            limit = 10
    except ValueError:
        limit = 10
    
    # Get currency
    currency = Prompt.ask("Currency (usd, eur, gbp, etc.)", default="usd").lower()
    
    # Show loading
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching crypto prices...", total=None)
        crypto_data = crypto_agent.get_top_cryptos(limit, currency)
    
    if crypto_data:
        _display_crypto_prices(crypto_data, currency)
        
        # Generate market insights if OpenAI is available
        if config.is_openai_enabled():
            if Confirm.ask("\nGenerate market insights?", default=True):
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task("Generating market insights...", total=None)
                    openai_agent = OpenAIAgent()
                    insights = openai_agent.generate_market_insights(crypto_data, currency)
                
                if insights:
                    _render_markdown_panel(f"### 🧠 Market Insights\n\n{insights}", "AI Analysis")
    else:
        _render_markdown_panel("### ❌ Failed to fetch crypto prices\n\nPlease check your internet connection and try again.", "Error")


def _manage_portfolio_interactive() -> None:
    """Interactive portfolio management"""
    portfolio_manager = PortfolioManager()
    crypto_agent = CoinGeckoAgent()
    
    while True:
        console.print("\n[bold]💼 Portfolio Management[/bold]")
        console.print("1. View portfolio")
        console.print("2. Add holding")
        console.print("3. Remove holding")
        console.print("4. Set currency")
        console.print("5. Back to main menu")
        
        choice = Prompt.ask("Select an option (1-5)", default="1").strip()
        
        if choice == "1":
            # View portfolio
            currency = portfolio_manager.get_portfolio().get("currency", "usd")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Calculating portfolio value...", total=None)
                portfolio_value = portfolio_manager.get_portfolio_value(crypto_agent, currency)
            
            _display_portfolio(portfolio_value, currency)
            
            # Risk analysis
            if portfolio_value.get("holdings"):
                risk_analysis = RiskAnalyzer.analyze_portfolio_risk(portfolio_value)
                risk_md = f"""
### ⚠️ Risk Analysis

- **Overall Risk Level**: {risk_analysis['risk_emoji']} {risk_analysis['risk_level']}
- **High Risk Holdings**: {risk_analysis['high_risk_count']}
- **Medium Risk Holdings**: {risk_analysis['medium_risk_count']}
- **Low Risk Holdings**: {risk_analysis['low_risk_count']}
"""
                if risk_analysis['factors']:
                    risk_md += "\n**Key Risk Factors:**\n"
                    for factor in risk_analysis['factors']:
                        risk_md += f"- {factor}\n"
                
                _render_markdown_panel(risk_md, "Risk Analysis")
                
                # AI risk analysis if available
                if config.is_openai_enabled() and Confirm.ask("Get AI risk analysis?", default=True):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                    ) as progress:
                        task = progress.add_task("Analyzing portfolio risk...", total=None)
                        openai_agent = OpenAIAgent()
                        ai_analysis = openai_agent.analyze_portfolio_risk(portfolio_value)
                    
                    if ai_analysis:
                        _render_markdown_panel(f"### 🤖 AI Risk Analysis\n\n{ai_analysis}", "AI Analysis")
        
        elif choice == "2":
            # Add holding
            crypto_id = Prompt.ask("Cryptocurrency ID (e.g., bitcoin, ethereum)").lower().strip()
            if not crypto_id:
                console.print("[red]Invalid crypto ID[/red]")
                continue
            
            # Verify crypto exists
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Verifying cryptocurrency...", total=None)
                crypto_info = crypto_agent.get_crypto_info(crypto_id)
            
            if not crypto_info:
                console.print(f"[red]Cryptocurrency '{crypto_id}' not found[/red]")
                continue
            
            amount_str = Prompt.ask("Amount to add")
            try:
                amount = float(amount_str)
                if amount <= 0:
                    console.print("[red]Amount must be positive[/red]")
                    continue
            except ValueError:
                console.print("[red]Invalid amount[/red]")
                continue
            
            purchase_price_str = Prompt.ask("Purchase price (optional)", default="")
            purchase_price = None
            if purchase_price_str:
                try:
                    purchase_price = float(purchase_price_str)
                except ValueError:
                    console.print("[yellow]Invalid purchase price, using current market price[/yellow]")
            
            if portfolio_manager.add_holding(crypto_id, amount, purchase_price):
                console.print(f"[green]Successfully added {amount} {crypto_id}[/green]")
            else:
                console.print("[red]Failed to add holding[/red]")
        
        elif choice == "3":
            # Remove holding
            portfolio = portfolio_manager.get_portfolio()
            holdings = portfolio.get("holdings", {})
            
            if not holdings:
                console.print("[yellow]Portfolio is empty[/yellow]")
                continue
            
            console.print("\nCurrent holdings:")
            for i, (crypto_id, holding) in enumerate(holdings.items(), 1):
                console.print(f"{i}. {crypto_id.upper()}: {holding['amount']:.6f}")
            
            crypto_id = Prompt.ask("Cryptocurrency ID to remove").lower().strip()
            if crypto_id not in holdings:
                console.print(f"[red]'{crypto_id}' not found in portfolio[/red]")
                continue
            
            amount_str = Prompt.ask("Amount to remove (leave empty to remove all)")
            if amount_str:
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        console.print("[red]Amount must be positive[/red]")
                        continue
                except ValueError:
                    console.print("[red]Invalid amount[/red]")
                    continue
            else:
                amount = None
            
            if portfolio_manager.remove_holding(crypto_id, amount):
                if amount:
                    console.print(f"[green]Successfully removed {amount} {crypto_id}[/green]")
                else:
                    console.print(f"[green]Successfully removed all {crypto_id}[/green]")
            else:
                console.print("[red]Failed to remove holding[/red]")
        
        elif choice == "4":
            # Set currency
            currency = Prompt.ask("Portfolio currency (usd, eur, gbp, etc.)", default="usd").lower()
            if portfolio_manager.set_currency(currency):
                console.print(f"[green]Portfolio currency set to {currency.upper()}[/green]")
            else:
                console.print("[red]Failed to set currency[/red]")
        
        elif choice == "5":
            break
        
        else:
            console.print("[yellow]Please select 1-5[/yellow]")


def _search_crypto_interactive() -> None:
    """Interactive cryptocurrency search"""
    crypto_agent = CoinGeckoAgent()
    
    query = Prompt.ask("Search for cryptocurrency (name or symbol)")
    if not query.strip():
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Searching cryptocurrencies...", total=None)
        results = crypto_agent.search_crypto(query)
    
    if not results:
        _render_markdown_panel("### ❌ No cryptocurrencies found\n\nTry a different search term.", "Search Results")
        return
    
    # Display search results
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Name", style="cyan", width=20)
    table.add_column("Symbol", style="blue", width=10)
    table.add_column("ID", style="green", width=15)
    table.add_column("Market Cap Rank", style="yellow", width=12)
    
    for result in results[:10]:  # Show top 10 results
        name = result.get('name', 'Unknown')
        symbol = result.get('symbol', '').upper()
        crypto_id = result.get('id', '')
        rank = result.get('market_cap_rank', 'N/A')
        
        table.add_row(name, symbol, crypto_id, str(rank))
    
    console.print(table)
    
    # Option to get detailed info
    if Confirm.ask("\nGet detailed information for a specific crypto?"):
        crypto_id = Prompt.ask("Enter crypto ID from the table above")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching detailed information...", total=None)
            crypto_info = crypto_agent.get_crypto_info(crypto_id)
        
        if crypto_info:
            # Display basic info
            name = crypto_info.get('name', 'Unknown')
            symbol = crypto_info.get('symbol', '').upper()
            current_price = crypto_info.get('market_data', {}).get('current_price', {}).get('usd', 0)
            change_24h = crypto_info.get('market_data', {}).get('price_change_percentage_24h', 0)
            market_cap = crypto_info.get('market_data', {}).get('market_cap', {}).get('usd', 0)
            
            info_md = f"""
### {name} ({symbol})

- **Current Price**: {_format_currency(current_price, 'usd')}
- **24h Change**: {_format_percentage(change_24h)}
- **Market Cap**: {_format_currency(market_cap / 1e9, 'usd')}B
- **ID**: `{crypto_id}`
"""
            _render_markdown_panel(info_md, "Crypto Details")
        else:
            _render_markdown_panel("### ❌ Failed to fetch detailed information", "Error")


def _menu_loop() -> None:
    """Main menu loop"""
    while True:
        _show_header()
        console.print("[bold]1.[/bold] Get crypto prices")
        console.print("[bold]2.[/bold] Manage portfolio")
        console.print("[bold]3.[/bold] Search cryptocurrency")
        console.print("[bold]4.[/bold] Exit")
        
        choice = Prompt.ask("Select an option (1-4)", default="1").strip()
        
        if choice == "1":
            _get_crypto_prices_interactive()
            if not Confirm.ask("Continue?", default=True):
                break
        elif choice == "2":
            _manage_portfolio_interactive()
        elif choice == "3":
            _search_crypto_interactive()
            if not Confirm.ask("Continue?", default=True):
                break
        elif choice == "4":
            break
        else:
            console.print("[yellow]Please select 1-4[/yellow]")
            Prompt.ask("Press Enter to continue")


@app.command()
def cli(
    crypto_id: Optional[str] = typer.Argument(None, help="Cryptocurrency ID to get price for"),
    currency: Optional[str] = typer.Argument(None, help="Currency for price display (default: usd)"),
):
    """Run interactive mode or get price for specific crypto.
    
    Examples:
    python -m 40_CryptoPriceAgent.main bitcoin usd
    """
    if crypto_id:
        # One-shot price lookup
        crypto_agent = CoinGeckoAgent()
        currency = currency or "usd"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Fetching {crypto_id} price...", total=None)
            prices = crypto_agent.get_crypto_prices([crypto_id], currency)
        
        if prices and crypto_id in prices:
            price_data = prices[crypto_id]
            current_price = price_data.get(currency, 0)
            change_24h = price_data.get(f"{currency}_24h_change", 0)
            
            result_md = f"""
### {crypto_id.upper()} Price

- **Current Price**: {_format_currency(current_price, currency)}
- **24h Change**: {_format_percentage(change_24h)}
- **Currency**: {currency.upper()}
"""
            _render_markdown_panel(result_md, "Price Result")
        else:
            _render_markdown_panel(f"### ❌ Failed to fetch price for {crypto_id}", "Error")
    else:
        # Interactive mode
        _menu_loop()


if __name__ == "__main__":
    app()
