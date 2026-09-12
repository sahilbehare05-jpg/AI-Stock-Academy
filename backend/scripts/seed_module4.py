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
        "title": "What Is a Price Chart?",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what a stock price chart represents.",
                "Understand price and time as the two basic dimensions of a chart.",
                "Learn how charts help organize historical market information.",
            ],
            "explanation": (
                "A price chart is a visual representation of how the price of a "
                "financial instrument has changed over time. The horizontal axis "
                "normally represents time, while the vertical axis represents "
                "price. Charts can help traders study historical behavior, trends, "
                "support and resistance, volatility, and other patterns. A chart "
                "describes past or current market data; it does not guarantee what "
                "will happen next."
            ),
            "example": (
                "If a stock moved from ₹100 to ₹120 over several weeks, a chart can "
                "show the sequence of those price movements and help you observe "
                "whether the stock was generally moving upward, downward, or sideways."
            ),
            "key_terms": [
                "Price Chart",
                "Price",
                "Time Axis",
                "Historical Data",
                "Trend",
            ],
            "takeaways": [
                "A price chart shows price movement over time.",
                "Time is normally shown horizontally and price vertically.",
                "Charts help analyze market behavior but cannot guarantee future prices.",
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Line Charts",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand how a line chart works.",
                "Learn what information a basic line chart displays.",
                "Understand when a line chart can be useful.",
            ],
            "explanation": (
                "A line chart connects selected price points over time with a line. "
                "Many financial line charts use closing prices for each period. "
                "Because they present a simplified view of price movement, line "
                "charts can make broad trends easier to see, although they omit "
                "some information available in candlestick or bar charts."
            ),
            "example": (
                "If the daily closing prices of a stock are ₹100, ₹103, ₹101 and "
                "₹106, a line chart connects these closing-price observations and "
                "makes the overall movement easy to visualize."
            ),
            "key_terms": [
                "Line Chart",
                "Closing Price",
                "Data Point",
                "Trend",
            ],
            "takeaways": [
                "Line charts provide a simple view of price movement.",
                "They often use closing prices.",
                "They show less detail than candlestick or bar charts.",
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Bar Charts",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a financial bar chart.",
                "Learn the four basic price values shown by a bar.",
                "Compare bar charts with line charts.",
            ],
            "explanation": (
                "A financial bar chart can show the open, high, low and close "
                "prices for each period. The vertical bar represents the range "
                "between the high and low, while marks on the bar indicate the "
                "opening and closing prices. This gives more information than a "
                "basic line chart."
            ),
            "example": (
                "Suppose a stock opens at ₹100, reaches ₹108, falls to ₹98 and "
                "closes at ₹105. One bar for that period can represent all four "
                "values: open ₹100, high ₹108, low ₹98 and close ₹105."
            ),
            "key_terms": [
                "Bar Chart",
                "Open",
                "High",
                "Low",
                "Close",
                "OHLC",
            ],
            "takeaways": [
                "Bar charts can display OHLC information.",
                "The high-low range shows the price range of the period.",
                "Bar charts provide more detail than a basic line chart.",
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Candlestick Charts",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand the structure of a candlestick.",
                "Understand what one candle represents.",
                "Learn why candlestick charts are widely used.",
            ],
            "explanation": (
                "A candlestick represents the open, high, low and close prices "
                "for a selected time period. The candle body represents the "
                "relationship between the open and close, while the wicks show "
                "the high and low reached during the period. Candlesticks allow "
                "traders to see price movement in a compact visual format."
            ),
            "example": (
                "If a stock opens at ₹100, reaches ₹110, falls to ₹97 and closes "
                "at ₹106 during one day, the daily candle contains all four values "
                "and shows that the closing price was above the opening price."
            ),
            "key_terms": [
                "Candlestick",
                "Candle Body",
                "Wick",
                "Open",
                "High",
                "Low",
                "Close",
            ],
            "takeaways": [
                "Each candle represents a chosen time period.",
                "A candle contains open, high, low and close information.",
                "Candlesticks provide a compact view of price behavior.",
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Understanding OHLC",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand Open, High, Low and Close.",
                "Learn how OHLC values describe a trading period.",
                "Understand why OHLC data is important for chart analysis.",
            ],
            "explanation": (
                "OHLC stands for Open, High, Low and Close. The open is the price "
                "at which the selected period begins according to the relevant "
                "market data convention. High is the highest traded price during "
                "the period, low is the lowest traded price, and close is the "
                "ending price for that period. OHLC data forms the basis of many "
                "technical charts."
            ),
            "example": (
                "For a daily candle with Open ₹200, High ₹215, Low ₹195 and Close "
                "₹210, the stock traded within a ₹20 range and finished the day "
                "above its opening level."
            ),
            "key_terms": [
                "OHLC",
                "Open",
                "High",
                "Low",
                "Close",
                "Trading Range",
            ],
            "takeaways": [
                "OHLC summarizes four important prices for a period.",
                "High and low show the period's price range.",
                "Open and close help describe the direction of the period.",
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Bullish & Bearish Candles",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand bullish and bearish candles.",
                "Understand the relationship between open and close.",
                "Avoid confusing candle direction with a guaranteed market trend.",
            ],
            "explanation": (
                "A candle is commonly described as bullish when the closing price "
                "is above the opening price, and bearish when the closing price is "
                "below the opening price. Charting platforms often use different "
                "visual conventions to distinguish them. A single bullish or "
                "bearish candle does not by itself prove that a larger trend will "
                "continue."
            ),
            "example": (
                "If a stock opens at ₹500 and closes at ₹515, the candle is "
                "bullish. If it opens at ₹515 and closes at ₹500, the candle is "
                "bearish."
            ),
            "key_terms": [
                "Bullish Candle",
                "Bearish Candle",
                "Open",
                "Close",
                "Body",
            ],
            "takeaways": [
                "Bullish means close is above open.",
                "Bearish means close is below open.",
                "One candle should be interpreted in its broader market context.",
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Candle Body & Wicks",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the candle body.",
                "Understand upper and lower wicks.",
                "Learn what the candle structure can tell us about price movement.",
            ],
            "explanation": (
                "The candle body represents the distance between the open and "
                "close. The upper wick extends from the body toward the high, "
                "while the lower wick extends toward the low. A long wick can "
                "show that price moved away from the open-close area during the "
                "period and then returned closer to the body."
            ),
            "example": (
                "If a stock opens at ₹100, rises to ₹115, falls to ₹98 and closes "
                "at ₹102, the candle has a small body and relatively long wicks, "
                "showing substantial movement away from the opening and closing area."
            ),
            "key_terms": [
                "Candle Body",
                "Upper Wick",
                "Lower Wick",
                "High",
                "Low",
            ],
            "takeaways": [
                "The body shows the open-to-close relationship.",
                "Wicks show movement toward the period's high and low.",
                "Candle structure should be interpreted with surrounding price action.",
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Timeframes",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand chart timeframes.",
                "Learn the difference between intraday and longer-term charts.",
                "Understand why the same stock can look different on different timeframes.",
            ],
            "explanation": (
                "A chart timeframe determines how much time each candle or data "
                "point represents. Common timeframes include one minute, five "
                "minutes, one hour, one day and one week. Shorter timeframes show "
                "more short-term price fluctuations, while longer timeframes can "
                "make broader trends easier to observe."
            ),
            "example": (
                "A one-minute chart can show many candles during a trading session, "
                "while a daily chart uses one candle for each trading day. The same "
                "stock may appear noisy on the one-minute chart but show a clearer "
                "longer-term trend on the daily chart."
            ),
            "key_terms": [
                "Timeframe",
                "Intraday",
                "Daily Chart",
                "Weekly Chart",
                "Candle Period",
            ],
            "takeaways": [
                "Timeframes define the period represented by each candle.",
                "Shorter timeframes show more short-term fluctuations.",
                "Longer timeframes can reveal broader trends.",
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Support & Resistance",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand support and resistance.",
                "Learn why these levels are watched by traders.",
                "Understand that support and resistance are zones rather than guaranteed barriers.",
            ],
            "explanation": (
                "Support is a price area where buying interest has historically "
                "been strong enough to slow or reverse a decline. Resistance is "
                "an area where selling interest has historically slowed or reversed "
                "an advance. These are analytical concepts rather than guaranteed "
                "price barriers, and they can change as market conditions change."
            ),
            "example": (
                "If a stock repeatedly falls toward ₹900 and then recovers, traders "
                "may identify the ₹900 area as potential support. If it repeatedly "
                "struggles near ₹1,000, that area may be viewed as potential resistance."
            ),
            "key_terms": [
                "Support",
                "Resistance",
                "Demand",
                "Supply",
                "Price Zone",
            ],
            "takeaways": [
                "Support is an area where buying interest may appear.",
                "Resistance is an area where selling interest may appear.",
                "Neither support nor resistance guarantees a reversal.",
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Trends & Trendlines",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand upward, downward and sideways trends.",
                "Understand the basic idea of a trendline.",
                "Learn why trend analysis is useful.",
            ],
            "explanation": (
                "A trend describes the general direction of price movement. An "
                "uptrend is commonly associated with a sequence of higher highs "
                "and higher lows, while a downtrend is commonly associated with "
                "lower highs and lower lows. A sideways market has no clear sustained "
                "direction. Trendlines are visual tools used to connect relevant "
                "price points and study the direction of movement."
            ),
            "example": (
                "If a stock forms progressively higher swing lows over time, a "
                "trader may draw a rising trendline beneath those lows to study "
                "the upward structure."
            ),
            "key_terms": [
                "Uptrend",
                "Downtrend",
                "Sideways Trend",
                "Higher High",
                "Higher Low",
                "Trendline",
            ],
            "takeaways": [
                "Trends describe the broad direction of price movement.",
                "Higher highs and higher lows can indicate an uptrend.",
                "Lower highs and lower lows can indicate a downtrend.",
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Gaps",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what a price gap is.",
                "Understand how gaps can appear on charts.",
                "Learn why traders monitor gaps.",
            ],
            "explanation": (
                "A price gap occurs when the opening or subsequent trading price "
                "is separated from the previous period's price range, creating a "
                "visible discontinuity on a chart. Gaps can occur because of news, "
                "earnings, market-wide events, changes in expectations or other "
                "factors. A gap does not automatically predict what price will do next."
            ),
            "example": (
                "If a stock closes at ₹500 and the next session opens at ₹530, "
                "there is a gap between the previous close and the new opening "
                "level, subject to the market's trading structure."
            ),
            "key_terms": [
                "Gap",
                "Gap Up",
                "Gap Down",
                "Opening Price",
                "Price Range",
            ],
            "takeaways": [
                "Gaps represent discontinuities between price areas.",
                "News and market events can contribute to gaps.",
                "A gap alone does not determine future price direction.",
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Volume on Charts",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand trading volume.",
                "Learn how volume is displayed with price charts.",
                "Understand how volume can provide context for price movement.",
            ],
            "explanation": (
                "Trading volume measures the quantity of shares or other units "
                "traded during a period. Volume is often displayed as vertical "
                "bars below a price chart. Traders may compare volume with price "
                "movement to assess market activity, although volume alone does "
                "not establish whether a trade or investment will be successful."
            ),
            "example": (
                "If a stock normally trades 2 lakh shares per day but suddenly "
                "trades 8 lakh shares while making a significant price move, the "
                "increase in volume indicates unusually high trading activity."
            ),
            "key_terms": [
                "Volume",
                "Trading Activity",
                "Volume Bar",
                "Price Movement",
                "Liquidity",
            ],
            "takeaways": [
                "Volume measures trading activity.",
                "Volume is commonly displayed below the price chart.",
                "Price and volume can be studied together for additional context.",
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Multiple Timeframe Analysis",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand multiple timeframe analysis.",
                "Learn why traders compare different chart timeframes.",
                "Understand the importance of keeping timeframes consistent with the trading objective.",
            ],
            "explanation": (
                "Multiple timeframe analysis means examining the same asset using "
                "more than one timeframe. A longer timeframe can provide broader "
                "context, while a shorter timeframe can show more detailed price "
                "movement. Comparing timeframes can help organize market information, "
                "but conflicting signals are possible."
            ),
            "example": (
                "A trader might study a weekly chart to understand the broad trend, "
                "a daily chart to study the intermediate structure, and a shorter "
                "chart to examine a specific trading setup."
            ),
            "key_terms": [
                "Multiple Timeframe Analysis",
                "Higher Timeframe",
                "Lower Timeframe",
                "Market Context",
            ],
            "takeaways": [
                "Different timeframes provide different perspectives.",
                "Higher timeframes can provide broader context.",
                "The chosen timeframes should match the trading objective.",
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Reading a Complete Stock Chart",
        "level": "Beginner",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Combine the main chart-reading concepts.",
                "Read OHLC, candles, trend, support, resistance and volume together.",
                "Develop a structured process for observing a stock chart.",
            ],
            "explanation": (
                "Reading a complete stock chart means examining several pieces of "
                "information together rather than relying on a single candle or "
                "indicator. A structured approach can begin with the timeframe, "
                "overall trend, important support and resistance zones, recent "
                "candlestick behavior, volume and notable gaps. The goal at this "
                "stage is to describe what the chart shows rather than make a "
                "guaranteed prediction."
            ),
            "example": (
                "Suppose a daily chart shows a generally rising trend, repeated "
                "reactions near a support zone, increased volume during a recent "
                "price move and a nearby resistance area. A learner can record "
                "these observations and then study what happens next instead of "
                "assuming the next move is certain."
            ),
            "key_terms": [
                "Chart Analysis",
                "Trend",
                "Support",
                "Resistance",
                "Candlestick",
                "Volume",
                "Timeframe",
            ],
            "takeaways": [
                "Read the chart systematically rather than focusing on one signal.",
                "Combine price, timeframe, volume and market structure.",
                "Chart analysis describes probabilities and observations, not certainties.",
            ],
        },
    },
]


async def seed_module4():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 4}
        )

        if not module:
            raise RuntimeError(
                "Module 4 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 4,
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

        print(f"Module 4 lessons inserted: {inserted}")
        print(f"Module 4 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module4())