import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.markdown import Markdown
try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

# Support running as a package (python -m 39_CurrencyConverterBot) and as a script (python 39_CurrencyConverterBot/main.py)
try:  # package-style imports
    from .agents import OpenAIAgent, ExchangeRateHostAgent
    from .utils import sanitize_currency, parse_amount, format_total, get_currency_symbol
    from . import config
except Exception:  # script-style fallback
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agents import OpenAIAgent, ExchangeRateHostAgent  # type: ignore
    from utils import sanitize_currency, parse_amount, format_total, get_currency_symbol  # type: ignore
    import config  # type: ignore


app = typer.Typer(add_completion=False, help="CurrencyConverterBot — Your Smart Finance Assistant")
console = Console()


def _render_result(amount: float, from_code: str, to_code: str) -> None:
    fx_agent = ExchangeRateHostAgent()
    converted, rate, meta = fx_agent.convert(amount, from_code, to_code)
    if converted is None or rate is None:
        md = f"""
### ❌ Error

{meta.get('error','Unknown error')}
"""
        _render_markdown_panel(md, title="Error")
        return

    timestamp = meta.get("timestamp") or "Unknown"
    source = meta.get("source", "?")
    warn = meta.get("warning")
    md = f"""
### 💱 Conversion Result

- **Exchange Rate**: `1 {from_code} = {rate:,.4f} {to_code}`
- **Total**: `{format_total(converted, to_code)}`
- **Data as of**: `{timestamp}`
- **Source**: `{source}`
{('- **Note**: ' + warn) if warn else ''}
"""
    _render_markdown_panel(md, title="CurrencyConverterBot")

    nlp_agent = OpenAIAgent()
    insight = nlp_agent.insight(from_code, to_code)
    if insight:
        md_insight = f"""
> {insight}

_Powered by GPT_
"""
        _render_markdown_panel(md_insight, title="Insight")

    if Confirm.ask("Save this conversion?", default=False):
        try:
            with open("conversions.log", "a", encoding="utf-8") as f:
                f.write(f"{from_code} {amount} -> {to_code} {converted:.2f} | rate {rate:.6f} | {timestamp} | {source}\n")
            console.print("Saved to conversions.log")
        except Exception:
            console.print("[yellow]Failed to save log.[/yellow]")


def _show_header() -> None:
    console.clear()
    console.print(Panel(
        "💱 CurrencyConverterBot — Your Smart Finance Assistant",
        title="💱 CurrencyConverterBot",
        subtitle="OpenAI + Rich CLI",
        border_style="cyan",
        expand=True,
    ))


def _render_markdown_panel(text: str, title: str = "CurrencyConverterBot") -> None:
    renderable = Markdown(text or "(no data)")
    console.print(Panel(renderable, title=title, border_style="cyan", expand=True))


def _chat_loop() -> None:
    if not getattr(config, "OPENAI_API_KEY", "") or OpenAI is None:
        _render_markdown_panel(
            """
### ❌ GPT Unavailable

Set `OPENAI_API_KEY` to enable chatbot mode.
""",
            title="Chatbot",
        )
        return
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    system_prompt = (
        "You are a concise currency assistant. Answer questions about currency conversions, rates, and brief context. "
        "Be accurate, avoid financial advice, and keep answers short."
    )
    _render_markdown_panel(
        """
### 💬 Chatbot Mode

Type your question. Type `exit` to quit.
""",
        title="Chatbot",
    )
    history = [{"role": "system", "content": system_prompt}]
    while True:
        try:
            user = console.input("[cyan]You[/cyan]: ")
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.strip().lower() in {"exit", "quit"}:
            break
        # Try to interpret as a conversion request first (web-search style tool using live API)
        try:
            nlp_agent = OpenAIAgent()
            parsed = nlp_agent.parse(user)
        except Exception:
            parsed = None
        if parsed:
            amt, src, dst = parsed
            fx_agent = ExchangeRateHostAgent()
            converted, rate, meta = fx_agent.convert(amt, src, dst)
            if converted is not None and rate is not None:
                timestamp = meta.get("timestamp") or "Unknown"
                source = meta.get("source", "?")
                warn = meta.get("warning")
                md = f"""
### 🌐 Live Rate (via exchangerate.host)

- **Query**: `{amt} {src} → {dst}`
- **Exchange Rate**: `1 {src} = {rate:,.4f} {dst}`
- **Total**: `{format_total(converted, dst)}`
- **Data as of**: `{timestamp}`
- **Source**: `{source}`
{('- **Note**: ' + warn) if warn else ''}
"""
                _render_markdown_panel(md, title="Assistant")
                # Also add a short GPT confirmation/explanation
                history.append({"role": "user", "content": user})
                history.append({"role": "assistant", "content": md})
                continue
        # Otherwise, answer via GPT
        history.append({"role": "user", "content": user})
        try:
            resp = client.chat.completions.create(
                model=getattr(config, "OPENAI_MODEL", "gpt-4o-mini"),
                messages=history,
                temperature=0.2,
            )
            answer = (resp.choices[0].message.content or "").strip()
            _render_markdown_panel(answer, title="Assistant")
            history.append({"role": "assistant", "content": answer})
        except Exception as e:
            _render_markdown_panel(f"### ❌ Error\n\n{e}", title="Chatbot")
            break


