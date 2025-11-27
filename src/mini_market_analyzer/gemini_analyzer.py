import os

from google import genai
from rich.console import Console

from mini_market_analyzer.strategy import AnalysisResult

console = Console()


class GeminiAnalyzer:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client: genai.Client | None = None

        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                console.print(
                    f"[yellow]Warning: Failed to initialize Gemini client: {e}[/yellow]"
                )
        else:
            console.print(
                "[yellow]Note: GEMINI_API_KEY not found. "
                "AI summaries will be disabled.[/yellow]"
            )

    def generate_summary(self, ticker: str, result: AnalysisResult) -> str:
        """
        Generates a natural language market summary using Gemini 2.5 Flash.
        """
        if not self.client:
            return "AI Summary unavailable (API Key missing)."

        prompt = (
            "You are an expert financial analyst. Provide a concise, 2-sentence market "
            f"summary for {ticker} based on the following technical data:\n\n"
            f"- Price: ${result.current_price:.2f}\n"
            f"- Trend Regime: {result.regime.value}\n"
            f"- Signal: {result.signal.value} (Confidence: {result.confidence:.0%})\n"
            f"- RSI (14): {result.rsi:.2f}\n"
            f"- MACD: {result.macd:.4f} (Signal: {result.macd_signal:.4f})\n"
            f"- EMA 50: {result.ema_50:.2f}\n"
            f"- EMA 200: {result.ema_200:.2f}\n\n"
            f"Explain *why* the signal is {result.signal.value} citing the most "
            f"important indicator. Do not use financial advice disclaimers. "
            f"Keep it professional and direct."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            if response.text:
                return response.text.strip()
            return "No summary generated."
        except Exception as e:
            return f"Error generating summary: {e}"
