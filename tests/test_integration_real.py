import pandas_ta as ta  # noqa: F401
import pytest

from mini_market_analyzer.data_loader import fetch_data
from mini_market_analyzer.indicators import add_indicators


@pytest.mark.integration
def test_indicators_with_real_data() -> None:
    """
    Integration test that fetches REAL data from Yahoo Finance
    and verifies indicator calculations.
    """
    ticker = "SPY"
    print(f"\nFetching real-time data for {ticker}...")

    # 1. Fetch Real Data (no mocking)
    try:
        df = fetch_data(ticker, period="2y")
    except Exception as e:
        pytest.fail(f"Failed to fetch real data: {e}")

    assert not df.empty, "Fetched DataFrame should not be empty"
    print(f"Fetched {len(df)} rows of real data.")

    # 2. Apply Indicators
    df_analyzed = add_indicators(df)

    # 3. Verify Columns
    expected_cols = [
        "EMA_50",
        "EMA_200",
        "MACD_12_26_9",
        "MACDs_12_26_9",
        "RSI_14",
        "ATRr_14",
    ]
    for col in expected_cols:
        assert col in df_analyzed.columns, f"Missing {col} in real data analysis"

    # 4. Sanity Checks on Values
    # RSI should be between 0 and 100
    rsi = df_analyzed["RSI_14"].dropna()
    assert ((rsi >= 0) & (rsi <= 100)).all(), "RSI values must be between 0 and 100"

    # MACD should not be all NaN (after warmup)
    macd = df_analyzed["MACD_12_26_9"].dropna()
    assert not macd.empty, "MACD should have calculated values"

    print("Real data verification successful!")
