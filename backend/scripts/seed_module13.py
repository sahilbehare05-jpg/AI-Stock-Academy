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
        "title": "Introduction to Quantitative Trading",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand quantitative trading.",
                "Learn how data and mathematical models can support market analysis.",
                "Understand the difference between a model and a guaranteed prediction.",
            ],
            "explanation": (
                "Quantitative trading uses mathematical, statistical and computational "
                "methods to analyze financial data and evaluate trading ideas. A quantitative "
                "system can transform historical observations into rules, signals or models "
                "that can be tested systematically. Quantitative analysis does not guarantee "
                "future results because financial markets can change and historical patterns "
                "may not continue."
            ),
            "example": (
                "A learner can use historical stock prices to calculate moving averages, "
                "generate a simulated signal and evaluate the signal across a historical period."
            ),
            "key_terms": [
                "Quantitative Trading",
                "Data",
                "Statistics",
                "Model",
                "Signal",
            ],
            "takeaways": [
                "Quantitative trading uses data and mathematical methods.",
                "Rules and models can be tested systematically.",
                "Historical results do not guarantee future performance.",
            ],
        },
    },
    {
        "lesson_order": 2,
        "title": "Quantitative Data",
        "level": "Advanced",
        "estimated_minutes": 30,
        "content": {
            "objectives": [
                "Understand quantitative financial data.",
                "Learn common market-data fields.",
                "Understand why data quality matters.",
            ],
            "explanation": (
                "Quantitative trading depends on reliable numerical data. Common market "
                "data includes open, high, low, close and volume values. Additional data "
                "can include corporate fundamentals, economic indicators, volatility measures "
                "and alternative datasets. Missing, duplicated, incorrect or improperly "
                "timestamped data can produce misleading results."
            ),
            "example": (
                "A historical dataset may contain daily OHLCV information for a stock. "
                "Before analysis, a learner should check dates, missing values, duplicate "
                "records and unusual data errors."
            ),
            "key_terms": [
                "OHLCV",
                "Historical Data",
                "Volume",
                "Data Quality",
                "Timestamp",
            ],
            "takeaways": [
                "Quantitative systems depend heavily on data quality.",
                "OHLCV is a common form of market data.",
                "Incorrect data can produce incorrect analysis.",
            ],
        },
    },
    {
        "lesson_order": 3,
        "title": "Statistical Thinking",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand statistical thinking in trading analysis.",
                "Learn about distributions, averages and variability.",
                "Understand why individual outcomes should not be overinterpreted.",
            ],
            "explanation": (
                "Statistical thinking helps analyze patterns and uncertainty in financial "
                "data. Measures such as mean, median, variance, standard deviation and "
                "percentiles can describe a dataset. A single observation may be unusual, "
                "so quantitative analysis generally benefits from studying distributions "
                "and sufficiently large samples."
            ),
            "example": (
                "A learner can calculate the average daily return and standard deviation "
                "for a historical dataset and compare those statistics across different periods."
            ),
            "key_terms": [
                "Mean",
                "Median",
                "Variance",
                "Standard Deviation",
                "Distribution",
            ],
            "takeaways": [
                "Statistics help describe uncertainty and variability.",
                "Large samples provide more information than isolated observations.",
                "Historical distributions can change over time.",
            ],
        },
    },
    {
        "lesson_order": 4,
        "title": "Trading Signals",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand quantitative trading signals.",
                "Learn how indicators can be converted into rules.",
                "Understand why signals require testing.",
            ],
            "explanation": (
                "A trading signal is a rule or model output that identifies a condition "
                "of interest. Signals can be based on price, volume, technical indicators, "
                "fundamental variables or statistical relationships. A signal should be "
                "tested on appropriate data before its usefulness is evaluated."
            ),
            "example": (
                "A simple simulated signal may be generated when a short moving average "
                "crosses above a longer moving average. The learner can then evaluate "
                "the signal historically."
            ),
            "key_terms": [
                "Signal",
                "Indicator",
                "Rule",
                "Feature",
                "Model Output",
            ],
            "takeaways": [
                "Signals convert observations into defined conditions.",
                "Signals should be tested objectively.",
                "A signal is not a guarantee of a future price movement.",
            ],
        },
    },
    {
        "lesson_order": 5,
        "title": "Factor-Based Analysis",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand factor-based analysis.",
                "Learn common categories of financial factors.",
                "Understand how multiple factors can be combined.",
            ],
            "explanation": (
                "Factor-based analysis evaluates securities using measurable characteristics "
                "that may help explain differences in historical returns or risk. Examples "
                "include value, momentum, quality, size and volatility. Factor relationships "
                "can change across markets and time periods, so they should be evaluated "
                "using appropriate statistical testing."
            ),
            "example": (
                "A simulated research model can rank companies using historical valuation "
                "and momentum measurements and then compare the results with a benchmark."
            ),
            "key_terms": [
                "Factor",
                "Value",
                "Momentum",
                "Quality",
                "Size",
            ],
            "takeaways": [
                "Factors are measurable characteristics used in systematic analysis.",
                "Multiple factors can be combined into a model.",
                "Historical factor performance can change over time.",
            ],
        },
    },
    {
        "lesson_order": 6,
        "title": "Algorithmic Trading Basics",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand algorithmic trading.",
                "Learn how predefined instructions can automate decisions.",
                "Understand the importance of testing and safeguards.",
            ],
            "explanation": (
                "Algorithmic trading uses computer programs to execute or simulate "
                "predefined decision rules. An algorithm may process market data, "
                "apply conditions and generate an action according to its design. "
                "Automation does not remove market risk and can amplify mistakes "
                "if the underlying logic or data is incorrect."
            ),
            "example": (
                "A paper-trading algorithm can read historical prices, apply a predefined "
                "moving-average rule and record simulated entries and exits."
            ),
            "key_terms": [
                "Algorithmic Trading",
                "Automation",
                "Rule",
                "Execution",
                "Simulation",
            ],
            "takeaways": [
                "Algorithms automate predefined decision processes.",
                "Automation can reproduce both good and bad logic.",
                "Testing and safeguards are essential.",
            ],
        },
    },
    {
        "lesson_order": 7,
        "title": "Rule-Based Trading Systems",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand rule-based systems.",
                "Learn how entry, exit and risk rules form a system.",
                "Understand why rules must be unambiguous.",
            ],
            "explanation": (
                "A rule-based trading system converts a strategy into explicit conditions "
                "that can be consistently evaluated. Rules may define the market universe, "
                "timeframe, entry conditions, exit conditions, position sizing and risk "
                "controls. Ambiguous rules make reliable backtesting and automation difficult."
            ),
            "example": (
                "Instead of saying 'buy when the trend looks strong,' an algorithmic "
                "system needs measurable conditions such as a specified indicator relationship "
                "and defined time period."
            ),
            "key_terms": [
                "Rule-Based System",
                "Entry Rule",
                "Exit Rule",
                "Condition",
                "Automation",
            ],
            "takeaways": [
                "Rules should be measurable and unambiguous.",
                "A complete system contains more than an entry signal.",
                "Clear rules improve reproducibility.",
            ],
        },
    },
    {
        "lesson_order": 8,
        "title": "Backtesting Algorithms",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand algorithmic backtesting.",
                "Learn the basic components of a backtest.",
                "Understand why realistic assumptions matter.",
            ],
            "explanation": (
                "Algorithmic backtesting applies a programmed strategy to historical "
                "data. A robust test should define the data period, strategy rules, "
                "transaction assumptions, portfolio logic and evaluation metrics. "
                "Researchers should avoid using future information that would not have "
                "been available at the time of each simulated decision."
            ),
            "example": (
                "A learner tests a strategy on historical data from 2018 to 2023 and "
                "then evaluates the unchanged rules on a later period to study generalization."
            ),
            "key_terms": [
                "Backtest",
                "Historical Data",
                "Simulation",
                "Transaction Cost",
                "Out-of-Sample",
            ],
            "takeaways": [
                "Backtesting evaluates algorithms using historical data.",
                "Future information must not leak into historical decisions.",
                "Out-of-sample testing improves evaluation.",
            ],
        },
    },
    {
        "lesson_order": 9,
        "title": "Python for Trading",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand how Python can support quantitative analysis.",
                "Learn common categories of Python tools.",
                "Understand the basic research workflow.",
            ],
            "explanation": (
                "Python is widely used for data processing, statistical analysis, "
                "visualization and machine-learning research. Libraries such as pandas "
                "can organize tabular data, NumPy supports numerical computation, "
                "Matplotlib supports visualization and scikit-learn provides machine "
                "learning tools. A typical workflow includes obtaining data, cleaning it, "
                "creating features, testing a model and evaluating results."
            ),
            "example": (
                "A learner can load historical price data into a pandas DataFrame, "
                "calculate returns and moving averages, visualize the results and "
                "prepare the dataset for a research experiment."
            ),
            "key_terms": [
                "Python",
                "pandas",
                "NumPy",
                "Matplotlib",
                "scikit-learn",
            ],
            "takeaways": [
                "Python can support the complete quantitative research workflow.",
                "Different libraries serve different analytical purposes.",
                "Good data preparation is as important as model selection.",
            ],
        },
    },
    {
        "lesson_order": 10,
        "title": "Data Preparation",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand data cleaning and preparation.",
                "Learn about missing values and inconsistent records.",
                "Understand why preprocessing must avoid future-data leakage.",
            ],
            "explanation": (
                "Data preparation transforms raw information into a format suitable "
                "for analysis or modeling. Tasks can include handling missing values, "
                "removing duplicates, aligning timestamps, correcting data types and "
                "creating derived variables. Preprocessing must respect the chronological "
                "structure of financial data so that future information does not influence "
                "past observations."
            ),
            "example": (
                "When calculating a rolling indicator for a historical date, the calculation "
                "should use information available up to that date rather than future observations."
            ),
            "key_terms": [
                "Data Cleaning",
                "Preprocessing",
                "Missing Values",
                "Timestamp",
                "Data Leakage",
            ],
            "takeaways": [
                "Clean data is essential for reliable analysis.",
                "Time alignment is especially important for market data.",
                "Preprocessing must not introduce future information.",
            ],
        },
    },
    {
        "lesson_order": 11,
        "title": "Machine Learning for Trading",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand how machine learning can be applied to financial research.",
                "Learn the difference between supervised and unsupervised learning.",
                "Understand why financial prediction is difficult."
            ],
            "explanation": (
                "Machine learning can be used to identify relationships in financial "
                "datasets, classify market conditions, estimate quantities or discover "
                "patterns. Supervised learning uses labeled outcomes, while unsupervised "
                "learning searches for structure without predefined labels. Financial "
                "data is noisy, non-stationary and influenced by changing external factors, "
                "so model performance can degrade outside the training environment."
            ),
            "example": (
                "A supervised model can be trained on historical features to classify "
                "whether a future return was positive or negative during a defined period. "
                "The model must then be evaluated on unseen chronological data."
            ),
            "key_terms": [
                "Machine Learning",
                "Supervised Learning",
                "Unsupervised Learning",
                "Classification",
                "Prediction",
            ],
            "takeaways": [
                "Machine learning can support financial research.",
                "Financial data contains substantial noise and changing relationships.",
                "Unseen data is essential for evaluating model generalization.",
            ],
        },
    },
    {
        "lesson_order": 12,
        "title": "Features & Target Variables",
        "level": "Advanced",
        "estimated_minutes": 35,
        "content": {
            "objectives": [
                "Understand features and target variables.",
                "Learn how financial datasets can be structured for machine learning.",
                "Understand the importance of defining the prediction horizon."
            ],
            "explanation": (
                "Features are input variables provided to a machine-learning model, "
                "while the target is the outcome the model is designed to estimate or "
                "classify. Features may include historical returns, volatility, volume, "
                "technical measurements or fundamental information. The target must be "
                "defined carefully so that it represents information available after "
                "the feature observation."
            ),
            "example": (
                "A model could use today's historical indicators as features and define "
                "the target as whether the next five trading days have a positive return."
            ),
            "key_terms": [
                "Feature",
                "Target",
                "Label",
                "Prediction Horizon",
                "Dataset",
            ],
            "takeaways": [
                "Features are model inputs.",
                "The target is the outcome being predicted.",
                "The target horizon must be defined without leaking future information."
            ],
        },
    },
    {
        "lesson_order": 13,
        "title": "Training & Testing Models",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand training and testing datasets.",
                "Learn why chronological splitting matters for financial data.",
                "Understand model generalization."
            ],
            "explanation": (
                "A model is trained using one portion of the dataset and evaluated "
                "on data that was not used during training. For time-dependent financial "
                "data, chronological splits are often more appropriate than randomly "
                "shuffling observations because the future should not influence the past. "
                "A model that performs well only on training data may be overfit."
            ),
            "example": (
                "A dataset can be divided into an earlier training period and a later "
                "testing period. The model is trained only on the earlier period and "
                "then evaluated on the later observations."
            ),
            "key_terms": [
                "Training Set",
                "Test Set",
                "Generalization",
                "Chronological Split",
                "Overfitting",
            ],
            "takeaways": [
                "Testing should use unseen data.",
                "Chronological structure is important in financial datasets.",
                "Strong training performance does not guarantee generalization."
            ],
        },
    },
    {
        "lesson_order": 14,
        "title": "Avoiding Data Leakage",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand data leakage.",
                "Learn common sources of leakage in financial models.",
                "Understand how leakage can create unrealistic performance."
            ],
            "explanation": (
                "Data leakage occurs when information that would not have been available "
                "at the time of a simulated decision enters the model or evaluation process. "
                "Examples include using future prices to calculate historical features, "
                "randomly splitting time-series observations when future information can "
                "influence preprocessing, or using revised information that was not available "
                "at the historical decision time."
            ),
            "example": (
                "If a feature for January uses a full-year average that includes December "
                "data, the feature contains future information and can make a backtest "
                "look unrealistically accurate."
            ),
            "key_terms": [
                "Data Leakage",
                "Future Information",
                "Time Series",
                "Preprocessing",
                "Backtest",
            ],
            "takeaways": [
                "Future information must not influence historical decisions.",
                "Leakage can produce misleadingly strong model results.",
                "Time-aware preprocessing is essential."
            ],
        },
    },
    {
        "lesson_order": 15,
        "title": "Model Evaluation",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand model evaluation.",
                "Learn common classification and regression metrics.",
                "Understand why financial usefulness requires more than one metric."
            ],
            "explanation": (
                "Machine-learning models can be evaluated using metrics appropriate "
                "to their task. Classification metrics include accuracy, precision, "
                "recall and F1 score, while regression can use measures such as MAE "
                "and RMSE. In financial research, model metrics should be combined "
                "with realistic simulation, risk measures, transaction assumptions "
                "and out-of-sample evaluation."
            ),
            "example": (
                "A classification model may have 60% accuracy but still be unsuitable "
                "for a financial application if its errors occur during important market "
                "conditions or if transaction costs eliminate any simulated advantage."
            ),
            "key_terms": [
                "Accuracy",
                "Precision",
                "Recall",
                "F1 Score",
                "RMSE",
            ],
            "takeaways": [
                "Different tasks require different evaluation metrics.",
                "Accuracy alone may not describe practical usefulness.",
                "Financial evaluation should include risk and realistic assumptions."
            ],
        },
    },
    {
        "lesson_order": 16,
        "title": "Time-Series Considerations",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand important properties of financial time series.",
                "Learn about temporal dependence and non-stationarity.",
                "Understand why time-aware validation is important."
            ],
            "explanation": (
                "Financial observations are ordered in time and may have changing "
                "distributions, trends, volatility and relationships. This is known "
                "as a time-series setting. Randomly shuffling observations can create "
                "unrealistic validation results. Walk-forward or rolling evaluation "
                "can better represent how a model would operate as new data becomes available."
            ),
            "example": (
                "A walk-forward experiment can train a model on an initial historical "
                "window, evaluate it on the next period, expand or move the training "
                "window and repeat the process."
            ),
            "key_terms": [
                "Time Series",
                "Non-Stationarity",
                "Walk-Forward",
                "Rolling Window",
                "Temporal Dependence",
            ],
            "takeaways": [
                "Financial data has an important chronological structure.",
                "Market relationships can change over time.",
                "Time-aware validation can provide a more realistic evaluation."
            ],
        },
    },
    {
        "lesson_order": 17,
        "title": "AI-Based Market Analysis",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand AI-assisted market analysis.",
                "Learn how AI can combine multiple information sources.",
                "Understand the limitations of AI-generated predictions."
            ],
            "explanation": (
                "AI-based market analysis can use machine learning and other computational "
                "methods to process large datasets, identify patterns, classify conditions "
                "or summarize information. AI systems can assist researchers by combining "
                "technical, fundamental and contextual features. However, AI models can "
                "overfit, inherit data problems, produce unstable predictions or fail when "
                "market conditions change."
            ),
            "example": (
                "A research system can combine historical price features, volatility "
                "measurements and selected company information to classify historical "
                "market conditions. The model can then be evaluated on unseen periods."
            ),
            "key_terms": [
                "Artificial Intelligence",
                "Machine Learning",
                "Pattern Recognition",
                "Prediction",
                "Model Risk",
            ],
            "takeaways": [
                "AI can process large and complex datasets.",
                "AI predictions are uncertain and model-dependent.",
                "Data quality and validation remain essential."
            ],
        },
    },
    {
        "lesson_order": 18,
        "title": "Automated Strategy Concepts",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand the architecture of an automated strategy.",
                "Learn the role of data, signals, risk controls and execution.",
                "Understand why automation requires monitoring and safeguards."
            ],
            "explanation": (
                "An automated strategy can be viewed as a pipeline containing data input, "
                "feature processing, signal generation, portfolio logic, risk controls, "
                "simulation or execution and logging. Each component can introduce errors. "
                "For educational systems, virtual execution is useful for validating the "
                "logic before considering any real-world application."
            ),
            "example": (
                "A virtual system can receive historical prices, calculate features, "
                "generate a simulated signal, apply portfolio constraints and record "
                "the result without sending real orders."
            ),
            "key_terms": [
                "Automation",
                "Signal",
                "Risk Control",
                "Execution",
                "Logging",
            ],
            "takeaways": [
                "Automated systems contain multiple connected components.",
                "Errors can occur in data, logic, risk controls or execution.",
                "Virtual execution is valuable for educational testing."
            ],
        },
    },
    {
        "lesson_order": 19,
        "title": "Limitations of AI in Trading",
        "level": "Advanced",
        "estimated_minutes": 40,
        "content": {
            "objectives": [
                "Understand major limitations of AI in financial markets.",
                "Learn about overfitting and regime changes.",
                "Understand why AI should not be treated as an infallible predictor."
            ],
            "explanation": (
                "AI models face several challenges in financial applications. Historical "
                "relationships can disappear, market regimes can change, datasets can "
                "contain biases, and rare events can behave differently from normal periods. "
                "Models can also overfit historical data or appear accurate because of data "
                "leakage. Therefore, AI outputs should be treated as uncertain research "
                "signals rather than guaranteed predictions."
            ),
            "example": (
                "A model trained during a low-volatility market may perform differently "
                "during a high-volatility period because the underlying data distribution "
                "has changed."
            ),
            "key_terms": [
                "Model Risk",
                "Overfitting",
                "Regime Change",
                "Bias",
                "Uncertainty",
            ],
            "takeaways": [
                "AI cannot reliably predict every market condition.",
                "Changing market regimes can reduce model performance.",
                "Validation, monitoring and risk controls are essential."
            ],
        },
    },
    {
        "lesson_order": 20,
        "title": "Building a Complete Quantitative & AI Framework",
        "level": "Advanced",
        "estimated_minutes": 45,
        "content": {
            "objectives": [
                "Combine quantitative and AI concepts into a complete framework.",
                "Understand the full research pipeline.",
                "Learn how to evaluate models systematically and responsibly."
            ],
            "explanation": (
                "A complete quantitative and AI framework begins with a clearly defined "
                "research question and reliable data. The process can include data cleaning, "
                "feature engineering, target definition, chronological training and testing, "
                "model selection, backtesting, risk analysis and ongoing monitoring. The "
                "framework should explicitly address data leakage, overfitting, transaction "
                "assumptions, changing market regimes and model uncertainty."
            ),
            "example": (
                "A learner can build a virtual research pipeline that collects historical "
                "data, prepares features, trains a model on an earlier period, evaluates "
                "it on later unseen data, simulates the model's signals and reports both "
                "performance and risk metrics."
            ),
            "key_terms": [
                "Quantitative Framework",
                "Machine Learning",
                "Feature Engineering",
                "Backtesting",
                "Model Evaluation",
                "Risk Management",
            ],
            "takeaways": [
                "A complete AI trading research system requires more than a prediction model.",
                "Data quality, leakage prevention and chronological validation are essential.",
                "Backtesting and simulation should include realistic assumptions.",
                "AI outputs should be treated as uncertain signals rather than guaranteed predictions."
            ],
        },
    },
]


async def seed_module13():
    connect_to_mongo()

    try:
        db = get_database()

        module = await db[Collections.MODULES].find_one(
            {"order": 13}
        )

        if not module:
            raise RuntimeError(
                "Module 13 not found. Run seed_academy.py first."
            )

        module_id = module["_id"]
        lessons_collection = db[Collections.LESSONS]

        inserted = 0
        existing = 0

        for lesson in LESSONS:
            document = {
                "module_id": module_id,
                "module_order": 13,
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

        print(f"Module 13 lessons inserted: {inserted}")
        print(f"Module 13 lessons already existed: {existing}")

    finally:
        close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_module13())