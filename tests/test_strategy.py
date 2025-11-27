import pandas as pd

from mini_market_analyzer.strategy import MarketRegime, Signal, analyze_market


def test_analyze_market_bullish_buy() -> None:
    # Setup: Bullish Trend (Price > EMA50 > EMA200) + Oversold RSI
    df = pd.DataFrame(
        {
            "close": [150.0],
            "EMA_50": [140.0],
            "EMA_200": [130.0],
            "RSI_14": [25.0],  # Oversold
            "MACD_12_26_9": [1.0],
            "MACDs_12_26_9": [0.5],
        }
    )

    result = analyze_market(df, "TEST")

    assert result.regime == MarketRegime.BULLISH
    assert result.signal == Signal.BUY
    assert result.confidence == 0.8


def test_analyze_market_bearish_sell() -> None:
    # Setup: Bearish Trend (Price < EMA50 < EMA200) + Overbought RSI
    df = pd.DataFrame(
        {
            "close": [100.0],
            "EMA_50": [110.0],
            "EMA_200": [120.0],
            "RSI_14": [75.0],  # Overbought
            "MACD_12_26_9": [-1.0],
            "MACDs_12_26_9": [-0.5],
        }
    )

    result = analyze_market(df, "TEST")

    assert result.regime == MarketRegime.BEARISH
    assert result.signal == Signal.SELL
    assert result.confidence == 0.8


def test_analyze_market_sideways() -> None:
    # Setup: Sideways (Mixed EMAs)
    df = pd.DataFrame(
        {
            "close": [115.0],
            "EMA_50": [120.0],
            "EMA_200": [110.0],
            "RSI_14": [50.0],
            "MACD_12_26_9": [0.0],
            "MACDs_12_26_9": [0.0],
        }
    )

    result = analyze_market(df, "TEST")

    assert result.regime == MarketRegime.SIDEWAYS
    assert result.signal == Signal.HOLD
