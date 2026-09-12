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
        "title": "Introduction to Trading Psychology",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand what trading psychology means.",
                "Learn how emotions and cognitive biases can affect decisions.",
                "Understand why a written process can improve consistency."
            ],
            "explanation": (
                "Trading psychology refers to the mental and emotional factors "
                "that influence financial decision-making. Fear, excitement, "
                "overconfidence, frustration and uncertainty can affect how a "
                "person interprets information and follows a strategy. Good "
                "psychological discipline means recognizing these influences "
                "and using a consistent decision process rather than reacting "
                "impulsively to every market movement."
            ),
            "example": (
                "A learner may have a clear simulated trading plan but abandon "
                "its rules after seeing a sudden price movement. Recording this "
                "event in a journal can help identify the emotional trigger."
            ),
            "key_terms": [
                "Trading Psychology",
                "Emotion",
                "Discipline",
                "Decision Making",
                "Bias"
            ],
            "takeaways": [
                "Psychology can influence financial decisions.",
                "Emotions can affect how consistently a strategy is followed.",
                "A structured process can reduce impulsive decisions."
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Emotions & Decision Making",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Identify common emotions involved in market decisions.",
                "Understand how emotions can change behavior.",
                "Learn how predefined rules can support consistent decisions."
            ],
            "explanation": (
                "Emotions such as fear, excitement, frustration and confidence "
                "are normal human responses. Problems can occur when emotional "
                "reactions override a previously defined decision process. "
                "A learner can reduce this influence by defining rules in advance, "
                "using checklists and reviewing decisions after the fact."
            ),
            "example": (
                "After a simulated loss, a learner may feel frustrated and want "
                "to immediately make another trade. A predefined process can "
                "require reviewing the journal and strategy conditions first."
            ),
            "key_terms": [
                "Emotion",
                "Decision Making",
                "Checklist",
                "Discipline",
                "Impulse"
            ],
            "takeaways": [
                "Emotions are normal but can influence decisions.",
                "Predefined rules can create structure.",
                "Reviewing decisions helps identify emotional patterns."
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Fear & Uncertainty",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the role of fear in decision-making.",
                "Learn why uncertainty is unavoidable in markets.",
                "Develop a framework for handling uncertain outcomes."
            ],
            "explanation": (
                "Markets involve uncertainty because future prices, company results "
                "and economic conditions cannot be known with certainty. Fear can "
                "cause hesitation, premature exits or avoidance of a valid process. "
                "A disciplined learner focuses on probabilities, predefined rules "
                "and risk limits rather than trying to eliminate uncertainty."
            ),
            "example": (
                "A learner may correctly follow a simulated strategy but experience "
                "fear after several losing outcomes. Reviewing a sufficiently large "
                "sample of historical results can provide better context than reacting "
                "to one outcome."
            ),
            "key_terms": [
                "Fear",
                "Uncertainty",
                "Probability",
                "Risk",
                "Decision Process"
            ],
            "takeaways": [
                "Uncertainty is a fundamental part of markets.",
                "Fear can influence otherwise planned decisions.",
                "Thinking in probabilities can provide better perspective."
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Greed & Overconfidence",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand overconfidence.",
                "Learn how excessive confidence can affect decision-making.",
                "Understand why successful outcomes do not prove skill."
            ],
            "explanation": (
                "Overconfidence occurs when a person becomes excessively certain "
                "about their knowledge, predictions or abilities. A sequence of "
                "successful outcomes can increase this feeling even when results "
                "were partly caused by favorable conditions or chance. Excessive "
                "confidence can lead to ignoring risk controls or changing strategy "
                "rules without sufficient evidence."
            ),
            "example": (
                "After several successful simulated trades, a learner may begin "
                "assuming every future setup will work. A trading journal can help "
                "compare confidence levels with actual results over a larger sample."
            ),
            "key_terms": [
                "Overconfidence",
                "Greed",
                "Confidence",
                "Probability",
                "Risk"
            ],
            "takeaways": [
                "Successful outcomes do not automatically prove skill.",
                "Overconfidence can weaken risk discipline.",
                "Confidence should be based on evidence rather than a short winning streak."
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "FOMO & Chasing the Market",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand FOMO.",
                "Learn why rapidly moving prices can create emotional pressure.",
                "Understand how predefined criteria can reduce impulsive decisions."
            ],
            "explanation": (
                "FOMO, or fear of missing out, occurs when a person feels pressure "
                "to participate because an asset is moving quickly or others appear "
                "to be benefiting. This can lead to entering without completing the "
                "planned analysis. A disciplined process allows a learner to accept "
                "that some opportunities will be missed rather than abandoning the rules."
            ),
            "example": (
                "A stock suddenly rises after a news event. Instead of immediately "
                "chasing the movement in a simulation, a learner can record the event "
                "and wait to see whether the predefined strategy conditions are actually met."
            ),
            "key_terms": [
                "FOMO",
                "Chasing",
                "Impulse",
                "Opportunity",
                "Discipline"
            ],
            "takeaways": [
                "Missing an opportunity is not the same as making a bad decision.",
                "FOMO can cause people to abandon predefined rules.",
                "A strategy should define conditions before a market move occurs."
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Loss Aversion",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand loss aversion.",
                "Learn why losses can feel more significant than equivalent gains.",
                "Understand how this bias can affect decision-making."
            ],
            "explanation": (
                "Loss aversion describes the tendency for people to experience "
                "losses as psychologically more significant than comparable gains. "
                "In financial decisions, this can contribute to behaviors such as "
                "holding an unfavorable position too long or becoming excessively "
                "cautious after a loss. Recognizing the bias can help learners "
                "evaluate decisions using predefined rules rather than emotion."
            ),
            "example": (
                "A learner may feel strongly attached to a losing simulated position "
                "because closing it would make the loss feel final. A predefined "
                "strategy exit rule can provide an objective decision framework."
            ),
            "key_terms": [
                "Loss Aversion",
                "Bias",
                "Loss",
                "Emotion",
                "Decision Rule"
            ],
            "takeaways": [
                "People may react more strongly to losses than gains.",
                "Loss aversion can distort financial decisions.",
                "Predefined rules can help reduce emotional decision-making."
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Confirmation Bias",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand confirmation bias.",
                "Learn how people may favor information supporting existing beliefs.",
                "Develop habits for considering alternative explanations."
            ],
            "explanation": (
                "Confirmation bias is the tendency to notice or give greater weight "
                "to information that supports an existing belief while overlooking "
                "contradictory evidence. In market analysis, a person who expects "
                "a stock to rise may focus heavily on positive news and discount "
                "negative information. A structured analysis should deliberately "
                "consider evidence that could invalidate the original view."
            ),
            "example": (
                "If a learner expects a simulated stock to rise, they can create "
                "a checklist requiring them to identify at least one factor that "
                "could make the bullish scenario incorrect."
            ),
            "key_terms": [
                "Confirmation Bias",
                "Bias",
                "Evidence",
                "Alternative Scenario",
                "Objectivity"
            ],
            "takeaways": [
                "People can unintentionally favor evidence supporting their beliefs.",
                "Considering contradictory evidence improves analysis.",
                "Every market thesis should have conditions that could invalidate it."
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Revenge Trading",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand revenge trading.",
                "Learn why frustration after losses can lead to poor decisions.",
                "Understand the importance of predefined stopping rules."
            ],
            "explanation": (
                "Revenge trading refers to making additional trades primarily "
                "because of frustration or a desire to recover a previous loss "
                "quickly. This can cause a person to increase exposure, abandon "
                "strategy rules or make decisions without adequate analysis. "
                "A structured process can include a pause, review period or "
                "maximum-loss rule to reduce emotionally driven decisions."
            ),
            "example": (
                "After an unfavorable simulated trade, a learner immediately "
                "wants to take another position to recover the result. A predefined "
                "cooling-off rule can require reviewing the previous trade before "
                "considering another setup."
            ),
            "key_terms": [
                "Revenge Trading",
                "Frustration",
                "Loss",
                "Cooling-Off Period",
                "Discipline"
            ],
            "takeaways": [
                "Trying to immediately recover a loss can distort decision-making.",
                "Emotional decisions can increase exposure to further losses.",
                "A predefined review or pause rule can improve discipline."
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Discipline & Consistency",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand trading discipline.",
                "Learn why consistency matters when evaluating a strategy.",
                "Develop habits for following predefined processes."
            ],
            "explanation": (
                "Discipline means following a defined process even when emotions "
                "or recent outcomes create pressure to change it. Consistency is "
                "important because a strategy cannot be evaluated properly if its "
                "rules are changed after every outcome. Discipline includes following "
                "entry criteria, risk limits, exit rules and record-keeping procedures."
            ),
            "example": (
                "A learner tests a strategy over 100 simulated outcomes. If the "
                "rules remain consistent, the results can be evaluated meaningfully. "
                "If the rules change after every loss, the final results become difficult to interpret."
            ),
            "key_terms": [
                "Discipline",
                "Consistency",
                "Process",
                "Rules",
                "Execution"
            ],
            "takeaways": [
                "Consistency makes strategy evaluation more meaningful.",
                "Discipline means following predefined rules.",
                "Changing rules impulsively can make results unreliable."
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Trading Journals",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand the purpose of a trading journal.",
                "Learn what information can be recorded.",
                "Use journal data to identify behavioral patterns."
            ],
            "explanation": (
                "A trading journal is a structured record of decisions and outcomes. "
                "It can contain the date, asset, setup, strategy rules, entry and "
                "exit assumptions, result, market conditions and emotional state. "
                "Reviewing journal data can reveal repeated mistakes, inconsistent "
                "rule-following and situations where decision quality changes."
            ),
            "example": (
                "A learner records 50 simulated trades and notes whether each "
                "decision followed the strategy. Later, the learner discovers that "
                "most rule violations occurred immediately after losing outcomes."
            ),
            "key_terms": [
                "Trading Journal",
                "Record Keeping",
                "Review",
                "Behavior",
                "Performance"
            ],
            "takeaways": [
                "A journal creates evidence for reviewing decisions.",
                "Behavioral patterns are easier to identify from recorded data.",
                "The journal should record both outcomes and decision quality."
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Handling Winning & Losing Streaks",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand winning and losing streaks.",
                "Learn why short-term streaks can affect confidence.",
                "Use statistical thinking when evaluating performance."
            ],
            "explanation": (
                "Winning and losing streaks can occur naturally even when a strategy "
                "has a stable long-term probability distribution. A winning streak "
                "may increase overconfidence, while a losing streak may increase fear "
                "or frustration. Learners should evaluate performance using sufficiently "
                "large samples and predefined metrics instead of drawing conclusions "
                "from a small number of outcomes."
            ),
            "example": (
                "A simulated strategy may produce five losses in a row even though "
                "its historical win rate is around 50%. The learner should record "
                "the streak and compare it with the strategy's expected variability "
                "rather than immediately changing every rule."
            ),
            "key_terms": [
                "Winning Streak",
                "Losing Streak",
                "Probability",
                "Sample Size",
                "Variance"
            ],
            "takeaways": [
                "Streaks can occur naturally.",
                "Short samples can create misleading conclusions.",
                "Performance should be evaluated using consistent metrics and adequate data."
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Building a Strong Trading Mindset",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Combine the major trading-psychology concepts.",
                "Develop a disciplined decision-making framework.",
                "Learn how to continuously improve through review and evidence."
            ],
            "explanation": (
                "A strong trading mindset is not about predicting every market move "
                "or eliminating emotions. It is about accepting uncertainty, following "
                "a defined process, controlling risk, reviewing decisions objectively "
                "and learning from evidence. A healthy educational approach focuses "
                "on process quality rather than becoming emotionally attached to individual outcomes."
            ),
            "example": (
                "A learner creates a complete simulation routine: review the market "
                "context, check strategy conditions, record the decision, follow "
                "predefined risk rules, document the result and review the decision "
                "later without changing the original rules simply because the outcome "
                "was unfavorable."
            ),
            "key_terms": [
                "Trading Mindset",
                "Discipline",
                "Uncertainty",
                "Process",
                "Journal",
                "Risk Management"
            ],
            "takeaways": [
                "The goal is disciplined decision-making, not perfect prediction.",
                "Emotions should be recognized rather than allowed to control the process.",
                "A journal and consistent rules support continuous improvement.",
                "Virtual and historical practice are useful ways to learn safely."
            ],
        },
    },
]


async def seed_module10():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 10}
        )

        if not module:
            raise RuntimeError(
                "Module 10 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 10,
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

        print(f"Module 10 lessons inserted: {inserted}")
        print(f"Module 10 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module10())