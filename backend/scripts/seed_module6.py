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
        "title": "Advanced Market Structure",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand advanced market structure.",
                "Identify structural highs and lows.",
                "Understand how a change in structure can provide analytical context.",
            ],
            "explanation": (
                "Advanced market structure focuses on the sequence and importance "
                "of swing highs, swing lows, higher highs, higher lows, lower highs "
                "and lower lows. Analysts use these relationships to describe whether "
                "price is maintaining an upward, downward or ranging structure. A "
                "change in the sequence can indicate that the existing structure "
                "may be weakening or changing."
            ),
            "example": (
                "Suppose a stock forms higher highs and higher lows for several "
                "weeks. If it later fails to form a new higher high and then breaks "
                "below an important previous swing low, the analyst may study this "
                "as a possible change in market structure."
            ),
            "key_terms": [
                "Market Structure",
                "Swing High",
                "Swing Low",
                "Higher High",
                "Higher Low",
                "Lower High",
                "Lower Low",
            ],
            "takeaways": [
                "Market structure is based on meaningful relationships between highs and lows.",
                "A structural change can provide useful analytical information.",
                "Structure should be evaluated across an appropriate timeframe.",
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Swing Highs & Swing Lows",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand swing highs and swing lows.",
                "Learn how swing points help identify market structure.",
                "Understand why the importance of a swing depends on timeframe and context.",
            ],
            "explanation": (
                "A swing high is a local price peak relative to nearby price action, "
                "while a swing low is a local price trough. Traders use these points "
                "to study trends, support and resistance, and market structure. Not "
                "every small fluctuation is equally important; the significance of "
                "a swing depends on the timeframe and surrounding price action."
            ),
            "example": (
                "If a stock rises from ₹500 to ₹550, declines to ₹525, and then "
                "rises again, ₹550 may be treated as a swing high and ₹525 as a "
                "swing low within that section of the chart."
            ),
            "key_terms": [
                "Swing High",
                "Swing Low",
                "Local High",
                "Local Low",
                "Market Structure",
            ],
            "takeaways": [
                "Swing points help describe price structure.",
                "Important swings are usually identified in relation to surrounding price action.",
                "The timeframe affects which swings are considered significant.",
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Breakouts & Breakdowns",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand breakouts and breakdowns.",
                "Learn how traders identify price moving beyond important levels.",
                "Understand why false breakouts can occur.",
            ],
            "explanation": (
                "A breakout occurs when price moves above an important resistance "
                "area or established range boundary. A breakdown occurs when price "
                "moves below an important support area or range boundary. Traders "
                "often examine volume, closing prices and subsequent price behavior "
                "to assess whether the move is meaningful. A breakout or breakdown "
                "can fail and return inside the previous range."
            ),
            "example": (
                "If a stock has repeatedly struggled near ₹1,000 and later moves "
                "above that level, traders may describe the move as a potential "
                "breakout. If price quickly falls back below ₹1,000, it may be "
                "studied as a failed breakout."
            ),
            "key_terms": [
                "Breakout",
                "Breakdown",
                "Resistance",
                "Support",
                "Range",
                "False Breakout",
            ],
            "takeaways": [
                "Breakouts move above important price areas.",
                "Breakdowns move below important price areas.",
                "A move beyond a level does not guarantee continuation.",
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Retests & Failed Breakouts",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the concept of a retest.",
                "Understand failed breakouts.",
                "Learn how price behavior after a breakout can provide additional context.",
            ],
            "explanation": (
                "A retest occurs when price returns toward a previously broken "
                "support or resistance area after a breakout or breakdown. Analysts "
                "may study whether the old level holds or fails. A failed breakout "
                "occurs when price moves beyond a level but later returns through "
                "that level. These concepts are useful for studying market behavior "
                "but do not guarantee a particular future movement."
            ),
            "example": (
                "A stock breaks above ₹1,000 and later falls back toward ₹1,000. "
                "If price stabilizes around that area and moves higher again, the "
                "event may be described as a potential retest."
            ),
            "key_terms": [
                "Retest",
                "Breakout",
                "Failed Breakout",
                "Support",
                "Resistance",
            ],
            "takeaways": [
                "Retests examine price behavior after a level is broken.",
                "A broken resistance area can sometimes act as support.",
                "Failed breakouts can return price into the previous range.",
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Candlestick Reversal Patterns",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the idea of candlestick reversal patterns.",
                "Learn common examples such as engulfing patterns and hammer-type structures.",
                "Understand why context matters when interpreting candlesticks.",
            ],
            "explanation": (
                "Candlestick reversal patterns are formations that traders may use "
                "to study a possible change in short-term price behavior. Examples "
                "include bullish or bearish engulfing patterns, hammer-type candles "
                "and shooting-star-type candles. These formations are not guaranteed "
                "reversal signals and are generally more meaningful when considered "
                "with trend, support or resistance, volume and other context."
            ),
            "example": (
                "A hammer-type candle appearing near a well-observed support area "
                "after a decline may attract attention because the candle shows "
                "rejection of lower prices. The analyst should still examine what "
                "happens afterward rather than assuming an immediate reversal."
            ),
            "key_terms": [
                "Reversal Pattern",
                "Engulfing",
                "Hammer",
                "Shooting Star",
                "Rejection",
            ],
            "takeaways": [
                "Candlestick patterns describe price behavior during selected periods.",
                "Context is important when interpreting reversal formations.",
                "No single candlestick pattern guarantees a reversal.",
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Continuation Patterns",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand continuation patterns.",
                "Learn why consolidations can appear within trends.",
                "Understand that a continuation pattern can also fail.",
            ],
            "explanation": (
                "Continuation patterns are chart structures that traders commonly "
                "interpret as periods of consolidation within an existing trend. "
                "Examples include flags, pennants and some triangle formations. "
                "The pattern represents a potential continuation scenario rather "
                "than a guaranteed outcome."
            ),
            "example": (
                "A stock makes a strong upward move and then trades in a narrow "
                "consolidation for several sessions. If the consolidation resembles "
                "a flag and price later moves upward, analysts may describe the "
                "structure as a potential continuation pattern."
            ),
            "key_terms": [
                "Continuation Pattern",
                "Consolidation",
                "Flag",
                "Pennant",
                "Triangle",
            ],
            "takeaways": [
                "Continuation patterns often develop during consolidation.",
                "Flags and pennants are common examples.",
                "A pattern can fail and should not be treated as certainty.",
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Double Top & Double Bottom",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand double-top and double-bottom formations.",
                "Understand the role of the neckline.",
                "Learn why confirmation matters.",
            ],
            "explanation": (
                "A double top is a chart formation in which price creates two "
                "significant peaks around a similar area with a decline between them. "
                "A double bottom has two significant troughs around a similar area "
                "with a recovery between them. Traders often watch the intermediate "
                "support or resistance level, sometimes called the neckline, for "
                "confirmation of a potential pattern."
            ),
            "example": (
                "A stock rises toward ₹1,000, declines to ₹900, rises again near "
                "₹1,000 and then falls below ₹900. Analysts may study this sequence "
                "as a potential double-top structure."
            ),
            "key_terms": [
                "Double Top",
                "Double Bottom",
                "Neckline",
                "Peak",
                "Trough",
            ],
            "takeaways": [
                "Double tops contain two important peaks.",
                "Double bottoms contain two important troughs.",
                "Confirmation levels can help distinguish a pattern from ordinary price movement.",
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Head & Shoulders",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the head-and-shoulders pattern.",
                "Understand the neckline.",
                "Learn about the inverse head-and-shoulders structure.",
            ],
            "explanation": (
                "The head-and-shoulders pattern is a chart formation consisting "
                "of a left shoulder, a higher central peak called the head, and "
                "a right shoulder. A neckline connects important troughs between "
                "these peaks. The inverse head-and-shoulders pattern is the opposite "
                "structure and consists of three troughs, with the middle trough "
                "being the deepest."
            ),
            "example": (
                "A stock forms a peak, pulls back, creates a higher peak, pulls "
                "back again, and then creates another peak near the first one. "
                "If the overall structure resembles three peaks with a higher "
                "middle peak, analysts may study it as a potential head-and-shoulders pattern."
            ),
            "key_terms": [
                "Head and Shoulders",
                "Inverse Head and Shoulders",
                "Shoulder",
                "Head",
                "Neckline",
            ],
            "takeaways": [
                "The head-and-shoulders structure has three major peaks.",
                "The middle peak is higher than the surrounding shoulders.",
                "Pattern interpretation depends on structure and confirmation.",
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Triangles",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand triangle chart patterns.",
                "Learn the basic idea of ascending, descending and symmetrical triangles.",
                "Understand how converging price ranges represent consolidation.",
            ],
            "explanation": (
                "Triangle patterns form when price moves within converging trendlines "
                "or boundaries. Ascending triangles commonly have a relatively flat "
                "upper boundary and rising lows. Descending triangles commonly have "
                "a relatively flat lower boundary and declining highs. Symmetrical "
                "triangles have converging rising and falling boundaries. The eventual "
                "direction of a breakout is not guaranteed."
            ),
            "example": (
                "If a stock repeatedly reaches approximately ₹500 while its lows "
                "rise from ₹450 to ₹470 and then ₹485, the narrowing structure may "
                "be studied as a potential ascending triangle."
            ),
            "key_terms": [
                "Triangle",
                "Ascending Triangle",
                "Descending Triangle",
                "Symmetrical Triangle",
                "Consolidation",
            ],
            "takeaways": [
                "Triangles represent periods of narrowing price movement.",
                "Different triangle types have different boundary structures.",
                "Breakout direction must be observed rather than assumed.",
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Flags & Pennants",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand flags and pennants.",
                "Identify the difference between their basic structures.",
                "Understand their relationship with strong prior price moves.",
            ],
            "explanation": (
                "Flags and pennants are short-term consolidation structures that "
                "often appear after a strong price movement. A flag usually resembles "
                "a small channel that slopes against the preceding move, while a "
                "pennant is a small converging structure. Traders may study these "
                "formations as potential continuation setups."
            ),
            "example": (
                "After a strong upward price movement, a stock may trade within a "
                "small downward-sloping channel for several sessions. This can be "
                "studied as a potential bullish flag if the broader structure supports it."
            ),
            "key_terms": [
                "Flag",
                "Pennant",
                "Consolidation",
                "Pole",
                "Continuation",
            ],
            "takeaways": [
                "Flags and pennants usually follow a notable price movement.",
                "They represent short-term consolidation.",
                "A continuation outcome is possible but not guaranteed.",
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Wedges",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand rising and falling wedge structures.",
                "Understand converging trendlines.",
                "Learn why wedges can have different interpretations depending on context.",
            ],
            "explanation": (
                "A wedge is a converging price structure formed by two trendlines "
                "that move toward each other. Rising and falling wedges are commonly "
                "studied as possible reversal or continuation formations depending "
                "on the context in which they occur. The eventual breakout direction "
                "must be confirmed by actual price behavior."
            ),
            "example": (
                "If both highs and lows are rising but the range between them becomes "
                "narrower, the structure may resemble a rising wedge. Analysts then "
                "watch the eventual price movement rather than assuming a particular outcome."
            ),
            "key_terms": [
                "Wedge",
                "Rising Wedge",
                "Falling Wedge",
                "Convergence",
                "Breakout",
            ],
            "takeaways": [
                "Wedges are formed by converging price boundaries.",
                "Context affects how a wedge is interpreted.",
                "The breakout direction should be observed and confirmed.",
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Fibonacci Retracement",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand Fibonacci retracement.",
                "Learn how retracement levels are calculated from a price move.",
                "Understand that Fibonacci levels are analytical reference points, not guaranteed reversal levels.",
            ],
            "explanation": (
                "Fibonacci retracement is a technical-analysis tool used to identify "
                "potential areas where a price correction may pause relative to a "
                "previous move. Commonly watched levels include approximately 23.6%, "
                "38.2%, 50%, 61.8% and 78.6%. These levels are reference zones and "
                "should be combined with price structure and other evidence."
            ),
            "example": (
                "Suppose a stock rises from ₹100 to ₹200. A 50% retracement would "
                "place a reference level around ₹150. This does not mean the stock "
                "must reverse at ₹150."
            ),
            "key_terms": [
                "Fibonacci Retracement",
                "Retracement",
                "38.2%",
                "50%",
                "61.8%",
            ],
            "takeaways": [
                "Fibonacci retracement measures possible correction areas.",
                "Several percentage levels are commonly observed.",
                "Fibonacci levels are reference points, not guaranteed support or resistance.",
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Fibonacci Extensions",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand Fibonacci extensions.",
                "Understand how extensions differ from retracements.",
                "Learn how extensions can be used to study potential price objectives.",
            ],
            "explanation": (
                "Fibonacci extensions project price levels beyond the original "
                "price movement. Analysts may use extension ratios to identify "
                "potential areas of interest after a breakout or continuation move. "
                "Like retracement levels, extensions are analytical reference points "
                "and do not guarantee that price will reach or reverse at those levels."
            ),
            "example": (
                "If a stock moves from ₹100 to ₹150 and then retraces toward ₹130, "
                "an analyst can use the earlier move and retracement to calculate "
                "possible extension levels above ₹150."
            ),
            "key_terms": [
                "Fibonacci Extension",
                "Price Projection",
                "Extension Level",
                "Retracement",
                "Target Zone",
            ],
            "takeaways": [
                "Extensions project potential areas beyond a prior price move.",
                "They differ from retracement levels, which study corrections within a move.",
                "Extensions should be treated as analytical reference levels.",
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Divergence",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand divergence between price and an indicator.",
                "Learn bullish and bearish divergence concepts.",
                "Understand why divergence is a warning or observation rather than a guaranteed reversal.",
            ],
            "explanation": (
                "Divergence occurs when price movement and an indicator such as RSI "
                "or MACD do not move in the same way. Bullish divergence is commonly "
                "described when price makes a lower low while the indicator makes a "
                "higher low. Bearish divergence can occur when price makes a higher "
                "high while the indicator makes a lower high. Divergence can persist "
                "and should be interpreted with broader market structure."
            ),
            "example": (
                "If a stock falls from ₹500 to ₹450 and later makes a new low near "
                "₹440, while RSI forms a higher low instead of a lower one, analysts "
                "may describe the situation as potential bullish divergence."
            ),
            "key_terms": [
                "Divergence",
                "Bullish Divergence",
                "Bearish Divergence",
                "RSI",
                "MACD",
            ],
            "takeaways": [
                "Divergence compares price behavior with an indicator.",
                "It can provide a warning that momentum may be changing.",
                "Divergence alone does not guarantee a price reversal.",
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Multi-Indicator Confirmation",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand confluence between technical tools.",
                "Learn how trend, momentum and volume can be analyzed together.",
                "Avoid treating multiple indicators as independent guarantees."
            ],
            "explanation": (
                "Multi-indicator confirmation means examining several complementary "
                "pieces of technical evidence before forming an analytical view. "
                "For example, market structure can describe trend, a moving average "
                "can provide trend context, RSI or MACD can describe momentum, and "
                "volume can provide participation information. Indicators that use "
                "similar underlying data may provide overlapping rather than independent evidence."
            ),
            "example": (
                "A stock may be above a rising moving average, form higher highs "
                "and higher lows, show supportive volume and maintain positive momentum. "
                "These observations together can provide stronger analytical context "
                "than relying on one indicator alone, while still not guaranteeing an outcome."
            ),
            "key_terms": [
                "Confluence",
                "Confirmation",
                "Market Structure",
                "Momentum",
                "Volume",
                "Indicator",
            ],
            "takeaways": [
                "Confluence combines different types of market information.",
                "Complementary tools can provide broader context.",
                "More indicators do not automatically mean better analysis.",
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Complete Advanced Chart Analysis",
        "level": "Intermediate",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine advanced chart-analysis concepts into one process.",
                "Learn how to move from market structure to confirmation.",
                "Develop a disciplined chart-review framework."
            ],
            "explanation": (
                "Advanced chart analysis combines market structure, support and "
                "resistance, chart patterns, candlestick behavior, Fibonacci tools, "
                "momentum, volume and multiple timeframes. A structured process "
                "should begin with broad context, identify important price areas, "
                "study current structure and patterns, examine supporting evidence, "
                "and record alternative scenarios. The objective is to understand "
                "probabilities and manage uncertainty rather than predict the market with certainty."
            ),
            "example": (
                "A learner can start with a weekly chart to understand the broader "
                "trend, use a daily chart to mark important support and resistance, "
                "study a possible chart pattern, examine volume and momentum, and "
                "then record what would confirm or invalidate the observation."
            ),
            "key_terms": [
                "Advanced Chart Analysis",
                "Market Structure",
                "Chart Pattern",
                "Fibonacci",
                "Divergence",
                "Confluence",
                "Scenario",
            ],
            "takeaways": [
                "Advanced analysis combines multiple forms of market information.",
                "Higher-timeframe context can help organize lower-timeframe observations.",
                "A good analysis includes both a primary view and conditions that could invalidate it.",
            ],
        },
    },
]


async def seed_module6():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 6}
        )

        if not module:
            raise RuntimeError(
                "Module 6 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 6,
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

        print(f"Module 6 lessons inserted: {inserted}")
        print(f"Module 6 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module6())