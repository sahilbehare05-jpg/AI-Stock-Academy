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
        "title": "What Is Risk Management?",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the meaning of risk management.",
                "Learn why protecting capital is important.",
                "Understand that profitable outcomes are never guaranteed."
            ],
            "explanation": (
                "Risk management is the process of identifying, measuring and "
                "controlling potential losses. In trading education, risk management "
                "includes position sizing, predefined exit conditions, diversification, "
                "drawdown monitoring and understanding leverage. The objective is not "
                "to eliminate risk completely, because that is generally impossible, "
                "but to keep potential losses within a defined and manageable framework."
            ),
            "example": (
                "In a paper-trading account, a learner can define a maximum acceptable "
                "loss for each simulated position and record whether the strategy "
                "follows that rule consistently."
            ),
            "key_terms": [
                "Risk Management",
                "Capital",
                "Loss",
                "Position Size",
                "Drawdown"
            ],
            "takeaways": [
                "Risk cannot usually be eliminated completely.",
                "Risk management focuses on controlling potential losses.",
                "A trading strategy should include risk rules."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Risk vs Reward",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the relationship between risk and potential reward.",
                "Learn why higher potential returns can involve higher uncertainty.",
                "Understand why expected reward should not be considered without risk."
            ],
            "explanation": (
                "Risk and reward describe two sides of an investment or trading "
                "decision. Potential reward refers to a possible positive outcome, "
                "while risk refers to the possibility and magnitude of an unfavorable "
                "outcome. A larger potential return does not automatically make an "
                "opportunity better because uncertainty and probability also matter."
            ),
            "example": (
                "Two simulated strategies may have similar potential returns, but "
                "one may have much larger historical losses. Comparing both the "
                "possible gain and possible loss gives a more complete picture."
            ),
            "key_terms": [
                "Risk",
                "Reward",
                "Potential Return",
                "Loss",
                "Probability"
            ],
            "takeaways": [
                "Reward should always be considered together with risk.",
                "Higher potential return can involve greater uncertainty.",
                "A good analysis considers both upside and downside scenarios."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Risk-Reward Ratio",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the risk-reward ratio.",
                "Learn how to calculate a simple risk-reward ratio.",
                "Understand why the ratio alone does not determine strategy quality."
            ],
            "explanation": (
                "The risk-reward ratio compares the potential amount of loss with "
                "the potential amount of gain under a defined scenario. For example, "
                "if a simulated setup risks ₹10 and targets ₹20, the risk-reward "
                "relationship is 1:2. The ratio should be considered alongside "
                "probability, win rate, costs and actual historical performance."
            ),
            "example": (
                "A paper-trading setup has a predefined potential loss of ₹100 "
                "and a potential gain of ₹200. Its simplified risk-reward ratio "
                "is 1:2."
            ),
            "key_terms": [
                "Risk-Reward Ratio",
                "Potential Loss",
                "Potential Gain",
                "Target",
                "Probability"
            ],
            "takeaways": [
                "Risk-reward compares potential loss with potential gain.",
                "A higher reward-to-risk ratio does not guarantee success.",
                "Probability and historical evidence also matter."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Position Sizing",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand position sizing.",
                "Learn why the size of a position affects total portfolio risk.",
                "Understand the importance of predefined risk limits."
            ],
            "explanation": (
                "Position sizing determines how much capital or how many units are "
                "allocated to a particular position. A smaller position can reduce "
                "the effect of an unfavorable price movement on the overall portfolio. "
                "Position sizing should consider the chosen risk limit, volatility, "
                "portfolio size and the characteristics of the asset."
            ),
            "example": (
                "In a virtual portfolio, a learner can compare two identical "
                "simulated trades using different position sizes and observe how "
                "the same percentage price movement affects total portfolio value."
            ),
            "key_terms": [
                "Position Sizing",
                "Portfolio",
                "Allocation",
                "Risk Limit",
                "Volatility"
            ],
            "takeaways": [
                "Position size directly affects portfolio impact.",
                "The same price movement can produce different portfolio outcomes.",
                "Position sizing should be part of the strategy's risk rules."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Stop-Loss Concepts",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the purpose of a stop-loss.",
                "Learn how predefined exit levels can limit planned losses.",
                "Understand why stop-loss execution is not guaranteed at an exact price."
            ],
            "explanation": (
                "A stop-loss is a predefined condition intended to exit a position "
                "when the market moves against the original scenario. It can help "
                "make risk limits explicit. However, actual execution can differ "
                "from the chosen level because of gaps, volatility, liquidity and "
                "order mechanics. A stop-loss is therefore a risk-control tool, "
                "not a guarantee of a specific loss."
            ),
            "example": (
                "In a simulated trade, a learner defines an exit condition below "
                "an important support area and records what would happen if price "
                "reached that condition."
            ),
            "key_terms": [
                "Stop-Loss",
                "Exit",
                "Risk Limit",
                "Gap",
                "Execution"
            ],
            "takeaways": [
                "Stop-losses are designed to control planned downside.",
                "Execution can differ from an intended level.",
                "Stop-loss placement should be consistent with the strategy."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Take-Profit & Exit Planning",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand exit planning.",
                "Learn why exits should be defined before evaluating a trade.",
                "Understand partial exits and changing market conditions."
            ],
            "explanation": (
                "Exit planning defines the conditions under which a position would "
                "be closed according to a strategy. An exit can be based on a target, "
                "a change in market structure, a time limit, a trailing condition or "
                "another predefined rule. Changing an exit impulsively can alter the "
                "risk profile of the original strategy."
            ),
            "example": (
                "A simulated strategy may define both a maximum-loss condition and "
                "a target condition before a position is recorded. The learner then "
                "evaluates whether the rules were followed."
            ),
            "key_terms": [
                "Take-Profit",
                "Exit Plan",
                "Target",
                "Trailing Exit",
                "Time Exit"
            ],
            "takeaways": [
                "Exit rules should be defined as part of the strategy.",
                "Different exit methods serve different purposes.",
                "Changing rules emotionally can distort strategy evaluation."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Maximum Loss & Daily Loss Limits",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand maximum-loss limits.",
                "Learn why daily loss limits can control repeated exposure.",
                "Understand how limits can support disciplined decision-making."
            ],
            "explanation": (
                "A maximum-loss limit defines the largest acceptable loss for a "
                "specified position, strategy, session or portfolio under a chosen "
                "framework. A daily loss limit can prevent repeated decisions after "
                "a sequence of unfavorable outcomes. In a simulation, these limits "
                "can be tested to study how they affect overall performance."
            ),
            "example": (
                "A virtual trading system may stop recording new simulated trades "
                "after a predefined daily loss threshold is reached. The learner "
                "can then study the effect of this rule on historical results."
            ),
            "key_terms": [
                "Maximum Loss",
                "Daily Loss Limit",
                "Risk Limit",
                "Exposure",
                "Discipline"
            ],
            "takeaways": [
                "Loss limits define boundaries for downside.",
                "Daily limits can reduce repeated exposure after losses.",
                "Limits should be tested and documented rather than changed impulsively."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Portfolio Diversification",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand diversification.",
                "Learn how spreading exposure can reduce concentration risk.",
                "Understand the limitations of diversification."
            ],
            "explanation": (
                "Diversification involves spreading exposure across different assets, "
                "sectors, regions or other categories. The purpose is to reduce the "
                "impact of a single source of risk on the overall portfolio. Diversification "
                "does not eliminate market-wide losses, and holding many assets that "
                "behave similarly may provide less diversification than expected."
            ),
            "example": (
                "A portfolio containing companies from several unrelated sectors "
                "may have less company-specific concentration than a portfolio "
                "containing only companies from one sector."
            ),
            "key_terms": [
                "Diversification",
                "Concentration",
                "Portfolio",
                "Sector",
                "Systematic Risk"
            ],
            "takeaways": [
                "Diversification can reduce concentration risk.",
                "Diversification does not eliminate overall market risk.",
                "Assets that move similarly may not provide much diversification."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Correlation & Concentration Risk",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand correlation between assets.",
                "Learn how hidden concentration can occur.",
                "Understand why counting the number of holdings is not enough."
            ],
            "explanation": (
                "Correlation describes how two variables have historically moved "
                "relative to each other. If several portfolio holdings are strongly "
                "exposed to the same economic factor, they may decline together. "
                "This creates concentration risk even when the portfolio contains "
                "many individual securities."
            ),
            "example": (
                "A learner may hold ten different companies, but if all ten depend "
                "heavily on the same industry cycle, the portfolio can still have "
                "significant sector concentration."
            ),
            "key_terms": [
                "Correlation",
                "Concentration Risk",
                "Portfolio",
                "Sector Exposure",
                "Diversification"
            ],
            "takeaways": [
                "The number of holdings alone does not measure diversification.",
                "Highly related assets can create hidden concentration.",
                "Correlation should be studied using historical data and context."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Leverage & Margin Risk",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand leverage.",
                "Understand why leverage magnifies both gains and losses.",
                "Learn why margin creates additional financial obligations."
            ],
            "explanation": (
                "Leverage allows exposure to an asset that is larger than the amount "
                "of capital directly allocated, depending on the financial product "
                "and rules involved. Because gains and losses are calculated on the "
                "larger exposure, leverage can magnify both outcomes. Margin arrangements "
                "can also involve additional requirements and forced position closure "
                "under certain conditions."
            ),
            "example": (
                "If a simulated position has exposure of ₹1,00,000 supported by "
                "₹25,000 of capital, a 5% move in the exposure corresponds to "
                "₹5,000 before costs and other effects. This illustrates why "
                "leverage increases sensitivity to price movements."
            ),
            "key_terms": [
                "Leverage",
                "Margin",
                "Exposure",
                "Collateral",
                "Margin Call"
            ],
            "takeaways": [
                "Leverage increases exposure relative to allocated capital.",
                "It magnifies both positive and negative outcomes.",
                "Margin arrangements introduce additional obligations and risks."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Gap & Overnight Risk",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand gap risk.",
                "Learn why prices can move significantly between trading sessions.",
                "Understand why predefined exits may not eliminate overnight risk."
            ],
            "explanation": (
                "Gap risk occurs when an asset opens at a substantially different "
                "price from its previous close. News, corporate announcements, "
                "global markets and unexpected events can contribute to gaps. "
                "A planned exit level may not be executed at exactly that price "
                "if the market opens beyond it."
            ),
            "example": (
                "If a simulated stock closes at ₹500 and opens the next session "
                "at ₹470 because of new information, the price has gapped lower. "
                "A risk model must account for this possibility."
            ),
            "key_terms": [
                "Gap Risk",
                "Overnight Risk",
                "Opening Price",
                "News Event",
                "Slippage"
            ],
            "takeaways": [
                "Prices can change substantially while a market is closed.",
                "Overnight positions have exposure to unexpected information.",
                "Exit levels do not guarantee exact execution prices."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Drawdown",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand drawdown.",
                "Learn how maximum drawdown is measured.",
                "Understand why recovery from losses becomes progressively harder."
            ],
            "explanation": (
                "Drawdown measures the decline in portfolio value from a previous "
                "peak to a subsequent low before a new peak is reached. Maximum "
                "drawdown is the largest such decline during a selected period. "
                "Drawdown is important because a strategy can have positive long-term "
                "returns while still experiencing significant temporary losses."
            ),
            "example": (
                "If a simulated portfolio rises from ₹1,00,000 to ₹1,20,000 and "
                "later falls to ₹90,000 before recovering, the decline from the "
                "₹1,20,000 peak to ₹90,000 is a ₹30,000 drawdown."
            ),
            "key_terms": [
                "Drawdown",
                "Maximum Drawdown",
                "Peak",
                "Recovery",
                "Portfolio Value"
            ],
            "takeaways": [
                "Drawdown measures decline from a previous portfolio peak.",
                "Maximum drawdown is an important risk metric.",
                "Large losses require disproportionately larger gains to recover."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Risk of Ruin",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the concept of risk of ruin.",
                "Learn how repeated losses can threaten a trading system.",
                "Understand why controlling per-trade risk matters."
            ],
            "explanation": (
                "Risk of ruin refers to the possibility that a sequence of losses "
                "could reduce available capital to a level where continuing the "
                "strategy becomes impractical. The probability depends on factors "
                "such as position size, win probability, payoff distribution and "
                "available capital. Keeping risk per simulated position controlled "
                "can reduce the impact of losing streaks."
            ),
            "example": (
                "Two simulated strategies have identical win rates, but one uses "
                "much larger position sizes. A long losing streak will generally "
                "have a much larger effect on the highly leveraged or aggressively "
                "sized strategy."
            ),
            "key_terms": [
                "Risk of Ruin",
                "Losing Streak",
                "Capital",
                "Position Size",
                "Probability"
            ],
            "takeaways": [
                "Repeated losses can seriously damage a strategy's capital base.",
                "Position sizing affects the severity of losing streaks.",
                "Risk of ruin should be considered when evaluating a strategy."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Building a Complete Risk Management Plan",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine risk-management concepts into one framework.",
                "Build a structured risk plan for simulated trading.",
                "Learn how to review and improve risk controls using evidence."
            ],
            "explanation": (
                "A complete risk-management plan defines maximum exposure, position "
                "sizing rules, loss limits, exit conditions, diversification principles, "
                "drawdown thresholds and procedures for reviewing performance. The "
                "plan should be written before evaluating results and should be tested "
                "using historical data or virtual trading. Risk controls should be "
                "appropriate to the strategy and reviewed when market conditions or "
                "the strategy itself changes."
            ),
            "example": (
                "A virtual trading plan can specify a maximum portfolio exposure, "
                "a predefined simulated loss limit per position, a maximum drawdown "
                "threshold, diversification rules and a review process after a "
                "series of simulated trades."
            ),
            "key_terms": [
                "Risk Management Plan",
                "Position Sizing",
                "Exposure",
                "Drawdown",
                "Diversification",
                "Risk Limit"
            ],
            "takeaways": [
                "Risk management should be integrated into the complete strategy.",
                "Position size, exposure and drawdown should be monitored together.",
                "Simulation can help learners test risk controls before making real-world decisions.",
                "No risk-management plan can guarantee that losses will not occur."
            ],
        },
    },
]


async def seed_module9():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 9}
        )

        if not module:
            raise RuntimeError(
                "Module 9 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 9,
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

        print(f"Module 9 lessons inserted: {inserted}")
        print(f"Module 9 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module9())