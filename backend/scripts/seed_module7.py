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
        "title": "Introduction to Fundamental Analysis",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the purpose of fundamental analysis.",
                "Learn how business performance can be studied before evaluating a stock.",
                "Understand the difference between company quality and stock price."
            ],
            "explanation": (
                "Fundamental analysis evaluates a company using its business model, "
                "financial statements, profitability, growth, competitive position, "
                "industry conditions, management and valuation. The purpose is to "
                "understand the underlying business and compare its estimated value "
                "with the market price. A strong business is not automatically a "
                "good investment at every price."
            ),
            "example": (
                "Two companies may have similar revenue, but one may generate stronger "
                "profits, carry less debt and have better cash flow. Fundamental analysis "
                "helps a learner compare these differences."
            ),
            "key_terms": [
                "Fundamental Analysis",
                "Business Model",
                "Financial Statements",
                "Valuation",
                "Intrinsic Value"
            ],
            "takeaways": [
                "Fundamental analysis studies the underlying business.",
                "Financial performance and business quality are important factors.",
                "Company quality and stock valuation are separate questions."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Understanding Business Models",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand what a business model is.",
                "Identify how a company generates revenue.",
                "Learn why business-model analysis matters."
            ],
            "explanation": (
                "A business model explains how a company creates value and earns "
                "revenue. Analysis can include products or services, customers, "
                "pricing, distribution, costs and competitive advantages. Understanding "
                "the business model helps investors interpret financial numbers in context."
            ),
            "example": (
                "A software company may earn recurring subscription revenue, while "
                "a retailer may generate revenue mainly by selling physical products. "
                "Their financial statements should therefore be interpreted differently."
            ),
            "key_terms": [
                "Business Model",
                "Revenue",
                "Customer",
                "Pricing",
                "Recurring Revenue"
            ],
            "takeaways": [
                "Every company has a mechanism for creating and capturing value.",
                "Revenue sources should be understood before analyzing financial ratios.",
                "Different industries have different business models."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Income Statement",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the purpose of an income statement.",
                "Learn revenue, expenses and profit.",
                "Understand how profitability changes over time."
            ],
            "explanation": (
                "The income statement summarizes a company's financial performance "
                "over a specified period. Important items can include revenue, operating "
                "expenses, operating profit, interest, taxes and net profit. Comparing "
                "these figures across multiple periods can help identify growth and "
                "changes in profitability."
            ),
            "example": (
                "If a company reports ₹100 crore of revenue and ₹80 crore of total "
                "expenses before applicable taxes and other items, the remaining "
                "amount contributes to its profit according to the accounting structure."
            ),
            "key_terms": [
                "Income Statement",
                "Revenue",
                "Expenses",
                "Operating Profit",
                "Net Profit"
            ],
            "takeaways": [
                "The income statement shows performance over a period.",
                "Revenue alone does not tell us whether a company is profitable.",
                "Profitability should be studied across multiple periods."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Balance Sheet",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the balance sheet.",
                "Learn assets, liabilities and equity.",
                "Understand why financial position matters."
            ],
            "explanation": (
                "A balance sheet presents a company's financial position at a "
                "specific date. Assets represent resources controlled by the company, "
                "liabilities represent obligations, and shareholders' equity represents "
                "the residual interest. The basic accounting relationship is Assets = "
                "Liabilities + Equity."
            ),
            "example": (
                "If a company has ₹500 crore in assets and ₹300 crore in liabilities, "
                "the accounting equity would be ₹200 crore."
            ),
            "key_terms": [
                "Balance Sheet",
                "Assets",
                "Liabilities",
                "Equity",
                "Financial Position"
            ],
            "takeaways": [
                "The balance sheet describes financial position at a point in time.",
                "Assets and liabilities are important for understanding financial strength.",
                "The accounting equation is Assets = Liabilities + Equity."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Cash Flow Statement",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the cash flow statement.",
                "Learn operating, investing and financing cash flows.",
                "Understand why profit and cash flow can differ."
            ],
            "explanation": (
                "The cash flow statement explains how cash and cash equivalents "
                "changed during a period. It is commonly divided into operating, "
                "investing and financing activities. A company can report accounting "
                "profit while generating weaker cash flow because accounting recognition "
                "and actual cash movements do not always occur at the same time."
            ),
            "example": (
                "A company may record a sale as revenue while the customer has not "
                "yet paid. The company can therefore show accounting profit while "
                "receiving less cash during that period."
            ),
            "key_terms": [
                "Cash Flow",
                "Operating Cash Flow",
                "Investing Cash Flow",
                "Financing Cash Flow",
                "Cash Equivalents"
            ],
            "takeaways": [
                "Cash flow tracks actual movements of cash and cash equivalents.",
                "Operating cash flow is especially important when evaluating business operations.",
                "Profit and cash generation should be analyzed together."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Revenue Growth",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand revenue growth.",
                "Learn year-over-year and sequential comparisons.",
                "Understand why revenue quality matters."
            ],
            "explanation": (
                "Revenue growth measures how a company's sales or operating revenue "
                "changes over time. Analysts may compare revenue year over year or "
                "between consecutive quarters. Growth should be evaluated together "
                "with margins, cash flow, competition and the reasons behind the growth."
            ),
            "example": (
                "If revenue increases from ₹1,000 crore to ₹1,200 crore, revenue "
                "has increased by 20% over the comparison period."
            ),
            "key_terms": [
                "Revenue Growth",
                "Year-over-Year",
                "Quarter-over-Quarter",
                "Sales",
                "Growth Rate"
            ],
            "takeaways": [
                "Revenue growth measures changes in sales over time.",
                "Growth should be compared with profitability and cash flow.",
                "High growth is not automatically valuable if it is achieved inefficiently."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Profit & Profit Margins",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand different measures of profit.",
                "Learn gross, operating and net margins.",
                "Understand how margins help compare profitability."
            ],
            "explanation": (
                "Profit margins express a company's profit as a percentage of revenue. "
                "Gross margin focuses on revenue after direct costs, operating margin "
                "considers operating expenses, and net margin considers the profit "
                "remaining after relevant expenses and taxes. Margin trends can reveal "
                "whether a business is becoming more or less efficient."
            ),
            "example": (
                "If a company generates ₹100 crore in revenue and ₹15 crore in net "
                "profit, its net profit margin is 15%."
            ),
            "key_terms": [
                "Gross Margin",
                "Operating Margin",
                "Net Margin",
                "Profitability",
                "Efficiency"
            ],
            "takeaways": [
                "Margins show profit relative to revenue.",
                "Different margins answer different analytical questions.",
                "Margin trends can be more informative than a single year's margin."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Earnings Per Share (EPS)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand earnings per share.",
                "Learn why EPS is used in stock analysis.",
                "Understand how changes in share count can affect EPS."
            ],
            "explanation": (
                "Earnings per share, or EPS, represents earnings attributable to "
                "ordinary shareholders divided by the relevant number of shares "
                "under the applicable accounting calculation. EPS helps relate "
                "company earnings to each share, although analysts should also "
                "consider share dilution and the quality of earnings."
            ),
            "example": (
                "If earnings attributable to shareholders are ₹100 crore and the "
                "relevant share count is 10 crore shares, the simplified EPS is ₹10 per share."
            ),
            "key_terms": [
                "EPS",
                "Earnings Per Share",
                "Earnings",
                "Shares Outstanding",
                "Dilution"
            ],
            "takeaways": [
                "EPS relates earnings to shares.",
                "EPS can change because of earnings changes or share-count changes.",
                "EPS should be analyzed alongside other financial measures."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Return on Equity (ROE)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand ROE.",
                "Learn how ROE relates profit to shareholders' equity.",
                "Understand why ROE should be interpreted with debt and business structure."
            ],
            "explanation": (
                "Return on Equity, or ROE, measures profitability relative to "
                "shareholders' equity. A simplified calculation divides net income "
                "by average shareholders' equity. A higher ROE can indicate efficient "
                "use of equity, but high leverage can also increase ROE, so the ratio "
                "should not be evaluated in isolation."
            ),
            "example": (
                "If annual net income is ₹20 crore and average shareholders' equity "
                "is ₹100 crore, the simplified ROE is 20%."
            ),
            "key_terms": [
                "ROE",
                "Return on Equity",
                "Net Income",
                "Shareholders' Equity",
                "Leverage"
            ],
            "takeaways": [
                "ROE measures profit generated relative to equity.",
                "High ROE can result partly from financial leverage.",
                "ROE should be compared with industry peers and historical levels."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Return on Capital Employed (ROCE)",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand ROCE.",
                "Learn why capital efficiency matters.",
                "Compare ROCE with the company's cost of capital conceptually."
            ],
            "explanation": (
                "Return on Capital Employed, or ROCE, evaluates operating profitability "
                "relative to the capital employed in a business. The exact formula can "
                "vary depending on the analytical convention, but the general purpose "
                "is to assess how effectively a company generates operating returns "
                "from the capital used in its operations."
            ),
            "example": (
                "If a business generates ₹30 crore of relevant operating profit on "
                "₹150 crore of capital employed under a chosen ROCE methodology, "
                "the resulting ROCE would be 20%."
            ),
            "key_terms": [
                "ROCE",
                "Capital Employed",
                "Operating Profit",
                "Capital Efficiency",
                "Return"
            ],
            "takeaways": [
                "ROCE studies returns generated from capital employed.",
                "Capital efficiency is important when comparing businesses.",
                "Formula definitions should be kept consistent when comparing companies."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Debt & Leverage",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand company debt.",
                "Learn the meaning of leverage.",
                "Understand why excessive debt can increase financial risk."
            ],
            "explanation": (
                "Debt allows a company to finance assets and operations using borrowed "
                "capital. Leverage refers to the use of debt or other fixed financial "
                "commitments to finance a business. Debt can support growth when used "
                "effectively, but high debt can increase interest obligations and "
                "financial risk, especially when cash flows weaken."
            ),
            "example": (
                "A company that borrows ₹500 crore must meet its contractual debt "
                "obligations regardless of whether its sales are temporarily strong "
                "or weak. Analysts therefore examine debt alongside cash flow and profitability."
            ),
            "key_terms": [
                "Debt",
                "Leverage",
                "Interest",
                "Borrowing",
                "Financial Risk"
            ],
            "takeaways": [
                "Debt can help finance growth but creates obligations.",
                "High leverage can increase financial risk.",
                "Debt should be evaluated relative to cash flow and business stability."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Debt-to-Equity Ratio",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the debt-to-equity ratio.",
                "Learn how it measures financial leverage.",
                "Understand why acceptable leverage varies by industry."
            ],
            "explanation": (
                "The debt-to-equity ratio compares a company's debt with shareholders' "
                "equity. It is commonly used to evaluate financial leverage. A higher "
                "ratio can indicate greater reliance on debt, although the appropriate "
                "level depends heavily on the company's industry, business model, "
                "cash flows and accounting definitions."
            ),
            "example": (
                "If a company has ₹200 crore of relevant debt and ₹100 crore of "
                "shareholders' equity, the simplified debt-to-equity ratio is 2.0."
            ),
            "key_terms": [
                "Debt-to-Equity",
                "Leverage",
                "Debt",
                "Equity",
                "Capital Structure"
            ],
            "takeaways": [
                "Debt-to-equity measures debt relative to equity.",
                "Higher leverage can increase financial risk.",
                "Compare the ratio with appropriate industry peers."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Price-to-Earnings (P/E) Ratio",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the P/E ratio.",
                "Learn how market price relates to earnings per share.",
                "Understand why P/E must be compared with context."
            ],
            "explanation": (
                "The price-to-earnings ratio compares a company's share price with "
                "its earnings per share. It is widely used as a valuation measure. "
                "A high P/E can reflect strong growth expectations, high quality or "
                "other factors, while a low P/E can reflect lower expectations or "
                "higher perceived risk. P/E alone cannot determine whether a stock is cheap or expensive."
            ),
            "example": (
                "If a stock trades at ₹1,000 and its relevant EPS is ₹50, the "
                "simplified P/E ratio is 20."
            ),
            "key_terms": [
                "P/E Ratio",
                "Price-to-Earnings",
                "EPS",
                "Valuation",
                "Earnings Multiple"
            ],
            "takeaways": [
                "P/E compares price with earnings per share.",
                "P/E is most useful when compared with history, peers and growth expectations.",
                "A low P/E is not automatically undervalued."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Price-to-Book (P/B) Ratio",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the price-to-book ratio.",
                "Learn how market price relates to book value.",
                "Understand why P/B can be particularly useful in some industries."
            ],
            "explanation": (
                "The price-to-book ratio compares a company's market value per share "
                "with its book value per share. It can be useful when analyzing businesses "
                "where balance-sheet assets and equity are particularly meaningful, "
                "such as certain financial institutions. Accounting book value does not "
                "necessarily equal the economic value of a company."
            ),
            "example": (
                "If a company's share price is ₹400 and its book value per share is "
                "₹200, the simplified P/B ratio is 2."
            ),
            "key_terms": [
                "P/B Ratio",
                "Price-to-Book",
                "Book Value",
                "Equity",
                "Valuation"
            ],
            "takeaways": [
                "P/B compares market price with book value.",
                "It can be useful for specific types of businesses.",
                "Book value should be interpreted with asset quality and business economics."
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Price-to-Sales (P/S) Ratio",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the price-to-sales ratio.",
                "Learn why revenue can be used in valuation.",
                "Understand the limitation of valuing a company without considering profitability."
            ],
            "explanation": (
                "The price-to-sales ratio compares a company's market value with "
                "its revenue. It can be useful for companies with low or temporarily "
                "negative earnings where P/E is less informative. However, two companies "
                "with the same revenue can have very different margins and cash flows, "
                "so P/S should not be used alone."
            ),
            "example": (
                "If a company has a market capitalization of ₹1,000 crore and annual "
                "revenue of ₹200 crore, the simplified price-to-sales ratio is 5."
            ),
            "key_terms": [
                "P/S Ratio",
                "Price-to-Sales",
                "Revenue",
                "Market Capitalization",
                "Valuation"
            ],
            "takeaways": [
                "P/S compares market value with revenue.",
                "It can be useful when earnings are temporarily weak or negative.",
                "Revenue quality and margins must also be considered."
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Free Cash Flow",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand free cash flow.",
                "Learn the relationship between operating cash flow and capital expenditure.",
                "Understand why sustainable cash generation matters."
            ],
            "explanation": (
                "Free cash flow is commonly described as the cash generated by "
                "operations after necessary capital expenditures, although exact "
                "definitions vary. It can indicate how much cash a business has "
                "available for activities such as debt reduction, dividends, buybacks "
                "or reinvestment after maintaining or expanding its asset base."
            ),
            "example": (
                "If operating cash flow is ₹100 crore and capital expenditure is "
                "₹40 crore under a chosen definition, simplified free cash flow "
                "would be ₹60 crore."
            ),
            "key_terms": [
                "Free Cash Flow",
                "Operating Cash Flow",
                "Capital Expenditure",
                "CapEx",
                "Cash Generation"
            ],
            "takeaways": [
                "Free cash flow focuses on cash remaining after relevant capital spending.",
                "Strong sustainable cash generation can support financial flexibility.",
                "Always check the definition used when comparing FCF across sources."
            ],
        },
    },
    {
        "lesson_order": 17,
        "title": "Dividends & Dividend Yield",
        "level": "Intermediate",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand dividends.",
                "Understand dividend yield.",
                "Learn why dividend sustainability matters more than yield alone."
            ],
            "explanation": (
                "A dividend is a distribution of part of a company's earnings or "
                "available resources to shareholders, subject to the company's "
                "financial position and applicable rules. Dividend yield relates "
                "the annual dividend per share to the share price. A high yield "
                "can result from a genuinely strong dividend or from a falling share "
                "price, so sustainability and payout capacity must be examined."
            ),
            "example": (
                "If a company pays ₹20 per share annually and the share price is "
                "₹500, the simplified dividend yield is 4%."
            ),
            "key_terms": [
                "Dividend",
                "Dividend Yield",
                "Payout",
                "Dividend Policy",
                "Sustainability"
            ],
            "takeaways": [
                "Dividends provide a distribution to shareholders.",
                "Dividend yield changes when the share price changes.",
                "Dividend sustainability should be studied along with cash flow and earnings."
            ],
        },
    },
    {
        "lesson_order": 18,
        "title": "Competitive Advantage & Moats",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand competitive advantage.",
                "Learn the concept of an economic moat.",
                "Identify common sources of sustainable competitive advantage."
            ],
            "explanation": (
                "A competitive advantage allows a company to perform better than "
                "competitors for a meaningful period. An economic moat is a commonly "
                "used concept describing a durable competitive advantage. Possible "
                "sources include strong brands, network effects, switching costs, "
                "cost advantages, intellectual property and efficient scale."
            ),
            "example": (
                "A platform with a large network of users may become more valuable "
                "as additional users join, making it harder for smaller competitors "
                "to attract the same network."
            ),
            "key_terms": [
                "Competitive Advantage",
                "Economic Moat",
                "Brand",
                "Network Effect",
                "Switching Cost"
            ],
            "takeaways": [
                "Competitive advantages can support long-term profitability.",
                "Moats can come from several different sources.",
                "A moat should be tested against actual financial and competitive evidence."
            ],
        },
    },
    {
        "lesson_order": 19,
        "title": "Industry & Sector Analysis",
        "level": "Intermediate",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand industry analysis.",
                "Learn why companies should be compared with appropriate peers.",
                "Understand the impact of industry cycles and regulation."
            ],
            "explanation": (
                "A company does not operate in isolation. Industry analysis examines "
                "market size, competition, regulation, customer behavior, technology, "
                "cyclicality and long-term growth drivers. Financial ratios should "
                "often be compared with companies operating in similar industries "
                "because normal margins, leverage and valuations can differ significantly."
            ),
            "example": (
                "A capital-intensive manufacturing company may naturally have different "
                "debt levels and margins from a software company. Comparing them directly "
                "without industry context can produce misleading conclusions."
            ),
            "key_terms": [
                "Industry Analysis",
                "Sector",
                "Competition",
                "Cyclicality",
                "Regulation",
                "Peer Comparison"
            ],
            "takeaways": [
                "Industry context is essential for interpreting financial metrics.",
                "Peer comparisons should use genuinely comparable businesses.",
                "Industry cycles can significantly affect company performance."
            ],
        },
    },
    {
        "lesson_order": 20,
        "title": "Complete Fundamental Stock Analysis",
        "level": "Intermediate",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine fundamental-analysis concepts into a structured process.",
                "Learn how to evaluate business quality, financial health and valuation.",
                "Develop a repeatable stock-analysis framework."
            ],
            "explanation": (
                "A complete fundamental analysis can begin with understanding the "
                "business model and industry, followed by analysis of revenue growth, "
                "profitability, balance-sheet strength, debt, cash flow, returns on "
                "capital and competitive advantages. The final stage is valuation, "
                "where measures such as P/E, P/B, P/S, cash-flow methods or other "
                "appropriate approaches can be considered. The goal is to form a "
                "well-supported view while recognizing uncertainty."
            ),
            "example": (
                "A learner analyzing a company can first understand how it makes money, "
                "then study several years of financial statements, compare margins and "
                "returns with peers, evaluate debt and cash flow, identify competitive "
                "advantages and finally examine whether the current market valuation "
                "is reasonable relative to the company's prospects."
            ),
            "key_terms": [
                "Fundamental Analysis",
                "Financial Statements",
                "Valuation",
                "Competitive Advantage",
                "Cash Flow",
                "Peer Comparison"
            ],
            "takeaways": [
                "Analyze the business before focusing only on the stock price.",
                "Use multiple financial measures rather than one ratio.",
                "A good company can still be overpriced, so valuation matters.",
                "A strong analysis should identify assumptions and risks."
            ],
        },
    },
]


async def seed_module7():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 7}
        )

        if not module:
            raise RuntimeError(
                "Module 7 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 7,
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

        print(f"Module 7 lessons inserted: {inserted}")
        print(f"Module 7 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module7())