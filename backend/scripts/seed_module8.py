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
        "title": "What Is a Trading Strategy?",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand what a trading strategy is.",
                "Learn why rules and consistency matter.",
                "Understand the difference between a strategy and a prediction."
            ],
            "explanation": (
                "A trading strategy is a defined framework for making decisions "
                "about when to consider entering, managing and exiting a market "
                "position. A strategy normally includes conditions, timeframe, "
                "risk controls and evaluation rules. A strategy does not guarantee "
                "profit because market conditions can change and outcomes are uncertain."
            ),
            "example": (
                "A learner may create a paper-trading strategy that studies a "
                "trend, waits for a predefined setup, records the entry conditions, "
                "defines an invalidation point and documents the result. The goal "
                "is to test the rules consistently rather than make random decisions."
            ),
            "key_terms": [
                "Trading Strategy",
                "Rules",
                "Setup",
                "Entry",
                "Exit",
                "Risk Control"
            ],
            "takeaways": [
                "A strategy is a repeatable decision framework.",
                "Clear rules make a strategy easier to test.",
                "A strategy cannot guarantee a profitable outcome."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Strategy vs Trading Setup",
        "level": "Intermediate",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand the difference between a strategy and a setup.",
                "Learn how a setup fits inside a broader strategy.",
                "Understand why precise conditions are useful."
            ],
            "explanation": (
                "A trading strategy is the complete framework used to make and "
                "evaluate decisions, while a setup is a particular market condition "
                "that may meet part of the strategy's requirements. A strategy can "
                "contain several possible setups. Separating the two helps traders "
                "avoid treating every interesting chart pattern as a complete strategy."
            ),
            "example": (
                "A strategy may focus on trend-following. One setup within that "
                "strategy could be a pullback toward a moving average followed by "
                "evidence that the existing trend is continuing."
            ),
            "key_terms": [
                "Strategy",
                "Setup",
                "Entry Condition",
                "Confirmation",
                "Rule"
            ],
            "takeaways": [
                "A setup is a specific market situation.",
                "A strategy contains the complete decision framework.",
                "Not every setup should automatically become a trade."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Trend-Following Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand trend-following.",
                "Learn how traders identify persistent price direction.",
                "Understand why trend-following can struggle in sideways markets."
            ],
            "explanation": (
                "Trend-following strategies attempt to participate in established "
                "price trends rather than predict exact turning points. Traders may "
                "use market structure, moving averages, breakouts or other tools to "
                "identify trends. Trend-following can generate repeated false signals "
                "when prices move sideways without a sustained direction."
            ),
            "example": (
                "A paper-trading system may classify a market as trending upward "
                "when price remains above a rising moving average and the chart "
                "continues to form higher highs and higher lows."
            ),
            "key_terms": [
                "Trend Following",
                "Uptrend",
                "Downtrend",
                "Moving Average",
                "Market Structure"
            ],
            "takeaways": [
                "Trend-following attempts to participate in sustained movements.",
                "Trend tools can lag the actual price movement.",
                "Sideways markets can produce repeated false signals."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Breakout Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand breakout-based strategies.",
                "Learn how consolidation areas can form breakout levels.",
                "Understand false breakouts."
            ],
            "explanation": (
                "A breakout strategy studies situations where price moves beyond "
                "an important resistance level, range boundary or other defined "
                "price area. Traders may use additional conditions such as volume, "
                "closing price or a retest to reduce ambiguity. A breakout can fail "
                "and return inside the previous range."
            ),
            "example": (
                "A stock trades between ₹900 and ₹1,000 for several weeks. A "
                "paper-trading strategy may define a breakout condition when price "
                "closes above ₹1,000 and then evaluate how the position behaves."
            ),
            "key_terms": [
                "Breakout",
                "Range",
                "Resistance",
                "False Breakout",
                "Retest"
            ],
            "takeaways": [
                "Breakout strategies focus on movement beyond defined levels.",
                "Additional confirmation can provide more context.",
                "Breakouts can fail."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Pullback Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand pullbacks within trends.",
                "Learn how support areas can be used in pullback analysis.",
                "Understand the difference between a pullback and a reversal."
            ],
            "explanation": (
                "A pullback is a temporary movement against the prevailing trend. "
                "A pullback strategy attempts to identify situations where price "
                "may resume the previous trend after a correction. Traders may study "
                "support, resistance, trendlines, moving averages and price action. "
                "A pullback can instead develop into a full trend reversal."
            ),
            "example": (
                "In an upward trend, price may decline from ₹500 to ₹470 before "
                "stabilizing near a previously observed support area. A learner "
                "can study whether the original trend resumes or the structure changes."
            ),
            "key_terms": [
                "Pullback",
                "Correction",
                "Trend",
                "Support",
                "Reversal"
            ],
            "takeaways": [
                "Pullbacks are movements against an existing trend.",
                "A pullback does not guarantee trend continuation.",
                "Market structure helps distinguish corrections from possible reversals."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Support & Resistance Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand strategies built around support and resistance.",
                "Learn how price reactions can be studied.",
                "Understand why levels should be treated as zones."
            ],
            "explanation": (
                "Support and resistance strategies examine how price behaves around "
                "important historical areas. A learner may study reactions, breakouts, "
                "retests and failures around those zones. Because markets are dynamic, "
                "support and resistance should generally be treated as areas rather "
                "than perfectly precise lines."
            ),
            "example": (
                "If a stock repeatedly reacts around ₹800, a learner can mark the "
                "area and record how price behaves each time it approaches that zone "
                "instead of assuming it must reverse."
            ),
            "key_terms": [
                "Support",
                "Resistance",
                "Zone",
                "Retest",
                "Rejection"
            ],
            "takeaways": [
                "Support and resistance can organize chart analysis.",
                "Price reactions near a level provide information for study.",
                "No level guarantees a reversal."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Moving Average Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand strategies using moving averages.",
                "Learn how moving averages can define trend conditions.",
                "Understand moving-average crossover concepts."
            ],
            "explanation": (
                "Moving-average strategies use smoothed price data to study trend "
                "direction or changes in momentum. One approach compares price with "
                "a moving average, while another studies the relationship between "
                "two moving averages. Because moving averages use historical data, "
                "their signals can occur after a market move has already started."
            ),
            "example": (
                "A paper strategy may compare a shorter moving average with a longer "
                "one and record what happened historically after one crossed the other."
            ),
            "key_terms": [
                "Moving Average",
                "SMA",
                "EMA",
                "Crossover",
                "Trend"
            ],
            "takeaways": [
                "Moving averages can help define trend conditions.",
                "Crossovers are historical signals rather than guarantees.",
                "Different periods produce different levels of responsiveness."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Momentum Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand momentum-based strategies.",
                "Learn how momentum indicators can be used.",
                "Understand why strong momentum can persist or reverse."
            ],
            "explanation": (
                "Momentum strategies attempt to identify assets or periods where "
                "price movement has notable strength. Tools such as RSI, MACD, rate "
                "of change and price acceleration can provide momentum information. "
                "Strong momentum does not guarantee continuation, and an asset can "
                "remain at an extreme indicator level during a strong trend."
            ),
            "example": (
                "A learner may create a paper-trading experiment that records "
                "instances where momentum rises above a chosen threshold and then "
                "measures what happened afterward."
            ),
            "key_terms": [
                "Momentum",
                "RSI",
                "MACD",
                "Rate of Change",
                "Acceleration"
            ],
            "takeaways": [
                "Momentum strategies focus on strength of price movement.",
                "Momentum indicators can provide useful context.",
                "Strong momentum does not guarantee future continuation."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Mean Reversion",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the concept of mean reversion.",
                "Learn how deviations from a reference value can be studied.",
                "Understand why mean reversion assumptions can fail."
            ],
            "explanation": (
                "Mean reversion strategies assume that under certain conditions "
                "a price or related measurement may move back toward a historical "
                "average or reference level. Tools such as moving averages, Bollinger "
                "Bands and statistical measures can be used to study deviations. "
                "Mean reversion is not guaranteed because markets can remain away "
                "from historical averages for long periods."
            ),
            "example": (
                "A stock may move significantly above its recent average. A learner "
                "can study historical examples to determine whether and how often "
                "the price later moved closer to the average."
            ),
            "key_terms": [
                "Mean Reversion",
                "Average",
                "Deviation",
                "Bollinger Bands",
                "Range"
            ],
            "takeaways": [
                "Mean reversion studies movement toward a reference value.",
                "Historical averages are not guaranteed future targets.",
                "Strong trends can remain away from an average for extended periods."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Range Trading",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand range-bound markets.",
                "Learn how support and resistance define a range.",
                "Understand why range strategies can fail when a breakout occurs."
            ],
            "explanation": (
                "Range trading focuses on markets where price repeatedly moves "
                "between identifiable support and resistance areas without a clear "
                "sustained trend. Traders may study reactions near the boundaries "
                "and monitor for a breakout. A range strategy becomes less suitable "
                "if price establishes a strong directional trend."
            ),
            "example": (
                "If a stock repeatedly trades between ₹400 and ₹450, a learner can "
                "study how frequently price reacts near those areas and what happens "
                "when the range eventually breaks."
            ),
            "key_terms": [
                "Range",
                "Support",
                "Resistance",
                "Consolidation",
                "Breakout"
            ],
            "takeaways": [
                "Range trading studies repeated movement between boundaries.",
                "Support and resistance are central to range analysis.",
                "A strong breakout can invalidate the range assumption."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Swing Trading Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand swing-trading strategy design.",
                "Learn how trend, pullbacks and chart structure can be combined.",
                "Understand overnight and weekend risk."
            ],
            "explanation": (
                "Swing-trading strategies generally attempt to capture price moves "
                "lasting several days or weeks. A strategy can combine trend direction, "
                "support and resistance, chart patterns, momentum and defined risk "
                "conditions. Positions held beyond a trading session remain exposed "
                "to news and price changes while the market is closed."
            ),
            "example": (
                "A learner can use historical data to study a hypothetical strategy "
                "that identifies an established trend, waits for a pullback and then "
                "records the outcome over a predefined holding period."
            ),
            "key_terms": [
                "Swing Trading",
                "Pullback",
                "Trend",
                "Holding Period",
                "Overnight Risk"
            ],
            "takeaways": [
                "Swing strategies target moves over days or weeks.",
                "Multiple technical concepts can be combined.",
                "Holding positions overnight introduces additional uncertainty."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Intraday Strategy Concepts",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the structure of an intraday strategy.",
                "Learn about session context and short-term market behavior.",
                "Understand the importance of simulation and risk controls."
            ],
            "explanation": (
                "Intraday strategy concepts focus on market behavior within a "
                "trading session. A strategy may define a timeframe, market condition, "
                "entry criteria, exit criteria and risk limits. Short-term markets "
                "can be highly variable, so learners should test ideas with historical "
                "data or paper trading before drawing conclusions."
            ),
            "example": (
                "A learner can simulate a strategy using historical intraday data, "
                "recording each hypothetical entry and exit according to fixed rules "
                "and then calculating the overall results."
            ),
            "key_terms": [
                "Intraday",
                "Trading Session",
                "Entry",
                "Exit",
                "Simulation"
            ],
            "takeaways": [
                "Intraday strategies operate within a trading session.",
                "Rules should be defined before evaluating results.",
                "Simulation can help learners study behavior without using real money."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Volume-Based Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand how volume can be incorporated into a strategy.",
                "Learn the idea of volume confirmation.",
                "Understand why high volume alone is not a directional signal."
            ],
            "explanation": (
                "Volume-based strategies use trading activity as part of their "
                "decision framework. A learner may compare current volume with an "
                "average or examine volume during breakouts and trend movements. "
                "High volume indicates increased activity, but it does not by itself "
                "determine whether prices will rise or fall."
            ),
            "example": (
                "A paper strategy may record breakouts that occur with volume above "
                "a selected average and compare their historical outcomes with "
                "breakouts that occur on lower volume."
            ),
            "key_terms": [
                "Volume",
                "Volume Average",
                "Confirmation",
                "Breakout",
                "Participation"
            ],
            "takeaways": [
                "Volume can add context to price movements.",
                "Volume confirmation can be tested objectively.",
                "High volume does not automatically mean bullish or bearish."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Multi-Timeframe Strategies",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand multi-timeframe strategy design.",
                "Learn how higher and lower timeframes can serve different purposes.",
                "Understand the risk of conflicting timeframe signals."
            ],
            "explanation": (
                "Multi-timeframe strategies examine an asset on multiple chart "
                "timeframes. A higher timeframe may define the broader market context, "
                "while a lower timeframe can provide more detailed information. "
                "The rules should clearly specify how conflicting signals are handled."
            ),
            "example": (
                "A simulated strategy might use a weekly chart to classify the "
                "broader trend and a daily chart to identify a potential setup."
            ),
            "key_terms": [
                "Multi-Timeframe",
                "Higher Timeframe",
                "Lower Timeframe",
                "Market Context",
                "Confirmation"
            ],
            "takeaways": [
                "Different timeframes provide different perspectives.",
                "Higher timeframes can provide broader context.",
                "Strategy rules should specify how different timeframe signals interact."
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Strategy Backtesting Basics",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand backtesting.",
                "Learn the basic components of a historical test.",
                "Understand why realistic assumptions matter."
            ],
            "explanation": (
                "Backtesting applies a defined strategy to historical market data "
                "to study how it would have behaved under specified assumptions. "
                "A useful backtest defines entry and exit rules, position assumptions, "
                "data periods, transaction costs where relevant and evaluation metrics. "
                "Historical performance does not guarantee future results."
            ),
            "example": (
                "A learner can test a moving-average strategy on several years of "
                "historical data and record every hypothetical signal instead of "
                "selecting only the successful examples."
            ),
            "key_terms": [
                "Backtesting",
                "Historical Data",
                "Transaction Cost",
                "Simulation",
                "Strategy Rule"
            ],
            "takeaways": [
                "Backtesting studies a strategy using historical data.",
                "Rules must be defined consistently before evaluating results.",
                "Past simulated performance does not guarantee future performance."
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Win Rate, Risk-Reward & Expectancy",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand win rate.",
                "Understand risk-reward ratio.",
                "Understand expectancy as a strategy-evaluation concept."
            ],
            "explanation": (
                "Win rate is the percentage of evaluated trades or outcomes that "
                "are profitable under the defined rules. Risk-reward compares the "
                "amount potentially risked with the amount targeted or gained in "
                "a trade. Expectancy combines the probabilities and average gains "
                "and losses to estimate the average outcome per trade under a "
                "specified model. These metrics must be calculated from consistent data."
            ),
            "example": (
                "Suppose a simulated strategy wins 40% of the time, with average "
                "winning outcome of 2 units and average losing outcome of 1 unit. "
                "Its simplified expectancy is (0.40 × 2) − (0.60 × 1) = 0.20 units "
                "per trade before considering other costs or assumptions."
            ),
            "key_terms": [
                "Win Rate",
                "Risk-Reward Ratio",
                "Expectancy",
                "Average Gain",
                "Average Loss"
            ],
            "takeaways": [
                "A high win rate alone does not make a strategy successful.",
                "Risk-reward and average outcomes matter.",
                "Expectancy combines outcome probabilities and payoff sizes."
            ],
        },
    },
    {
        "lesson_order": 17,
        "title": "Avoiding Overfitting",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand overfitting in strategy development.",
                "Learn why excessive optimization can produce misleading results.",
                "Understand the importance of out-of-sample testing."
            ],
            "explanation": (
                "Overfitting occurs when a strategy becomes excessively tailored "
                "to historical data and captures patterns that may not persist. "
                "Adding many parameters or repeatedly changing rules based on past "
                "results can produce impressive backtests that fail on new data. "
                "Using separate training and testing periods and keeping rules "
                "reasonably simple can help evaluate robustness."
            ),
            "example": (
                "If a learner repeatedly changes indicator periods until a strategy "
                "produces an unusually high historical return, the result may be "
                "overfit. Testing the unchanged strategy on a separate time period "
                "can provide a more realistic evaluation."
            ),
            "key_terms": [
                "Overfitting",
                "Optimization",
                "Out-of-Sample",
                "Robustness",
                "Parameter"
            ],
            "takeaways": [
                "A strategy that perfectly fits historical data may not generalize.",
                "Out-of-sample testing is important.",
                "Simpler and robust rules can be easier to evaluate."
            ],
        },
    },
    {
        "lesson_order": 18,
        "title": "Building & Evaluating a Complete Strategy",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine the major strategy-development concepts.",
                "Build a structured strategy for simulation.",
                "Learn how to evaluate and improve a strategy without changing rules arbitrarily."
            ],
            "explanation": (
                "A complete strategy should define the market or asset universe, "
                "timeframe, market conditions, setup, entry rules, exit rules, "
                "risk controls, position-sizing assumptions and evaluation metrics. "
                "After the rules are fixed, the strategy can be tested using historical "
                "data and paper trading. Results should be reviewed using multiple "
                "metrics and different market conditions. Any changes should be "
                "documented and tested again rather than made simply to improve one result."
            ),
            "example": (
                "A learner can create a hypothetical strategy based on trend and "
                "pullbacks, write every rule clearly, test it over historical periods, "
                "calculate win rate and expectancy, then evaluate the strategy on a "
                "separate period using the same rules."
            ),
            "key_terms": [
                "Strategy",
                "Backtesting",
                "Position Sizing",
                "Expectancy",
                "Risk Control",
                "Out-of-Sample Testing"
            ],
            "takeaways": [
                "A complete strategy needs clearly defined rules.",
                "Historical testing should use realistic assumptions.",
                "A strategy should be evaluated across different market conditions.",
                "Simulation and paper trading are useful learning tools before considering real-world decisions."
            ],
        },
    },
]


async def seed_module8():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 8}
        )

        if not module:
            raise RuntimeError(
                "Module 8 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 8,
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

        print(f"Module 8 lessons inserted: {inserted}")
        print(f"Module 8 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module8())