import yfinance as yf
import pandas as pd
import numpy as np


# ---------------------------------------------------------
# TIMEFRAME CONFIGURATION
# ---------------------------------------------------------

TIMEFRAME_CONFIG = {
    "1m": {
        "yf_interval": "1m",
        "max_period": "7d",
        "rule": None,
    },
    "3m": {
        "yf_interval": "1m",
        "max_period": "7d",
        "rule": "3min",
    },
    "5m": {
        "yf_interval": "5m",
        "max_period": "60d",
        "rule": None,
    },
    "10m": {
        "yf_interval": "5m",
        "max_period": "60d",
        "rule": "10min",
    },
    "15m": {
        "yf_interval": "15m",
        "max_period": "60d",
        "rule": None,
    },
    "30m": {
        "yf_interval": "30m",
        "max_period": "60d",
        "rule": None,
    },
    "1H": {
        "yf_interval": "60m",
        "max_period": "730d",
        "rule": None,
    },
    "1D": {
        "yf_interval": "1d",
        "max_period": None,
        "rule": None,
    },
    "1W": {
        "yf_interval": "1wk",
        "max_period": None,
        "rule": None,
    },
    "1M": {
        "yf_interval": "1mo",
        "max_period": None,
        "rule": None,
    },
}


def _prepare_dataframe(history):
    """Clean and prepare yfinance dataframe."""

    if history.empty:
        return history

    # Flatten MultiIndex columns
    if isinstance(history.columns, pd.MultiIndex):
        history.columns = history.columns.get_level_values(0)

    history = history.reset_index()

    # Make sure timestamp column exists
    if "Date" in history.columns:
        history["Date"] = pd.to_datetime(
            history["Date"],
            errors="coerce",
        )

    if "Datetime" in history.columns:
        history["Datetime"] = pd.to_datetime(
            history["Datetime"],
            errors="coerce",
        )

    return history


def _resample_ohlcv(history, rule):
    """Create custom candles such as 3m and 10m."""

    if history.empty or not rule:
        return history

    time_column = None

    if "Datetime" in history.columns:
        time_column = "Datetime"
    elif "Date" in history.columns:
        time_column = "Date"

    if not time_column:
        return history

    df = history.copy()

    df = df.dropna(
        subset=[time_column]
    )

    df = df.set_index(time_column)

    # OHLCV aggregation
    aggregation = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }

    available = {
        key: value
        for key, value in aggregation.items()
        if key in df.columns
    }

    df = df.resample(rule).agg(available)

    df = df.dropna(
        subset=["Open", "High", "Low", "Close"]
    )

    df = df.reset_index()

    return df


