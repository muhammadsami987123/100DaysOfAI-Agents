#!/usr/bin/env python3
"""
InvestmentAdvisorBot - Day 41

CLI entrypoint that collects user profile, calls the advisor, and exports markdown/json.
"""

import argparse
import sys
import json
from pathlib import Path

from config import get_api_key, setup_instructions
from investment_agent import InvestmentAdvisor

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from time import sleep


def parse_args():
    parser = argparse.ArgumentParser(description="InvestmentAdvisorBot - CLI financial advisor")

    parser.add_argument('--income', type=float, help='Monthly income amount (number)')
    parser.add_argument('--age', type=int, help='Age in years')
    parser.add_argument('--risk', choices=['low', 'medium', 'high'], default='medium', help='Risk appetite')
    parser.add_argument('--goal', type=str, default='long-term', help='Investment goal (retirement, short-term, education, etc.)')
    parser.add_argument('--currency', type=str, default='USD', help='Preferred currency')
    parser.add_argument('--save-pct', type=int, help='Suggested percent of income to save (overrides suggestion)')

    parser.add_argument('--export-json', action='store_true', help='Export output as JSON')
    parser.add_argument('--export-pdf', action='store_true', help='Export output as PDF (optional)')
    parser.add_argument('--output', type=str, default='investment_advice.md', help='Output filename for markdown')
    parser.add_argument('--simulate-returns', action='store_true', help='Show a simple 5-year growth simulation')
    parser.add_argument('--language', choices=['en','ur','hi'], default='en', help='Language for output')
    parser.add_argument('--chat', action='store_true', help='Run in interactive chatbot mode')
    parser.add_argument('--non-interactive', action='store_true', help='Run without interactive prompts (useful for scripts/tests)')

    return parser.parse_args()


def simulate_growth(allocation: dict, monthly_savings: float, years: int = 5):
    # Simple annualized returns per asset class (heuristic)
    rates = {
        'stocks': 0.08,
        'mutual_funds': 0.07,
        'bonds': 0.03,
        'gold': 0.02,
        'crypto': 0.15,
        'cash': 0.01
    }
    results = {str(y): 0 for y in range(1, years+1)}
    principal = 0
    for year in range(1, years+1):
        principal += monthly_savings * 12
        growth = 0
        for asset, pct in allocation.items():
            rate = rates.get(asset, 0.03)
            portion = principal * (pct/100)
            growth += portion * rate
        principal += growth
        results[str(year)] = round(principal, 2)
    return results


