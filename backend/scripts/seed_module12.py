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
        "title": "What Are Derivatives?",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand what a derivative is.",
                "Learn the basic purpose of derivative contracts.",
                "Understand that derivatives can involve substantial risk."
            ],
            "explanation": (
                "A derivative is a financial contract whose value is linked to an "
                "underlying asset, index, rate or other reference. Common derivatives "
                "include futures and options. Their value changes according to the "
                "underlying reference. Derivatives are used for purposes such as "
                "hedging, risk management and speculation, but they can also involve "
                "significant losses, especially when leverage is involved."
            ),
            "example": (
                "A futures contract may derive its value from an equity index. "
                "If the index changes, the value of the futures contract can also change."
            ),
            "key_terms": [
                "Derivative",
                "Underlying Asset",
                "Futures",
                "Options",
                "Leverage"
            ],
            "takeaways": [
                "Derivatives derive their value from an underlying reference.",
                "Futures and options are common derivative instruments.",
                "Derivatives can increase financial risk and require careful understanding."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Futures Contracts",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand futures contracts.",
                "Learn the basic structure of a futures agreement.",
                "Understand why futures can create leveraged exposure."
            ],
            "explanation": (
                "A futures contract is a standardized agreement to buy or sell an "
                "underlying asset or reference at a specified price according to "
                "contract terms. Futures are commonly traded on organized exchanges "
                "and are subject to margin requirements. Because only part of the "
                "contract value may be required as margin, price movements can have "
                "a relatively large effect on the capital committed."
            ),
            "example": (
                "An index futures contract represents exposure to an index according "
                "to its contract specifications. A change in the index changes the "
                "value of the futures position."
            ),
            "key_terms": [
                "Futures Contract",
                "Underlying",
                "Contract Size",
                "Margin",
                "Expiry"
            ],
            "takeaways": [
                "Futures are standardized derivative contracts.",
                "Futures have defined contract specifications and expiry terms.",
                "Margin can create leveraged exposure."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Futures Pricing",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand the factors affecting futures prices.",
                "Learn the relationship between spot and futures prices.",
                "Understand basis."
            ],
            "explanation": (
                "A futures price is related to the current spot price of the underlying "
                "and factors such as financing costs, expected income or distributions, "
                "time to expiry and market conditions. The difference between the spot "
                "price and futures price is commonly described as the basis. The exact "
                "relationship depends on the underlying asset and contract."
            ),
            "example": (
                "If an index has a spot value of 20,000 and its futures contract trades "
                "at 20,100, the difference between the two prices represents the current "
                "basis under that simple comparison."
            ),
            "key_terms": [
                "Futures Price",
                "Spot Price",
                "Basis",
                "Cost of Carry",
                "Expiry"
            ],
            "takeaways": [
                "Futures prices are connected to spot prices.",
                "Financing and income-related factors can affect futures pricing.",
                "The relationship between spot and futures changes as expiry approaches."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Futures Margin",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand futures margin.",
                "Learn the difference between margin and the full contract value.",
                "Understand why margin creates leverage."
            ],
            "explanation": (
                "Futures margin is collateral required to support a futures position. "
                "It is not simply a partial payment for owning the underlying asset. "
                "Exchanges and clearing systems establish margin requirements to help "
                "manage counterparty and market risk. Because the margin may be smaller "
                "than the total contract exposure, gains and losses can be large relative "
                "to the deposited amount."
            ),
            "example": (
                "If a simulated futures contract has exposure of ₹5,00,000 and the "
                "required margin is ₹1,00,000, the position has exposure five times "
                "the margin amount."
            ),
            "key_terms": [
                "Margin",
                "Initial Margin",
                "Maintenance Margin",
                "Collateral",
                "Leverage"
            ],
            "takeaways": [
                "Margin acts as collateral for futures positions.",
                "Margin is not the same as owning the underlying asset.",
                "Large exposure relative to margin increases risk."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Options Basics",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand options contracts.",
                "Learn the basic difference between calls and puts.",
                "Understand the concept of option premium."
            ],
            "explanation": (
                "An option is a derivative contract that gives the buyer a right, "
                "but generally not an obligation, to buy or sell an underlying "
                "according to specified terms. A call gives the holder the right "
                "to buy, while a put gives the holder the right to sell. The buyer "
                "pays a premium for this contractual right."
            ),
            "example": (
                "A call option on a stock gives its buyer a contractual right to "
                "buy the stock at a specified strike price before or at expiry, "
                "depending on the option style."
            ),
            "key_terms": [
                "Option",
                "Call",
                "Put",
                "Premium",
                "Strike Price"
            ],
            "takeaways": [
                "Options give the buyer a defined contractual right.",
                "Calls relate to buying and puts relate to selling.",
                "The buyer pays an option premium."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Call Options",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand call options.",
                "Learn the relationship between strike price and underlying price.",
                "Understand the buyer's maximum premium loss concept."
            ],
            "explanation": (
                "A call option gives the holder the right to buy the underlying at "
                "the strike price under the contract terms. A call buyer pays a premium "
                "and may benefit if the underlying rises sufficiently relative to the "
                "strike and premium. For a standard long call, the premium paid is the "
                "maximum loss for the buyer at expiry, excluding transaction costs."
            ),
            "example": (
                "A simulated call has a strike price of ₹1,000 and a premium of ₹40. "
                "The buyer pays ₹40 per unit of option exposure. The option's value "
                "depends on the underlying price, time and other factors."
            ),
            "key_terms": [
                "Call Option",
                "Strike Price",
                "Premium",
                "Underlying",
                "Expiry"
            ],
            "takeaways": [
                "Call options provide a right to buy under specified terms.",
                "The premium is paid by the option buyer.",
                "A long call buyer can lose the premium paid if the option expires worthless."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Put Options",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand put options.",
                "Learn the relationship between strike price and underlying price.",
                "Understand how puts can be used for risk-management concepts."
            ],
            "explanation": (
                "A put option gives the holder the right to sell the underlying at "
                "the strike price according to the contract terms. A put can gain "
                "value when the underlying declines sufficiently relative to the "
                "strike and premium. Put options can also be used in hedging frameworks."
            ),
            "example": (
                "A simulated put has a strike price of ₹1,000 and a premium of ₹35. "
                "If the underlying declines substantially, the option's intrinsic "
                "value can increase, although the overall result also depends on "
                "the premium paid and expiry."
            ),
            "key_terms": [
                "Put Option",
                "Strike Price",
                "Premium",
                "Hedging",
                "Expiry"
            ],
            "takeaways": [
                "Put options provide a right to sell under specified terms.",
                "Puts can gain value when the underlying declines.",
                "Puts can be part of a risk-management or hedging framework."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Strike Price & Expiry",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand strike price.",
                "Understand option expiry.",
                "Learn why time remaining affects option value."
            ],
            "explanation": (
                "The strike price is the specified price at which an option's holder "
                "has the contractual right to buy or sell the underlying, depending "
                "on whether it is a call or put. Expiry is the date or time when the "
                "option contract ends according to its terms. As expiry approaches, "
                "the amount of time available for favorable price movement decreases."
            ),
            "example": (
                "Two otherwise similar call options have strikes of ₹900 and ₹1,000. "
                "Their values can differ because the strikes have different relationships "
                "to the current underlying price."
            ),
            "key_terms": [
                "Strike Price",
                "Expiry",
                "Option Contract",
                "Time to Expiry",
                "Underlying"
            ],
            "takeaways": [
                "Strike price defines an important contractual price.",
                "Every option has defined expiry terms.",
                "Time remaining is an important component of option value."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Intrinsic & Time Value",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand intrinsic value.",
                "Understand time value.",
                "Learn how option premium relates to these components."
            ],
            "explanation": (
                "Option premium can be viewed conceptually as intrinsic value plus "
                "time value. Intrinsic value represents the amount an option would "
                "have if exercised immediately under simplified assumptions. Time "
                "value reflects the possibility that the option may become more "
                "valuable before expiry. Time value generally decreases as expiry "
                "approaches, all else equal."
            ),
            "example": (
                "A call with a strike of ₹1,000 and underlying price of ₹1,080 has "
                "₹80 of intrinsic value under the standard simplified calculation. "
                "If the option trades for ₹110, the remaining ₹30 represents its "
                "time value under that simplified model."
            ),
            "key_terms": [
                "Intrinsic Value",
                "Time Value",
                "Premium",
                "Strike Price",
                "Expiry"
            ],
            "takeaways": [
                "Premium can be separated conceptually into intrinsic and time value.",
                "Time value reflects remaining uncertainty and opportunity.",
                "Time value generally declines as expiry approaches, all else equal."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Option Premium",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand option premium.",
                "Learn the major factors affecting option prices.",
                "Understand why option premiums change continuously."
            ],
            "explanation": (
                "An option premium is the market price paid for the option contract. "
                "Important factors include the underlying price, strike price, time "
                "to expiry, implied volatility, interest rates and expected distributions "
                "such as dividends. Option prices change as these factors and market "
                "expectations change."
            ),
            "example": (
                "Two call options on the same stock can have different premiums if "
                "they have different strikes or expiry dates."
            ),
            "key_terms": [
                "Premium",
                "Volatility",
                "Strike Price",
                "Expiry",
                "Underlying Price"
            ],
            "takeaways": [
                "Premium is the market price of an option.",
                "Several variables influence option premium.",
                "Premium can change substantially before expiry."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "ITM, ATM & OTM Options",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand in-the-money options.",
                "Understand at-the-money options.",
                "Understand out-of-the-money options."
            ],
            "explanation": (
                "Moneyness describes the relationship between an option's strike "
                "price and the current underlying price. For a call, an option is "
                "generally in-the-money when the underlying is above the strike and "
                "out-of-the-money when it is below. For a put, the relationship is "
                "reversed. At-the-money generally describes a strike close to the "
                "current underlying price."
            ),
            "example": (
                "If a stock is at ₹1,000, a ₹900 call is generally in-the-money, "
                "while a ₹1,100 call is generally out-of-the-money."
            ),
            "key_terms": [
                "In-the-Money",
                "At-the-Money",
                "Out-of-the-Money",
                "Moneyness",
                "Strike"
            ],
            "takeaways": [
                "Moneyness compares the strike with the underlying price.",
                "Calls and puts have opposite moneyness relationships.",
                "Moneyness is important when analyzing option value."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Option Greeks — Overview",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the purpose of option Greeks.",
                "Learn what Delta, Gamma, Theta and Vega describe.",
                "Understand that Greeks are sensitivity measures rather than predictions."
            ],
            "explanation": (
                "Option Greeks are measures used to describe how an option's value "
                "may respond to changes in important variables. Delta relates to "
                "underlying price changes, Gamma describes changes in Delta, Theta "
                "describes sensitivity to time decay and Vega describes sensitivity "
                "to implied volatility. Greeks are model-based measures and can change "
                "as market conditions change."
            ),
            "example": (
                "If a simulated call has a Delta of 0.50, a small ₹1 increase in "
                "the underlying may correspond approximately to a ₹0.50 change "
                "in option value under simplified assumptions, with other variables held constant."
            ),
            "key_terms": [
                "Greeks",
                "Delta",
                "Gamma",
                "Theta",
                "Vega"
            ],
            "takeaways": [
                "Greeks measure sensitivity to different variables.",
                "They are not guarantees of future option prices.",
                "Greeks change as the underlying and market conditions change."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Delta",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand option Delta.",
                "Learn how Delta relates to underlying price changes.",
                "Understand Delta as a sensitivity measure."
            ],
            "explanation": (
                "Delta estimates how much an option's price may change for a small "
                "change in the underlying price, under the assumptions of the pricing "
                "model. Call Delta is generally positive while put Delta is generally "
                "negative. Delta can also be interpreted in some contexts as a rough "
                "measure of an option's sensitivity to the underlying."
            ),
            "example": (
                "If a call has a Delta of 0.60, a ₹1 increase in the underlying may "
                "correspond approximately to a ₹0.60 increase in the option price "
                "for a small move, assuming other variables remain unchanged."
            ),
            "key_terms": [
                "Delta",
                "Sensitivity",
                "Call Delta",
                "Put Delta",
                "Underlying"
            ],
            "takeaways": [
                "Delta measures sensitivity to underlying price changes.",
                "Call Delta is generally positive.",
                "Put Delta is generally negative."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Gamma",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand Gamma.",
                "Learn how Gamma relates to Delta.",
                "Understand why Gamma is important for option sensitivity."
            ],
            "explanation": (
                "Gamma measures the rate at which an option's Delta changes when "
                "the underlying price changes. Higher Gamma means Delta can change "
                "more rapidly for a given movement in the underlying. Gamma is especially "
                "important when studying options close to expiry and near the strike, "
                "where sensitivity can change quickly."
            ),
            "example": (
                "If an option's Delta is 0.50 and its Gamma indicates that Delta "
                "would rise by about 0.05 for a small upward move, the new Delta "
                "would be approximately 0.55 under the simplified assumption."
            ),
            "key_terms": [
                "Gamma",
                "Delta",
                "Sensitivity",
                "Option Greeks",
                "Expiry"
            ],
            "takeaways": [
                "Gamma measures how quickly Delta changes.",
                "High Gamma means Delta can change rapidly.",
                "Gamma is important when studying changing option sensitivity."
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Theta",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand Theta.",
                "Learn the concept of time decay.",
                "Understand why time decay can accelerate near expiry."
            ],
            "explanation": (
                "Theta measures an option's sensitivity to the passage of time under "
                "a pricing model. Option time value generally declines as expiry "
                "approaches, assuming other variables remain constant. The effect "
                "can become more significant near expiry, particularly for options "
                "whose value depends heavily on time value."
            ),
            "example": (
                "A simulated option may lose some of its time value as one day passes "
                "without a favorable movement in the underlying."
            ),
            "key_terms": [
                "Theta",
                "Time Decay",
                "Time Value",
                "Expiry",
                "Option Premium"
            ],
            "takeaways": [
                "Theta measures sensitivity to the passage of time.",
                "Time value generally declines as expiry approaches.",
                "Time decay is an important factor in option valuation."
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Vega",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand Vega.",
                "Learn the relationship between implied volatility and option premium.",
                "Understand why volatility changes can affect options significantly."
            ],
            "explanation": (
                "Vega measures an option's sensitivity to changes in implied volatility. "
                "All else equal, higher implied volatility generally increases option "
                "premiums because a wider range of possible future outcomes increases "
                "the potential value of the option's flexibility. Vega is not a guarantee "
                "that an option will rise when volatility rises because other variables "
                "can change at the same time."
            ),
            "example": (
                "If a simulated option has positive Vega, an increase in implied "
                "volatility can increase its theoretical value under the pricing model."
            ),
            "key_terms": [
                "Vega",
                "Implied Volatility",
                "Premium",
                "Volatility",
                "Sensitivity"
            ],
            "takeaways": [
                "Vega measures sensitivity to implied volatility.",
                "Higher implied volatility generally increases option premiums, all else equal.",
                "Volatility and price can change simultaneously."
            ],
        },
    },
    {
        "lesson_order": 17,
        "title": "Implied & Historical Volatility",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand historical volatility.",
                "Understand implied volatility.",
                "Learn why the two measures can differ."
            ],
            "explanation": (
                "Historical volatility describes how much an asset's price has varied "
                "over a past period using a chosen statistical method. Implied volatility "
                "is derived from market option prices using an option-pricing model and "
                "represents the market's implied estimate of future volatility under "
                "that model. Implied volatility can differ from historical volatility "
                "because expectations about future conditions may differ from the past."
            ),
            "example": (
                "An asset may have experienced relatively low historical volatility "
                "while its options trade with higher implied volatility because the "
                "market expects a significant upcoming event."
            ),
            "key_terms": [
                "Historical Volatility",
                "Implied Volatility",
                "Volatility",
                "Option Price",
                "Expectation"
            ],
            "takeaways": [
                "Historical volatility describes past price variation.",
                "Implied volatility comes from option-market pricing.",
                "The two measures can differ because future expectations may differ from past behavior."
            ],
        },
    },
    {
        "lesson_order": 18,
        "title": "Options Strategies — Educational Overview",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand the broad categories of options strategies.",
                "Learn the concepts behind protective and income-oriented structures.",
                "Understand that multi-leg strategies can have complex risk profiles."
            ],
            "explanation": (
                "Options can be combined into different structures to represent "
                "various market views or risk-management objectives. Examples include "
                "protective puts, covered calls, spreads and combinations of calls "
                "and puts. Each structure has its own payoff, costs, margin requirements "
                "and risks. In this academy, these structures should first be studied "
                "using payoff diagrams and virtual simulations."
            ),
            "example": (
                "A protective-put structure can be studied by combining a simulated "
                "underlying holding with a put option and examining how the combined "
                "payoff changes across different underlying prices."
            ),
            "key_terms": [
                "Options Strategy",
                "Protective Put",
                "Covered Call",
                "Spread",
                "Payoff"
            ],
            "takeaways": [
                "Options can be combined into different structures.",
                "Each structure has a distinct payoff and risk profile.",
                "Payoff diagrams and simulation are useful learning tools."
            ],
        },
    },
    {
        "lesson_order": 19,
        "title": "Derivatives Risk Management",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand the major risks associated with derivatives.",
                "Learn why leverage, volatility and liquidity matter.",
                "Understand the importance of simulation and predefined risk limits."
            ],
            "explanation": (
                "Derivative risk can come from leverage, rapid price movements, "
                "volatility changes, time decay, liquidity conditions, margin requirements "
                "and counterparty or settlement considerations depending on the instrument. "
                "A risk-management framework should consider total exposure rather than "
                "only the amount initially deposited. Historical testing and virtual "
                "trading can help learners understand these risks without committing real capital."
            ),
            "example": (
                "A virtual futures position may require a relatively small margin "
                "amount compared with its notional exposure. A learner can simulate "
                "different price movements to see how quickly portfolio value can change."
            ),
            "key_terms": [
                "Derivative Risk",
                "Leverage",
                "Margin",
                "Volatility",
                "Liquidity"
            ],
            "takeaways": [
                "Derivatives can create large exposure relative to deposited capital.",
                "Volatility and liquidity can change quickly.",
                "Risk should be evaluated using total exposure and not only margin."
            ],
        },
    },
    {
        "lesson_order": 20,
        "title": "Complete Derivatives Framework",
        "level": "Advanced",
        "estimated_minutes": 45,
        "content": {
            "objectives": [
                "Combine the major derivatives concepts.",
                "Build a structured framework for analyzing futures and options.",
                "Understand the importance of payoff, sensitivity and risk analysis."
            ],
            "explanation": (
                "A complete derivatives analysis begins with understanding the "
                "underlying asset, contract specifications, expiry, pricing factors "
                "and payoff structure. For futures, the learner should study contract "
                "size, margin, leverage and basis. For options, the learner should "
                "study strike, premium, moneyness, intrinsic value, time value, "
                "volatility and Greeks. Risk analysis should include potential losses, "
                "liquidity, margin requirements and scenario analysis."
            ),
            "example": (
                "A learner can build a virtual derivatives worksheet containing "
                "the underlying price, contract details, strike, expiry, premium, "
                "moneyness, theoretical payoff and selected risk metrics. Different "
                "market scenarios can then be simulated to understand how the "
                "position behaves."
            ),
            "key_terms": [
                "Derivatives",
                "Futures",
                "Options",
                "Payoff",
                "Greeks",
                "Risk Management"
            ],
            "takeaways": [
                "Derivative analysis requires understanding the contract and underlying.",
                "Options require analysis of price, time and volatility.",
                "Futures require careful attention to exposure and margin.",
                "Scenario analysis and virtual practice are valuable learning methods."
            ],
        },
    },
]


async def seed_module12():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 12}
        )

        if not module:
            raise RuntimeError(
                "Module 12 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 12,
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

        print(f"Module 12 lessons inserted: {inserted}")
        print(f"Module 12 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module12())