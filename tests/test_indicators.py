import pandas as pd
import pandas_ta as ta  # noqa: F401

from mini_market_analyzer.indicators import add_indicators


def test_add_indicators() -> None:
    # Create a dummy DataFrame with enough data for indicators
    data = {
        "close": [100 + i for i in range(300)],
        "high": [105 + i for i in range(300)],
        "low": [95 + i for i in range(300)],
        "open": [100 + i for i in range(300)],
        "volume": [1000 for _ in range(300)],
    }
    df = pd.DataFrame(data)

    df_analyzed = add_indicators(df)

    # Check if new columns were added
    expected_cols = [
        "EMA_50",
        "EMA_200",
        "MACD_12_26_9",
        "MACDs_12_26_9",
        "RSI_14",
        "ATRr_14",
    ]

    for col in expected_cols:
        assert col in df_analyzed.columns, f"Missing indicator column: {col}"

    # Ensure original data is preserved
    assert len(df_analyzed) == len(df)
    assert "close" in df_analyzed.columns