def main():
    args = parse_args()

    api_key = get_api_key()
    if not api_key:
        print('Warning: OPENAI_API_KEY not set. Running in offline heuristic mode.')

    advisor = InvestmentAdvisor(api_key=api_key)

    console = Console()

    def print_banner():
        console.print(Panel.fit("[bold cyan]InvestmentAdvisorBot[/bold cyan] — Simulated financial advisor (educational only)\n[dim]Type 'exit' to quit interactive mode.[/dim]"))

    def profile_from_prompts() -> dict:
        """Ask the user for profile fields step-by-step and return a profile dict."""
        try:
            income = Prompt.ask("Monthly income", default="0")
            age = Prompt.ask("Age", default="30")
            risk = Prompt.ask("Risk appetite", choices=["low", "medium", "high"], default="medium")
            goal = Prompt.ask("Investment goal (retirement, short-term, education)", default="long-term")
            currency = Prompt.ask("Preferred currency", default="USD")
            save_pct = Prompt.ask("Preferred save % (optional)", default="")

            profile = {
                'income': float(income) if income else 0,
                'age': int(age) if age else 30,
                'risk': risk,
                'goal': goal,
                'currency': currency,
                'save_pct': int(save_pct) if save_pct else None
            }
            return profile
        except Exception as e:
            console.print(f"[red]Invalid input:[/red] {e}")
            return {}

    def render_and_offer_actions(profile: dict, markdown: str, allocation: dict):
        """Render advice and offer export/simulation options."""
        if not markdown:
            console.print("[yellow]No advice generated.[/yellow]")
            return
        renderable = Markdown(markdown)
        console.print(Panel(renderable, title='InvestmentAdvisorBot', border_style='cyan', expand=True))

        if Prompt.ask("Export to markdown?", choices=["y","n"], default="y") == 'y':
            out_name = Prompt.ask("Output filename", default='investment_advice.md')
            advisor.export_markdown(markdown, out_name)
            console.print(f"Saved markdown to {out_name}")

        if Prompt.ask("Also export JSON?", choices=["y","n"], default="n") == 'y':
            json_name = Prompt.ask("JSON filename", default='investment_advice.json')
            data = {'profile': profile, 'allocation': allocation, 'markdown': markdown}
            advisor.export_json(data, json_name)
            console.print(f"Saved JSON to {json_name}")

        if Prompt.ask("Run 5-year simulation?", choices=["y","n"], default="n") == 'y':
            monthly_savings = (profile.get('income', 0) * (profile.get('save_pct') or advisor.recommend_save_pct(profile))) / 100.0
            sim = simulate_growth(allocation, monthly_savings)
            console.print("[bold]5-Year Simulation Results[/bold]")
            for year, val in sim.items():
                console.print(f"- Year {year}: {val} {profile.get('currency','')}")


    # If script is run with no additional args, show a simple menu launcher
    if len(sys.argv) == 1:
        print_banner()
        while True:
            console.print("\n[bold]Select an option:[/bold]")
            console.print("1) Step-by-step profile (guided)")
            console.print("2) Quick input (enter required fields)")
            console.print("3) Chat mode")
            console.print("4) Exit")

            choice = Prompt.ask("Choice", choices=["1","2","3","4"], default="1")
            if choice == '1':
                profile = profile_from_prompts()
                if not profile:
                    continue
                with Live(Spinner('dots', text='Generating advice...'), console=console, refresh_per_second=12):
                    out = advisor.generate_advice(profile)
                render_and_offer_actions(profile, out.get('markdown',''), out.get('allocation', {}))
            elif choice == '2':
                # quick input: ask only income and age and use defaults
                income = Prompt.ask("Monthly income", default="1000")
                age = Prompt.ask("Age", default="30")
                risk = Prompt.ask("Risk", choices=["low","medium","high"], default="medium")
                goal = Prompt.ask("Goal", default="long-term")
                profile = {'income': float(income), 'age': int(age), 'risk': risk, 'goal': goal, 'currency': 'USD'}
                with Live(Spinner('dots', text='Generating advice...'), console=console, refresh_per_second=12):
                    out = advisor.generate_advice(profile)
                render_and_offer_actions(profile, out.get('markdown',''), out.get('allocation', {}))
            elif choice == '3':
                # enter chat mode
                args.chat = True
                break
            else:
                console.print('[yellow]Goodbye![/yellow]')
                return

    if args.chat:
        # Rich chat loop modeled after Day 18 UI
        print_banner()
        try:
            while True:
                user_input = Prompt.ask("[cyan]You[/cyan]")
                if not user_input or user_input.strip().lower() in {"exit", "quit"}:
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                profile = {
                    'income': args.income or 'N/A',
                    'age': args.age or 'N/A',
                    'risk': args.risk,
                    'goal': args.goal,
                    'currency': args.currency,
                    'notes': user_input
                }

                console.print('[bold blue]Processing...[/bold blue]')
                spinner = Spinner('dots', text='Generating advice...')
                streamed = ''
                with Live(spinner, console=console, refresh_per_second=12):
                    # we don't stream tokens from heuristic mode, so just call generate_advice
                    out = advisor.generate_advice(profile)
                    streamed = out.get('markdown', '')

                with console.status('[bold magenta]Formatting...[/bold magenta]', spinner='dots12'):
                    renderable = Markdown(streamed or '(no response)')
                    sleep(0.05)

                console.print(Panel(renderable, title='InvestmentAdvisorBot', border_style='cyan', expand=True))

        except KeyboardInterrupt:
            console.print('\n[yellow]Interrupted.[/yellow]')
        return

    # Non-chat mode: require income and age
    if args.income is None or args.age is None:
        print('Error: --income and --age are required for non-chat mode')
        sys.exit(1)

    profile = {
        'income': args.income,
        'age': args.age,
        'risk': args.risk,
        'goal': args.goal,
        'currency': args.currency,
        'save_pct': args.save_pct
    }

    with Live(Spinner('dots', text='Generating advice...'), console=console, refresh_per_second=12):
        result = advisor.generate_advice(profile)
    markdown = result.get('markdown','')
    allocation = result.get('allocation', {})
    # Render advice to console
    console = Console()
    if markdown:
        console.print(Panel(Markdown(markdown), title='InvestmentAdvisorBot', border_style='cyan', expand=True))
    else:
        console.print('[yellow]No advice generated.[/yellow]')

    interactive = sys.stdin.isatty() and not args.non_interactive

    if interactive:
        # Ask user where to save
        save_md = Prompt.ask('Save advice as markdown?', choices=['y','n'], default='y')
        if save_md == 'y':
            out_name = Prompt.ask('Markdown filename', default=str(args.output))
            advisor.export_markdown(markdown, out_name)
            console.print(f'Markdown saved to: {out_name}')

        if Prompt.ask('Also export JSON?', choices=['y','n'], default='n') == 'y':
            json_name = Prompt.ask('JSON filename', default=str(Path(str(args.output)).with_suffix('.json')))
            data = {'profile': profile, 'allocation': allocation, 'markdown': markdown}
            advisor.export_json(data, json_name)
            console.print(f'JSON saved to: {json_name}')
    else:
        # Non-interactive: auto-save as before
        out_path = Path(args.output)
        advisor.export_markdown(markdown, str(out_path))
        print(f'\nMarkdown advice saved to: {out_path}')

        if args.export_json:
            json_path = out_path.with_suffix('.json')
            data = {'profile': profile, 'allocation': allocation, 'markdown': markdown}
            advisor.export_json(data, str(json_path))
            print(f'JSON exported to: {json_path}')

    if args.simulate_returns:
        monthly_savings = (args.income * (args.save_pct or advisor.recommend_save_pct(profile))) / 100.0
        sim = simulate_growth(allocation, monthly_savings)
        console.print('\n## 5-Year Simulation Results')
        for year, val in sim.items():
            console.print(f'- Year {year}: {val} {args.currency}')


if __name__ == '__main__':
    main()

