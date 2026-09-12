import asyncio

from app.database.db import connect_to_mongo, close_mongo_connection, get_database, Collections


MODULES = [
    {
        "title": "Absolute Beginner",
        "description": "Start from zero and understand what money, investing, trading and financial markets are.",
        "level": "Beginner",
        "order": 1,
        "lesson_count": 10,
    },
    {
        "title": "Stock Market Fundamentals",
        "description": "Learn stocks, exchanges, IPOs, indexes, dividends, market capitalization and essential market terminology.",
        "level": "Beginner",
        "order": 2,
        "lesson_count": 12,
    },
    {
        "title": "Trading Basics",
        "description": "Understand buying, selling, order types, intraday trading, delivery, swing trading and position management.",
        "level": "Beginner",
        "order": 3,
        "lesson_count": 12,
    },
    {
        "title": "Reading Charts",
        "description": "Learn candlesticks, price structure, trends, support, resistance, breakouts, pullbacks and gaps.",
        "level": "Beginner",
        "order": 4,
        "lesson_count": 14,
    },
    {
        "title": "Technical Analysis",
        "description": "Learn major technical indicators including SMA, EMA, RSI, MACD, Bollinger Bands, VWAP and volume analysis.",
        "level": "Intermediate",
        "order": 5,
        "lesson_count": 18,
    },
    {
        "title": "Advanced Chart Analysis",
        "description": "Study chart patterns, Fibonacci tools, price action, divergence, multi-timeframe analysis and advanced setups.",
        "level": "Intermediate",
        "order": 6,
        "lesson_count": 16,
    },
    {
        "title": "Fundamental Analysis",
        "description": "Learn how to analyze companies using financial statements, ratios, cash flow, growth, valuation and business quality.",
        "level": "Intermediate",
        "order": 7,
        "lesson_count": 20,
    },
    {
        "title": "Trading Strategies",
        "description": "Study trend following, breakouts, pullbacks, momentum, mean reversion and strategy evaluation.",
        "level": "Intermediate",
        "order": 8,
        "lesson_count": 18,
    },
    {
        "title": "Risk Management",
        "description": "Learn capital preservation, position sizing, stop-losses, risk-reward, drawdown and portfolio exposure.",
        "level": "Advanced",
        "order": 9,
        "lesson_count": 14,
    },
    {
        "title": "Trading Psychology",
        "description": "Understand discipline, fear, greed, FOMO, overconfidence, cognitive biases and building a trading plan.",
        "level": "Advanced",
        "order": 10,
        "lesson_count": 12,
    },
    {
        "title": "Advanced Market Knowledge",
        "description": "Learn market cycles, economic indicators, interest rates, inflation, central banks, sectors and global markets.",
        "level": "Advanced",
        "order": 11,
        "lesson_count": 16,
    },
    {
        "title": "Derivatives",
        "description": "Understand futures, options, calls, puts, strike prices, expiry, open interest, volatility and Greeks.",
        "level": "Advanced",
        "order": 12,
        "lesson_count": 20,
    },
    {
        "title": "Quantitative, Algorithmic & AI Trading",
        "description": "Learn statistics, time series, backtesting, algorithmic trading, machine learning and AI applications in trading.",
        "level": "Advanced",
        "order": 13,
        "lesson_count": 20,
    },
]


async def seed_academy():
    connect_to_mongo()

    try:
        db = get_database()
        modules = db[Collections.MODULES]

        inserted = 0
        existing = 0

        for module in MODULES:
            result = await modules.update_one(
                {"order": module["order"]},
                {"$setOnInsert": module},
                upsert=True,
            )

            if result.upserted_id:
                inserted += 1
            else:
                existing += 1

        print(f"Academy modules inserted: {inserted}")
        print(f"Academy modules already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_academy())