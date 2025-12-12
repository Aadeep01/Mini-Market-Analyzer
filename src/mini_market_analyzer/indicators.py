import pandas as pd
import pandas_ta as ta  # noqa: F401


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical indicators to the DataFrame using pandas-ta Strategy.

    Indicators:
    - EMA: 50, 200
    - MACD: 12, 26, 9
    - RSI: 14
    - Bollinger Bands: 20, 2
    - ATR: 14
    """
    # Run the strategy
    # We use a copy to avoid SettingWithCopy warnings on the original df if passed
    df_analyzed = df.copy()

    # Trend
    df_analyzed.ta.ema(length=50, append=True)
    df_analyzed.ta.ema(length=200, append=True)
    df_analyzed.ta.macd(fast=12, slow=26, signal=9, append=True)

    # Momentum
    df_analyzed.ta.rsi(length=14, append=True)

    # Volatility
    df_analyzed.ta.bbands(length=20, std=2, append=True)
    df_analyzed.ta.atr(length=14, append=True)

    return df_analyzed
