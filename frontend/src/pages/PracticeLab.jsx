import React, { useMemo, useState } from 'react'
import {
  Activity,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  CircleHelp,
  RotateCcw,
  Target,
  TrendingDown,
  TrendingUp,
  Clock,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const SCENARIOS = [
  // ============================================================
  // BEGINNER — 1 to 15
  // ============================================================

  {
    id: 1,
    title: 'Understanding an Uptrend',
    difficulty: 'Beginner',
    category: 'Trend',
    description:
      'Price is making a series of higher highs and higher lows.',
    question:
      'What is the most likely description of the current market structure?',
    correct: 'BUY',
    explanation:
      'The chart is showing an uptrend through higher highs and higher lows. However, recognizing an uptrend does not automatically mean entering immediately.',
    lesson:
      'An uptrend generally contains higher highs and higher lows.',
  },

  {
    id: 2,
    title: 'Understanding a Downtrend',
    difficulty: 'Beginner',
    category: 'Trend',
    description:
      'Price is consistently forming lower highs and lower lows.',
    question:
      'What should you recognize first?',
    correct: 'SELL',
    explanation:
      'Lower highs and lower lows indicate a downward market structure. Recognizing the trend is the first step before considering any trade.',
    lesson:
      'A downtrend generally contains lower highs and lower lows.',
  },

  {
    id: 3,
    title: 'Sideways Market',
    difficulty: 'Beginner',
    category: 'Market Structure',
    description:
      'Price is moving repeatedly between a relatively clear upper and lower area.',
    question:
      'What is the safest educational response while the direction remains unclear?',
    correct: 'WAIT',
    explanation:
      'A sideways market does not provide a clear directional trend. Waiting for a clearer setup can help avoid forcing a trade.',
    lesson:
      'Markets can move sideways when neither buyers nor sellers clearly dominate.',
  },

  {
    id: 4,
    title: 'Bullish Candle',
    difficulty: 'Beginner',
    category: 'Candlestick',
    description:
      'The latest candle closes above its opening price.',
    question:
      'What does the candle primarily show?',
    correct: 'BUY',
    explanation:
      'A bullish candle means the closing price is above the opening price for that period. It indicates buying pressure during that candle.',
    lesson:
      'Bullish candles show that price closed higher than it opened.',
  },

  {
    id: 5,
    title: 'Bearish Candle',
    difficulty: 'Beginner',
    category: 'Candlestick',
    description:
      'The latest candle closes below its opening price.',
    question:
      'What does this candle primarily indicate?',
    correct: 'SELL',
    explanation:
      'A bearish candle closes below its opening price and indicates selling pressure during that period.',
    lesson:
      'Bearish candles show that price closed lower than it opened.',
  },

  {
    id: 6,
    title: 'Approaching Resistance',
    difficulty: 'Beginner',
    category: 'Support & Resistance',
    description:
      'Price has risen toward a level where it previously struggled to move higher.',
    question:
      'What should a beginner consider before entering immediately?',
    correct: 'WAIT',
    explanation:
      'Resistance can cause upward movement to slow or reverse. Waiting for confirmation is often more sensible than entering simply because price is rising.',
    lesson:
      'Resistance is an area where selling interest may increase.',
  },

  {
    id: 7,
    title: 'Approaching Support',
    difficulty: 'Beginner',
    category: 'Support & Resistance',
    description:
      'Price has fallen toward an area where buyers previously appeared.',
    question:
      'What should you consider before buying?',
    correct: 'WAIT',
    explanation:
      'Support can attract buyers, but it can also fail. Waiting for evidence that buyers are actually defending the area can be useful.',
    lesson:
      'Support is an area where buying interest may increase.',
  },

  {
    id: 8,
    title: 'Strong Buying Pressure',
    difficulty: 'Beginner',
    category: 'Price Action',
    description:
      'Several bullish candles are appearing with relatively strong upward movement.',
    question:
      'What does the price action suggest?',
    correct: 'BUY',
    explanation:
      'The sequence suggests strong buying pressure. It is still important to consider location, trend and risk before entering.',
    lesson:
      'A sequence of strong bullish candles can indicate strong buying pressure.',
  },

  {
    id: 9,
    title: 'Strong Selling Pressure',
    difficulty: 'Beginner',
    category: 'Price Action',
    description:
      'Several bearish candles appear consecutively.',
    question:
      'What does the price action suggest?',
    correct: 'SELL',
    explanation:
      'The sequence indicates strong selling pressure. The direction should be understood before considering a trade.',
    lesson:
      'Multiple bearish candles can indicate persistent selling pressure.',
  },

  {
    id: 10,
    title: 'Long Upper Wick',
    difficulty: 'Beginner',
    category: 'Candlestick',
    description:
      'A candle moves higher during the period but closes considerably below its high.',
    question:
      'What should you pay attention to?',
    correct: 'WAIT',
    explanation:
      'A long upper wick can show that higher prices were rejected. It can be a warning that sellers became active at higher levels.',
    lesson:
      'Long upper wicks can indicate rejection of higher prices.',
  },

  {
    id: 11,
    title: 'Long Lower Wick',
    difficulty: 'Beginner',
    category: 'Candlestick',
    description:
      'Price moves significantly lower but recovers before the candle closes.',
    question:
      'What does this potentially suggest?',
    correct: 'WAIT',
    explanation:
      'A long lower wick can show rejection of lower prices. Additional confirmation is useful before interpreting it as a reversal.',
    lesson:
      'Long lower wicks can indicate rejection of lower prices.',
  },

  {
    id: 12,
    title: 'Trend Following',
    difficulty: 'Beginner',
    category: 'Trend',
    description:
      'Price is making higher highs and higher lows and has not yet reached a major resistance area.',
    question:
      'Which direction is more aligned with the current structure?',
    correct: 'BUY',
    explanation:
      'The current structure is upward, so a bullish bias is more aligned with the trend. The actual entry still requires risk consideration.',
    lesson:
      'Trend-following means considering trades that align with the broader market direction.',
  },

  {
    id: 13,
    title: 'Falling Into Support',
    difficulty: 'Beginner',
    category: 'Support',
    description:
      'Price has fallen rapidly and is now reaching a previously respected support zone.',
    question:
      'What should you avoid doing automatically?',
    correct: 'WAIT',
    explanation:
      'A support level does not guarantee a bounce. Avoid assuming that every support touch is an automatic buying opportunity.',
    lesson:
      'A support level is a zone to analyze, not an automatic buy signal.',
  },

  {
    id: 14,
    title: 'Chasing a Large Candle',
    difficulty: 'Beginner',
    category: 'Risk Awareness',
    description:
      'A very large bullish candle has already moved significantly upward.',
    question:
      'What should a beginner consider before chasing the move?',
    correct: 'WAIT',
    explanation:
      'Entering after a large move without analyzing the setup can increase risk. Waiting for a more structured opportunity can be useful.',
    lesson:
      'Strong price movement does not mean you must immediately enter a trade.',
  },

  {
    id: 15,
    title: 'Basic Market Decision',
    difficulty: 'Beginner',
    category: 'Decision Making',
    description:
      'The chart has mixed signals with no clear trend or important level nearby.',
    question:
      'What is the most disciplined choice?',
    correct: 'WAIT',
    explanation:
      'When the setup is unclear, waiting is a valid trading decision. A trader does not need to trade every market movement.',
    lesson:
      'Not trading is sometimes the best decision when the setup is unclear.',
  },

  // ============================================================
  // INTERMEDIATE — 16 to 30
  // ============================================================

  {
    id: 16,
    title: 'Breakout Above Resistance',
    difficulty: 'Intermediate',
    category: 'Breakout',
    description:
      'Price moves above a previously identified resistance level.',
    question:
      'What should you consider before treating the breakout as confirmed?',
    correct: 'WAIT',
    explanation:
      'A move above resistance can be a breakout attempt. Confirmation and sustained movement can help distinguish it from a false breakout.',
    lesson:
      'Not every move above resistance becomes a successful breakout.',
  },

  {
    id: 17,
    title: 'False Breakout',
    difficulty: 'Intermediate',
    category: 'Breakout',
    description:
      'Price briefly moves above resistance but quickly falls back below it.',
    question:
      'What does this situation warn you about?',
    correct: 'SELL',
    explanation:
      'The failed move above resistance suggests rejection. A trader should recognize the possibility of a false breakout rather than assuming the upward move will continue.',
    lesson:
      'A false breakout happens when price breaks a level but fails to sustain the move.',
  },

  {
    id: 18,
    title: 'Breakdown Below Support',
    difficulty: 'Intermediate',
    category: 'Breakdown',
    description:
      'Price moves below an established support area with strong selling pressure.',
    question:
      'What market condition should you recognize?',
    correct: 'SELL',
    explanation:
      'A strong move below support can indicate a bearish breakdown. Confirmation and risk management remain important.',
    lesson:
      'A breakdown occurs when price moves below an important support area.',
  },

  {
    id: 19,
    title: 'Retest After Breakout',
    difficulty: 'Intermediate',
    category: 'Breakout',
    description:
      'Price breaks resistance and then returns toward the previous resistance area.',
    question:
      'What should you observe during the retest?',
    correct: 'WAIT',
    explanation:
      'A retest can help determine whether the old resistance is behaving like new support. Price reaction around the level is important.',
    lesson:
      'After a breakout, the old resistance can sometimes act as support.',
  },

  {
    id: 20,
    title: 'Higher High Confirmation',
    difficulty: 'Intermediate',
    category: 'Market Structure',
    description:
      'Price breaks above a previous swing high and establishes a new high.',
    question:
      'What does this add to the bullish structure?',
    correct: 'BUY',
    explanation:
      'A new higher high strengthens the existing bullish market structure, although it does not guarantee that price will continue upward.',
    lesson:
      'Higher highs are an important component of an uptrend.',
  },

  {
    id: 21,
    title: 'Lower Low Confirmation',
    difficulty: 'Intermediate',
    category: 'Market Structure',
    description:
      'Price falls below a previous swing low.',
    question:
      'What does this add to the bearish structure?',
    correct: 'SELL',
    explanation:
      'A new lower low strengthens the bearish structure and indicates that sellers have pushed price below the previous low.',
    lesson:
      'Lower lows are an important component of a downtrend.',
  },

  {
    id: 22,
    title: 'Volume Confirmation',
    difficulty: 'Intermediate',
    category: 'Volume',
    description:
      'Price breaks resistance while trading volume increases noticeably.',
    question:
      'What should this combination make you consider?',
    correct: 'BUY',
    explanation:
      'A breakout accompanied by increased volume can provide stronger confirmation than a breakout on very weak volume.',
    lesson:
      'Volume can help evaluate the strength behind a price move.',
  },

  {
    id: 23,
    title: 'Weak Breakout Volume',
    difficulty: 'Intermediate',
    category: 'Volume',
    description:
      'Price moves above resistance but volume remains unusually low.',
    question:
      'What should you consider?',
    correct: 'WAIT',
    explanation:
      'A weak-volume breakout may deserve additional confirmation because the move may not have strong participation behind it.',
    lesson:
      'Breakouts with weak participation can be more vulnerable to failure.',
  },

  {
    id: 24,
    title: 'Moving Average Trend',
    difficulty: 'Intermediate',
    category: 'Indicators',
    description:
      'Price is above a rising moving average and the broader structure is bullish.',
    question:
      'What does the combined picture suggest?',
    correct: 'BUY',
    explanation:
      'Price above a rising moving average supports the existing bullish structure. It should still be combined with proper risk management.',
    lesson:
      'Moving averages can help identify trend direction and dynamic areas of interest.',
  },

  {
    id: 25,
    title: 'Price Below Moving Average',
    difficulty: 'Intermediate',
    category: 'Indicators',
    description:
      'Price is below a declining moving average and the market is forming lower highs.',
    question:
      'What bias does the chart currently support?',
    correct: 'SELL',
    explanation:
      'The declining moving average and lower-high structure both support a bearish bias.',
    lesson:
      'Combining price structure with indicators can provide additional context.',
  },

  {
    id: 26,
    title: 'RSI Overbought',
    difficulty: 'Intermediate',
    category: 'RSI',
    description:
      'Price has risen strongly and RSI is in an overbought region.',
    question:
      'Should you automatically buy because price has been rising?',
    correct: 'WAIT',
    explanation:
      'An overbought RSI does not guarantee an immediate fall, but it can warn that price has moved strongly and deserves caution.',
    lesson:
      'Overbought does not automatically mean sell, and it does not guarantee a reversal.',
  },

  {
    id: 27,
    title: 'RSI Oversold',
    difficulty: 'Intermediate',
    category: 'RSI',
    description:
      'Price has fallen strongly and RSI is in an oversold region.',
    question:
      'Should you automatically buy?',
    correct: 'WAIT',
    explanation:
      'Oversold conditions can persist during strong downtrends. RSI should be combined with price structure and other evidence.',
    lesson:
      'Oversold does not automatically mean that price must rise.',
  },

  {
    id: 28,
    title: 'MACD Bullish Signal',
    difficulty: 'Intermediate',
    category: 'MACD',
    description:
      'The MACD shows a bullish crossover while price structure is beginning to improve.',
    question:
      'What should the signal be treated as?',
    correct: 'BUY',
    explanation:
      'A bullish MACD crossover combined with improving price structure can provide supportive evidence for a bullish setup.',
    lesson:
      'Indicators are most useful when interpreted together with price action.',
  },

  {
    id: 29,
    title: 'MACD Bearish Signal',
    difficulty: 'Intermediate',
    category: 'MACD',
    description:
      'MACD shows a bearish crossover while price is making lower highs.',
    question:
      'What direction does the combined evidence support?',
    correct: 'SELL',
    explanation:
      'The bearish MACD signal agrees with the declining price structure, creating a stronger bearish context.',
    lesson:
      'Agreement between price structure and indicators can strengthen a market hypothesis.',
  },

  {
    id: 30,
    title: 'Conflicting Indicators',
    difficulty: 'Intermediate',
    category: 'Indicators',
    description:
      'Price action appears bullish while one indicator gives a bearish signal.',
    question:
      'What should you do when signals conflict?',
    correct: 'WAIT',
    explanation:
      'Conflicting evidence means the setup is less clear. Waiting for stronger alignment can help avoid forcing a decision.',
    lesson:
      'Conflicting signals require careful analysis rather than automatic action.',
  },

  // ============================================================
  // ADVANCED — 31 to 42
  // ============================================================

  {
    id: 31,
    title: 'Breakout With Confirmation',
    difficulty: 'Advanced',
    category: 'Breakout',
    description:
      'Price breaks resistance, volume increases and the next candle remains above the breakout level.',
    question:
      'What does the combined evidence suggest?',
    correct: 'BUY',
    explanation:
      'Price breaking resistance, increased volume and sustained movement provide stronger breakout confirmation than price moving above resistance alone.',
    lesson:
      'Multiple confirming signals can strengthen a trading setup.',
  },

  {
    id: 32,
    title: 'Breakout Failure',
    difficulty: 'Advanced',
    category: 'Breakout',
    description:
      'Price breaks resistance but the following candles quickly return below the level.',
    question:
      'How should this situation be treated?',
    correct: 'SELL',
    explanation:
      'The failed breakout suggests rejection at the previous resistance. This can create a bearish warning.',
    lesson:
      'Always consider the possibility that a breakout can fail.',
  },

  {
    id: 33,
    title: 'Trend Pullback',
    difficulty: 'Advanced',
    category: 'Trend',
    description:
      'A stock is in an established uptrend but temporarily pulls back toward a previous support area.',
    question:
      'What should you analyze before considering a continuation trade?',
    correct: 'WAIT',
    explanation:
      'A pullback inside an uptrend can provide an opportunity, but confirmation that support is holding is important.',
    lesson:
      'A pullback is not automatically a reversal.',
  },

  {
    id: 34,
    title: 'Trend Reversal Warning',
    difficulty: 'Advanced',
    category: 'Reversal',
    description:
      'An established uptrend begins forming lower highs and breaks an important support area.',
    question:
      'What should you recognize?',
    correct: 'SELL',
    explanation:
      'The change from higher highs to lower highs combined with a support breakdown can indicate that the previous bullish structure is weakening.',
    lesson:
      'A trend can change when market structure changes significantly.',
  },

  {
    id: 35,
    title: 'Bullish Divergence',
    difficulty: 'Advanced',
    category: 'Divergence',
    description:
      'Price forms a lower low while an oscillator forms a higher low.',
    question:
      'What does this potentially warn about?',
    correct: 'WAIT',
    explanation:
      'Bullish divergence can indicate weakening downward momentum, but it is not a guaranteed reversal signal. Confirmation remains important.',
    lesson:
      'Divergence can warn that momentum and price are behaving differently.',
  },

  {
    id: 36,
    title: 'Bearish Divergence',
    difficulty: 'Advanced',
    category: 'Divergence',
    description:
      'Price forms a higher high while an oscillator forms a lower high.',
    question:
      'What should you recognize?',
    correct: 'WAIT',
    explanation:
      'Bearish divergence can indicate weakening upward momentum. It should be treated as a warning rather than a guaranteed reversal.',
    lesson:
      'Bearish divergence can warn of weakening bullish momentum.',
  },

  {
    id: 37,
    title: 'High Volatility',
    difficulty: 'Advanced',
    category: 'Volatility',
    description:
      'Candles suddenly become much larger and price swings rapidly in both directions.',
    question:
      'What should you consider before entering?',
    correct: 'WAIT',
    explanation:
      'High volatility can make entries and stop-loss placement more difficult. Waiting for conditions to stabilize can be a disciplined approach.',
    lesson:
      'Higher volatility generally means larger and faster price movements.',
  },

  {
    id: 38,
    title: 'Volume Spike Without Direction',
    difficulty: 'Advanced',
    category: 'Volume',
    description:
      'Trading volume suddenly becomes very high, but price closes near its starting point.',
    question:
      'How should you interpret this immediately?',
    correct: 'WAIT',
    explanation:
      'A large volume spike without clear directional movement can indicate strong activity but not necessarily a clear direction.',
    lesson:
      'High volume does not automatically mean bullish or bearish.',
  },

  {
    id: 39,
    title: 'Risk Before Entry',
    difficulty: 'Advanced',
    category: 'Risk Management',
    description:
      'A potential setup looks attractive, but there is no clear logical location for a stop-loss.',
    question:
      'What should you do?',
    correct: 'WAIT',
    explanation:
      'A trade should have a clearly considered risk point before entry. If risk cannot be defined logically, waiting is preferable.',
    lesson:
      'Risk planning should happen before trade execution.',
  },

  {
    id: 40,
    title: 'Late Entry',
    difficulty: 'Advanced',
    category: 'Trade Management',
    description:
      'A breakout has already moved a long distance from the breakout level.',
    question:
      'What should you consider before entering late?',
    correct: 'WAIT',
    explanation:
      'Entering far from the original setup can worsen the risk-to-reward relationship. Waiting for a better structure may be more disciplined.',
    lesson:
      'A missed entry is often better than forcing a poor entry.',
  },

  {
    id: 41,
    title: 'Risk Reward Check',
    difficulty: 'Advanced',
    category: 'Risk Management',
    description:
      'A setup offers a potential reward that is smaller than the amount being risked.',
    question:
      'What should you consider?',
    correct: 'WAIT',
    explanation:
      'A poor risk-to-reward relationship can make a setup unattractive even if the market direction appears correct.',
    lesson:
      'Risk and potential reward should be evaluated before entering a trade.',
  },

  {
    id: 42,
    title: 'Strong Trend Near Resistance',
    difficulty: 'Advanced',
    category: 'Multi-Signal Analysis',
    description:
      'The trend is strongly bullish, but price is now very close to a major resistance zone.',
    question:
      'How should the conflicting information be handled?',
    correct: 'WAIT',
    explanation:
      'The bullish trend supports buyers, while nearby resistance creates caution. Waiting for price to show whether resistance breaks or rejects can improve the analysis.',
    lesson:
      'Multiple valid signals can still conflict with one another.',
  },

  // ============================================================
  // EXPERT — 43 to 50
  // ============================================================

  {
    id: 43,
    title: 'Multiple Confirmation Setup',
    difficulty: 'Expert',
    category: 'Multi-Signal Analysis',
    description:
      'Price is in an uptrend, breaks resistance, volume expands and the breakout level holds during a retest.',
    question:
      'What does the overall setup suggest?',
    correct: 'BUY',
    explanation:
      'Trend direction, breakout, volume and successful retest all point in the same direction. This is stronger than relying on one signal alone.',
    lesson:
      'High-quality setups often involve several pieces of evidence aligning.',
  },

  {
    id: 44,
    title: 'Conflicting Market Evidence',
    difficulty: 'Expert',
    category: 'Multi-Signal Analysis',
    description:
      'Price is bullish, but momentum is weakening and the stock is approaching major resistance.',
    question:
      'What is the disciplined response?',
    correct: 'WAIT',
    explanation:
      'The evidence is mixed. Rather than forcing a trade, wait for the market to provide clearer confirmation.',
    lesson:
      'A professional decision can be to remain inactive when evidence is conflicting.',
  },

  {
    id: 45,
    title: 'Protecting an Open Position',
    difficulty: 'Expert',
    category: 'Trade Management',
    description:
      'A long position is profitable, but price begins showing signs of weakening near resistance.',
    question:
      'What should be considered first?',
    correct: 'SELL',
    explanation:
      'When an open position reaches an important resistance area and momentum weakens, protecting some or all of the position may deserve consideration.',
    lesson:
      'Managing an existing position is different from finding a new entry.',
  },

  {
    id: 46,
    title: 'Stop Loss Discipline',
    difficulty: 'Expert',
    category: 'Risk Management',
    description:
      'Your trade reaches the predetermined stop-loss level.',
    question:
      'What is the disciplined response?',
    correct: 'SELL',
    explanation:
      'If the predetermined risk level is reached, following the original risk plan is generally more disciplined than moving the stop simply to avoid realizing a loss.',
    lesson:
      'A stop-loss should be part of the trade plan before the trade begins.',
  },

  {
    id: 47,
    title: 'Emotional Revenge Trade',
    difficulty: 'Expert',
    category: 'Trading Psychology',
    description:
      'You have just experienced a loss and immediately see another uncertain setup.',
    question:
      'What should you consider doing?',
    correct: 'WAIT',
    explanation:
      'Trading immediately to recover a previous loss can lead to emotional decision-making. A pause can help restore objectivity.',
    lesson:
      'A previous loss should not determine the next trading decision.',
  },

  {
    id: 48,
    title: 'Overconfidence After Winning',
    difficulty: 'Expert',
    category: 'Trading Psychology',
    description:
      'You have had several successful trades and feel confident enough to increase risk substantially on the next trade.',
    question:
      'What is the disciplined response?',
    correct: 'WAIT',
    explanation:
      'A winning streak does not guarantee the next trade will succeed. Increasing risk because of recent success can create unnecessary exposure.',
    lesson:
      'Confidence should not replace a consistent risk-management process.',
  },

  {
    id: 49,
    title: 'Sudden Market Shock',
    difficulty: 'Expert',
    category: 'Market Risk',
    description:
      'A sudden event causes extremely large candles and rapid price movement.',
    question:
      'What should be prioritized before taking a new position?',
    correct: 'WAIT',
    explanation:
      'During a sudden market shock, volatility and uncertainty can increase dramatically. Understanding the new market conditions should come before taking a fresh position.',
    lesson:
      'Unexpected events can rapidly change market conditions.',
  },

  {
    id: 50,
    title: 'Complete Trader Decision',
    difficulty: 'Expert',
    category: 'Full Scenario',
    description:
      'Price is in an uptrend and has broken resistance with strong volume, but the move has already become extended and the next resistance area is close.',
    question:
      'What is the most disciplined decision?',
    correct: 'WAIT',
    explanation:
      'Several signals are bullish, but entering after an extended move with nearby resistance can create an unfavorable setup. A disciplined trader can wait for a better entry or confirmation.',
    lesson:
      'Good trading is not simply about finding bullish or bearish signals. Entry quality, risk and context matter.',
    candles: [
      [18, 190, 160, 178, 166],
      [58, 176, 142, 160, 148],
      [98, 158, 124, 145, 132],
      [138, 142, 105, 130, 112],
      [178, 125, 92, 110, 100],
      [218, 116, 78, 98, 84],
      [258, 105, 66, 82, 72],
      [298, 94, 50, 70, 58],
      [338, 80, 36, 55, 44],
      [378, 64, 22, 40, 28],
      [418, 54, 15, 28, 18],
      [458, 45, 10, 20, 12],
    ],
    resistance: 25,
    support: 190,
  },
]

function ScenarioChart({ scenario }) {
  const width = 520
  const height = 260
  const candleWidth = 14

  // ------------------------------------------------------------
  // Generate a visual chart when a scenario does not provide
  // its own candle data.
  // ------------------------------------------------------------

  const generateCandles = () => {
  const category = scenario.category?.toLowerCase() || ''
  const title = scenario.title?.toLowerCase() || ''

  // ------------------------------------------------------------
  // Helper
  // ------------------------------------------------------------
  const makeCandles = (values) =>
    values.map(([high, low, open, close], index) => [
      18 + index * 40,
      high,
      low,
      open,
      close,
    ])

  // ------------------------------------------------------------
  // UPTREND
  // Higher highs + higher lows
  // ------------------------------------------------------------
  if (
    category.includes('trend') &&
    !title.includes('downtrend') &&
    !title.includes('falling')
  ) {
    return makeCandles([
      [190, 160, 178, 168],
      [175, 145, 164, 152],
      [160, 130, 148, 138],
      [150, 118, 136, 122],
      [135, 102, 120, 108],
      [125, 88, 110, 94],
      [112, 76, 92, 82],
      [102, 64, 80, 70],
      [90, 52, 68, 58],
      [80, 42, 56, 48],
      [70, 30, 46, 36],
      [58, 20, 34, 25],
    ])
  }

  // ------------------------------------------------------------
  // DOWNTREND
  // Lower highs + lower lows
  // ------------------------------------------------------------
  if (
    category.includes('trend') &&
    (
      title.includes('downtrend') ||
      title.includes('falling')
    )
  ) {
    return makeCandles([
      [40, 18, 28, 36],
      [58, 25, 38, 52],
      [72, 35, 50, 65],
      [88, 46, 62, 80],
      [105, 58, 78, 96],
      [120, 70, 94, 110],
      [138, 82, 108, 128],
      [152, 96, 126, 144],
      [168, 110, 142, 158],
      [182, 122, 156, 174],
      [194, 135, 172, 188],
      [205, 148, 186, 198],
    ])
  }

  // ------------------------------------------------------------
  // SIDEWAYS MARKET
  // ------------------------------------------------------------
  if (
    category.includes('market structure') ||
    title.includes('sideways')
  ) {
    return makeCandles([
      [120, 82, 105, 94],
      [108, 72, 92, 104],
      [125, 84, 105, 92],
      [112, 70, 88, 106],
      [122, 78, 106, 90],
      [110, 68, 88, 104],
      [124, 80, 104, 92],
      [114, 70, 90, 108],
      [126, 82, 108, 94],
      [112, 68, 92, 104],
      [120, 76, 104, 88],
      [110, 65, 86, 100],
    ])
  }

  // ------------------------------------------------------------
  // SUPPORT BOUNCE
  // Falling price → support → bullish reaction
  // ------------------------------------------------------------
  if (
    category.includes('support') ||
    title.includes('support')
  ) {
    return makeCandles([
      [70, 42, 55, 64],
      [82, 50, 66, 76],
      [96, 62, 78, 90],
      [110, 76, 92, 102],
      [125, 90, 106, 116],
      [140, 104, 120, 132],
      [154, 118, 136, 146],
      [170, 132, 150, 158],
      [184, 145, 162, 178],
      [190, 150, 178, 158],
      [180, 128, 158, 138],
      [162, 110, 136, 118],
    ])
  }

  // ------------------------------------------------------------
  // BREAKOUT
  // Consolidation → resistance break
  // ------------------------------------------------------------
  if (
    category.includes('breakout') ||
    title.includes('breakout')
  ) {
    return makeCandles([
      [150, 112, 130, 142],
      [146, 108, 140, 120],
      [148, 110, 120, 142],
      [145, 106, 140, 118],
      [150, 108, 120, 145],
      [148, 105, 142, 118],
      [151, 108, 120, 144],
      [148, 102, 142, 112],
      [135, 84, 112, 92],
      [118, 62, 90, 70],
      [98, 42, 68, 50],
      [76, 24, 48, 32],
    ])
  }

  // ------------------------------------------------------------
  // BREAKDOWN
  // Support → strong downward break
  // ------------------------------------------------------------
  if (
    category.includes('breakdown') ||
    title.includes('breakdown')
  ) {
    return makeCandles([
      [70, 42, 55, 64],
      [76, 48, 64, 54],
      [72, 44, 52, 68],
      [78, 50, 68, 58],
      [74, 46, 58, 70],
      [76, 48, 70, 54],
      [80, 50, 54, 74],
      [82, 52, 74, 60],
      [100, 65, 62, 94],
      [125, 82, 96, 118],
      [152, 105, 120, 145],
      [180, 126, 148, 170],
    ])
  }

  // ------------------------------------------------------------
  // REVERSAL
  // Downward movement → rejection → upward movement
  // ------------------------------------------------------------
  if (
    category.includes('reversal') ||
    title.includes('reversal')
  ) {
    return makeCandles([
      [65, 38, 48, 60],
      [82, 48, 62, 76],
      [100, 60, 78, 94],
      [120, 74, 96, 112],
      [140, 88, 114, 132],
      [158, 105, 134, 150],
      [170, 122, 148, 132],
      [156, 112, 132, 118],
      [145, 98, 118, 104],
      [130, 82, 104, 90],
      [118, 68, 90, 76],
      [105, 55, 76, 62],
    ])
  }

  // ------------------------------------------------------------
  // VOLUME
  // Price move with stronger final candles
  // ------------------------------------------------------------
  if (
    category.includes('volume')
  ) {
    return makeCandles([
      [170, 145, 158, 150],
      [165, 140, 150, 158],
      [160, 136, 158, 142],
      [162, 138, 142, 155],
      [158, 132, 154, 140],
      [160, 135, 140, 152],
      [155, 128, 150, 136],
      [150, 120, 136, 145],
      [140, 100, 126, 108],
      [118, 72, 106, 82],
      [92, 42, 80, 52],
      [66, 20, 50, 28],
    ])
  }

  // ------------------------------------------------------------
  // RSI / MACD / INDICATORS
  // General directional chart
  // ------------------------------------------------------------
  if (
    category.includes('rsi') ||
    category.includes('macd') ||
    category.includes('indicator')
  ) {
    return makeCandles([
      [185, 155, 172, 162],
      [172, 140, 160, 148],
      [158, 126, 146, 134],
      [150, 112, 132, 120],
      [138, 102, 120, 108],
      [128, 92, 108, 98],
      [118, 82, 98, 88],
      [110, 72, 88, 80],
      [102, 62, 80, 70],
      [94, 54, 70, 62],
      [88, 46, 62, 52],
      [80, 38, 52, 44],
    ])
  }

  // ------------------------------------------------------------
  // DIVERGENCE
  // Price continues making new extremes
  // ------------------------------------------------------------
  if (
    category.includes('divergence')
  ) {
    return makeCandles([
      [70, 40, 54, 64],
      [86, 50, 66, 80],
      [100, 62, 82, 94],
      [118, 74, 96, 110],
      [135, 86, 112, 128],
      [150, 98, 130, 142],
      [164, 108, 144, 156],
      [178, 118, 158, 170],
      [190, 126, 172, 182],
      [184, 116, 180, 130],
      [172, 104, 132, 118],
      [160, 92, 120, 100],
    ])
  }

  // ------------------------------------------------------------
  // VOLATILITY / MARKET SHOCK
  // Large candles and rapid movement
  // ------------------------------------------------------------
  if (
    category.includes('volatility') ||
    category.includes('market risk') ||
    title.includes('shock')
  ) {
    return makeCandles([
      [130, 95, 112, 102],
      [120, 82, 100, 114],
      [145, 70, 112, 78],
      [180, 52, 82, 155],
      [205, 78, 158, 92],
      [190, 42, 86, 165],
      [215, 90, 170, 108],
      [200, 35, 110, 180],
      [185, 72, 178, 92],
      [220, 45, 96, 190],
      [195, 58, 188, 82],
      [170, 38, 80, 150],
    ])
  }

  // ------------------------------------------------------------
  // TRADING PSYCHOLOGY
  // Moderate trend with uncertainty
  // ------------------------------------------------------------
  if (
    category.includes('psychology')
  ) {
    return makeCandles([
      [155, 120, 138, 128],
      [142, 108, 126, 116],
      [150, 105, 118, 142],
      [160, 112, 140, 122],
      [148, 98, 120, 136],
      [158, 104, 138, 112],
      [170, 110, 114, 156],
      [162, 96, 154, 104],
      [176, 108, 106, 164],
      [168, 92, 160, 116],
      [182, 100, 118, 170],
      [175, 88, 168, 104],
    ])
  }

  // ------------------------------------------------------------
  // RISK MANAGEMENT / TRADE MANAGEMENT
  // Clear trade movement
  // ------------------------------------------------------------
  if (
    category.includes('risk') ||
    category.includes('trade management')
  ) {
    return makeCandles([
      [175, 145, 160, 150],
      [164, 130, 148, 138],
      [152, 118, 136, 125],
      [140, 105, 124, 112],
      [130, 92, 110, 100],
      [120, 82, 98, 90],
      [110, 72, 88, 78],
      [104, 65, 76, 96],
      [112, 72, 98, 82],
      [122, 80, 84, 114],
      [135, 92, 116, 102],
      [148, 104, 106, 136],
    ])
  }

  // ------------------------------------------------------------
  // FULL SCENARIO / MULTI-SIGNAL
  // Strong uptrend + breakout
  // ------------------------------------------------------------
  if (
    category.includes('full scenario') ||
    category.includes('multi-signal')
  ) {
    return makeCandles([
      [190, 158, 178, 166],
      [176, 140, 164, 148],
      [160, 124, 146, 132],
      [150, 108, 130, 116],
      [138, 94, 114, 102],
      [126, 82, 100, 90],
      [116, 70, 88, 78],
      [108, 60, 76, 68],
      [100, 48, 66, 54],
      [82, 32, 52, 38],
      [64, 18, 36, 24],
      [52, 10, 22, 14],
    ])
  }

  // ------------------------------------------------------------
  // DEFAULT
  // ------------------------------------------------------------
  return makeCandles([
    [180, 150, 165, 155],
    [170, 140, 155, 162],
    [164, 130, 160, 145],
    [152, 120, 142, 148],
    [145, 108, 148, 124],
    [138, 98, 120, 132],
    [130, 92, 132, 108],
    [122, 82, 106, 116],
    [114, 74, 116, 94],
    [108, 66, 92, 102],
    [100, 58, 102, 76],
    [94, 48, 74, 86],
  ])
  }

  const candles = generateCandles()

  return (
    <div className="w-full overflow-x-auto">
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        className="w-full max-w-[520px]"
      >
        {candles.map(([x, high, low, open, close], index) => {
          const bullish = close >= open
          const bodyTop = height - Math.max(open, close)
          const bodyHeight = Math.max(Math.abs(close - open), 3)

          return (
            <g key={index}>
              <line
                x1={x}
                y1={height - high}
                x2={x}
                y2={height - low}
                stroke="currentColor"
                strokeWidth="2"
              />

              <rect
                x={x - candleWidth / 2}
                y={bodyTop}
                width={candleWidth}
                height={bodyHeight}
                fill={bullish ? "#22c55e" : "#ef4444"}
                rx="2"
              />
            </g>
          )
        })}
      </svg>
    </div>
  )
}

export default function PracticeLab() {
  const navigate = useNavigate()

  const [scenarioIndex, setScenarioIndex] = useState(0)
  const [selected, setSelected] = useState(null)
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState(0)

  const scenario = SCENARIOS[scenarioIndex]

  const progress = useMemo(() => {
    return ((scenarioIndex + 1) / SCENARIOS.length) * 100
  }, [scenarioIndex])

  const handleDecision = (decision) => {
    if (submitted) return

    setSelected(decision)
  }

  const submitDecision = () => {
    if (!selected || submitted) return

    setSubmitted(true)

    if (selected === scenario.correct) {
      setScore((value) => value + 1)
    }
  }

  const nextScenario = () => {
    if (scenarioIndex >= SCENARIOS.length - 1) {
      return
    }

    setScenarioIndex((value) => value + 1)
    setSelected(null)
    setSubmitted(false)
  }

  const restart = () => {
    setScenarioIndex(0)
    setSelected(null)
    setSubmitted(false)
    setScore(0)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const isCorrect = selected === scenario.correct

  return (
    <div className="space-y-6 pb-12">

      {/* Header */}
      <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-accent-blue/15 via-navy-900 to-accent-cyan/10 p-6 lg:p-8">

        <div className="absolute -top-24 -right-24 w-64 h-64 rounded-full bg-accent-cyan/10 blur-3xl" />

        <div className="relative">

          <button
            onClick={() => navigate('/app/dashboard')}
            className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors mb-6"
          >
            <ArrowLeft size={17} />
            Back to Dashboard
          </button>

          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5">

            <div>
              <div className="flex items-center gap-3 mb-3">

                <div className="w-12 h-12 rounded-2xl bg-accent-cyan/10 border border-accent-cyan/20 flex items-center justify-center">
                  <Activity
                    size={25}
                    className="text-accent-cyan"
                  />
                </div>

                <div>
                  <p className="text-xs font-semibold text-accent-cyan uppercase tracking-wider">
                    Trading Practice
                  </p>

                  <h1 className="text-2xl lg:text-3xl font-bold text-white">
                    Practice Lab
                  </h1>
                </div>

              </div>

              <p className="text-sm text-slate-400 max-w-2xl leading-6">
                Analyze simulated market situations and practice
                making trading decisions before using Virtual Trading.
              </p>
            </div>

            <div className="rounded-2xl bg-white/5 border border-white/10 px-5 py-4 min-w-[170px]">
              <p className="text-xs text-slate-500">
                Practice Score
              </p>

              <p className="text-2xl font-bold text-white mt-1">
                {score}
                <span className="text-sm text-slate-500">
                  /{SCENARIOS.length}
                </span>
              </p>
            </div>

          </div>

        </div>
      </section>

      {/* Progress */}
      <section className="card p-4">

        <div className="flex items-center justify-between mb-2">

          <span className="text-xs text-slate-500">
            Scenario {scenarioIndex + 1} of {SCENARIOS.length}
          </span>

          <span className="text-xs text-accent-cyan">
            {Math.round(progress)}%
          </span>

        </div>

        <div className="h-2 rounded-full bg-white/5 overflow-hidden">

          <div
            className="h-full bg-accent-cyan rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />

        </div>

      </section>

      {/* Scenario */}
      <section className="card overflow-hidden">

        <div className="p-5 lg:p-7 border-b border-white/10">

          <div className="flex flex-wrap items-center gap-2 mb-4">

            <span className="text-[10px] px-2.5 py-1 rounded-full bg-accent-cyan/10 border border-accent-cyan/20 text-accent-cyan font-semibold">
              {scenario.category}
            </span>

            <span className="text-[10px] px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-slate-400">
              {scenario.difficulty}
            </span>

          </div>

          <h2 className="text-xl lg:text-2xl font-bold text-white">
            {scenario.title}
          </h2>

          <p className="text-sm text-slate-400 mt-3 leading-6">
            {scenario.description}
          </p>

        </div>

        {/* Chart */}
        <div className="p-4 lg:p-7">

          <ScenarioChart scenario={scenario} />

          <div className="grid grid-cols-3 gap-3 mt-4">

            <div className="rounded-xl bg-white/5 border border-white/10 p-3">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <TrendingUp size={14} />
                Bullish
              </div>
              <p className="text-sm text-slate-300 mt-1">
                Buying pressure
              </p>
            </div>

            <div className="rounded-xl bg-white/5 border border-white/10 p-3">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <TrendingDown size={14} />
                Bearish
              </div>
              <p className="text-sm text-slate-300 mt-1">
                Selling pressure
              </p>
            </div>

            <div className="rounded-xl bg-white/5 border border-white/10 p-3">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <Clock size={14} />
                Mode
              </div>
              <p className="text-sm text-slate-300 mt-1">
                Simulation
              </p>
            </div>

          </div>

        </div>

        {/* Question */}
        <div className="p-5 lg:p-7 border-t border-white/10">

          <div className="flex items-start gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center shrink-0">
              <CircleHelp
                size={20}
                className="text-accent-blue"
              />
            </div>

            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">
                Your Decision
              </p>

              <h3 className="text-base lg:text-lg font-bold text-white mt-1">
                {scenario.question}
              </h3>
            </div>

          </div>

          {/* Decision buttons */}
          <div className="grid sm:grid-cols-3 gap-3">

            {[
              {
                value: 'BUY',
                label: 'Buy / Enter',
                icon: TrendingUp,
              },
              {
                value: 'WAIT',
                label: 'Wait / Observe',
                icon: Clock,
              },
              {
                value: 'SELL',
                label: 'Sell / Exit',
                icon: TrendingDown,
              },
            ].map((option) => {

              const Icon = option.icon

              const active =
                selected === option.value

              return (
                <button
                  key={option.value}
                  onClick={() =>
                    handleDecision(option.value)
                  }
                  disabled={submitted}
                  className={`rounded-2xl border p-4 text-left transition-all ${
                    active
                      ? 'border-accent-cyan bg-accent-cyan/10'
                      : 'border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/5'
                  } ${
                    submitted
                      ? 'cursor-default'
                      : 'cursor-pointer'
                  }`}
                >

                  <div className="flex items-center justify-between">

                    <div className="flex items-center gap-3">

                      <div className="w-9 h-9 rounded-xl bg-white/5 flex items-center justify-center">
                        <Icon
                          size={18}
                          className={
                            option.value === 'BUY'
                              ? 'text-emerald-400'
                              : option.value === 'SELL'
                                ? 'text-rose-400'
                                : 'text-slate-400'
                          }
                        />
                      </div>

                      <span className="text-sm font-semibold text-white">
                        {option.label}
                      </span>

                    </div>

                    {active && (
                      <CheckCircle2
                        size={18}
                        className="text-accent-cyan"
                      />
                    )}

                  </div>

                </button>
              )
            })}

          </div>

          {/* Submit */}
          {!submitted && (
            <button
              onClick={submitDecision}
              disabled={!selected}
              className="btn-primary w-full mt-5 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Evaluate My Decision
            </button>
          )}

        </div>

      </section>

      {/* Result */}
      {submitted && (
        <section
          className={`rounded-2xl border p-5 lg:p-7 ${
            isCorrect
              ? 'border-emerald-400/20 bg-emerald-400/5'
              : 'border-amber-400/20 bg-amber-400/5'
          }`}
        >

          <div className="flex items-start gap-4">

            <div
              className={`w-11 h-11 rounded-full flex items-center justify-center shrink-0 ${
                isCorrect
                  ? 'bg-emerald-400/10'
                  : 'bg-amber-400/10'
              }`}
            >
              {isCorrect ? (
                <CheckCircle2
                  size={23}
                  className="text-emerald-400"
                />
              ) : (
                <Target
                  size={23}
                  className="text-amber-400"
                />
              )}
            </div>

            <div className="flex-1">

              <h3 className="font-bold text-white">
                {isCorrect
                  ? 'Good Decision'
                  : 'Decision Review'}
              </h3>

              <p className="text-sm text-slate-300 mt-2 leading-6">
                The educational reference decision for this
                scenario was{' '}
                <span className="font-bold text-white">
                  {scenario.correct}
                </span>
                .
              </p>

              <div className="mt-4 rounded-xl bg-black/10 border border-white/10 p-4">

                <p className="text-xs font-semibold text-white mb-2">
                  Why?
                </p>

                <p className="text-sm text-slate-400 leading-6">
                  {scenario.explanation}
                </p>

              </div>

              <div className="mt-4 rounded-xl bg-black/10 border border-white/10 p-4">

                <p className="text-xs font-semibold text-accent-cyan mb-2">
                  Learning Point
                </p>

                <p className="text-sm text-slate-400 leading-6">
                  {scenario.lesson}
                </p>

              </div>

            </div>

          </div>

          <div className="flex flex-col sm:flex-row gap-3 mt-6">

            {scenarioIndex < SCENARIOS.length - 1 ? (
              <button
                onClick={nextScenario}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                Next Scenario
                <ArrowRight size={17} />
              </button>
            ) : (
              <button
                onClick={restart}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                <RotateCcw size={17} />
                Practice Again
              </button>
            )}

          </div>

        </section>
      )}

      {/* Educational note */}
      <div className="text-center max-w-3xl mx-auto">

        <p className="text-[11px] text-slate-600 leading-5">
          Practice Lab uses simulated educational scenarios.
          Its decisions are designed to teach market analysis
          and should not be treated as financial advice or
          predictions of real market outcomes.
        </p>

      </div>

    </div>
  )
}
