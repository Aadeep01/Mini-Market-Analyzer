from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mini_market_analyzer.data_loader import fetch_data


@pytest.fixture
def mock_yf_download() -> Generator[MagicMock, None, None]:
    with patch("yfinance.download") as mock:
        yield mock


def test_fetch_data_success(mock_yf_download: MagicMock) -> None:
    # Mock successful data return
    mock_df = pd.DataFrame(
        {
            "Open": [100.0],
            "High": [105.0],
            "Low": [95.0],
            "Close": [102.0],
            "Volume": [1000],
        }
    )
    mock_yf_download.return_value = mock_df

    df = fetch_data("AAPL")

    assert not df.empty
    assert "close" in df.columns
    assert "volume" in df.columns
    mock_yf_download.assert_called_once()


def test_fetch_data_empty(mock_yf_download: MagicMock) -> None:
    # Mock empty data return
    mock_yf_download.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No data found"):
        fetch_data("INVALID")


def test_fetch_data_missing_columns(mock_yf_download: MagicMock) -> None:
    # Mock data with missing columns
    mock_df = pd.DataFrame({"Close": [100.0]})
    mock_yf_download.return_value = mock_df

    with pytest.raises(ValueError, match="Missing required columns"):
        fetch_data("AAPL")
