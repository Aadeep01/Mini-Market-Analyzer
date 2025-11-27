from collections.abc import Iterable

import pandas as pd
import plotext as plt
import typer
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mini_market_analyzer.data_loader import fetch_data
from mini_market_analyzer.gemini_analyzer import GeminiAnalyzer
from mini_market_analyzer.indicators import add_indicators
from mini_market_analyzer.strategy import Signal, analyze_market

# Load environment variables
load_dotenv()


class MMACompleter(Completer):
    """Context-aware completer for Mini Market Analyzer."""

    def __init__(self) -> None:
        self.commands = ["analyze", "chart", "popular", "help", "exit", "quit"]
        self.tickers = [
            "AAPL",
            "NVDA",
            "TSLA",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "SPY",
            "QQQ",
            "BTC-USD",
            "ETH-USD",
            "GC=F",
        ]

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text_before_cursor
        words = text.split()

        # If no words yet, suggest commands
        if not words or (len(words) == 1 and not text.endswith(" ")):
            word = words[0] if words else ""
            for cmd in self.commands:
                if cmd.startswith(word.lower()):
                    yield Completion(cmd, start_position=-len(word))

        # If first word is analyze or chart, suggest tickers
        elif len(words) >= 1 and words[0] in ["analyze", "chart"]:
            current_word = words[-1] if not text.endswith(" ") else ""
            for ticker in self.tickers:
                if ticker.lower().startswith(current_word.lower()):
                    yield Completion(ticker, start_position=-len(current_word))
        # For standalone commands (exit, quit, help, popular), don't suggest anything


app = typer.Typer(help="Mini Market Analyzer CLI")
console = Console()


