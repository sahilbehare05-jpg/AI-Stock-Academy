"""
Offline AI Trading Tutor.

This tutor works without an external AI API.
It uses a local educational knowledge base and
keyword-based topic matching.
"""

import re


SYSTEM_INTRO = (
    "I am the AI Trading Tutor for AI Stock Academy. "
    "I can explain stock-market and trading concepts "
    "step by step at your selected learning level."
)


KNOWLEDGE_BASE = {

    "bullish candlestick": {
        "keywords": ["bullish candlestick", "green candle", "bullish candle"],
        "answer": """
### Bullish Candlestick

A bullish candlestick means that the price **closed higher than it opened** during that time period.

For example:

- Open: ₹100
- Close: ₹108
- High: ₹110
- Low: ₹98

Because ₹108 is higher than ₹100, the candle is bullish.

### Key points
- Open < Close
- Often displayed as a green candle
- Shows buying pressure during that period
- A single bullish candle does NOT guarantee that the price will continue rising

### Common mistake
Do not assume that every green candle means "BUY". The surrounding trend, volume, support/resistance and other factors also matter.

### Quick check
If a stock opens at ₹200 and closes at ₹190, is the candle bullish or bearish?
"""
    },

    "bearish candlestick": {
        "keywords": ["bearish candlestick", "red candle", "bearish candle"],
        "answer": """
### Bearish Candlestick

A bearish candlestick means that the price **closed lower than it opened**.

Example:

- Open: ₹200
- Close: ₹190
- High: ₹205
- Low: ₹185

Since the closing price is below the opening price, the candle is bearish.

### Key points
- Open > Close
- Often displayed as a red candle
- Indicates selling pressure during that period
- One bearish candle does not guarantee that the market will fall

### Common mistake
Do not make a trading decision from one candle alone.
"""
    },

    "support": {
        "keywords": ["support", "support level", "support and resistance"],
        "answer": """
### Support

Support is a price area where a stock has historically found buying interest and may have difficulty moving lower.

Imagine a stock repeatedly falling toward ₹100 and then recovering. ₹100 may act as a support area.

### Example

₹120
  ↓
₹110
  ↓
₹100 ← Support
  ↑
₹105
  ↑

### Why does support happen?

Buyers may consider the price attractive around that level, increasing demand.

### Important
Support is not a guaranteed floor. If strong selling pressure breaks the level, the price can move lower.

### Common mistake
Treating support as an exact single price rather than a zone.
"""
    },

    "resistance": {
        "keywords": ["resistance", "resistance level"],
        "answer": """
### Resistance

Resistance is a price area where selling pressure has historically made it difficult for a stock to move higher.

For example, if a stock repeatedly reaches ₹500 and then falls, ₹500 may act as resistance.

### Key idea

Support → potential buying-interest area

Resistance → potential selling-pressure area

Resistance can also be broken. A breakout does not guarantee that the price will continue rising.
"""
    },

    "moving average": {
        "keywords": [
            "moving average",
            "sma",
            "ema",
            "simple moving average",
            "exponential moving average"
        ],
        "answer": """
### Moving Average

A moving average smooths price data to help identify the general direction of a market.

Two common types are:

**SMA — Simple Moving Average**
- Gives equal weight to prices in the selected period.

**EMA — Exponential Moving Average**
- Gives more weight to recent prices.

### Example

A 10-day moving average calculates an average using the relevant 10 trading days and updates as new data arrives.

### Uses
- Identifying trends
- Studying dynamic support/resistance
- Comparing current price with an average price

### Important
Moving averages are lagging indicators because they are calculated from historical prices.
"""
    },

    "rsi": {
        "keywords": ["rsi", "relative strength index"],
        "answer": """
### RSI — Relative Strength Index

RSI is a momentum indicator commonly used to study the strength of recent price movements.

It normally ranges from **0 to 100**.

A commonly used interpretation is:

- Above 70 → potentially overbought
- Below 30 → potentially oversold
- Around 50 → relatively balanced momentum

### Important

RSI above 70 does NOT automatically mean "sell".

RSI below 30 does NOT automatically mean "buy".

Market trend and other evidence should also be considered.
"""
    },

    "volume": {
        "keywords": ["volume", "trading volume", "volume analysis"],
        "answer": """
### Trading Volume

Volume represents the number of shares or contracts traded during a particular period.

Volume can help traders understand how much participation is behind a price movement.

### Example

If a stock rises sharply while volume is also much higher than usual, there may be strong market participation behind the move.

### Key points
- Price tells you what happened to price.
- Volume tells you how much trading activity occurred.
- High volume can provide additional context for breakouts or major moves.

Volume alone should not be treated as a guaranteed signal.
"""
    },

    "fundamental analysis": {
        "keywords": [
            "fundamental analysis",
            "fundamentals",
            "financial statements",
            "company analysis"
        ],
        "answer": """
### Fundamental Analysis

Fundamental analysis evaluates a company's financial and business condition.

Common areas include:

- Revenue
- Profit
- Earnings
- Debt
- Cash flow
- Valuation
- Business growth
- Industry conditions
- Management

### Example

Suppose a company is increasing revenue and profit while maintaining manageable debt. An analyst may consider these factors when evaluating the company.

### Key point

Fundamental analysis focuses more on the underlying business, while technical analysis focuses mainly on price and market data.
"""
    },

    "technical analysis": {
        "keywords": [
            "technical analysis",
            "technical indicators",
            "chart analysis"
        ],
        "answer": """
### Technical Analysis

Technical analysis studies market data such as:

- Price
- Volume
- Candlesticks
- Trends
- Support and resistance
- Indicators
- Chart patterns

The goal is to identify patterns and understand possible market behavior.

### Important

Technical analysis does not predict the future with certainty. It provides a framework for analyzing probabilities and risk.
"""
    },

    "risk management": {
        "keywords": [
            "risk management",
            "manage risk",
            "stop loss",
            "position sizing",
            "risk"
        ],
        "answer": """
### Risk Management

Risk management is one of the most important parts of trading.

It focuses on controlling potential losses rather than trying to guarantee profits.

Important concepts include:

1. Position sizing
2. Stop-loss planning
3. Risk/reward analysis
4. Diversification
5. Avoiding excessive leverage
6. Maintaining a trading plan

### Example

Instead of asking:

"How much can I make?"

A disciplined trader also asks:

"How much could I lose if the idea is wrong?"

### Key point

No trading strategy guarantees profits.
"""
    },

    "candlestick": {
        "keywords": [
            "candlestick",
            "candle",
            "open high low close",
            "ohlc"
        ],
        "answer": """
### Candlestick Chart

A candlestick represents price movement during a specific period.

It contains four important prices:

- Open
- High
- Low
- Close

The candle body shows the relationship between the opening and closing prices.

The wicks/shadows show the high and low reached during that period.

### Example

If:

Open = ₹100
High = ₹110
Low = ₹95
Close = ₹108

the candle is bullish because the close is above the open.

### Quick check

What four prices are represented by a candlestick?

Answer: Open, High, Low and Close.
"""
    },

    "stock market": {
        "keywords": [
            "stock market",
            "share market",
            "what is a stock",
            "what are stocks"
        ],
        "answer": """
### Stock Market

The stock market is a marketplace where shares of companies can be bought and sold.

A share represents a small ownership interest in a company.

### Example

If a company has many shares and you own some of them, you own a small portion of that company.

Stock prices change because of factors such as:

- Supply and demand
- Company performance
- Economic conditions
- News
- Investor expectations
- Interest rates

### Important

Stock prices can rise or fall, and investing/trading involves risk.
"""
    },

    "trading": {
        "keywords": [
            "what is trading",
            "trading basics",
            "trading meaning",
            "how trading works"
        ],
        "answer": """
### Trading

Trading involves buying and selling financial assets with the goal of benefiting from price movements.

Common styles include:

- Intraday trading
- Swing trading
- Position trading

### Example

A trader may study a stock, create a trading plan, define the acceptable risk and then decide whether to enter or avoid the trade.

### Important

Trading is not guaranteed income. Risk management and discipline are essential.
"""
    },

    "derivatives": {
        "keywords": [
            "derivatives",
            "futures",
            "options",
            "option trading"
        ],
        "answer": """
### Derivatives

A derivative is a financial contract whose value is linked to an underlying asset.

Examples include:

- Futures
- Options

The underlying asset can be a stock, index, commodity or another financial instrument.

### Important

Derivatives can involve significant complexity and risk, especially when leverage is involved.

They should be learned carefully before being used in real trading.
"""
    },

    "algorithmic trading": {
        "keywords": [
            "algorithmic trading",
            "algo trading",
            "automated trading",
            "algorithm trading"
        ],
        "answer": """
### Algorithmic Trading

Algorithmic trading uses computer programs to execute trading rules automatically.

A basic system may contain:

1. Market data
2. Trading rules
3. Signal generation
4. Risk controls
5. Order execution
6. Performance monitoring

### Example

A program could be designed to identify when certain predefined conditions occur and then simulate what would happen.

### Important

An algorithm does not automatically make a strategy profitable. Poor assumptions, bad data and weak risk management can produce poor results.
"""
    },

    "machine learning": {
        "keywords": [
            "machine learning",
            "ml",
            "ai trading",
            "artificial intelligence trading"
        ],
        "answer": """
### Machine Learning in Trading

Machine learning can be used to identify patterns in historical market data.

A typical workflow is:

1. Collect data
2. Clean the data
3. Create features
4. Train a model
5. Test the model
6. Evaluate performance
7. Monitor the model

Possible features include price returns, volume and technical indicators.

### Important

A model performing well on historical data does not guarantee future performance. Overfitting is an important risk.
"""
    },

    "trend": {
        "keywords": [
            "trend",
            "uptrend",
            "downtrend",
            "sideways market"
        ],
        "answer": """
### Market Trend

A trend describes the general direction of price movement.

**Uptrend**
- Higher highs
- Higher lows

**Downtrend**
- Lower highs
- Lower lows

**Sideways**
- Price moves within a relatively defined range.

### Important

Trends can change. Always consider the timeframe being analyzed.
"""
    },
}