def _menu_loop() -> None:
    while True:
        _show_header()
        console.print("[bold]1.[/bold] Convert (amount, FROM, TO)")
        console.print("[bold]2.[/bold] Natural language query")
        console.print("[bold]3.[/bold] Chatbot (GPT)")
        console.print("[bold]4.[/bold] Exit")
        choice = Prompt.ask("Select an option (1-4)", default="1").strip()
        if choice == "1":
            amt_str = Prompt.ask("Amount", default="100").strip()
            amt = parse_amount(amt_str)
            if amt is None:
                console.print("[red]Invalid amount.[/red]")
                Prompt.ask("Press Enter to continue")
                continue
            src = Prompt.ask("From currency or country (e.g., USD or Pakistan)", default="USD").strip()
            dst = Prompt.ask("To currency or country (e.g., INR or Canada)", default="INR").strip()
            # Try resolving via resolver agent
            try:
                from .agents import CurrencyResolverAgent  # type: ignore
            except Exception:
                from agents import CurrencyResolverAgent  # type: ignore
            resolver = CurrencyResolverAgent()
            src_resolved = resolver.resolve(src) or src
            dst_resolved = resolver.resolve(dst) or dst
            src_s = sanitize_currency(src_resolved)
            dst_s = sanitize_currency(dst_resolved)
            if not src_s or not dst_s:
                console.print("[yellow]Please enter valid currency names or 3-letter codes.[/yellow]")
                Prompt.ask("Press Enter to continue")
                continue
            _render_result(amt, src_s, dst_s)
            if not Confirm.ask("Another conversion?", default=True):
                break
        elif choice == "2":
            query = Prompt.ask("Enter your query", default="Convert 100 USD to INR")
            nlp_agent = OpenAIAgent()
            parsed = nlp_agent.parse(query)
            if not parsed:
                console.print("[yellow]Couldn't parse. Try format like: Convert 100 USD to INR[/yellow]")
                Prompt.ask("Press Enter to continue")
                continue
            amt, src, dst = parsed
            _render_result(amt, src, dst)
            if not Confirm.ask("Another conversion?", default=True):
                break
        elif choice == "3":
            _chat_loop()
            if not Confirm.ask("Back to menu?", default=True):
                break
        elif choice == "4":
            break
        else:
            console.print("[yellow]Please select 1-4.[/yellow]")
            Prompt.ask("Press Enter to continue")


@app.command()
def cli(
    amount: Optional[float] = typer.Argument(None, help="Amount to convert"),
    from_currency: Optional[str] = typer.Argument(None, help="3-letter source currency code"),
    to_currency: Optional[str] = typer.Argument(None, help="3-letter target currency code"),
):
    """Run interactive mode or one-shot conversion.

    Examples:
    python -m 39_CurrencyConverterBot.main 100 USD INR
    """
    if amount is not None and from_currency and to_currency:
        from_code = sanitize_currency(from_currency) or from_currency
        to_code = sanitize_currency(to_currency) or to_currency
        if from_code and to_code:
            _render_result(amount, from_code, to_code)
            raise typer.Exit()
    _menu_loop()


if __name__ == "__main__":
    app()


