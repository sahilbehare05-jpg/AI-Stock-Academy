import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def prepare_data(symbol, period="5y"):
    history = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(f"No data for {symbol}")

    if isinstance(history.columns, pd.MultiIndex):
        history.columns = history.columns.get_level_values(0)

    df = history.copy()

    close = df["Close"]

    # Returns
    df["Return_1D"] = close.pct_change(1)
    df["Return_3D"] = close.pct_change(3)
    df["Return_5D"] = close.pct_change(5)
    df["Return_10D"] = close.pct_change(10)

    # Moving averages
    df["SMA20"] = close.rolling(20).mean()
    df["SMA50"] = close.rolling(50).mean()

    df["SMA20_distance"] = (
        close / df["SMA20"] - 1
    )

    df["SMA50_distance"] = (
        close / df["SMA50"] - 1
    )

    # RSI
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI"] = (
        100 - (100 / (1 + rs))
    )

    # Volatility
    df["Volatility20"] = (
        df["Return_1D"].rolling(20).std()
    )

    # Volume
    df["VolumeChange"] = (
        df["Volume"].pct_change()
    )

    df["RelativeVolume"] = (
        df["Volume"] /
        df["Volume"].rolling(20).mean()
    )

    feature_columns = [
        "Return_1D",
        "Return_3D",
        "Return_5D",
        "Return_10D",
        "SMA20_distance",
        "SMA50_distance",
        "RSI",
        "Volatility20",
        "VolumeChange",
        "RelativeVolume",
    ]

    return df, feature_columns


def test_horizon(
    df,
    feature_columns,
    horizon,
):
    data = df.copy()

    future_return = (
        data["Close"].shift(-horizon)
        / data["Close"]
        - 1
    )

    data["Target"] = (
        future_return > 0
    ).astype(int)

    data = data.dropna(
        subset=feature_columns + ["Target"]
    )

    if len(data) < 200:
        return None

    split = int(
        len(data) * 0.80
    )

    train = data.iloc[:split]
    test = data.iloc[split:]

    X_train = train[feature_columns]
    y_train = train["Target"]

    X_test = test[feature_columns]
    y_test = test["Target"]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    return {
        "accuracy": accuracy * 100,
        "train": len(train),
        "test": len(test),
        "actual_up": int(
            (y_test == 1).sum()
        ),
        "actual_down": int(
            (y_test == 0).sum()
        ),
    }


symbol = "AAPL"

print("\n================================")
print("PREDICTION HORIZON EXPERIMENT")
print("================================")
print(f"\nStock: {symbol}")
print("Period: 5 years\n")

df, features = prepare_data(
    symbol,
    "5y",
)

for horizon in [
    1,
    3,
    5,
    10,
]:
    result = test_horizon(
        df,
        features,
        horizon,
    )

    if result is None:
        print(
            f"{horizon}-day: insufficient data"
        )
        continue

    print(
        f"{horizon}-day: "
        f"Accuracy={result['accuracy']:.2f}% | "
        f"Train={result['train']} | "
        f"Test={result['test']} | "
        f"UP={result['actual_up']} | "
        f"DOWN={result['actual_down']}"
    )

print("\nExperiment complete.")