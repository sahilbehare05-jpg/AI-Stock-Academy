"""
SELECTED FEATURE + RANDOM FOREST OPTIMIZATION EXPERIMENT

Selected features:
    Price + Volume + Lag

Stocks:
    AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA

Validation:
    Walk-forward chronological

Prediction horizon:
    3 days
"""

import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]

PERIOD = "5y"
HORIZON = 3

INITIAL_TRAINING = 500
TEST_BLOCK = 60

RANDOM_STATE = 42


# ============================================================
# FEATURE CREATION
# ============================================================

def create_features(data):
    df = data.copy()

    # Handle yfinance MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Basic price features
    df["Return_1D"] = df["Close"].pct_change(fill_method=None)
    df["Return_3D"] = df["Close"].pct_change(3, fill_method=None)

    # Price features
    df["Price_Ratio"] = df["Close"] / df["Open"] - 1
    df["High_Low_Range"] = (
        df["High"] - df["Low"]
    ) / df["Close"]

    # Volume features
    df["Volume_Change"] = df["Volume"].pct_change(
        fill_method=None
    )

    df["Volume_Ratio"] = (
        df["Volume"]
        / df["Volume"].rolling(20).mean()
    )

    # Lag features
    df["Return_Lag_1"] = df["Return_1D"].shift(1)
    df["Return_Lag_2"] = df["Return_1D"].shift(2)
    df["Return_Lag_3"] = df["Return_1D"].shift(3)

    df["Return_Lag_5"] = df["Return_1D"].shift(5)
    df["Return_Lag_10"] = df["Return_1D"].shift(10)

    # Target: direction after 3 trading days
    future_return = (
        df["Close"].shift(-HORIZON)
        / df["Close"]
        - 1
    )

    df["Target"] = (future_return > 0).astype(int)

    df = df.replace([np.inf, -np.inf], np.nan)

    return df


# ============================================================
# SELECTED FEATURE GROUP
# ============================================================

FEATURES = [
    "Price_Ratio",
    "High_Low_Range",
    "Return_1D",
    "Return_3D",
    "Volume_Change",
    "Volume_Ratio",
    "Return_Lag_1",
    "Return_Lag_2",
    "Return_Lag_3",
    "Return_Lag_5",
    "Return_Lag_10",
]


# ============================================================
# MODEL CONFIGURATIONS
# ============================================================

CONFIGURATIONS = {
    "Baseline": {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "More Trees": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "500 Trees": {
        "n_estimators": 500,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "Depth 6": {
        "n_estimators": 300,
        "max_depth": 6,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "Depth 8": {
        "n_estimators": 300,
        "max_depth": 8,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "Depth 12": {
        "n_estimators": 300,
        "max_depth": 12,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
    },

    "Leaf 4": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 4,
        "max_features": "sqrt",
    },

    "Leaf 8": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 8,
        "max_features": "sqrt",
    },

    "Leaf 12": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 12,
        "max_features": "sqrt",
    },

    "Max Features 0.5": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": 0.5,
    },

    "Max Features 0.75": {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": 0.75,
    },

    "Regularized": {
        "n_estimators": 300,
        "max_depth": 8,
        "min_samples_leaf": 5,
        "max_features": 0.75,
    },
}


# ============================================================
# WALK-FORWARD EVALUATION
# ============================================================

