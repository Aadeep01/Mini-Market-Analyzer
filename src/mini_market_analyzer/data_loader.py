import pandas as pd
import yfinance as yf


def fetch_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetches historical market data for a given ticker using yfinance.

    Args:
        ticker: The stock symbol (e.g., "AAPL", "BTC-USD").
        period: The data period to download (e.g., "1y", "1mo", "max").
        interval: The data interval (e.g., "1d", "1h").

    Returns:
        pd.DataFrame: A DataFrame containing OHLCV data.

    Raises:
        ValueError: If no data is found for the ticker.
        ConnectionError: If there is an issue fetching data.
    """
    try:
        # Download data
        df = yf.download(
            ticker, period=period, interval=interval, progress=False, auto_adjust=True
        )

        if df.empty:
            raise ValueError(
                f"No data found for ticker '{ticker}'. Please check the symbol."
            )

        # Ensure standard column names (yfinance sometimes returns MultiIndex columns)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Standardize column names to lowercase
        df.columns = [c.lower() for c in df.columns]

        # Ensure required columns exist
        required_cols = ["open", "high", "low", "close", "volume"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        return df

    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise ConnectionError(f"Failed to fetch data for '{ticker}': {e!s}") from e
