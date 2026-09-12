import React, { useState } from 'react'
import {
  Search,
  Brain,
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  RefreshCw,
  ShieldCheck,
  Minus,
} from 'lucide-react'
import { predictionAPI } from '../services/api'

export default function AIPrediction() {
  const [symbol, setSymbol] = useState('AAPL')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handlePredict = async () => {
    const cleanSymbol = symbol.trim().toUpperCase()

    if (!cleanSymbol) {
      setError('Please enter a stock symbol.')
      return
    }

    try {
      setLoading(true)
      setError('')
      setPrediction(null)

      const response = await predictionAPI.predict(cleanSymbol)

      setPrediction(response.data.data)
    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.detail ||
          'Unable to generate prediction. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const predictionValue = prediction?.prediction

  const isUp = predictionValue === 'UP'
  const isDown = predictionValue === 'DOWN'
  const isNeutral = predictionValue === 'NO STRONG SIGNAL'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
            <Brain size={23} className="text-accent-blue" />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              AI Prediction
            </h1>

            <p className="text-slate-400 mt-1">
              Machine-learning based stock direction prediction.
            </p>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="card p-5">
        <div className="grid grid-cols-1 md:grid-cols-[1fr_150px] gap-3">
          <div className="relative flex-1">
            <Search
              size={20}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
            />

            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handlePredict()
                }
              }}
              placeholder="Enter stock symbol..."
              className="input-field w-full pl-11"
            />
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="btn-primary min-w-[130px] min-h-[42px]"
          >
            {loading ? (
              <RefreshCw size={18} className="animate-spin" />
            ) : (
              <Brain size={18} />
            )}

            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </div>

        <p className="text-xs text-slate-500 mt-3">
          Examples: AAPL, MSFT, GOOGL, RELIANCE.NS, TCS.NS, INFY.NS
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-4 border border-red-500/30">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Empty state */}
      {!prediction && !loading && !error && (
        <div className="card p-10 text-center">
          <Brain
            size={48}
            className="mx-auto text-accent-blue mb-4"
          />

          <h2 className="text-xl font-bold text-white">
            Generate an AI Prediction
          </h2>

          <p className="text-slate-400 mt-2 max-w-lg mx-auto">
            Enter a stock symbol to analyze recent market data using
            the Random Forest prediction model.
          </p>
        </div>
      )}

      {/* Prediction result */}
      {prediction && (
        <>
          {/* Main prediction */}
          <div className="card p-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
              <div>
                <p className="text-sm text-slate-400">
                  AI Prediction for
                </p>

                <h2 className="text-3xl font-bold text-white mt-1">
                  {prediction.symbol}
                </h2>

                <div className="flex items-center gap-2 mt-3">
                  <ShieldCheck
                    size={16}
                    className="text-slate-400"
                  />

                  <span className="text-sm text-slate-400">
                    Model: {prediction.model}
                  </span>
                </div>
              </div>

              {/* Prediction badge */}
              <div
                className={`rounded-2xl border px-8 py-6 text-center ${
                  isUp
                    ? 'border-emerald-500/30 bg-emerald-500/10'
                    : isDown
                    ? 'border-red-500/30 bg-red-500/10'
                    : 'border-amber-500/30 bg-amber-500/10'
                }`}
              >
                {isUp ? (
                  <TrendingUp
                    size={38}
                    className="mx-auto text-emerald-400 mb-2"
                  />
                ) : isDown ? (
                  <TrendingDown
                    size={38}
                    className="mx-auto text-red-400 mb-2"
                  />
                ) : (
                  <Minus
                    size={38}
                    className="mx-auto text-amber-400 mb-2"
                  />
                )}

                <p
                  className={`text-3xl font-black ${
                    isUp
                      ? 'text-emerald-400'
                      : isDown
                      ? 'text-red-400'
                      : 'text-amber-400'
                  }`}
                >
                  {prediction.prediction}
                </p>

                <p className="text-sm text-slate-400 mt-1">
                  Direction
                </p>
              </div>
            </div>
          </div>

          {/* Confidence */}
          <div className="card p-5">
            <div className="flex justify-between items-center mb-3">
              <div>
                <p className="text-sm text-slate-400">
                  Model Confidence
                </p>

                <p className="text-2xl font-bold text-white mt-1">
                  {prediction.confidence}%
                </p>
              </div>

              <Activity
                size={22}
                className="text-accent-blue"
              />
            </div>

            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-accent-blue rounded-full transition-all"
                style={{
                  width: `${Math.min(
                    Number(prediction.confidence) || 0,
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

          {/* Features */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <BarChart3
                size={20}
                className="text-accent-blue"
              />

              <h3 className="font-bold text-white">
                Model Features
              </h3>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <FeatureCard
                label="Volatility 10"
                value={prediction.features?.volatility_10}
                suffix="%"
                isPercentage
              />

              <FeatureCard
                label="Volatility 20"
                value={prediction.features?.volatility_20}
                suffix="%"
                isPercentage
              />

              <FeatureCard
                label="High-Low Range"
                value={prediction.features?.high_low_range}
                suffix="%"
                isPercentage
              />

              <FeatureCard
                label="Open-Close Range"
                value={prediction.features?.open_close_range}
                suffix="%"
                isPercentage
              />
            </div>
          </div>

          {/* Model information */}
          <div className="card p-5">
            <h3 className="font-bold text-white">
              How this prediction works
            </h3>

            <p className="text-slate-400 text-sm leading-6 mt-2">
              The Random Forest model analyzes recent historical
              market data and uses volatility and daily price-range
              features to classify the expected direction of the
              next market session.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-5">
              <InfoItem
                title="Algorithm"
                value="Random Forest"
              />

              <InfoItem
                title="Prediction"
                value="UP / DOWN / NO STRONG SIGNAL"
              />

              <InfoItem
                title="Data Source"
                value="Yahoo Finance"
              />
            </div>
          </div>

          {/* Educational disclaimer */}
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
    </div>
  )
}

function FeatureCard({
  label,
  value,
  suffix = '',
  isPercentage = false,
}) {
  return (
    <div className="card p-5">
      <p className="text-sm text-slate-400">
        {label}
      </p>

      <p className="text-xl font-bold text-white mt-2">
        {formatFeatureValue(value, isPercentage)}
        {value !== null &&
          value !== undefined &&
          suffix}
      </p>
    </div>
  )
}

function InfoItem({ title, value }) {
  return (
    <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
      <p className="text-xs text-slate-500">
        {title}
      </p>

      <p className="text-sm font-semibold text-white mt-1">
        {value}
      </p>
    </div>
  )
}

function formatFeatureValue(value, isPercentage = false) {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  const number = Number(value)

  if (Number.isNaN(number)) {
    return 'N/A'
  }

  if (isPercentage) {
    return `${(number * 100).toFixed(2)}`
  }

  return number.toLocaleString('en-IN', {
    maximumFractionDigits: 4,
  })
}