import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


STOCKS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "TSLA",
]

PERIOD = "5y"
HORIZON = 3


FEATURE_COLUMNS = [
    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",
    "SMA20_distance",
    "SMA50_distance",
    "EMA20_distance",
    "RSI",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "Volatility10",
    "Volatility20",
    "High_Low_Range",
    "Open_Close_Range",
    "VolumeChange",
    "RelativeVolume",
    "Return_Lag_1",
    "Return_Lag_2",
    "Return_Lag_3",
    "Return_Lag_5",
]


def prepare_data(symbol):

    history = yf.download(
        symbol,
        period=PERIOD,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(
            f"No data found for {symbol}"
        )

    if isinstance(
        history.columns,
        pd.MultiIndex,
    ):
        history.columns = (
            history.columns
            .get_level_values(0)
        )

    df = history.copy()

    close = df["Close"]

    # Returns
    df["Return_1D"] = close.pct_change(
        1,
        fill_method=None,
    )

    df["Return_3D"] = close.pct_change(
        3,
        fill_method=None,
    )

    df["Return_5D"] = close.pct_change(
        5,
        fill_method=None,
    )

    df["Return_10D"] = close.pct_change(
        10,
        fill_method=None,
    )

    # Moving averages
    sma20 = close.rolling(20).mean()
    sma50 = close.rolling(50).mean()

    ema20 = close.ewm(
        span=20,
        adjust=False,
    ).mean()

    df["SMA20_distance"] = (
        close / sma20 - 1
    )

    df["SMA50_distance"] = (
        close / sma50 - 1
    )

    df["EMA20_distance"] = (
        close / ema20 - 1
    )

    # RSI
    delta = close.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = (
        avg_gain /
        avg_loss.replace(
            0,
            np.nan,
        )
    )

    df["RSI"] = (
        100 -
        (100 / (1 + rs))
    )

    # MACD
    ema12 = close.ewm(
        span=12,
        adjust=False,
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False,
    ).mean()

    macd = ema12 - ema26

    macd_signal = macd.ewm(
        span=9,
        adjust=False,
    ).mean()

    df["MACD"] = macd
    df["MACD_Signal"] = macd_signal
    df["MACD_Histogram"] = (
        macd - macd_signal
    )

    # Volatility
    df["Volatility10"] = (
        df["Return_1D"]
        .rolling(10)
        .std()
    )

    df["Volatility20"] = (
        df["Return_1D"]
        .rolling(20)
        .std()
    )

    # Price ranges
    df["High_Low_Range"] = (
        (df["High"] - df["Low"])
        / close
    )

    df["Open_Close_Range"] = (
        (df["Close"] - df["Open"])
        / df["Open"]
    )

    # Volume
    df["VolumeChange"] = (
        df["Volume"].pct_change(
            fill_method=None
        )
    )

    volume_average = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["RelativeVolume"] = (
        df["Volume"]
        / volume_average
    )

    # Lagged returns
    df["Return_Lag_1"] = (
        df["Return_1D"].shift(1)
    )

    df["Return_Lag_2"] = (
        df["Return_1D"].shift(2)
    )

    df["Return_Lag_3"] = (
        df["Return_1D"].shift(3)
    )

    df["Return_Lag_5"] = (
        df["Return_1D"].shift(5)
    )

    # 3-day target
    future_return = (
        close.shift(-HORIZON)
        / close
        - 1
    )

    df["Target"] = (
        future_return > 0
    ).astype(int)

    data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    return data


def evaluate(symbol):

    data = prepare_data(symbol)

    split = int(
        len(data) * 0.80
    )

    train = data.iloc[:split]
    test = data.iloc[split:]

    X_train = train[
        FEATURE_COLUMNS
    ]

    y_train = train[
        "Target"
    ]

    X_test = test[
        FEATURE_COLUMNS
    ]

    y_test = test[
        "Target"
    ]

    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.03,
        max_depth=3,
        min_samples_leaf=5,
        random_state=42,
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    return {
        "accuracy": accuracy_score(
            y_test,
            predictions,
        ) * 100,

        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ) * 100,

        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ) * 100,

        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ) * 100,

        "train": len(train),
        "test": len(test),
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n=========================================="
)

print(
    "GRADIENT BOOSTING MULTI-STOCK BENCHMARK"
)

print(
    "==========================================\n"
)

print(
    f"Period: {PERIOD}"
)

print(
    f"Prediction horizon: {HORIZON} days"
)

print(
    "Split: 80/20 chronological\n"
)


results = []


for symbol in STOCKS:

    print(
        f"Testing {symbol}..."
    )

    try:

        result = evaluate(
            symbol
        )

        results.append({
            "symbol": symbol,
            **result,
        })

    except Exception as e:

        print(
            f"ERROR {symbol}: {e}"
        )


print(
    "\n=========================================="
)

print(
    "RESULTS"
)

print(
    "==========================================\n"
)


for r in results:

    print(
        f"{r['symbol']}: "
        f"Accuracy={r['accuracy']:.2f}% | "
        f"Precision={r['precision']:.2f}% | "
        f"Recall={r['recall']:.2f}% | "
        f"F1={r['f1']:.2f}%"
    )


if results:

    avg_accuracy = (
        sum(
            r["accuracy"]
            for r in results
        )
        / len(results)
    )

    avg_precision = (
        sum(
            r["precision"]
            for r in results
        )
        / len(results)
    )

    avg_recall = (
        sum(
            r["recall"]
            for r in results
        )
        / len(results)
    )

    avg_f1 = (
        sum(
            r["f1"]
            for r in results
        )
        / len(results)
    )

    print(
        "\n=========================================="
    )

    print(
        "AVERAGE PERFORMANCE"
    )

    print(
        "=========================================="
    )

    print(
        f"Accuracy:  {avg_accuracy:.2f}%"
    )

    print(
        f"Precision: {avg_precision:.2f}%"
    )

    print(
        f"Recall:    {avg_recall:.2f}%"
    )

    print(
        f"F1 Score:  {avg_f1:.2f}%"
    )


print(
    "\nExperiment complete."
)