import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]

PERIOD = "5y"
HORIZON = 3
INITIAL_TRAINING = 500
TEST_BLOCK = 60


# ============================================================
# FEATURE CREATION
# ============================================================

def create_features(history: pd.DataFrame) -> pd.DataFrame:

    df = history.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close = pd.to_numeric(df["Close"], errors="coerce")
    open_price = pd.to_numeric(df["Open"], errors="coerce")
    high = pd.to_numeric(df["High"], errors="coerce")
    low = pd.to_numeric(df["Low"], errors="coerce")
    volume = pd.to_numeric(df["Volume"], errors="coerce")

    # --------------------------------------------------------
    # PRICE / RETURN FEATURES
    # --------------------------------------------------------

    df["Return_1D"] = close.pct_change(1, fill_method=None)
    df["Return_3D"] = close.pct_change(3, fill_method=None)
    df["Return_5D"] = close.pct_change(5, fill_method=None)
    df["Return_10D"] = close.pct_change(10, fill_method=None)

    df["Open_Close_Range"] = (close - open_price) / open_price
    df["High_Low_Range"] = (high - low) / close

    # --------------------------------------------------------
    # TECHNICAL INDICATORS
    # --------------------------------------------------------

    df["SMA20"] = close.rolling(20).mean()
    df["SMA50"] = close.rolling(50).mean()

    df["EMA20"] = close.ewm(
        span=20,
        adjust=False
    ).mean()

    df["EMA50"] = close.ewm(
        span=50,
        adjust=False
    ).mean()

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI14"] = 100 - (
        100 / (1 + rs)
    )

    # MACD

    ema12 = close.ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    # --------------------------------------------------------
    # VOLATILITY FEATURES
    # --------------------------------------------------------

    df["Volatility_10"] = (
        df["Return_1D"].rolling(10).std()
    )

    df["Volatility_20"] = (
        df["Return_1D"].rolling(20).std()
    )

    df["Volatility_50"] = (
        df["Return_1D"].rolling(50).std()
    )

    # --------------------------------------------------------
    # VOLUME FEATURES
    # --------------------------------------------------------

    df["Volume_Change"] = volume.pct_change(
        1,
        fill_method=None
    )

    df["Volume_SMA20"] = volume.rolling(20).mean()

    df["Volume_Ratio"] = (
        volume / df["Volume_SMA20"]
    )

    # --------------------------------------------------------
    # LAG FEATURES
    # --------------------------------------------------------

    df["Return_Lag_1"] = df["Return_1D"].shift(1)
    df["Return_Lag_2"] = df["Return_1D"].shift(2)
    df["Return_Lag_3"] = df["Return_1D"].shift(3)
    df["Return_Lag_5"] = df["Return_1D"].shift(5)

    # --------------------------------------------------------
    # DISTANCE FROM MOVING AVERAGES
    # --------------------------------------------------------

    df["SMA20_distance"] = (
        close / df["SMA20"] - 1
    )

    df["SMA50_distance"] = (
        close / df["SMA50"] - 1
    )

    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

    df["Target"] = (
        close.shift(-HORIZON) > close
    ).astype(int)

    return df


# ============================================================
# FEATURE GROUPS
# ============================================================

FEATURE_GROUPS = {

    "Price + Returns": [
        "Return_1D",
        "Return_3D",
        "Return_5D",
        "Return_10D",
        "Open_Close_Range",
        "High_Low_Range",
    ],

    "Technical Indicators": [
        "SMA20",
        "SMA50",
        "EMA20",
        "EMA50",
        "RSI14",
        "MACD",
        "MACD_Signal",
        "SMA20_distance",
        "SMA50_distance",
    ],

    "Volatility": [
        "Volatility_10",
        "Volatility_20",
        "Volatility_50",
    ],

    "Volume": [
        "Volume_Change",
        "Volume_SMA20",
        "Volume_Ratio",
    ],

    "Lag Features": [
        "Return_Lag_1",
        "Return_Lag_2",
        "Return_Lag_3",
        "Return_Lag_5",
    ],

}


FEATURE_GROUPS["All Features"] = list(
    dict.fromkeys(
        feature
        for group_name, group in FEATURE_GROUPS.items()
        for feature in group
    )
)


# ============================================================
# WALK-FORWARD EVALUATION
# ============================================================

