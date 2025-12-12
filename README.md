<div align="center">

# Mini Market Analyzer

**A simple CLI tool to check stock prices, indicators, and charts in your terminal.**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5+-blue.svg)](https://aistudio.google.com/app/apikey)

</div>



## Overview

This is a command-line tool that fetches stock data from Yahoo Finance and calculates common technical indicators like RSI, MACD, and Moving Averages. It displays the data in a table and can render candlestick charts directly in your terminal.

**What makes it different:** Every analysis includes an AI-powered summary from **Gemini 2.5 Flash** that explains the market conditions in plain English, so you understand *why* you're seeing a particular signal.

## Key Features

*   **AI Market Summaries**: Get natural language explanations from Gemini 2.5 Flash.
*   **Stock Data**: Fetches live data using `yfinance`.
*   **Indicators**: Calculates RSI, MACD, EMA (50/200), Bollinger Bands, and ATR.
*   **Terminal Charts**: Draws candlestick charts right in your console.
*   **Interactive Mode**: A simple shell to run commands without restarting the app.
*   **Basic Signals**: Tells you if the trend looks Bullish, Bearish, or Sideways based on simple rules.

## Quick Start

This project uses **uv** for dependency management and a **Makefile** for simplified commands.

### Prerequisites

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation

```bash
git clone https://github.com/Aadeep01/Mini-Market-Analyzer.git
cd Mini-Market-Analyzer
make install
```

### Configuration

1. Copy the example config:
```bash
cp .env.example .env
```

2. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

3. Add it to `.env`:
```bash
GEMINI_API_KEY=your_actual_key_here
```

### Usage

Start the interactive dashboard:

```bash
make run
```

Inside the interactive session:
```text
MMA > analyze NVDA
MMA > chart AAPL
MMA > popular
```

Or run a single command:
```bash
make analyze args="NVDA"
```

### Supported Tickers

The tool works with **any ticker supported by Yahoo Finance**, including:
- **Stocks**: `AAPL`, `TSLA`, `RELIANCE.NS` (Indian stocks), `0700.HK` (Hong Kong)
- **Crypto**: `BTC-USD`, `ETH-USD`, `DOGE-USD`
- **ETFs**: `SPY`, `QQQ`, `VOO`
- **Indices**: `^GSPC` (S&P 500), `^NSEI` (Nifty 50)
- **Forex**: `EURUSD=X`, `GBPUSD=X`
- **Commodities**: `GC=F` (Gold), `CL=F` (Crude Oil)

The autocomplete suggestions show popular tickers for convenience, but you can analyze any valid Yahoo Finance symbol.

## Development

We use a `Makefile` to streamline development tasks:

| Command | Description |
| :--- | :--- |
| `make check` | Run **all** quality checks (Lint, Type Check, Tests) |
| `make test` | Run unit tests |
| `make test-integration` | Run integration tests with **real data** |
| `make format` | Auto-format code with Ruff |
