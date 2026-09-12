import asyncio
from datetime import datetime, timezone

from app.database.db import (
    connect_to_mongo,
    close_mongo_connection,
    get_database,
    Collections,
)


LESSONS = [
    {
        "module_order": 2,
        "lesson_order": 1,
        "title": "IPO & Public Companies",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what an Initial Public Offering (IPO) is.",
                "Understand why private companies become publicly listed.",
                "Understand the basic journey from private company to listed company.",
            ],
            "explanation": (
                "An Initial Public Offering, or IPO, is the process through which "
                "a private company offers shares to the public for the first time "
                "and becomes publicly listed, subject to applicable rules and "
                "regulatory requirements. Companies may use an IPO to raise capital "
                "for expansion, repayment of obligations, acquisitions, or other "
                "business purposes. After listing, the company's shares can generally "
                "be traded in the secondary market."
            ),
            "example": (
                "Imagine a growing private company needs ₹500 crore to expand its "
                "business. It may decide to raise part of that capital by offering "
                "shares to investors through an IPO. After the shares are listed, "
                "investors can trade them in the secondary market."
            ),
            "key_terms": [
                "IPO",
                "Private Company",
                "Public Company",
                "Listing",
                "Primary Market",
            ],
            "takeaways": [
                "An IPO is a company's first public offering of shares.",
                "Companies can raise capital through an IPO.",
                "After listing, shares can generally trade in the secondary market.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 2,
        "title": "Primary Market vs Secondary Market",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the primary market.",
                "Understand the secondary market.",
                "Understand the difference between the two.",
            ],
            "explanation": (
                "The primary market is where securities are issued and sold to "
                "investors for the first time, allowing issuers to raise capital. "
                "The secondary market is where existing securities are bought and "
                "sold between investors. In a typical secondary-market transaction, "
                "the company does not directly receive the purchase money from the "
                "investor buying the shares."
            ),
            "example": (
                "When investors subscribe to a new share issue by a company, that "
                "transaction belongs to the primary market. When one investor later "
                "sells those shares to another investor on an exchange, that is a "
                "secondary-market transaction."
            ),
            "key_terms": [
                "Primary Market",
                "Secondary Market",
                "New Issue",
                "Investor",
                "Issuer",
            ],
            "takeaways": [
                "Primary markets deal with newly issued securities.",
                "Secondary markets allow existing securities to be traded.",
                "The two markets serve different purposes.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 3,
        "title": "Market Capitalization",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand market capitalization.",
                "Learn the basic calculation.",
                "Understand why market cap is useful.",
            ],
            "explanation": (
                "Market capitalization, commonly called market cap, is the market "
                "value of a company's outstanding equity shares. A simplified "
                "calculation is: market capitalization = current share price × "
                "number of outstanding shares. Market cap can change as the share "
                "price changes or as the number of shares changes."
            ),
            "example": (
                "If a company has 10 crore outstanding shares and its market price "
                "is ₹200 per share, its simplified market capitalization is "
                "₹2,000 crore."
            ),
            "key_terms": [
                "Market Capitalization",
                "Outstanding Shares",
                "Share Price",
                "Equity Value",
            ],
            "takeaways": [
                "Market cap measures the market value of outstanding equity.",
                "It is calculated using share price and outstanding shares.",
                "Market cap changes with the market value of the company.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 4,
        "title": "Large Cap, Mid Cap & Small Cap",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand the meaning of large-cap, mid-cap and small-cap stocks.",
                "Understand why market-cap categories are useful.",
                "Understand that size does not guarantee investment performance.",
            ],
            "explanation": (
                "Market-cap categories group companies according to their market "
                "capitalization. Large-cap companies are generally among the larger "
                "companies by market value, while mid-cap and small-cap companies "
                "are progressively smaller according to the applicable classification "
                "methodology. Category definitions can vary by market or regulatory "
                "framework."
            ),
            "example": (
                "Two companies may operate in the same industry but have very "
                "different market capitalizations. Investors can use market-cap "
                "categories as one way to organize and compare companies."
            ),
            "key_terms": [
                "Large Cap",
                "Mid Cap",
                "Small Cap",
                "Market Cap",
                "Classification",
            ],
            "takeaways": [
                "Market-cap categories describe company size by market value.",
                "Classification rules can vary.",
                "A larger company is not automatically a better investment.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 5,
        "title": "Equity & Ownership",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand equity ownership.",
                "Understand how shares represent ownership.",
                "Understand the relationship between ownership and shareholder rights.",
            ],
            "explanation": (
                "Equity represents an ownership interest in a company. Shares are "
                "units through which that ownership can be represented. Depending "
                "on the share class and applicable rules, shareholders may have "
                "rights such as voting rights and may receive dividends when "
                "declared. Ownership also exposes investors to the company's "
                "business and market risks."
            ),
            "example": (
                "If an investor owns shares representing a small percentage of a "
                "company's equity, that investor has an ownership interest in the "
                "company rather than simply lending money to it."
            ),
            "key_terms": [
                "Equity",
                "Ownership",
                "Shareholder",
                "Share Class",
                "Voting Rights",
            ],
            "takeaways": [
                "Equity represents ownership in a company.",
                "Shares are units of equity ownership.",
                "Shareholder rights depend on the shares owned and applicable rules.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 6,
        "title": "Dividends",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand what a dividend is.",
                "Understand why companies may pay dividends.",
                "Understand that dividends are not guaranteed.",
            ],
            "explanation": (
                "A dividend is a distribution of part of a company's profits or "
                "reserves to eligible shareholders when properly declared according "
                "to applicable rules. Companies may choose to retain earnings for "
                "growth instead of distributing them. Dividend payments and amounts "
                "are not guaranteed."
            ),
            "example": (
                "If a company declares a dividend of ₹5 per eligible share and an "
                "investor holds 100 eligible shares on the relevant record date, "
                "the investor may receive ₹500 before any applicable taxes or "
                "adjustments."
            ),
            "key_terms": [
                "Dividend",
                "Profit",
                "Retained Earnings",
                "Record Date",
                "Shareholder",
            ],
            "takeaways": [
                "Dividends are distributions to eligible shareholders.",
                "Companies can retain earnings instead of paying dividends.",
                "Dividend payments are not guaranteed.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 7,
        "title": "Bonus Shares",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand bonus shares.",
                "Understand why companies issue bonus shares.",
                "Understand the effect on the number of shares held.",
            ],
            "explanation": (
                "Bonus shares are additional shares issued to eligible existing "
                "shareholders without requiring them to pay an additional amount "
                "for those shares, subject to applicable rules. A bonus issue can "
                "increase the number of shares held by investors while the overall "
                "economic value of the investor's holding does not automatically "
                "increase merely because more shares were issued."
            ),
            "example": (
                "In a 1:1 bonus issue, an eligible shareholder holding 100 shares "
                "could receive 100 additional shares, resulting in 200 shares. "
                "The market price may adjust to reflect the increased number of "
                "shares."
            ),
            "key_terms": [
                "Bonus Shares",
                "Bonus Issue",
                "Existing Shareholder",
                "Record Date",
            ],
            "takeaways": [
                "Bonus shares are additional shares given to eligible shareholders.",
                "A bonus issue increases the number of shares outstanding.",
                "More shares do not automatically mean more total wealth.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 8,
        "title": "Stock Splits",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a stock split.",
                "Understand how the number of shares changes.",
                "Understand the basic effect on the per-share price.",
            ],
            "explanation": (
                "A stock split divides existing shares into a larger number of "
                "shares according to a specified ratio. The face value may also "
                "change depending on the structure of the split. In a simple split, "
                "the market price per share is adjusted proportionally, so the split "
                "by itself does not create additional economic value."
            ),
            "example": (
                "In a 1:2 split, one existing share may become two shares. If the "
                "pre-split market price were ₹1,000, the adjusted price could be "
                "approximately ₹500 per share, subject to market movements."
            ),
            "key_terms": [
                "Stock Split",
                "Split Ratio",
                "Face Value",
                "Market Price",
            ],
            "takeaways": [
                "A stock split increases the number of shares.",
                "The per-share price is generally adjusted proportionally.",
                "A split itself does not create economic value.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 9,
        "title": "Rights Issues",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a rights issue.",
                "Understand why companies use rights issues.",
                "Understand the concept of rights entitlement.",
            ],
            "explanation": (
                "A rights issue is an offer by a company to existing eligible "
                "shareholders to purchase additional shares, usually in a specified "
                "proportion and at terms announced by the company. The offer gives "
                "existing shareholders an opportunity to participate in the new "
                "issue, subject to the applicable rules and offer conditions."
            ),
            "example": (
                "Suppose a company announces a rights issue of 1 new share for "
                "every 5 existing shares. An eligible investor holding 500 shares "
                "may be entitled to subscribe for 100 additional shares, subject "
                "to the issue terms."
            ),
            "key_terms": [
                "Rights Issue",
                "Rights Entitlement",
                "Eligible Shareholder",
                "Subscription",
            ],
            "takeaways": [
                "Rights issues are offered to eligible existing shareholders.",
                "They can help companies raise additional equity capital.",
                "Investors should read the specific offer terms before deciding.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 10,
        "title": "Share Buybacks",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand a share buyback.",
                "Understand why companies buy back shares.",
                "Understand how buybacks can affect outstanding shares.",
            ],
            "explanation": (
                "A share buyback occurs when a company repurchases its own shares "
                "from eligible shareholders according to an approved mechanism "
                "and applicable regulations. A company may use buybacks for several "
                "reasons, including returning capital to shareholders or changing "
                "its capital structure."
            ),
            "example": (
                "If a company has 100 crore outstanding shares and successfully "
                "repurchases some shares and cancels them according to the applicable "
                "process, the number of outstanding shares can decrease."
            ),
            "key_terms": [
                "Buyback",
                "Repurchase",
                "Outstanding Shares",
                "Capital Structure",
            ],
            "takeaways": [
                "A buyback involves a company repurchasing its own shares.",
                "Buybacks can reduce the number of outstanding shares.",
                "The effect depends on the company's financial position and market conditions.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 11,
        "title": "Liquidity & Volatility",
        "level": "Beginner",
        "estimated_minutes": 20,
        "content": {
            "objectives": [
                "Understand liquidity.",
                "Understand volatility.",
                "Understand why both concepts matter to traders and investors.",
            ],
            "explanation": (
                "Liquidity describes how easily an asset can be bought or sold "
                "without causing a large price change. Volatility describes how "
                "much and how quickly the price of an asset fluctuates. High "
                "liquidity can make transactions easier, while high volatility "
                "can increase both potential opportunity and risk."
            ),
            "example": (
                "A heavily traded stock may have many buyers and sellers and can "
                "often be easier to trade. A stock with low trading activity may "
                "have fewer available orders, potentially causing larger price "
                "changes when a sizable order is placed."
            ),
            "key_terms": [
                "Liquidity",
                "Volatility",
                "Bid",
                "Ask",
                "Spread",
            ],
            "takeaways": [
                "Liquidity concerns how easily an asset can be traded.",
                "Volatility measures price fluctuations.",
                "Liquidity and volatility are important when evaluating trading risk.",
            ],
        },
    },
    {
        "module_order": 2,
        "lesson_order": 12,
        "title": "Trading Volume & Circuit Breakers",
        "level": "Beginner",
        "estimated_minutes": 25,
        "content": {
            "objectives": [
                "Understand trading volume.",
                "Understand why volume matters.",
                "Understand the purpose of circuit breakers and price limits.",
            ],
            "explanation": (
                "Trading volume represents the quantity of securities traded "
                "during a specified period. Volume can help traders understand "
                "the level of market activity. Circuit breakers and price limits "
                "are mechanisms designed to temporarily restrict trading or price "
                "movement under specified market conditions, helping markets deal "
                "with unusually rapid movements according to applicable exchange "
                "rules."
            ),
            "example": (
                "If a stock normally trades 1 lakh shares per day but suddenly "
                "trades 10 lakh shares, the unusual volume may indicate increased "
                "market activity. A price-limit or circuit mechanism may apply "
                "when specified thresholds are reached."
            ),
            "key_terms": [
                "Trading Volume",
                "Circuit Breaker",
                "Price Limit",
                "Market Activity",
                "Order Flow",
            ],
            "takeaways": [
                "Volume measures the amount of trading activity.",
                "Unusual volume can indicate increased market interest.",
                "Circuit mechanisms are designed to help manage extreme market movements.",
            ],
        },
    },
]


async def seed_module2():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 2}
        )

        if not module:
            raise RuntimeError(
                "Module 2 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]

        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
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

        print(f"Module 2 lessons inserted: {inserted}")
        print(f"Module 2 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module2())