def evaluate_configuration(
    df,
    feature_columns,
    model_params,
):
    clean = df[feature_columns + ["Target"]].dropna()

    X = clean[feature_columns]
    y = clean["Target"].astype(int)

    predictions = []
    actuals = []

    start = INITIAL_TRAINING

    while start < len(X):

        train_end = start
        test_end = min(
            start + TEST_BLOCK,
            len(X)
        )

        if train_end >= len(X):
            break

        X_train = X.iloc[:train_end]
        y_train = y.iloc[:train_end]

        X_test = X.iloc[train_end:test_end]
        y_test = y.iloc[train_end:test_end]

        if len(X_test) == 0:
            break

        model = RandomForestClassifier(
            **model_params,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        predictions.extend(pred)
        actuals.extend(y_test)

        start = test_end

    if not predictions:
        return None

    accuracy = accuracy_score(
        actuals,
        predictions
    )

    precision = precision_score(
        actuals,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        actuals,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        actuals,
        predictions,
        zero_division=0
    )

    return {
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "predictions": len(predictions),
    }


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print()
    print("=" * 70)
    print("SELECTED FEATURE + RANDOM FOREST OPTIMIZATION")
    print("=" * 70)
    print()
    print("Selected features: Price + Volume + Lag")
    print(f"Stocks: {', '.join(STOCKS)}")
    print(f"Period: {PERIOD}")
    print(f"Prediction horizon: {HORIZON} days")
    print(f"Initial training: {INITIAL_TRAINING}")
    print(f"Test block: {TEST_BLOCK}")
    print("Validation: Walk-forward chronological")
    print()
    print("=" * 70)
    print()

    all_results = []

    for symbol in STOCKS:

        print("=" * 70)
        print(f"STOCK: {symbol}")
        print("=" * 70)

        try:
            print("Downloading data...")

            data = yf.download(
                symbol,
                period=PERIOD,
                interval="1d",
                auto_adjust=False,
                progress=False,
            )

            print(f"Rows downloaded: {len(data)}")

            if data.empty:
                print("No data available.")
                continue

            print("Creating selected features...")

            df = create_features(data)

            valid = df[
                FEATURES + ["Target"]
            ].dropna()

            print(f"Valid observations: {len(valid)}")
            print(f"Features used: {len(FEATURES)}")
            print()

            stock_results = {}

            for name, params in CONFIGURATIONS.items():

                print(f"Testing {name}...")

                result = evaluate_configuration(
                    df,
                    FEATURES,
                    params,
                )

                if result is None:
                    print("  No valid result.")
                    continue

                stock_results[name] = result

                print(
                    f"  Accuracy={result['accuracy']:.2f}% | "
                    f"Precision={result['precision']:.2f}% | "
                    f"Recall={result['recall']:.2f}% | "
                    f"F1={result['f1']:.2f}% | "
                    f"N={result['predictions']}"
                )

                all_results.append({
                    "stock": symbol,
                    "configuration": name,
                    **result,
                })

            print()

        except Exception as e:

            print(
                f"ERROR while testing {symbol}: {e}"
            )

            continue

    # ========================================================
    # AVERAGES
    # ========================================================

    if not all_results:
        print("No results generated.")
        return

    results_df = pd.DataFrame(all_results)

    print("=" * 70)
    print("AVERAGE PERFORMANCE BY CONFIGURATION")
    print("=" * 70)
    print()

    averages = (
        results_df
        .groupby("configuration")
        .agg({
            "accuracy": "mean",
            "precision": "mean",
            "recall": "mean",
            "f1": "mean",
        })
        .sort_values(
            "accuracy",
            ascending=False
        )
    )

    for configuration, row in averages.iterrows():

        print(f"{configuration}:")
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

    # ========================================================
    # BEST BY ACCURACY
    # ========================================================

    best_accuracy = averages.iloc[0]

    print("=" * 70)
    print("BEST CONFIGURATION BY ACCURACY")
    print("=" * 70)

    print(
        f"Configuration: {averages.index[0]}"
    )
    print(
        f"Accuracy: {best_accuracy['accuracy']:.2f}%"
    )
    print(
        f"Precision: {best_accuracy['precision']:.2f}%"
    )
    print(
        f"Recall: {best_accuracy['recall']:.2f}%"
    )
    print(
        f"F1 Score: {best_accuracy['f1']:.2f}%"
    )

    # ========================================================
    # BEST BY F1
    # ========================================================

    best_f1_name = averages["f1"].idxmax()
    best_f1 = averages.loc[best_f1_name]

    print()
    print("=" * 70)
    print("BEST CONFIGURATION BY F1")
    print("=" * 70)

    print(
        f"Configuration: {best_f1_name}"
    )
    print(
        f"Accuracy: {best_f1['accuracy']:.2f}%"
    )
    print(
        f"Precision: {best_f1['precision']:.2f}%"
    )
    print(
        f"Recall: {best_f1['recall']:.2f}%"
    )
    print(
        f"F1 Score: {best_f1['f1']:.2f}%"
    )

    # ========================================================
    # BASELINE COMPARISON
    # ========================================================

    baseline_accuracy = (
        averages.loc["Baseline", "accuracy"]
    )

    print()
    print("=" * 70)
    print("IMPROVEMENT OVER BASELINE")
    print("=" * 70)
    print()

    for configuration in averages.index:

        improvement = (
            averages.loc[
                configuration,
                "accuracy"
            ]
            - baseline_accuracy
        )

        print(
            f"{configuration}: "
            f"{improvement:+.2f} percentage points"
        )

    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()