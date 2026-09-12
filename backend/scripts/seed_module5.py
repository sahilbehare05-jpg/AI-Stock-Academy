import asyncio

from app.database.db import (
    connect_to_mongo,
    close_mongo_connection,
    get_database,
    Collections,
)


LESSONS = [
    {
        "lesson_order": 1,
        "title": "Introduction to Technical Analysis",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand the purpose of technical analysis.",
                "Understand how price and volume data are used.",
                "Understand the limitations of technical analysis."
            ],
            "explanation": (
                "Technical analysis is the study of market data, especially price "
                "and volume, to identify trends, patterns, momentum and potential "
                "areas of interest. Analysts use charts and indicators to organize "
                "information about market behavior. Technical analysis does not "
                "guarantee future prices or profits."
            ),
            "example": (
                "A trader notices that a stock has been making higher highs and "
                "higher lows while trading volume remains active. The trader can "
                "study this information as part of a technical analysis process "
                "instead of assuming that the upward movement must continue."
            ),
            "key_terms": [
                "Technical Analysis",
                "Price Action",
                "Volume",
                "Trend",
                "Indicator"
            ],
            "takeaways": [
                "Technical analysis primarily studies market data.",
                "Price and volume are important sources of information.",
                "Technical analysis provides observations and probabilities, not certainty."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Dow Theory Basics",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand the basic ideas behind Dow Theory.",
                "Understand primary, secondary and minor market movements.",
                "Understand why trends are important in technical analysis."
            ],
            "explanation": (
                "Dow Theory is a foundational framework for studying market trends. "
                "Its commonly taught principles include the idea that markets reflect "
                "available information, that prices move in trends, and that trends "
                "can have different degrees or durations. It also emphasizes studying "
                "confirmation and market behavior rather than relying on isolated price moves."
            ),
            "example": (
                "If an index continues to form higher highs and higher lows over a "
                "long period, a technical analyst may classify the broader movement "
                "as an upward primary trend while separately studying shorter corrections."
            ),
            "key_terms": [
                "Dow Theory",
                "Primary Trend",
                "Secondary Trend",
                "Minor Trend",
                "Confirmation"
            ],
            "takeaways": [
                "Dow Theory is one of the foundations of technical analysis.",
                "Markets can contain trends of different durations.",
                "Broader trend analysis should consider multiple pieces of evidence."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Price Action",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand price action.",
                "Learn how traders study raw price movement.",
                "Understand the relationship between price action and indicators."
            ],
            "explanation": (
                "Price action refers to the study of how price moves over time "
                "without requiring an indicator to interpret every movement. "
                "Traders may examine swing highs, swing lows, candles, breakouts, "
                "rejections and changes in market structure. Indicators can be added "
                "later as supporting tools."
            ),
            "example": (
                "A stock repeatedly makes higher highs and higher lows. A trader "
                "studying price action may identify this structure before adding "
                "any moving average or oscillator."
            ),
            "key_terms": [
                "Price Action",
                "Swing High",
                "Swing Low",
                "Breakout",
                "Rejection",
                "Market Structure"
            ],
            "takeaways": [
                "Price action focuses directly on market price behavior.",
                "Market structure is an important part of price-action analysis.",
                "Indicators can complement price action but do not replace judgment."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Market Trends & Structure",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand market structure.",
                "Identify higher highs, higher lows, lower highs and lower lows.",
                "Understand how structure can change."
            ],
            "explanation": (
                "Market structure describes the sequence of significant highs and "
                "lows in price. A series of higher highs and higher lows is commonly "
                "associated with an upward structure, while lower highs and lower "
                "lows indicate downward structure. A change in this sequence can "
                "suggest that the previous structure is weakening or changing."
            ),
            "example": (
                "If a stock moves from ₹100 to ₹120, pulls back to ₹110, and then "
                "rises to ₹130, the sequence contains a higher high and higher low "
                "relative to the earlier movement."
            ),
            "key_terms": [
                "Market Structure",
                "Higher High",
                "Higher Low",
                "Lower High",
                "Lower Low"
            ],
            "takeaways": [
                "Market structure is based on meaningful highs and lows.",
                "Higher highs and higher lows commonly describe upward structure.",
                "Structure can change as new price information develops."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Support and Resistance in Depth",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Study support and resistance more deeply.",
                "Understand zones, previous highs and lows, and role reversal.",
                "Understand why support and resistance should not be treated as exact guarantees."
            ],
            "explanation": (
                "Support and resistance are areas where price has previously shown "
                "meaningful reactions. Analysts may identify these zones using prior "
                "swing points, consolidation areas and other chart structures. A former "
                "resistance area can sometimes become support after a successful breakout, "
                "but such role reversal is not guaranteed."
            ),
            "example": (
                "A stock repeatedly struggles around ₹1,000 and later closes above "
                "that area with strong market participation. If the stock subsequently "
                "falls back toward ₹1,000 and finds buying interest, the old resistance "
                "may be acting as potential support."
            ),
            "key_terms": [
                "Support Zone",
                "Resistance Zone",
                "Role Reversal",
                "Breakout",
                "Retest"
            ],
            "takeaways": [
                "Support and resistance are better viewed as zones than exact numbers.",
                "Previous market reactions can help identify important areas.",
                "A breakout or retest should be evaluated with broader market context."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Trendlines & Channels",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand trendlines.",
                "Understand price channels.",
                "Learn how trendlines can help organize market structure."
            ],
            "explanation": (
                "Trendlines are lines drawn through relevant swing points to help "
                "visualize the direction of price movement. A channel can be formed "
                "by combining two roughly parallel lines around price action. "
                "Trendlines and channels are analytical tools rather than guaranteed "
                "boundaries."
            ),
            "example": (
                "If several significant lows occur along a rising path, an analyst "
                "may draw an upward trendline through those lows. A roughly parallel "
                "line through relevant highs can form a channel."
            ),
            "key_terms": [
                "Trendline",
                "Channel",
                "Swing Point",
                "Breakout",
                "Slope"
            ],
            "takeaways": [
                "Trendlines help visualize directional movement.",
                "Channels use two approximately parallel boundaries.",
                "A price break through a trendline should be interpreted in context."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Moving Averages",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand moving averages.",
                "Learn why moving averages smooth price data.",
                "Understand common uses of moving averages."
            ],
            "explanation": (
                "A moving average calculates an average of prices over a selected "
                "number of periods and updates as new data arrives. It smooths some "
                "short-term fluctuations and can help analysts study trend direction. "
                "Moving averages are lagging tools because they are calculated from "
                "past data."
            ),
            "example": (
                "A 10-day moving average uses the selected price observations from "
                "the most recent 10 trading days according to the chosen calculation "
                "method. As a new trading day arrives, the oldest observation drops "
                "out and the average is recalculated."
            ),
            "key_terms": [
                "Moving Average",
                "Period",
                "Smoothing",
                "Trend",
                "Lagging Indicator"
            ],
            "takeaways": [
                "Moving averages smooth price data.",
                "The period determines how much historical data is included.",
                "Moving averages respond to past prices and therefore lag price movement."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Simple Moving Average (SMA)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the Simple Moving Average.",
                "Learn the basic SMA calculation.",
                "Understand common uses of SMA."
            ],
            "explanation": (
                "A Simple Moving Average, or SMA, is calculated by adding the selected "
                "price observations and dividing the total by the number of observations. "
                "For example, a 5-period SMA gives equal weight to the five selected periods. "
                "SMA can be used to study trend direction and price relationships."
            ),
            "example": (
                "If five closing prices are ₹100, ₹102, ₹104, ₹106 and ₹108, the "
                "5-period SMA is (100 + 102 + 104 + 106 + 108) ÷ 5 = ₹104."
            ),
            "key_terms": [
                "SMA",
                "Simple Moving Average",
                "Period",
                "Closing Price",
                "Average"
            ],
            "takeaways": [
                "SMA gives equal weight to the observations in its period.",
                "A longer SMA generally changes more slowly than a shorter SMA.",
                "SMA is commonly used as a trend-analysis tool."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Exponential Moving Average (EMA)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the Exponential Moving Average.",
                "Understand how EMA differs from SMA.",
                "Learn why traders may use EMA for more responsive analysis."
            ],
            "explanation": (
                "An Exponential Moving Average, or EMA, gives greater weight to more "
                "recent observations than older observations. Because of this weighting, "
                "an EMA generally reacts more quickly to recent price changes than an "
                "SMA with a comparable period."
            ),
            "example": (
                "If a stock experiences a sudden price movement, a 20-period EMA will "
                "generally respond more quickly to the new price information than a "
                "20-period SMA because recent prices receive greater weight."
            ),
            "key_terms": [
                "EMA",
                "Exponential Moving Average",
                "Weighting",
                "Recent Price",
                "SMA"
            ],
            "takeaways": [
                "EMA gives more weight to recent data.",
                "EMA generally reacts faster than a comparable SMA.",
                "Both EMA and SMA are based on historical price information."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Relative Strength Index (RSI)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand what RSI measures.",
                "Understand the RSI scale.",
                "Understand why RSI should not be treated as a standalone buy or sell signal."
            ],
            "explanation": (
                "The Relative Strength Index, or RSI, is a momentum oscillator that "
                "measures the magnitude of recent gains and losses over a selected "
                "period. RSI is commonly displayed on a scale from 0 to 100. Traditional "
                "technical analysis often discusses levels such as 70 and 30, but "
                "these levels are not automatic signals and should be interpreted "
                "with trend and market context."
            ),
            "example": (
                "If RSI rises above a commonly watched level such as 70, an analyst "
                "may describe the instrument as showing strong recent upward momentum. "
                "This does not necessarily mean that the price must fall immediately."
            ),
            "key_terms": [
                "RSI",
                "Momentum",
                "Oscillator",
                "Relative Strength",
                "Overbought",
                "Oversold"
            ],
            "takeaways": [
                "RSI is a momentum oscillator.",
                "RSI commonly uses a 0–100 scale.",
                "Extreme RSI readings can persist during strong trends."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "MACD",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the MACD indicator.",
                "Understand MACD line, signal line and histogram.",
                "Understand how MACD can be used to study momentum and trend."
            ],
            "explanation": (
                "Moving Average Convergence Divergence, commonly called MACD, is "
                "an indicator based on exponential moving averages. A standard "
                "configuration uses the difference between two EMAs, a signal line "
                "based on that difference, and a histogram showing the relationship "
                "between them. Traders use MACD to study momentum, trend changes and "
                "possible divergences."
            ),
            "example": (
                "If the MACD line moves above the signal line, a trader may study "
                "whether momentum is strengthening. The signal should be considered "
                "alongside price structure and other information."
            ),
            "key_terms": [
                "MACD",
                "Signal Line",
                "Histogram",
                "EMA",
                "Momentum",
                "Divergence"
            ],
            "takeaways": [
                "MACD is based on exponential moving averages.",
                "The histogram helps visualize the relationship between MACD and signal line.",
                "MACD signals should be interpreted in context."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Bollinger Bands",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand Bollinger Bands.",
                "Understand the middle band and volatility bands.",
                "Understand the concept of band expansion and contraction."
            ],
            "explanation": (
                "Bollinger Bands are a volatility-based technical indicator consisting "
                "of a moving average and upper and lower bands positioned using a measure "
                "of price variability, commonly standard deviation. When volatility "
                "changes, the distance between the bands can change. The bands should "
                "not be interpreted as guaranteed support or resistance."
            ),
            "example": (
                "During a period of increasing price variability, the upper and lower "
                "bands may move farther apart. During a quieter period, the bands may "
                "move closer together."
            ),
            "key_terms": [
                "Bollinger Bands",
                "Volatility",
                "Standard Deviation",
                "Middle Band",
                "Band Width"
            ],
            "takeaways": [
                "Bollinger Bands combine a moving average with volatility-based bands.",
                "Band width changes as volatility changes.",
                "Touching a band is not automatically a buy or sell signal."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Stochastic Oscillator",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the Stochastic Oscillator.",
                "Understand how it compares the close with a recent price range.",
                "Understand the limitations of oscillator signals."
            ],
            "explanation": (
                "The Stochastic Oscillator is a momentum indicator that compares "
                "a security's closing price with its recent high-low range. It is "
                "commonly displayed on a 0–100 scale and can include %K and %D lines. "
                "Traditional interpretations often examine high and low zones, but "
                "strong trends can keep an oscillator at extreme levels for extended periods."
            ),
            "example": (
                "If the closing price is consistently near the upper end of its recent "
                "range, the Stochastic reading may move toward the higher end of its "
                "scale, indicating strong recent momentum."
            ),
            "key_terms": [
                "Stochastic",
                "%K",
                "%D",
                "Momentum",
                "Oscillator",
                "Price Range"
            ],
            "takeaways": [
                "Stochastic compares closing price with a recent range.",
                "It is commonly shown on a 0–100 scale.",
                "Oscillator extremes do not guarantee an immediate reversal."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Average True Range (ATR)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand ATR.",
                "Understand what ATR measures.",
                "Understand how ATR can help assess market volatility."
            ],
            "explanation": (
                "Average True Range, or ATR, is a volatility indicator that measures "
                "the average true range of price movement over a selected period. "
                "True range considers the current high-low range and gaps relative "
                "to the previous close. ATR measures volatility rather than predicting "
                "whether price will rise or fall."
            ),
            "example": (
                "If a stock's ATR increases significantly, it indicates that the "
                "stock has recently experienced larger typical price ranges. A higher "
                "ATR does not indicate a bullish or bearish direction by itself."
            ),
            "key_terms": [
                "ATR",
                "True Range",
                "Volatility",
                "Price Range",
                "Gap"
            ],
            "takeaways": [
                "ATR measures price volatility.",
                "ATR does not identify market direction by itself.",
                "Volatility information can help put price movements into context."
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Volume Indicators",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand how volume indicators complement price analysis.",
                "Learn the basic ideas behind OBV and volume-based confirmation.",
                "Understand the limitations of volume indicators."
            ],
            "explanation": (
                "Volume indicators use trading volume to provide additional context "
                "for price movement. On-Balance Volume (OBV), for example, cumulatively "
                "adds or subtracts volume based on whether the closing price is higher "
                "or lower than the previous close. Other tools include volume averages "
                "and volume-based oscillators."
            ),
            "example": (
                "If price is rising while volume also increases, an analyst may study "
                "whether trading participation is supporting the move. This is evidence "
                "to examine, not proof that the trend will continue."
            ),
            "key_terms": [
                "Volume",
                "OBV",
                "On-Balance Volume",
                "Volume Average",
                "Confirmation"
            ],
            "takeaways": [
                "Volume can provide context for price movements.",
                "OBV combines price direction with volume.",
                "Volume-based signals should be evaluated with price structure."
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Momentum",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand momentum in technical analysis.",
                "Understand the difference between price direction and momentum strength.",
                "Learn why momentum can change before a trend changes."
            ],
            "explanation": (
                "Momentum describes the strength or speed of price movement over "
                "a selected period. Momentum indicators attempt to quantify changes "
                "in price movement. Strong momentum can occur during both upward and "
                "downward moves, and weakening momentum does not automatically mean "
                "that the existing trend has reversed."
            ),
            "example": (
                "A stock may continue rising while the size of its daily gains becomes "
                "smaller. The price trend may still be upward even though momentum "
                "appears to be weakening."
            ),
            "key_terms": [
                "Momentum",
                "Rate of Change",
                "Trend",
                "Strength",
                "Acceleration"
            ],
            "takeaways": [
                "Momentum describes the strength or speed of price movement.",
                "Momentum and trend direction are related but not identical.",
                "Weakening momentum can occur before or without a full trend reversal."
            ],
        },
    },
    {
        "lesson_order": 17,
        "title": "Combining Technical Indicators",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand why traders combine technical tools.",
                "Learn how different indicators can serve different purposes.",
                "Avoid using too many indicators without a clear analytical reason."
            ],
            "explanation": (
                "Different technical indicators can provide different types of "
                "information. A moving average can help study trend direction, RSI "
                "can provide momentum information, and volume can provide participation "
                "context. Combining tools can reduce dependence on a single signal, "
                "but using many highly similar indicators can create redundant information."
            ),
            "example": (
                "A learner might first identify the broader trend with a moving average, "
                "then study momentum with RSI and finally examine volume for additional "
                "context. The result should be treated as an analytical framework rather "
                "than a guaranteed prediction."
            ),
            "key_terms": [
                "Indicator",
                "Confirmation",
                "Trend",
                "Momentum",
                "Volume",
                "Confluence"
            ],
            "takeaways": [
                "Different indicators can answer different analytical questions.",
                "A small number of complementary tools can be easier to interpret.",
                "No combination of indicators guarantees a profitable trade."
            ],
        },
    },
    {
        "lesson_order": 18,
        "title": "Building a Technical Analysis Workflow",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Build a structured technical-analysis process.",
                "Learn how to move from broad context to detailed analysis.",
                "Understand the importance of recording observations and reviewing results."
            ],
            "explanation": (
                "A technical-analysis workflow should be systematic rather than "
                "based on random indicator signals. A learner can begin by defining "
                "the timeframe and objective, studying the broader trend and market "
                "structure, identifying important price zones, reviewing volume and "
                "momentum, and then documenting the reasoning. Results can later be "
                "reviewed to understand which assumptions worked or failed."
            ),
            "example": (
                "A learner studying a stock could first inspect the weekly and daily "
                "trend, mark important support and resistance areas, review moving "
                "averages and volume, then record the observations in a journal "
                "without assuming that a particular outcome is guaranteed."
            ),
            "key_terms": [
                "Workflow",
                "Market Structure",
                "Trend",
                "Support",
                "Resistance",
                "Momentum",
                "Trading Journal"
            ],
            "takeaways": [
                "A repeatable workflow makes technical analysis more consistent.",
                "Start with market context before focusing on individual indicators.",
                "Record and review observations to improve analytical discipline."
            ],
        },
    },
]


async def seed_module5():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 5}
        )

        if not module:
            raise RuntimeError(
                "Module 5 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 5,
                **lesson,
            }

            result = await lessons_collection.update_one(
                {
                    "module_id": module_id,
                    "lesson_order": lesson["lesson_order"],
                },
                {
                    "$setOnInsert": document
                },
                upsert=True,
            )

            if result.upserted_id:
                inserted += 1
            else:
                existing += 1

        await db[Collections.MODULES].update_one(
            {"_id": module_id},
            {
                "$set": {
                    "lesson_count": len(LESSONS)
                }
            },
        )

        print(f"Module 5 lessons inserted: {inserted}")
        print(f"Module 5 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module5())