import argparse
import os
import sys
import subprocess
import json
from typing import List, Tuple

from config import settings
from utils import ensure_directory, parse_date
from news_fetcher import NewsFetcher
from summarizer import Summarizer, ArticleSummary

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

# PDF export
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

console = Console()


def build_markdown(date_str: str, summaries: List[ArticleSummary], query: str | None) -> str:
    lines: List[str] = []
    title = "Top News" if not query else f"Top results for: {query}"
    lines.append(f"# Daily News Summary — {date_str}")
    lines.append("")
    lines.append(f"## {title}")
    lines.append("")
    for s in summaries:
        lines.append(f"### {s.title}")
        lines.append(f"- **date**: {date_str}")
        lines.append(f"- **source**: {s.source}")
        if s.tags:
            lines.append(f"- **tags**: {', '.join(s.tags)}")
        lines.append(f"- **label**: {s.label}")
        lines.append("- **summary**:")
        for b in s.bullets:
            lines.append(f"  - {b}")
        lines.append(f"- **link**: {s.url}")
        lines.append("")
    return "\n".join(lines)


def build_json(date_str: str, summaries: List[ArticleSummary], query: str | None) -> str:
    payload = {
        "date": date_str,
        "query": query,
        "count": len(summaries),
        "items": [
            {
                "title": s.title,
                "source": s.source,
                "url": s.url,
                "tags": s.tags,
                "label": s.label,
                "bullets": s.bullets,
            }
            for s in summaries
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def save_pdf(path: str, date_str: str, summaries: List[ArticleSummary], query: str | None) -> None:
    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_text = f"Daily News Summary — {date_str}"
    section_text = "Top News" if not query else f"Top results for: {query}"

    story.append(Paragraph(title_text, styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(section_text, styles["Heading2"]))
    story.append(Spacer(1, 12))

    for s in summaries:
        story.append(Paragraph(s.title, styles["Heading3"]))
        meta = f"Source: {s.source} | Label: {s.label}"
        story.append(Paragraph(meta, styles["Normal"]))
        story.append(Spacer(1, 6))
        for b in s.bullets:
            story.append(Paragraph(f"• {b}", styles["Normal"]))
        story.append(Paragraph(f"Link: {s.url}", styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)


def render_results_table(summaries: List[ArticleSummary], query: str | None) -> None:
    section = "Top News" if not query else f"Top results for: {query}"
    table = Table(title=section, show_lines=False)
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Label", style="yellow")
    table.add_column("Keyword", style="green")
    for s in summaries:
        keyword = query or "—"
        table.add_row(s.title[:60] + ("..." if len(s.title) > 60 else ""), s.source, s.label, keyword)
    console.print(table)


def open_file_cross_platform(path: str) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception as e:
        console.print(f"[yellow]⚠️ Could not open file automatically: {e}[/yellow]")


def choose_result_count(default_count: int, query: str | None) -> int:
    # If user provides very short/empty keywords, default to fewer results (2–3)
    if not query or len(query.strip()) < 4 or len(query.split()) <= 1:
        suggested = 3
    else:
        suggested = default_count
    try:
        num_str = Prompt.ask("How many top results?", default=str(suggested))
        num = int(num_str)
        if num <= 0:
            num = suggested
        return max(1, min(25, num))
    except Exception:
        return suggested


def choose_save_format() -> Tuple[str, bool]:
    # Returns (format, open_after)
    choices = ["md", "pdf", "json"]
    fmt = Prompt.ask("Save format", choices=choices, default="md")
    open_after = Confirm.ask("View saved file now?", default=True)
    return fmt, open_after


def main() -> None:
    parser = argparse.ArgumentParser(description="News Summarizer Agent (Day 37)")
    parser.add_argument("--date", type=str, default=None, help="Date in YYYY-MM-DD")
    parser.add_argument("--search", type=str, default=None, help="Keyword search")
    parser.add_argument("--category", type=str, default=None, help="Category tag (tech, world, business, etc.)")
    parser.add_argument("--interactive", action="store_true", help="Use interactive prompts (menu-style)")

    args = parser.parse_args()

    # Interactive prompts if requested or no args given
    if args.interactive or (args.date is None and args.search is None and args.category is None):
        console.print(Panel.fit("📰 NewsSummarizer — Interactive Mode", border_style="green"))
        default_date = parse_date(None)
        date_input = Prompt.ask("Date (YYYY-MM-DD)", default=default_date)
        date_str = parse_date(date_input)
        search = Prompt.ask("Search keywords (optional)", default="").strip() or None
        category = Prompt.ask("Category tag (optional)", default="").strip() or None
        top_n = choose_result_count(10, search)
        if not Confirm.ask("Proceed with these settings?", default=True):
            console.print("Aborted.")
            return
    else:
        date_str = parse_date(args.date)
        search = args.search
        category = args.category
        top_n = 10

    summaries_dir = os.path.join(settings.data_dir, "summaries")
    ensure_directory(summaries_dir)

    console.print(Panel.fit(f"📰 NewsSummarizer for [bold]{date_str}[/bold]", border_style="blue"))

    fetcher = NewsFetcher()
    summarizer = Summarizer()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task_fetch = progress.add_task("Fetching articles via SerpAPI...", total=None)
        items = fetcher.fetch_with_text(date=date_str, search=search, category=category)
        progress.update(task_fetch, description=f"Fetched {len(items)} articles")

        # Limit items according to top_n
        items = items[:top_n]

        summaries: List[ArticleSummary] = []
        task_sum = progress.add_task("Summarizing articles with OpenAI...", total=len(items) if items else 1)
        for item in items:
            summaries.append(
                summarizer.summarize(
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    category=item.get("category"),
                    text=item.get("text", ""),
                )
            )
            progress.advance(task_sum)

    # Render results table (with section title and keyword)
    render_results_table(summaries, search)

    # Choose save format
    fmt, open_after = choose_save_format()

    # Construct output path
    base_name = f"{date_str}_news_summary"
    out_md = os.path.join(summaries_dir, f"{base_name}.md")
    out_pdf = os.path.join(summaries_dir, f"{base_name}.pdf")
    out_json = os.path.join(summaries_dir, f"{base_name}.json")

    # Always build markdown and json strings; PDF on demand
    md_content = build_markdown(date_str, summaries, search)
    json_content = build_json(date_str, summaries, search)

    # Save according to chosen format
    if fmt == "md":
        with open(out_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        console.print(f"[green]✅ News summaries saved as Markdown at[/green] [bold]{out_md}[/bold]")
        out_path = out_md
    elif fmt == "json":
        with open(out_json, "w", encoding="utf-8") as f:
            f.write(json_content)
        console.print(f"[green]✅ News summaries saved as JSON at[/green] [bold]{out_json}[/bold]")
        out_path = out_json
    else:
        # pdf
        save_pdf(out_pdf, date_str, summaries, search)
        console.print(f"[green]✅ News summaries saved as PDF at[/green] [bold]{out_pdf}[/bold]")
        out_path = out_pdf

    # Offer to open the saved file
    if open_after:
        open_file_cross_platform(out_path)


if __name__ == "__main__":
    main()
