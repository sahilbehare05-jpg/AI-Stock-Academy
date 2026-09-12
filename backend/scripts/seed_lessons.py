import asyncio

from app.database.db import (
    connect_to_mongo,
    close_mongo_connection,
    get_database,
    Collections,
)


LESSONS = [
    {
        "module_order": 1,
        "lesson_order": 1,
        "title": "What Is Money, Saving & Investing?",
        "level": "Beginner",
        "estimated_minutes": 15,
        "content": {
            "objectives": [
                "Understand the basic purpose of money.",
                "Understand the difference between saving and investing.",
                "Understand why people invest for long-term goals.",
            ],
            "explanation": (
                "Money is a medium used to buy goods and services and to store "
                "purchasing power. Saving means keeping part of your income "
                "available for future needs. Investing means putting money into "
                "assets with the expectation that they may grow in value or "
                "generate income over time. Investing involves risk, and returns "
                "are never guaranteed."
            ),
            "example": (
                "Suppose a person receives ₹30,000 and keeps ₹5,000 aside for "
                "future needs. That is saving. If they later decide to invest "
                "some money in a diversified investment after understanding the "
                "risks, that is investing."
            ),
            "key_terms": [
                "Money",
                "Saving",
                "Investing",
                "Return",
                "Risk",
            ],
            "takeaways": [
                "Saving focuses mainly on keeping money available.",
                "Investing focuses on potentially growing wealth over time.",
                "Every investment has some level of risk.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 2,
        "title": "What Is the Stock Market?",
        "level": "Beginner",
        "estimated_minutes": 15,
        "content": {
            "objectives": [
                "Understand what the stock market is.",
                "Understand why stocks are bought and sold.",
                "Understand the role of supply and demand.",
            ],
            "explanation": (
                "The stock market is a marketplace where shares of publicly "
                "listed companies can be bought and sold. Investors and traders "
                "participate through regulated exchanges and brokers. Stock prices "
                "can change because of supply and demand and because investors "
                "react to company, economic and market information."
            ),
            "example": (
                "If many investors want to buy shares of a company while fewer "
                "people are willing to sell at the current price, buying pressure "
                "can push the market price higher."
            ),
            "key_terms": [
                "Stock Market",
                "Share",
                "Buyer",
                "Seller",
                "Supply",
                "Demand",
            ],
            "takeaways": [
                "The stock market facilitates buying and selling of shares.",
                "Prices constantly change as market conditions change.",
                "A rising price does not guarantee that a company is a good investment.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 3,
        "title": "What Is a Stock?",
        "level": "Beginner",
        "estimated_minutes": 15,
        "content": {
            "objectives": [
                "Understand what a stock represents.",
                "Understand ownership through shares.",
                "Understand why stock prices change.",
            ],
            "explanation": (
                "A stock, also called a share or equity, represents a unit of "
                "ownership in a company. When a company issues shares to the "
                "public, investors can become shareholders. Shareholders may "
                "benefit if the value of their shares increases and may receive "
                "dividends when a company declares them. Neither price gains nor "
                "dividends are guaranteed."
            ),
            "example": (
                "If a company has 1,000 shares and an investor owns 10 shares, "
                "the investor owns a small fraction of that company."
            ),
            "key_terms": [
                "Stock",
                "Share",
                "Equity",
                "Shareholder",
                "Dividend",
            ],
            "takeaways": [
                "A stock represents ownership in a company.",
                "Share prices can rise or fall.",
                "Owning a stock involves investment risk.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 4,
        "title": "How Companies & Shareholders Work",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the relationship between companies and shareholders.",
                "Understand why companies issue shares.",
                "Understand basic shareholder rights.",
            ],
            "explanation": (
                "Companies can raise capital by issuing shares. Investors who "
                "purchase those shares become shareholders. Depending on the "
                "share class and applicable rules, shareholders may have voting "
                "rights and may receive dividends if declared by the company."
            ),
            "example": (
                "Imagine a company wants capital to expand its business. It can "
                "raise money by issuing shares to investors. Investors provide "
                "capital and receive ownership represented by those shares."
            ),
            "key_terms": [
                "Company",
                "Shareholder",
                "Capital",
                "Ownership",
                "Dividend",
                "Voting Rights",
            ],
            "takeaways": [
                "Companies can use equity markets to raise capital.",
                "Shareholders own a portion of the company.",
                "Shareholder rights depend on the type of shares and applicable rules.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 5,
        "title": "What Is a Stock Exchange?",
        "level": "Beginner",
        "estimated_minutes": 15,
        "content": {
            "objectives": [
                "Understand the purpose of a stock exchange.",
                "Understand how exchanges support organized trading.",
                "Understand the importance of market regulation.",
            ],
            "explanation": (
                "A stock exchange is an organized marketplace that provides "
                "infrastructure and rules for trading securities. Exchanges help "
                "facilitate transparent price discovery and orderly transactions. "
                "Investors normally access exchanges through registered brokers."
            ),
            "example": (
                "When an investor places an order through a broker to buy a listed "
                "stock, the order can be routed to the relevant exchange where it "
                "may be matched with a suitable seller."
            ),
            "key_terms": [
                "Stock Exchange",
                "Broker",
                "Order",
                "Price Discovery",
                "Listed Company",
            ],
            "takeaways": [
                "Exchanges provide organized trading infrastructure.",
                "They operate under rules and regulations.",
                "Brokers provide investors access to exchanges.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 6,
        "title": "NSE, BSE & Global Exchanges",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand NSE and BSE.",
                "Understand why different countries have different exchanges.",
                "Recognize major global exchanges.",
            ],
            "explanation": (
                "India has two major stock exchanges: the National Stock Exchange "
                "of India (NSE) and BSE Ltd. Globally, major exchanges include "
                "NYSE and Nasdaq in the United States and other exchanges across "
                "Europe and Asia. Different exchanges list different securities "
                "and operate under their respective market rules."
            ),
            "example": (
                "A company listed on NSE may have an NSE trading symbol that "
                "differs from identifiers used on another exchange."
            ),
            "key_terms": [
                "NSE",
                "BSE",
                "NYSE",
                "Nasdaq",
                "Exchange",
            ],
            "takeaways": [
                "NSE and BSE are major Indian stock exchanges.",
                "Different countries have different exchanges.",
                "A company can sometimes be listed on more than one exchange.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 7,
        "title": "What Is a Stock Market Index?",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what a market index is.",
                "Learn the purpose of NIFTY 50 and Sensex.",
                "Understand why indexes are used as market indicators.",
            ],
            "explanation": (
                "A stock market index tracks the performance of a selected group "
                "of securities according to a defined methodology. In India, "
                "NIFTY 50 and the S&P BSE Sensex are widely followed benchmarks. "
                "An index can help investors understand the general performance "
                "of a segment of the market."
            ),
            "example": (
                "If a major Indian index rises during a trading session, it means "
                "the securities included in that index have produced an overall "
                "positive index movement according to its methodology. It does "
                "not mean every stock in the market increased."
            ),
            "key_terms": [
                "Index",
                "NIFTY 50",
                "Sensex",
                "Benchmark",
                "Constituent",
            ],
            "takeaways": [
                "An index represents a selected group of securities.",
                "Indexes are useful benchmarks.",
                "Index movement does not describe every individual stock.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 8,
        "title": "Who Participates in the Market?",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Identify major stock market participants.",
                "Understand the difference between investors and traders.",
                "Understand the role of institutions and regulators.",
            ],
            "explanation": (
                "Stock markets include many participants such as individual "
                "investors, traders, mutual funds, pension funds, insurance "
                "companies, foreign investors, companies, market makers and "
                "brokers. Regulators establish rules intended to support fair "
                "and orderly markets."
            ),
            "example": (
                "An individual investor may buy shares for long-term ownership, "
                "while a trader may buy and sell based on shorter-term market "
                "conditions. An institution may manage a large portfolio on "
                "behalf of its clients."
            ),
            "key_terms": [
                "Retail Investor",
                "Trader",
                "Institutional Investor",
                "Broker",
                "Regulator",
            ],
            "takeaways": [
                "Different participants have different objectives.",
                "Institutions can manage substantial amounts of capital.",
                "Regulators establish and enforce market rules.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 9,
        "title": "Broker, Demat & Trading Accounts",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the basic purpose of a broker.",
                "Understand a demat account.",
                "Understand a trading account.",
            ],
            "explanation": (
                "A broker provides access to financial markets and facilitates "
                "orders. In India, a demat account is used to hold securities in "
                "electronic form, while a trading account is used to place buy "
                "and sell orders. The exact account structure and services depend "
                "on the intermediary and applicable regulations."
            ),
            "example": (
                "An investor may use a registered broker's platform to place an "
                "order for shares. After settlement, purchased securities are "
                "held electronically in the investor's demat account."
            ),
            "key_terms": [
                "Broker",
                "Demat Account",
                "Trading Account",
                "Order",
                "Settlement",
            ],
            "takeaways": [
                "A broker provides market access.",
                "A demat account holds securities electronically.",
                "A trading account is used to place transactions.",
            ],
        },
    },
    {
        "module_order": 1,
        "lesson_order": 10,
        "title": "How a Stock Trade Actually Works",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand the basic lifecycle of a stock order.",
                "Understand buyers and sellers.",
                "Understand order execution and settlement.",
            ],
            "explanation": (
                "A basic stock transaction starts when an investor places an "
                "order through a broker. The order is sent to the relevant "
                "marketplace and may be matched with an appropriate opposite "
                "order. If executed, the transaction goes through the applicable "
                "clearing and settlement process."
            ),
            "example": (
                "Suppose an investor places a limit order to buy 10 shares at "
                "₹1,000 or less. The order can execute if a matching seller is "
                "available at the required price and market conditions permit."
            ),
            "key_terms": [
                "Buy Order",
                "Sell Order",
                "Market Order",
                "Limit Order",
                "Execution",
                "Settlement",
            ],
            "takeaways": [
                "Placing an order does not always guarantee execution.",
                "A trade requires a suitable matching order.",
                "Executed trades go through clearing and settlement procedures.",
            ],
        },
    },
]


async def seed_lessons():
    connect_to_mongo()

    try:
        db = get_database()
        lessons = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        module = await db[Collections.MODULES].find_one(
            {"order": 1}
        )

        if not module:
            raise RuntimeError(
                "Module 1 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                **lesson,
            }

            result = await lessons.update_one(
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

        print(f"Academy lessons inserted: {inserted}")
        print(f"Academy lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_lessons())