@app.command()
def analyze(ticker: str, period: str = "1y") -> None:
    """
    Analyze a given ticker symbol.
    """
    console.print(f"[bold blue]Fetching data for {ticker}...[/bold blue]")
    try:
        # 1. Fetch Data
        df = fetch_data(ticker, period=period)

        # 2. Add Indicators
        with console.status("[bold green]Computing indicators...[/bold green]"):
            df_analyzed = add_indicators(df)

        # 3. Run Strategy
        result = analyze_market(df_analyzed, ticker)

        # 4. Display Results
        # Signal Color
        color = "white"
        if result.signal == Signal.BUY:
            color = "green"
        elif result.signal == Signal.SELL:
            color = "red"
        elif result.signal == Signal.CAUTION:
            color = "yellow"

        # Summary Panel
        summary_text = f"""
        [bold]Price:[/bold] ${result.current_price:.2f}
        [bold]Regime:[/bold] {result.regime.value}
        [bold]Signal:[/bold] [{color}]{result.signal.value}[/{color}]
        [bold]Confidence:[/bold] {result.confidence:.0%}
        """
        console.print(
            Panel(summary_text, title=f"Analysis: {ticker.upper()}", expand=False)
        )

        # 5. AI Summary
        analyzer = GeminiAnalyzer()
        with console.status("[bold green]Generating AI Summary...[/bold green]"):
            ai_summary = analyzer.generate_summary(ticker, result)

        console.print(
            Panel(ai_summary, title="Gemini 2.5 Flash Insight", border_style="green")
        )

        # Indicators Table
        table = Table(title="Technical Indicators")
        table.add_column("Indicator", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("RSI (14)", f"{result.rsi:.2f}")
        table.add_row("MACD", f"{result.macd:.4f}")
        table.add_row("MACD Signal", f"{result.macd_signal:.4f}")
        table.add_row("EMA (50)", f"{result.ema_50:.2f}")
        table.add_row("EMA (200)", f"{result.ema_200:.2f}")

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


def render_chart(df: pd.DataFrame, ticker: str) -> str:
    """
    Renders a terminal chart using plotext and returns the string representation.
    """
    # Prepare data
    dates = df.index.strftime("%Y-%m-%d").tolist()

    # Use Candlestick if OHLC data is available
    if all(col in df.columns for col in ["open", "high", "low", "close"]):
        opens = df["open"].tolist()
        highs = df["high"].tolist()
        lows = df["low"].tolist()
        closes = df["close"].tolist()

        plt.clf()
        plt.date_form("Y-m-d")
        plt.title(f"{ticker} Price History")

        # Candlestick plot
        plt.candlestick(
            dates, data={"Open": opens, "High": highs, "Low": lows, "Close": closes}
        )

        # Add EMAs
        if "EMA_50" in df.columns:
            ema50 = df["EMA_50"].tolist()
            plt.plot(dates, ema50, label="EMA 50", color="green")

        if "EMA_200" in df.columns:
            ema200 = df["EMA_200"].tolist()
            plt.plot(dates, ema200, label="EMA 200", color="red")

        plt.theme("clear")  # Cleaner theme
        plt.grid(False, False)  # Remove grid
        plt.xlabel("Date")
        plt.ylabel("Price")

        return str(plt.build())

    else:
        # Fallback to line chart
        close = df["close"].tolist()

        plt.clf()
        plt.date_form("Y-m-d")
        plt.title(f"{ticker} Price History")
        plt.plot(dates, close, label="Close Price", color="blue")

        plt.theme("clear")
        plt.grid(False, False)

        return str(plt.build())


@app.command()
def chart(ticker: str, period: str = "1y") -> None:
    """
    Display a terminal chart for a given ticker.
    """
    console.print(f"[bold blue]Fetching data for {ticker}...[/bold blue]")
    try:
        df = fetch_data(ticker, period=period)
        df = add_indicators(df)

        chart_str = render_chart(df, ticker)
        console.print(Text.from_ansi(chart_str))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@app.command()
def interactive() -> None:
    """
    Start an interactive session.
    """
    welcome_msg = (
        "[bold green]Welcome to Mini Market Analyzer Interactive Mode![/bold green]\n\n"
        "[bold]Commands:[/bold]\n"
        "- [cyan]analyze <ticker>[/cyan]: Full technical analysis "
        "(e.g., `analyze AAPL`)\n"
        "- [cyan]chart <ticker>[/cyan]: View price chart "
        "(e.g., `chart BTC-USD`)\n"
        "- [cyan]popular[/cyan]: See a list of popular tickers\n"
        "- [cyan]help[/cyan]: Show this help message\n"
        "- [cyan]exit[/cyan]: Quit the app"
    )
    console.print(Panel(welcome_msg, title="Interactive Session", expand=False))

    # Setup context-aware autocomplete
    completer = MMACompleter()
    session: PromptSession[str] = PromptSession(
        completer=completer,
        auto_suggest=AutoSuggestFromHistory(),
        complete_while_typing=True,
    )

    while True:
        try:
            command = session.prompt("MMA > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Goodbye![/yellow]")
            break

        if command in ["exit", "quit"]:
            console.print("[yellow]Goodbye![/yellow]")
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "analyze":
            if not args:
                console.print("[red]Usage: analyze <ticker> (e.g., AAPL, TSLA)[/red]")
                continue
            analyze(args[0])

        elif cmd == "chart":
            if not args:
                console.print("[red]Usage: chart <ticker> (e.g., AAPL, TSLA)[/red]")
                continue
            chart(args[0])

        elif cmd == "popular":
            table = Table(title="Popular Tickers")
            table.add_column("Name", style="cyan")
            table.add_column("Ticker", style="magenta")
            table.add_column("Type", style="green")

            rows = [
                ("Apple", "AAPL", "Stock"),
                ("NVIDIA", "NVDA", "Stock"),
                ("Tesla", "TSLA", "Stock"),
                ("S&P 500 ETF", "SPY", "ETF"),
                ("Bitcoin", "BTC-USD", "Crypto"),
                ("Ethereum", "ETH-USD", "Crypto"),
                ("Gold", "GC=F", "Commodity"),
            ]
            for row in rows:
                table.add_row(*row)
            console.print(table)

        elif cmd == "help":
            console.print(welcome_msg)

        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")
            console.print("Type [bold cyan]help[/bold cyan] to see available commands.")


if __name__ == "__main__":
    app()
