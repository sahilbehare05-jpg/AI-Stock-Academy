import React, { useState } from 'react'
import {
  Search,
  Brain,
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  ShieldCheck,
  Minus,
} from 'lucide-react'
import { predictionAPI } from '../services/api'

export default function WhyPrediction() {
  const [symbol, setSymbol] = useState('AAPL')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const getExplanation = async (stockSymbol = symbol) => {
    const cleanSymbol = stockSymbol.trim().toUpperCase()

    if (!cleanSymbol) return

    setLoading(true)
    setError('')

    try {
      const response = await predictionAPI.explain(cleanSymbol)
      setData(response.data.data)
    } catch (err) {
      setData(null)
      setError(
        err.response?.data?.detail ||
          'Unable to generate prediction explanation.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    getExplanation()
  }

  const predictionIsUp = data?.prediction === 'UP'
  const predictionIsDown = data?.prediction === 'DOWN'
  const predictionIsNeutral = data?.prediction === 'NO STRONG SIGNAL'

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
            <Brain size={22} className="text-accent-blue" />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              Why This Prediction?
            </h1>

            <p className="text-slate-400 text-sm mt-1">
              Understand why the AI model predicted the stock direction.
            </p>
          </div>
        </div>
      </div>

      {/* Search */}
      <form onSubmit={handleSubmit} className="card p-5">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="Enter stock symbol e.g. AAPL"
              className="input-field pl-11 w-full"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary px-6"
          >
            <Brain size={17} />
            {loading ? 'Analyzing...' : 'Explain Prediction'}
          </button>
        </div>

        <p className="text-xs text-slate-500 mt-3">
          Examples: AAPL, MSFT, GOOGL, RELIANCE.NS, TCS.NS
        </p>
      </form>

      {/* Error */}
      {error && (
        <div className="card p-5 border border-accent-red/30">
          <p className="text-accent-red text-sm">
            {error}
          </p>
        </div>
      )}

      {/* Result */}
      {data && (
        <>
          {/* Prediction Summary */}
          <div className="card p-6">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">

              <div>
                <p className="text-slate-400 text-sm">
                  AI Prediction Analysis
                </p>

                <h2 className="text-3xl font-bold text-white mt-1">
                  {data.symbol}
                </h2>

                <div className="flex items-center gap-2 mt-3">
                  <ShieldCheck
                    size={17}
                    className="text-accent-blue"
                  />

                  <span className="text-slate-400">
                    Model: {data.model}
                  </span>
                </div>
              </div>

              {/* Prediction Badge */}
              <div
                className={`rounded-2xl border px-8 py-5 text-center ${
                  predictionIsUp
                    ? 'border-accent-green/30 bg-accent-green/10'
                    : predictionIsDown
                    ? 'border-accent-red/30 bg-accent-red/10'
                    : 'border-amber-500/30 bg-amber-500/10'
                }`}
              >
                {predictionIsUp ? (
                  <TrendingUp
                    size={30}
                    className="mx-auto text-accent-green mb-2"
                  />
                ) : predictionIsDown ? (
                  <TrendingDown
                    size={30}
                    className="mx-auto text-accent-red mb-2"
                  />
                ) : (
                  <Minus
                    size={30}
                    className="mx-auto text-amber-400 mb-2"
                  />
                )}

                <p
                  className={`text-2xl font-bold ${
                    predictionIsUp
                      ? 'text-accent-green'
                      : predictionIsDown
                      ? 'text-accent-red'
                      : 'text-amber-400'
                  }`}
                >
                  {data.prediction}
                </p>

                <p className="text-slate-400 text-sm mt-1">
                  Predicted Direction
                </p>
              </div>
            </div>
          </div>

          {/* Confidence */}
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">
                  Model Confidence
                </p>

                <p className="text-3xl font-bold text-white mt-1">
                  {data.confidence}%
                </p>
              </div>

              <Activity
                size={24}
                className="text-accent-blue"
              />
            </div>

            <div className="mt-5 h-3 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-accent-blue rounded-full transition-all"
                style={{
                  width: `${Math.min(
                    Number(data.confidence) || 0,
                    100
                  )}%`,
                }}
              />
            </div>

            <p className="text-xs text-slate-500 mt-3">
              This is the model's classification confidence, not a
              guarantee of future market movement.
            </p>
          </div>

          {/* AI Explanation */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-3">
              <Brain
                size={19}
                className="text-accent-blue"
              />

              <h2 className="text-lg font-semibold text-white">
                AI Explanation
              </h2>
            </div>

            <p className="text-slate-300 leading-7">
              {data.summary}
            </p>
          </div>

          {/* Indicators */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <BarChart3
                size={20}
                className="text-accent-blue"
              />

              <h2 className="text-lg font-semibold text-white">
                Model Feature Analysis
              </h2>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {data.indicators?.map((item) => (
                <div
                  key={item.indicator}
                  className="card card-hover p-5"
                >
                  <p className="text-sm text-slate-400">
                    {item.indicator}
                  </p>

                  <p className="text-2xl font-bold text-white mt-2">
                    {item.value}%
                  </p>

                  <p className="text-sm text-slate-400 leading-6 mt-3">
                    {item.explanation}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Current Features */}
          {data.features && (
            <div className="card p-6">
              <h2 className="text-lg font-semibold text-white mb-4">
                Current Model Features
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

                <Feature
                  label="Volatility 10"
                  value={formatPercentage(
                    data.features.volatility_10
                  )}
                />

                <Feature
                  label="Volatility 20"
                  value={formatPercentage(
                    data.features.volatility_20
                  )}
                />

                <Feature
                  label="High-Low Range"
                  value={formatPercentage(
                    data.features.high_low_range
                  )}
                />

                <Feature
                  label="Open-Close Range"
                  value={formatPercentage(
                    data.features.open_close_range
                  )}
                />

              </div>
            </div>
          )}

          {/* Method */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-white mb-3">
              How the AI makes this prediction
            </h2>

            <p className="text-slate-400 leading-7">
              The Random Forest model analyzes recent historical
              market data using volatility and daily price-range
              features. These features are used to classify the
              expected direction of the next market session.
            </p>

            <div className="grid md:grid-cols-3 gap-4 mt-5">

              <InfoBox
                title="Algorithm"
                value="Random Forest"
              />

              <InfoBox
                title="Prediction"
                value="UP / DOWN / NO STRONG SIGNAL"
              />

              <InfoBox
                title="Data Source"
                value="Yahoo Finance"
              />

            </div>
          </div>

          {/* Educational Disclaimer */}
          <div className="card p-4 border border-slate-800">
            <p className="text-xs text-slate-500 leading-5">
              <strong className="text-slate-400">
                Educational use:
              </strong>{' '}
              This prediction is generated by an experimental
              machine-learning model for learning and simulated
              trading purposes. It should not be treated as a
              guarantee or financial advice.
            </p>
          </div>
        </>
      )}

      {/* Initial state */}
      {!data && !loading && !error && (
        <div className="card p-10 text-center">
          <Brain
            size={42}
            className="mx-auto text-accent-blue mb-4"
          />

          <h2 className="text-lg font-semibold text-white">
            Understand the AI prediction
          </h2>

          <p className="text-slate-400 text-sm mt-2 max-w-lg mx-auto">
            Enter a stock symbol above to see the prediction,
            confidence, model features and the reasons behind
            the model's prediction.
          </p>
        </div>
      )}

    </div>
  )
}

function Feature({ label, value }) {
  return (
    <div className="rounded-xl border border-white/10 p-4">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="text-lg font-semibold text-white mt-1">
        {value}
      </p>
    </div>
  )
}

function InfoBox({ title, value }) {
  return (
    <div className="rounded-xl border border-white/10 p-4">
      <p className="text-xs text-slate-500">
        {title}
      </p>

      <p className="text-sm font-semibold text-white mt-1">
        {value}
      </p>
    </div>
  )
}

function formatPercentage(value) {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  const number = Number(value)

  if (Number.isNaN(number)) {
    return 'N/A'
  }

  return `${(number * 100).toFixed(2)}%`
}