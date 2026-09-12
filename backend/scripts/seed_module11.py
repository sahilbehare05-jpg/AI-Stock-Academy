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
        "title": "Market Cycles",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the concept of market cycles.",
                "Learn how expansion, contraction and recovery can affect markets.",
                "Understand why cycles do not follow perfectly predictable schedules.",
            ],
            "explanation": (
                "Markets can move through broad phases influenced by economic growth, "
                "liquidity, earnings, investor expectations and financial conditions. "
                "A simplified cycle can include expansion, peak, slowdown and recovery. "
                "Different assets and sectors may move through these phases at different "
                "times, so market cycles should be treated as analytical frameworks rather "
                "than precise timing rules."
            ),
            "example": (
                "During a period of strong economic growth, company earnings may improve "
                "and investor confidence may rise. Later, slowing growth or tighter "
                "financial conditions can change market expectations."
            ),
            "key_terms": [
                "Market Cycle",
                "Expansion",
                "Peak",
                "Slowdown",
                "Recovery",
            ],
            "takeaways": [
                "Markets can experience recurring broad phases.",
                "Different assets may behave differently during the same cycle.",
                "Cycles are useful frameworks, not exact prediction tools.",
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Bull & Bear Markets",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand bull and bear markets.",
                "Learn how market direction and investor sentiment interact.",
                "Understand why market classifications can depend on the index and measurement period.",
            ],
            "explanation": (
                "A bull market generally refers to a prolonged period of rising market "
                "prices and positive sentiment, while a bear market generally refers "
                "to a prolonged period of declining prices and weaker sentiment. The "
                "exact percentage definitions used to classify a market can vary by "
                "source and index. Bull and bear phases can contain significant temporary "
                "moves in the opposite direction."
            ),
            "example": (
                "An equity index can remain in a broader bullish phase while experiencing "
                "a temporary correction. Similarly, a bear market can contain short periods "
                "of strong price recovery."
            ),
            "key_terms": [
                "Bull Market",
                "Bear Market",
                "Correction",
                "Sentiment",
                "Trend",
            ],
            "takeaways": [
                "Bull markets generally involve sustained upward price behavior.",
                "Bear markets generally involve sustained downward price behavior.",
                "Short-term movements do not always change the broader market regime.",
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Economic Indicators",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand economic indicators.",
                "Learn the difference between leading, coincident and lagging indicators.",
                "Understand how economic data can influence market expectations.",
            ],
            "explanation": (
                "Economic indicators provide information about economic activity. "
                "Leading indicators may change before broader economic conditions, "
                "coincident indicators describe current activity, and lagging indicators "
                "often confirm changes after they have occurred. Examples include "
                "employment data, inflation measures, industrial production, consumer "
                "confidence and purchasing activity."
            ),
            "example": (
                "A decline in new business orders may provide an early indication of "
                "slowing activity, while employment data may provide additional evidence "
                "about the condition of the economy."
            ),
            "key_terms": [
                "Economic Indicator",
                "Leading Indicator",
                "Coincident Indicator",
                "Lagging Indicator",
                "Economic Growth",
            ],
            "takeaways": [
                "Economic indicators provide different types of information.",
                "Leading indicators may provide earlier signals but are not guarantees.",
                "Markets often react to changes in expectations as well as the data itself.",
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Interest Rates & Markets",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand how interest rates affect financial markets.",
                "Learn why borrowing costs matter to businesses and consumers.",
                "Understand the relationship between rates, valuation and investor behavior.",
            ],
            "explanation": (
                "Interest rates influence borrowing costs, saving incentives, company "
                "financing and the valuation of financial assets. Higher rates can increase "
                "borrowing costs and can reduce the present value assigned to future cash "
                "flows under common valuation models. Lower rates can have the opposite "
                "effect, although the actual market response depends on economic conditions "
                "and expectations."
            ),
            "example": (
                "If borrowing costs rise, a highly indebted company may face higher "
                "interest expenses. Investors may also reassess the valuation of growth "
                "companies whose expected cash flows are far in the future."
            ),
            "key_terms": [
                "Interest Rate",
                "Borrowing Cost",
                "Valuation",
                "Discount Rate",
                "Monetary Policy",
            ],
            "takeaways": [
                "Interest rates affect financing and valuation.",
                "Highly indebted companies can be more sensitive to borrowing costs.",
                "Market reactions depend on expectations and the broader economic environment.",
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Inflation & Markets",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand inflation.",
                "Learn how inflation can affect companies and consumers.",
                "Understand why different businesses respond differently to inflation.",
            ],
            "explanation": (
                "Inflation refers to a broad increase in the prices of goods and services "
                "over time, reducing the purchasing power of money. Inflation can increase "
                "input costs, wages and financing costs. Companies with strong pricing power "
                "may be better positioned to pass some costs to customers, while businesses "
                "with weak pricing power may experience pressure on margins."
            ),
            "example": (
                "If raw-material costs increase significantly but a company cannot raise "
                "its selling prices, its operating margin may come under pressure."
            ),
            "key_terms": [
                "Inflation",
                "Purchasing Power",
                "Input Cost",
                "Pricing Power",
                "Margin",
            ],
            "takeaways": [
                "Inflation changes the purchasing power of money.",
                "Higher input costs can affect company profitability.",
                "The effect of inflation differs across industries and businesses.",
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Monetary Policy",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand monetary policy.",
                "Learn the role of central banks.",
                "Understand how policy decisions can affect financial conditions.",
            ],
            "explanation": (
                "Monetary policy refers to actions taken by a central bank to influence "
                "financial and economic conditions. Depending on the country and framework, "
                "central banks may use policy interest rates, liquidity operations and other "
                "tools. Changes in monetary policy can affect borrowing costs, currency "
                "conditions, demand, inflation expectations and asset valuations."
            ),
            "example": (
                "If a central bank tightens monetary policy, borrowing conditions may become "
                "more restrictive. Investors can then reassess company earnings expectations "
                "and asset valuations."
            ),
            "key_terms": [
                "Monetary Policy",
                "Central Bank",
                "Policy Rate",
                "Liquidity",
                "Financial Conditions",
            ],
            "takeaways": [
                "Central banks influence financial conditions through monetary policy.",
                "Policy changes can affect borrowing costs and market expectations.",
                "Markets can react to both policy decisions and anticipated future policy.",
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Fiscal Policy",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand fiscal policy.",
                "Learn how government spending and taxation affect economic activity.",
                "Understand why fiscal policy can influence sectors differently.",
            ],
            "explanation": (
                "Fiscal policy refers to government decisions involving spending, taxation "
                "and related public-finance measures. Expansionary fiscal policy can support "
                "economic activity through higher government spending or lower taxes, while "
                "contractionary policy can reduce demand. The effects depend on the size, "
                "timing and composition of government measures."
            ),
            "example": (
                "Increased infrastructure spending may directly benefit construction, "
                "engineering and materials companies, while changes in taxation can affect "
                "consumer demand or company profitability."
            ),
            "key_terms": [
                "Fiscal Policy",
                "Government Spending",
                "Taxation",
                "Budget",
                "Public Finance",
            ],
            "takeaways": [
                "Fiscal policy uses government spending and taxation tools.",
                "Different industries can experience different effects.",
                "Fiscal measures should be analyzed in their economic context.",
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Global Markets & Correlations",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand connections between global markets.",
                "Learn how international events can affect domestic assets.",
                "Understand correlation and why it can change over time.",
            ],
            "explanation": (
                "Financial markets are connected through trade, capital flows, currencies, "
                "commodities, interest rates and investor sentiment. A major movement in "
                "one global market can influence another. Correlation measures how assets "
                "have moved relative to each other historically, but correlations are not "
                "constant and can change during periods of stress."
            ),
            "example": (
                "A significant change in global oil prices can affect energy companies, "
                "transportation businesses, inflation expectations and currencies in "
                "oil-importing or oil-exporting economies."
            ),
            "key_terms": [
                "Global Markets",
                "Correlation",
                "Capital Flow",
                "Currency",
                "Commodity",
            ],
            "takeaways": [
                "Global markets are connected through multiple channels.",
                "International events can affect domestic financial assets.",
                "Historical correlations can change under different market conditions.",
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Sector Rotation",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand sector rotation.",
                "Learn why different sectors can perform differently during economic cycles.",
                "Understand how investors study relative sector performance.",
            ],
            "explanation": (
                "Sector rotation describes changes in relative investor interest and "
                "performance across economic sectors. Different sectors can respond "
                "differently to changes in growth, inflation, interest rates and market "
                "sentiment. Analysts may compare sector indexes, earnings trends, valuations "
                "and relative strength to study these shifts."
            ),
            "example": (
                "During an economic slowdown, defensive sectors may behave differently "
                "from highly cyclical industries. If expectations later improve, cyclical "
                "sectors may attract greater investor attention."
            ),
            "key_terms": [
                "Sector Rotation",
                "Cyclical Sector",
                "Defensive Sector",
                "Relative Strength",
                "Economic Cycle",
            ],
            "takeaways": [
                "Different sectors can respond differently to economic conditions.",
                "Sector rotation focuses on relative performance and capital allocation.",
                "Historical sector behavior is not a guarantee of future performance.",
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Institutional Investors",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand institutional investors.",
                "Learn why large investors can influence market liquidity and flows.",
                "Understand why institutional activity should not be treated as a guaranteed signal.",
            ],
            "explanation": (
                "Institutional investors include organizations such as mutual funds, "
                "pension funds, insurance companies and other large investment entities. "
                "Their transactions can represent substantial market flows, particularly "
                "in less liquid securities. However, observing institutional buying or "
                "selling does not reveal every reason behind a decision and should not "
                "automatically be treated as a buy or sell signal."
            ),
            "example": (
                "A large fund may reduce a holding because of portfolio rebalancing "
                "rather than because its fundamental view of the company has changed."
            ),
            "key_terms": [
                "Institutional Investor",
                "Mutual Fund",
                "Pension Fund",
                "Capital Flow",
                "Rebalancing",
            ],
            "takeaways": [
                "Institutions can create significant market flows.",
                "Institutional activity can have many different reasons.",
                "Large-investor activity should be interpreted with broader evidence.",
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Market Liquidity",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand market liquidity.",
                "Learn how trading volume and bid-ask spreads relate to liquidity.",
                "Understand why liquidity matters for execution risk.",
            ],
            "explanation": (
                "Liquidity describes how easily an asset can be bought or sold without "
                "causing a large change in its price. Highly liquid markets often have "
                "greater trading activity and narrower bid-ask spreads, although liquidity "
                "can change rapidly during stressful conditions. Lower liquidity can increase "
                "transaction costs and execution uncertainty."
            ),
            "example": (
                "A highly traded large-cap stock may have many buyers and sellers, while "
                "a thinly traded security may have fewer participants and a wider spread."
            ),
            "key_terms": [
                "Liquidity",
                "Bid-Ask Spread",
                "Trading Volume",
                "Market Depth",
                "Execution",
            ],
            "takeaways": [
                "Liquidity affects how easily transactions can occur.",
                "Lower liquidity can increase execution uncertainty.",
                "Liquidity can deteriorate during volatile market conditions.",
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Market Regimes",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand market regimes.",
                "Learn how trends, volatility and macro conditions can define different environments.",
                "Understand why a strategy can behave differently across regimes.",
            ],
            "explanation": (
                "A market regime is a broad set of conditions describing how a market "
                "is behaving during a particular period. Examples include trending, "
                "range-bound, high-volatility and low-volatility environments. Economic "
                "growth, inflation, liquidity and investor sentiment can contribute to "
                "regime changes. A strategy that works well in one regime may perform "
                "differently in another."
            ),
            "example": (
                "A trend-following strategy may perform differently during a persistent "
                "trend than during a sideways market with frequent reversals."
            ),
            "key_terms": [
                "Market Regime",
                "Volatility",
                "Trend",
                "Range",
                "Regime Change",
            ],
            "takeaways": [
                "Market conditions change over time.",
                "Strategies can have different results in different regimes.",
                "Regime analysis helps put historical strategy results into context.",
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Geopolitical & Event Risk",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand geopolitical risk.",
                "Learn how major events can affect markets.",
                "Understand why event outcomes are difficult to predict.",
            ],
            "explanation": (
                "Geopolitical and event risks include conflicts, elections, policy "
                "announcements, trade restrictions, natural disasters and other events "
                "that can change economic expectations. Markets may react through "
                "equities, currencies, commodities, bonds and volatility. The direction "
                "and size of a reaction can be difficult to predict because markets "
                "respond to both the event and expectations about future consequences."
            ),
            "example": (
                "A sudden change in trade policy may affect companies with significant "
                "international supply chains differently from businesses focused primarily "
                "on domestic markets."
            ),
            "key_terms": [
                "Geopolitical Risk",
                "Event Risk",
                "Policy",
                "Trade",
                "Volatility",
            ],
            "takeaways": [
                "Major events can quickly change market expectations.",
                "Different companies have different event exposures.",
                "Event-driven market reactions are uncertain and can be rapid.",
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Earnings & Corporate Events",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand earnings events.",
                "Learn about dividends, buybacks, splits and other corporate actions.",
                "Understand why expectations matter around company announcements.",
            ],
            "explanation": (
                "Corporate events can materially affect a company's stock price and "
                "financial outlook. Earnings announcements provide information about "
                "revenue, profitability, guidance and other business conditions. Other "
                "events include dividends, buybacks, stock splits, acquisitions and "
                "management changes. Market reactions depend not only on the reported "
                "result but also on how it compares with investor expectations."
            ),
            "example": (
                "A company can report higher profit than the previous year but still "
                "experience a negative market reaction if investors expected an even "
                "stronger result or weaker future guidance."
            ),
            "key_terms": [
                "Earnings",
                "Guidance",
                "Dividend",
                "Buyback",
                "Corporate Action",
            ],
            "takeaways": [
                "Corporate events can change market expectations.",
                "Reported results should be compared with expectations and previous periods.",
                "The market reaction to an event is not always obvious beforehand.",
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Intermarket Analysis",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand intermarket analysis.",
                "Learn how equities, bonds, currencies and commodities can interact.",
                "Understand why relationships between markets are dynamic."
            ],
            "explanation": (
                "Intermarket analysis studies relationships between major asset classes "
                "such as equities, bonds, currencies and commodities. Changes in interest "
                "rates, inflation expectations, economic growth and risk sentiment can "
                "influence several markets simultaneously. These relationships can provide "
                "context, but historical relationships are not fixed and can break down."
            ),
            "example": (
                "A change in inflation expectations may influence bond yields, currency "
                "markets and equity valuations at the same time. An analyst can examine "
                "these movements together instead of studying each market in isolation."
            ),
            "key_terms": [
                "Intermarket Analysis",
                "Equities",
                "Bonds",
                "Currencies",
                "Commodities",
            ],
            "takeaways": [
                "Asset classes can influence one another through economic channels.",
                "Intermarket analysis provides broader market context.",
                "Historical relationships can change as economic conditions change.",
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Complete Advanced Market Analysis",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine macroeconomic and market-structure concepts.",
                "Build a complete framework for analyzing market conditions.",
                "Understand how multiple factors interact."
            ],
            "explanation": (
                "Advanced market analysis combines economic indicators, monetary and "
                "fiscal policy, inflation, interest rates, global markets, sector behavior, "
                "liquidity, market regimes and corporate events. A structured analysis "
                "should distinguish current facts from expectations and scenarios. No "
                "single macroeconomic indicator or market relationship can reliably "
                "predict every future price movement."
            ),
            "example": (
                "A learner can review economic growth, inflation, interest-rate expectations, "
                "global market behavior, sector performance and corporate earnings before "
                "forming a simulated market scenario. The learner can then record what "
                "evidence would confirm or challenge that scenario."
            ),
            "key_terms": [
                "Macro Analysis",
                "Market Regime",
                "Economic Cycle",
                "Intermarket Analysis",
                "Sector Rotation",
                "Event Risk",
            ],
            "takeaways": [
                "Advanced analysis combines multiple economic and market factors.",
                "Different factors can reinforce or contradict one another.",
                "Scenarios and probabilities are more realistic than certainty.",
                "A complete analysis should clearly identify assumptions and risks.",
            ],
        },
    },
]


async def seed_module11():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 11}
        )

        if not module:
            raise RuntimeError(
                "Module 11 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 11,
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

        print(f"Module 11 lessons inserted: {inserted}")
        print(f"Module 11 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module11())