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
        "title": "What Is Trading?",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what trading means in financial markets.",
                "Understand how traders attempt to benefit from price movements.",
                "Understand why trading involves risk."
            ],
            "explanation": (
                "Trading means buying and selling financial instruments such as "
                "shares with the goal of managing or potentially benefiting from "
                "price movements. Traders may hold positions for different lengths "
                "of time, from very short periods to several months or longer. "
                "Trading decisions involve uncertainty, and profits are never guaranteed."
            ),
            "example": (
                "Suppose a trader buys a stock at ₹500 and later sells it at ₹520. "
                "Ignoring charges and taxes, the price difference is ₹20 per share. "
                "If the price instead falls, the trader may incur a loss."
            ),
            "key_terms": [
                "Trading",
                "Trader",
                "Position",
                "Buy",
                "Sell",
                "Price Movement"
            ],
            "takeaways": [
                "Trading involves buying and selling financial instruments.",
                "Traders may use different time horizons and strategies.",
                "Trading carries the possibility of both gains and losses."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Investing vs Trading",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the difference between investing and trading.",
                "Compare their typical time horizons.",
                "Understand that both involve financial risk."
            ],
            "explanation": (
                "Investing generally focuses on building wealth over a longer "
                "time horizon by owning assets based on their expected long-term "
                "value or income potential. Trading generally focuses more on "
                "price movements over shorter or medium-term periods. The boundary "
                "between investing and trading is not always exact."
            ),
            "example": (
                "An investor may buy shares after studying a company's long-term "
                "business prospects and intend to hold them for years. A trader "
                "may buy the same stock because they expect a price movement over "
                "the coming days or weeks."
            ),
            "key_terms": [
                "Investing",
                "Trading",
                "Time Horizon",
                "Capital Growth",
                "Price Movement"
            ],
            "takeaways": [
                "Investing usually emphasizes longer-term objectives.",
                "Trading often focuses more on shorter-term price movements.",
                "Neither approach guarantees returns."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Intraday Trading",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand intraday trading.",
                "Understand its time horizon.",
                "Understand why risk management is important for intraday traders."
            ],
            "explanation": (
                "Intraday trading refers to buying and selling a security during "
                "the same trading session, with positions generally intended to "
                "be closed before the session ends. Intraday traders often focus "
                "on short-term price movements and may use charts, volume, news "
                "and market data to make decisions."
            ),
            "example": (
                "A trader buys 100 shares during the trading session and sells "
                "those shares later on the same trading day. The trader is attempting "
                "to benefit from an intraday price movement."
            ),
            "key_terms": [
                "Intraday",
                "Trading Session",
                "Short-Term",
                "Position",
                "Volatility"
            ],
            "takeaways": [
                "Intraday trades are generally opened and closed within the same session.",
                "Short-term price movements can be unpredictable.",
                "Risk management is especially important for short-term trading."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Swing Trading",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand swing trading.",
                "Understand how swing traders use price movements.",
                "Understand the importance of managing overnight risk."
            ],
            "explanation": (
                "Swing trading generally involves holding a position for several "
                "days or weeks while attempting to benefit from a meaningful price "
                "move. Swing traders may use technical analysis, market trends, "
                "company information and other data. Positions can be exposed to "
                "overnight and weekend market movements."
            ),
            "example": (
                "A trader identifies a potential upward trend and buys shares with "
                "the intention of holding them for several days. If the expected "
                "movement occurs, the trader may later sell the position."
            ),
            "key_terms": [
                "Swing Trading",
                "Trend",
                "Breakout",
                "Overnight Risk",
                "Position"
            ],
            "takeaways": [
                "Swing trades commonly last several days or weeks.",
                "Price movements can change while the market is closed.",
                "A defined risk-management plan is important."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Positional Trading",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand positional trading.",
                "Understand longer trading time horizons.",
                "Understand how trends and broader market factors can matter."
            ],
            "explanation": (
                "Positional trading generally involves holding positions for "
                "weeks or months, attempting to benefit from larger market trends "
                "or changes in an asset's value. Positional traders may combine "
                "technical and fundamental information and must account for "
                "market developments during the holding period."
            ),
            "example": (
                "A trader identifies a long-term trend in a stock and decides to "
                "hold a position for several weeks. The trader monitors the trend "
                "and relevant company or market developments during that period."
            ),
            "key_terms": [
                "Positional Trading",
                "Trend",
                "Holding Period",
                "Market Trend"
            ],
            "takeaways": [
                "Positional trading generally uses a longer horizon than intraday trading.",
                "Broader market and company developments can affect the position.",
                "Longer holding periods still involve significant uncertainty."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Delivery Trading",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand delivery-based share transactions.",
                "Understand how delivery differs from intraday trading.",
                "Understand the role of a demat account."
            ],
            "explanation": (
                "In a typical delivery-based equity transaction, shares purchased "
                "are intended to be held beyond the trading session and are credited "
                "to the investor's demat account after settlement. Delivery-based "
                "ownership allows an investor to hold shares for a chosen period "
                "subject to the applicable market and settlement rules."
            ),
            "example": (
                "An investor purchases 50 shares and does not close the position "
                "during the same session. After the applicable settlement process, "
                "the shares can be credited to the investor's demat account."
            ),
            "key_terms": [
                "Delivery",
                "Demat Account",
                "Settlement",
                "Holding",
                "Equity Shares"
            ],
            "takeaways": [
                "Delivery transactions are intended to result in holding shares.",
                "Shares are held electronically in a demat account.",
                "Settlement occurs according to applicable market rules."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Market Orders",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a market order.",
                "Understand how market orders are executed.",
                "Understand why the final execution price may differ from the displayed price."
            ],
            "explanation": (
                "A market order instructs a broker or trading system to buy or "
                "sell a specified quantity at the best available prices in the "
                "market. Because prices can change rapidly, the actual execution "
                "price is not guaranteed to be the same as the price displayed "
                "when the order was submitted."
            ),
            "example": (
                "If the best available selling price is ₹100 when a market buy "
                "order is executed, the order may fill around that level. If available "
                "liquidity changes, different portions of the order may execute "
                "at different prices."
            ),
            "key_terms": [
                "Market Order",
                "Execution",
                "Liquidity",
                "Best Available Price",
                "Slippage"
            ],
            "takeaways": [
                "Market orders prioritize execution over a specific price.",
                "The execution price can change as market conditions change.",
                "Liquidity can affect the execution of larger orders."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Limit Orders",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a limit order.",
                "Understand the difference between market and limit orders.",
                "Understand why a limit order may remain unfilled."
            ],
            "explanation": (
                "A limit order specifies the maximum price a buyer is willing to "
                "pay or the minimum price a seller is willing to accept. It provides "
                "price control but does not guarantee execution. The order may remain "
                "unfilled if the market does not reach the specified price."
            ),
            "example": (
                "Suppose a stock is trading near ₹500 and a trader places a limit "
                "buy order at ₹490. The order will generally execute only if matching "
                "sell orders become available at ₹490 or better under the market's "
                "order-matching rules."
            ),
            "key_terms": [
                "Limit Order",
                "Limit Price",
                "Execution",
                "Order Book"
            ],
            "takeaways": [
                "Limit orders provide price control.",
                "A limit order does not guarantee execution.",
                "The specified price determines when matching can occur."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Stop-Loss Orders",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the purpose of a stop-loss order.",
                "Understand how stop prices can trigger an order.",
                "Understand that stop-loss orders do not guarantee a particular exit price."
            ],
            "explanation": (
                "A stop-loss order is designed to trigger an order when a specified "
                "stop price is reached, according to the rules of the relevant "
                "trading system. Traders may use such orders as part of a risk-"
                "management plan. Rapid markets or gaps can cause the actual execution "
                "price to differ from the intended level."
            ),
            "example": (
                "A trader buys a stock at ₹500 and decides that they want to limit "
                "the planned loss on the position. They may place a suitable stop "
                "order according to their broker's available order types and rules."
            ),
            "key_terms": [
                "Stop-Loss",
                "Stop Price",
                "Risk Management",
                "Trigger",
                "Execution"
            ],
            "takeaways": [
                "Stop orders can be part of a risk-management plan.",
                "Triggering does not guarantee a specific execution price.",
                "Order types and rules vary by broker and market."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Bid, Ask & Spread",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand bid and ask prices.",
                "Understand the bid-ask spread.",
                "Understand why spread matters when trading."
            ],
            "explanation": (
                "The bid is the highest price currently offered by a buyer, while "
                "the ask is the lowest price currently offered by a seller. The "
                "difference between the ask and bid is called the bid-ask spread. "
                "The spread can vary depending on liquidity, market conditions and "
                "the security."
            ),
            "example": (
                "Suppose the highest available bid is ₹99 and the lowest available "
                "ask is ₹100. The bid-ask spread is ₹1."
            ),
            "key_terms": [
                "Bid",
                "Ask",
                "Spread",
                "Order Book",
                "Liquidity"
            ],
            "takeaways": [
                "Bid represents a buyer's available price.",
                "Ask represents a seller's available price.",
                "The difference between them is the spread."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Long & Short Positions",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand long positions.",
                "Understand the basic concept of short positions.",
                "Understand that short selling has additional risks and rules."
            ],
            "explanation": (
                "A long position generally means holding an asset with the "
                "expectation that its value may rise. Short selling is a strategy "
                "where a trader seeks to benefit from a decline in price through "
                "a permitted short-sale mechanism. Short selling is subject to "
                "specific market, broker and regulatory requirements and can involve "
                "substantial risk."
            ),
            "example": (
                "In a long position, a trader buys a share and hopes its price "
                "increases. In a permitted short position, a trader sells first "
                "under the applicable mechanism and seeks to buy back later at a "
                "lower price, although the price could instead rise."
            ),
            "key_terms": [
                "Long Position",
                "Short Position",
                "Short Selling",
                "Borrowing",
                "Margin"
            ],
            "takeaways": [
                "A long position generally benefits from an increase in price.",
                "A short position generally seeks to benefit from a price decline.",
                "Short selling has specific rules and potentially significant risks."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Trade Execution & Settlement",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand trade execution.",
                "Understand the basic settlement process.",
                "Understand why settlement is different from order execution."
            ],
            "explanation": (
                "Trade execution occurs when a buy and sell order are matched "
                "according to the market's order-matching system. Settlement is "
                "the subsequent process through which the obligations from the "
                "trade are completed, such as transferring securities and funds "
                "according to the applicable settlement cycle and market rules. "
                "Execution and settlement are therefore different stages."
            ),
            "example": (
                "An investor's buy order may be matched with a seller's order "
                "during market hours. The trade is executed at the matched price, "
                "while the transfer of securities and funds is completed through "
                "the applicable settlement process."
            ),
            "key_terms": [
                "Execution",
                "Order Matching",
                "Settlement",
                "Securities",
                "Settlement Cycle"
            ],
            "takeaways": [
                "Execution means the orders have been matched.",
                "Settlement completes the obligations created by the trade.",
                "Settlement timelines depend on the applicable market rules."
            ],
        },
    },
]


async def seed_module3():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 3}
        )

        if not module:
            raise RuntimeError(
                "Module 3 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 3,
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

        print(f"Module 3 lessons inserted: {inserted}")
        print(f"Module 3 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module3())