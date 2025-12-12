from dataclasses import dataclass
from enum import Enum

import pandas as pd


class MarketRegime(str, Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    SIDEWAYS = "Sideways"


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CAUTION = "CAUTION"


@dataclass
class AnalysisResult:
    ticker: str
    current_price: float
    regime: MarketRegime
    signal: Signal
    rsi: float
    macd: float
    macd_signal: float
    ema_50: float
    ema_200: float
    confidence: float = 0.0


RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70


def analyze_market(df: pd.DataFrame, ticker: str) -> AnalysisResult:
    """
    Analyzes the latest data point to determine market regime and signal.
    Assumes indicators have already been added to the DataFrame.
    """
    # Get latest row
    latest = df.iloc[-1]

    # Extract values (handling potential missing column names from pandas-ta)
    # pandas-ta default names: EMA_50, EMA_200, MACD_12_26_9, MACDs_12_26_9, RSI_14
    close = latest["close"]
    ema_50 = latest.get("EMA_50", 0.0)
    ema_200 = latest.get("EMA_200", 0.0)
    macd = latest.get("MACD_12_26_9", 0.0)
    macd_signal = latest.get("MACDs_12_26_9", 0.0)
    rsi = latest.get("RSI_14", 50.0)

    # 1. Determine Regime
    regime = MarketRegime.SIDEWAYS
    if close > ema_50 > ema_200:
        regime = MarketRegime.BULLISH
    elif close < ema_50 < ema_200:
        regime = MarketRegime.BEARISH

    # 2. Determine Signal
    signal = Signal.HOLD
    confidence = 0.5

    # Simple Logic
    if regime == MarketRegime.BULLISH:
        if rsi < RSI_OVERSOLD:
            signal = Signal.BUY  # Pullback in uptrend
            confidence = 0.8
        elif rsi > RSI_OVERBOUGHT:
            signal = Signal.CAUTION  # Overbought
            confidence = 0.6
        elif macd > macd_signal:
            signal = Signal.BUY  # Momentum follow
            confidence = 0.7

    elif regime == MarketRegime.BEARISH:
        if rsi > RSI_OVERBOUGHT:
            signal = Signal.SELL  # Oversold bounce fade
            confidence = 0.8
        elif rsi < RSI_OVERSOLD:
            signal = Signal.CAUTION  # Oversold
            confidence = 0.6
        elif macd < macd_signal:
            signal = Signal.SELL  # Momentum follow
            confidence = 0.7

    # Sideways logic
    elif rsi < RSI_OVERSOLD:
        signal = Signal.BUY  # Range bound bounce
        confidence = 0.6
    elif rsi > RSI_OVERBOUGHT:
        signal = Signal.SELL  # Range bound fade
        confidence = 0.6

    return AnalysisResult(
        ticker=ticker,
        current_price=close,
        regime=regime,
        signal=signal,
        rsi=rsi,
        macd=macd,
        macd_signal=macd_signal,
        ema_50=ema_50,
        ema_200=ema_200,
        confidence=confidence,
    )