def evaluate_model(
    df: pd.DataFrame,
    features: list
):

    data = df.dropna(
        subset=features + ["Target"]
    ).copy()

    if len(data) < INITIAL_TRAINING + TEST_BLOCK:
        return None

    y_true = []
    y_pred = []

    start = INITIAL_TRAINING

    while start < len(data):

        end = min(
            start + TEST_BLOCK,
            len(data)
        )

        train = data.iloc[:start]
        test = data.iloc[start:end]

        if len(test) == 0:
            break

        X_train = train[features]
        y_train = train["Target"]

        X_test = test[features]

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            max_depth=6,
            n_jobs=1,
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(X_test)

        y_true.extend(
            test["Target"].astype(int).tolist()
        )

        y_pred.extend(
            predictions.astype(int).tolist()
        )

        start = end

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    return {
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "predictions": len(y_true),
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

print()
print("=" * 70)
print("FEATURE GROUP SELECTION EXPERIMENT")
print("=" * 70)

print()
print("Stocks:", ", ".join(STOCKS))
print("Period:", PERIOD)
print("Prediction horizon:", HORIZON, "days")
print("Initial training:", INITIAL_TRAINING)
print("Test block:", TEST_BLOCK)
print("Validation: Walk-forward chronological")
print()
print("=" * 70)


all_results = []


for symbol in STOCKS:

    print()
    print("=" * 70)
    print("STOCK:", symbol)
    print("=" * 70)

    try:

        print("Downloading data...")

        history = yf.download(
            symbol,
            period=PERIOD,
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if history.empty:
            print("No data available.")
            continue

        if isinstance(
            history.columns,
            pd.MultiIndex
        ):
            history.columns = (
                history.columns
                .get_level_values(0)
            )

        print(
            "Rows downloaded:",
            len(history)
        )

        print("Creating features...")

        df = create_features(history)

        print(
            "Valid rows:",
            len(df.dropna())
        )

        for group_name, features in FEATURE_GROUPS.items():

            print(
                f"Testing {group_name}..."
            )

            result = evaluate_model(
                df,
                features
            )

            if result is None:
                print(
                    "  Not enough data."
                )
                continue

            print(
                f"  Accuracy={result['accuracy']:.2f}% "
                f"| Precision={result['precision']:.2f}% "
                f"| Recall={result['recall']:.2f}% "
                f"| F1={result['f1']:.2f}% "
                f"| N={result['predictions']}"
            )

            all_results.append({
                "stock": symbol,
                "group": group_name,
                **result
            })

    except Exception as e:

        print(
            f"ERROR testing {symbol}: {e}"
        )


# ============================================================
# AVERAGES
# ============================================================

print()
print("=" * 70)
print("AVERAGE PERFORMANCE BY FEATURE GROUP")
print("=" * 70)

if all_results:

    results_df = pd.DataFrame(
        all_results
    )

    averages = (
        results_df
        .groupby("group")
        [
            [
                "accuracy",
                "precision",
                "recall",
                "f1",
            ]
        ]
        .mean()
        .sort_values(
            "accuracy",
            ascending=False
        )
    )

    print()

    for group_name, row in averages.iterrows():

        print(
            f"{group_name}:"
        )

        print(
            f"  Accuracy  = {row['accuracy']:.2f}%"
        )

        print(
            f"  Precision = {row['precision']:.2f}%"
        )

        print(
            f"  Recall    = {row['recall']:.2f}%"
        )

        print(
            f"  F1        = {row['f1']:.2f}%"
        )

        print()

    best_accuracy = averages.iloc[0]

    best_f1_name = averages["f1"].idxmax()
    best_accuracy_name = averages.index[0]

    print("=" * 70)
    print("BEST FEATURE GROUP BY ACCURACY")
    print("=" * 70)

    print(
        "Feature Group:",
        best_accuracy_name
    )

    print(
        f"Accuracy: {best_accuracy['accuracy']:.2f}%"
    )

    print(
        f"F1 Score: {best_accuracy['f1']:.2f}%"
    )

    print()

    print("=" * 70)
    print("BEST FEATURE GROUP BY F1")
    print("=" * 70)

    print(
        "Feature Group:",
        best_f1_name
    )

    print(
        f"Accuracy: "
        f"{averages.loc[best_f1_name, 'accuracy']:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{averages.loc[best_f1_name, 'f1']:.2f}%"
    )

else:

    print("No results generated.")


print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)