def normalize(text: str) -> str:
    """Normalize text for simple matching."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def find_topic(question: str):
    """Find the best matching local topic."""
    q = normalize(question)

    best_topic = None
    best_score = 0

    for topic, data in KNOWLEDGE_BASE.items():
        score = 0

        for keyword in data["keywords"]:
            keyword = normalize(keyword)

            if keyword in q:
                # Longer/more specific keywords get more weight.
                score += len(keyword)

        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic


def general_response(question: str, level: str) -> str:
    """Fallback response when no topic matches."""

    return f"""
### AI Trading Tutor

You asked:

**{question}**

I don't have a dedicated lesson for that topic in my current offline knowledge base.

Your selected level is **{level}**.

I can currently explain topics such as:

- Stock market basics
- Trading basics
- Candlestick charts
- Bullish and bearish candles
- Support and resistance
- Technical analysis
- Moving averages
- RSI
- Volume
- Fundamental analysis
- Risk management
- Market trends
- Derivatives
- Algorithmic trading
- Machine learning in trading

Try asking something like:

**"What is support and resistance?"**

or

**"Explain RSI for a beginner."**

This tutor is educational and does not provide guaranteed trading signals or guaranteed profits.
"""


def ask_tutor(
    question: str,
    level: str = "Beginner",
    context: str = "",
) -> str:

    topic = find_topic(question)

    if topic:
        answer = KNOWLEDGE_BASE[topic]["answer"]

        level_note = f"\n\n**Learning level:** {level}"

        return answer.strip() + level_note

    return general_response(question, level)