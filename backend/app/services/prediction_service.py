import yfinance as yf
import pandas as pd

from app.ml.prediction import predict_stock_direction


def get_prediction(symbol: str):
    symbol = symbol.strip().upper()

    history = yf.download(
        symbol,
        period="2y",
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(f"No stock data found for {symbol}")

    if isinstance(history.columns, pd.MultiIndex):
        history.columns = history.columns.get_level_values(0)

    result = predict_stock_direction(history)

    return {
        "symbol": symbol,
        **result,
    }


def get_prediction_explanation(symbol: str):
    symbol = symbol.strip().upper()

    history = yf.download(
        symbol,
        period="2y",
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(f"No stock data found for {symbol}")

    if isinstance(history.columns, pd.MultiIndex):
        history.columns = history.columns.get_level_values(0)

    result = predict_stock_direction(history)

    features = result["features"]

    volatility_10 = features["volatility_10"]
    volatility_20 = features["volatility_20"]
    high_low_range = features["high_low_range"]
    open_close_range = features["open_close_range"]

    # ---------------------------------------------------------
    # FEATURE EXPLANATIONS
    # ---------------------------------------------------------

    volatility_10_text = (
        f"Short-term price volatility over the last 10 trading "
        f"sessions is {volatility_10 * 100:.2f}%."
    )

    volatility_20_text = (
        f"Price volatility over the last 20 trading sessions "
        f"is {volatility_20 * 100:.2f}%."
    )

    if high_low_range > 0:
        high_low_text = (
            f"The latest daily high-low range was "
            f"{high_low_range * 100:.2f}% of the closing price."
        )
    else:
        high_low_text = (
            "The latest daily high-low range was very small."
        )

    if open_close_range > 0:
        open_close_text = (
            f"The opening price was above the closing price by "
            f"{open_close_range * 100:.2f}%."
        )
    elif open_close_range < 0:
        open_close_text = (
            f"The closing price was above the opening price by "
            f"{abs(open_close_range) * 100:.2f}%."
        )
    else:
        open_close_text = (
            "The opening and closing prices were approximately equal."
        )

    prediction = result["prediction"]
    confidence = result["confidence"]

    # ---------------------------------------------------------
    # MODEL SUMMARY
    # ---------------------------------------------------------

    if prediction == "UP":
        summary = (
            f"The Random Forest model predicts an upward direction "
            f"with {confidence}% classification confidence based on "
            f"recent volatility and daily price-range features."
        )

    elif prediction == "DOWN":
        summary = (
            f"The Random Forest model predicts a downward direction "
            f"with {confidence}% classification confidence based on "
            f"recent volatility and daily price-range features."
        )

    else:
        summary = (
            f"The Random Forest model does not identify a strong "
            f"directional signal. Its classification confidence is "
            f"{confidence}%, which is below the 65% confidence threshold."
        )

    return {
        "symbol": symbol,
        "prediction": prediction,
        "confidence": confidence,
        "model": result["model"],
        "features": features,
        "indicators": [
            {
                "indicator": "Volatility (10)",
                "value": round(volatility_10 * 100, 2),
                "explanation": volatility_10_text,
            },
            {
                "indicator": "Volatility (20)",
                "value": round(volatility_20 * 100, 2),
                "explanation": volatility_20_text,
            },
            {
                "indicator": "High-Low Range",
                "value": round(high_low_range * 100, 2),
                "explanation": high_low_text,
            },
            {
                "indicator": "Open-Close Range",
                "value": round(open_close_range * 100, 2),
                "explanation": open_close_text,
            },
        ],
        "summary": summary,
    }