def _calculate_indicators(history):
    """Calculate technical indicators for trading analysis."""

    if history.empty:
        return history

    close = pd.to_numeric(history["Close"], errors="coerce")
    high = pd.to_numeric(history["High"], errors="coerce")
    low = pd.to_numeric(history["Low"], errors="coerce")
    volume = pd.to_numeric(
        history["Volume"],
        errors="coerce",
    ).fillna(0)

    # SMA
    history["SMA_20"] = close.rolling(
        window=20,
        min_periods=1,
    ).mean()

    history["SMA_50"] = close.rolling(
        window=50,
        min_periods=1,
    ).mean()

    # EMA
    history["EMA_20"] = close.ewm(
        span=20,
        adjust=False,
    ).mean()

    history["EMA_50"] = close.ewm(
        span=50,
        adjust=False,
    ).mean()

    # Bollinger Bands
    bb_middle = close.rolling(
        window=20,
        min_periods=1,
    ).mean()

    bb_std = close.rolling(
        window=20,
        min_periods=1,
    ).std()

    history["BB_MIDDLE"] = bb_middle
    history["BB_UPPER"] = bb_middle + (2 * bb_std)
    history["BB_LOWER"] = bb_middle - (2 * bb_std)

    # RSI 14
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(
        window=14,
        min_periods=14,
    ).mean()

    avg_loss = loss.rolling(
        window=14,
        min_periods=14,
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    history["RSI_14"] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = close.ewm(
        span=12,
        adjust=False,
    ).mean()

    ema_26 = close.ewm(
        span=26,
        adjust=False,
    ).mean()

    macd = ema_12 - ema_26

    macd_signal = macd.ewm(
        span=9,
        adjust=False,
    ).mean()

    history["MACD"] = macd
    history["MACD_SIGNAL"] = macd_signal
    history["MACD_HISTOGRAM"] = macd - macd_signal

    # ATR 14
    previous_close = close.shift(1)

    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    history["ATR_14"] = true_range.rolling(
        window=14,
        min_periods=1,
    ).mean()

    # Stochastic
    lowest_low = low.rolling(
        window=14,
        min_periods=1,
    ).min()

    highest_high = high.rolling(
        window=14,
        min_periods=1,
    ).max()

    price_range = (
        highest_high - lowest_low
    ).replace(0, np.nan)

    history["STOCH_K"] = (
        (close - lowest_low) / price_range
    ) * 100

    history["STOCH_D"] = (
        history["STOCH_K"]
        .rolling(
            window=3,
            min_periods=1,
        )
        .mean()
    )

    # VWAP
    typical_price = (high + low + close) / 3

    cumulative_volume = volume.cumsum()

    cumulative_price_volume = (
        typical_price * volume
    ).cumsum()

    history["VWAP"] = (
        cumulative_price_volume
        / cumulative_volume.replace(0, np.nan)
    )

    # OBV
    direction = np.sign(
        close.diff()
    ).fillna(0)

    history["OBV"] = (
        direction * volume
    ).cumsum()

    # CCI 20
    cci_mean = typical_price.rolling(
        window=20,
        min_periods=1,
    ).mean()

    mean_deviation = (
        typical_price
        .rolling(
            window=20,
            min_periods=1,
        )
        .apply(
            lambda values: np.mean(
                np.abs(
                    values - np.mean(values)
                )
            ),
            raw=True,
        )
    )

    history["CCI_20"] = (
        (typical_price - cci_mean)
        / (
            0.015
            * mean_deviation.replace(
                0,
                np.nan,
            )
        )
    )

    return history


def _clean_records(history):
    """Convert dataframe into JSON-safe records."""

    # Convert datetime values to strings
    for column in ["Date", "Datetime"]:
        if column in history.columns:
            history[column] = history[column].apply(
                lambda value: (
                    value.isoformat()
                    if pd.notna(value)
                    else None
                )
            )

    # Replace infinity
    history = history.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # Convert NaN -> None
    history = history.astype(object).where(
        pd.notna(history),
        None,
    )

    return history.to_dict(
        orient="records"
    )


# ---------------------------------------------------------
# MAIN STOCK DATA FUNCTION
# ---------------------------------------------------------

def get_stock_data(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
):
    symbol = symbol.strip().upper()

    interval = interval.strip()

    # Backward compatibility
    old_interval_map = {
    "1h": "1H",
    "60m": "1H",
    "1d": "1D",
    "1day": "1D",
    "day": "1D",
    "week": "1W",
    "month": "1M",
}

    interval = old_interval_map.get(
        interval.lower(),
        interval,
    )

    if interval not in TIMEFRAME_CONFIG:
        raise ValueError(
            f"Unsupported timeframe: {interval}. "
            f"Supported timeframes: "
            f"{', '.join(TIMEFRAME_CONFIG.keys())}"
        )

    config = TIMEFRAME_CONFIG[interval]

    yf_interval = config["yf_interval"]

    # -----------------------------------------------------
    # PERIOD HANDLING
    # -----------------------------------------------------

    requested_period = period.strip()

    if interval in [
        "1m",
        "3m",
    ]:
        allowed_periods = [
            "1d",
            "5d",
            "7d",
        ]

        if requested_period not in allowed_periods:
            requested_period = "7d"

    elif interval in [
        "5m",
        "10m",
        "15m",
        "30m",
    ]:
        allowed_periods = [
            "1d",
            "5d",
            "1mo",
            "3mo",
        ]

        if requested_period not in allowed_periods:
            requested_period = "3mo"

    elif interval == "1H":
        allowed_periods = [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
        ]

        if requested_period not in allowed_periods:
            requested_period = "1y"

    else:
        allowed_periods = [
            "1d",
            "5d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "10y",
            "max",
        ]

        if requested_period not in allowed_periods:
            requested_period = "1mo"

    # -----------------------------------------------------
    # DOWNLOAD DATA
    # -----------------------------------------------------

    history = yf.download(
        symbol,
        period=requested_period,
        interval=yf_interval,
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(
            f"No stock data found for {symbol}"
        )

    # -----------------------------------------------------
    # PREPARE DATA
    # -----------------------------------------------------

    history = _prepare_dataframe(
        history
    )

    # -----------------------------------------------------
    # CUSTOM TIMEFRAMES
    # -----------------------------------------------------

    if config["rule"]:
        history = _resample_ohlcv(
            history,
            config["rule"],
        )

    if history.empty:
        raise ValueError(
            f"No usable stock data found for {symbol}"
        )

    # -----------------------------------------------------
    # INDICATORS
    # -----------------------------------------------------

    history = _calculate_indicators(
        history
    )

    # -----------------------------------------------------
    # JSON RECORDS
    # -----------------------------------------------------

    records = _clean_records(
        history
    )

    if not records:
        raise ValueError(
            f"No stock records available for {symbol}"
        )

    latest = records[-1]

    latest_date = (
        latest.get("Date")
        or latest.get("Datetime")
    )

    return {
        "symbol": symbol,

        "period": requested_period,

        "interval": interval,

        "source_interval": yf_interval,

        "latest": {
            "date": latest_date,

            "open": latest.get("Open"),

            "high": latest.get("High"),

            "low": latest.get("Low"),

            "close": latest.get("Close"),

            "volume": latest.get("Volume"),

            "sma_20": latest.get("SMA_20"),

            "ema_20": latest.get("EMA_20"),

            "rsi_14": latest.get("RSI_14"),
        },

        "history": records,
    }
def get_live_price(symbol: str):
    symbol = symbol.strip().upper()

    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period="1d",
        interval="1m",
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(
            f"No live price data found for {symbol}"
        )

    latest = history.iloc[-1]

    close = float(latest["Close"])

    previous_close = None

    try:
        info = ticker.fast_info
        previous_close = info.get("previous_close")
    except Exception:
        previous_close = None

    if previous_close is None:
        if len(history) > 1:
            previous_close = float(
                history.iloc[-2]["Close"]
            )
        else:
            previous_close = close

    change = close - float(previous_close)

    change_percent = (
        (change / float(previous_close)) * 100
        if float(previous_close) != 0
        else 0
    )

    timestamp = history.index[-1]

    return {
        "symbol": symbol,
        "price": round(close, 2),
        "previous_close": round(
            float(previous_close),
            2,
        ),
        "change": round(change, 2),
        "change_percent": round(
            change_percent,
            2,
        ),
        "timestamp": timestamp.isoformat(),
    }