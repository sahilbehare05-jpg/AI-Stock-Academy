import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_features(history: pd.DataFrame) -> pd.DataFrame:
    df = history.copy()

    # ---------------------------------------------------------
    # NORMALIZE YFINANCE COLUMNS
    # ---------------------------------------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Make sure important columns are numeric
    for column in ["Open", "High", "Low", "Close", "Volume"]:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # ---------------------------------------------------------
    # PRICE RETURNS / MOMENTUM
    # ---------------------------------------------------------
    df["Return_1D"] = close.pct_change(1, fill_method=None)
    df["Return_3D"] = close.pct_change(3, fill_method=None)
    df["Return_5D"] = close.pct_change(5, fill_method=None)
    df["Return_10D"] = close.pct_change(10, fill_method=None)

    # ---------------------------------------------------------
    # MOVING AVERAGES
    # ---------------------------------------------------------
    df["SMA_10"] = close.rolling(10).mean()
    df["SMA_20"] = close.rolling(20).mean()
    df["SMA_50"] = close.rolling(50).mean()

    df["EMA_10"] = close.ewm(
        span=10,
        adjust=False
    ).mean()

    df["EMA_20"] = close.ewm(
        span=20,
        adjust=False
    ).mean()

    df["EMA_50"] = close.ewm(
        span=50,
        adjust=False
    ).mean()

    # Distance from moving averages
    df["SMA20_distance"] = (
        close / df["SMA_20"] - 1
    )

    df["SMA50_distance"] = (
        close / df["SMA_50"] - 1
    )

    df["EMA20_distance"] = (
        close / df["EMA_20"] - 1
    )

    # ---------------------------------------------------------
    # RSI 14
    # ---------------------------------------------------------
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI_14"] = 100 - (
        100 / (1 + rs)
    )

    # ---------------------------------------------------------
    # MACD
    # ---------------------------------------------------------
    ema_12 = close.ewm(
        span=12,
        adjust=False
    ).mean()

    ema_26 = close.ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema_12 - ema_26

    df["MACD_Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["MACD_Histogram"] = (
        df["MACD"] - df["MACD_Signal"]
    )

    # ---------------------------------------------------------
    # BOLLINGER BANDS
    # ---------------------------------------------------------
    bb_middle = close.rolling(20).mean()
    bb_std = close.rolling(20).std()

    df["BB_Upper"] = (
        bb_middle + 2 * bb_std
    )

    df["BB_Lower"] = (
        bb_middle - 2 * bb_std
    )

    df["BB_Position"] = (
        (close - df["BB_Lower"])
        /
        (df["BB_Upper"] - df["BB_Lower"])
    )

    # ---------------------------------------------------------
    # VOLATILITY
    # ---------------------------------------------------------
    df["Volatility_10"] = (
        df["Return_1D"].rolling(10).std()
    )

    df["Volatility_20"] = (
        df["Return_1D"].rolling(20).std()
    )

    # ---------------------------------------------------------
    # DAILY PRICE RANGE
    # ---------------------------------------------------------
    df["High_Low_Range"] = (
        (high - low) / close
    )

    df["Open_Close_Range"] = (
        (df["Open"] - close) / close
    )

    # ---------------------------------------------------------
    # VOLUME FEATURES
    # ---------------------------------------------------------
    df["Volume_Change"] = volume.pct_change()

    df["Volume_SMA_20"] = (
        volume.rolling(20).mean()
    )

    df["Relative_Volume"] = (
        volume / df["Volume_SMA_20"]
    )

    # ---------------------------------------------------------
    # LAG FEATURES
    # ---------------------------------------------------------
    df["Return_Lag_1"] = df["Return_1D"].shift(1)
    df["Return_Lag_2"] = df["Return_1D"].shift(2)
    df["Return_Lag_3"] = df["Return_1D"].shift(3)
    df["Return_Lag_5"] = df["Return_1D"].shift(5)

    # ---------------------------------------------------------
    # TARGET
    # ---------------------------------------------------------
    # Predict whether the NEXT day's close is higher
    # than today's close.
    df["Target"] = (
        close.shift(-1) > close
    ).astype(int)

    return df


# =============================================================
# MODEL PREDICTION
# =============================================================

def predict_stock_direction(history: pd.DataFrame):

    df = create_features(history)

    # ---------------------------------------------------------
    # PRODUCTION FEATURE SET
    # Validated experimentally:
    # Volatility features performed best among tested groups.
    # ---------------------------------------------------------

    feature_columns = [
        "Volatility_10",
        "Volatility_20",
        "High_Low_Range",
        "Open_Close_Range",
    ]

    # ---------------------------------------------------------
    # TRAINING DATA
    # ---------------------------------------------------------

    training_data = df.dropna(
        subset=feature_columns + ["Target"]
    ).copy()

    if len(training_data) < 80:
        raise ValueError(
            "Not enough historical data to train "
            "the prediction model."
        )

    X = training_data[feature_columns]
    y = training_data["Target"]

    # ---------------------------------------------------------
    # RANDOM FOREST
    # ---------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X, y)

    # ---------------------------------------------------------
    # LATEST AVAILABLE DATA
    # ---------------------------------------------------------

    latest_data = df.dropna(
        subset=feature_columns
    ).copy()

    if latest_data.empty:
        raise ValueError(
            "Not enough valid feature data for prediction."
        )

    latest = latest_data.iloc[-1]

    latest_features = pd.DataFrame(
        [latest[feature_columns].values],
        columns=feature_columns,
    )

    # ---------------------------------------------------------
    # PREDICTION
    # ---------------------------------------------------------

    prediction = int(
        model.predict(latest_features)[0]
    )

    probabilities = model.predict_proba(
        latest_features
    )[0]

    confidence = float(
        max(probabilities) * 100
    )

    # ---------------------------------------------------------
    # CONFIDENCE FILTER
    # ---------------------------------------------------------

    CONFIDENCE_THRESHOLD = 65.0

    if confidence >= CONFIDENCE_THRESHOLD:

        direction = (
            "UP"
            if prediction == 1
            else "DOWN"
        )

    else:

        direction = "NO STRONG SIGNAL"

    # ---------------------------------------------------------
    # RETURN
    # ---------------------------------------------------------

    return {
        "prediction": direction,

        "confidence": round(
            confidence,
            2
        ),

        "model": "Random Forest",

        "features": {
            "volatility_10": float(
                latest["Volatility_10"]
            ),

            "volatility_20": float(
                latest["Volatility_20"]
            ),

            "high_low_range": float(
                latest["High_Low_Range"]
            ),

            "open_close_range": float(
                latest["Open_Close_Range"]
            ),
        },
    }