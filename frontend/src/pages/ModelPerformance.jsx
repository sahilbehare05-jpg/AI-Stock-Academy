import React, { useEffect, useState } from 'react'
import {
  Activity,
  BarChart3,
  Brain,
  CheckCircle2,
  RefreshCw,
  Target,
  TrendingDown,
  TrendingUp,
  XCircle,
} from 'lucide-react'
import { modelPerformanceAPI } from '../services/api'

const PERIODS = [
  { value: '6mo', label: '6 Months' },
  { value: '1y', label: '1 Year' },
  { value: '2y', label: '2 Years' },
  { value: '5y', label: '5 Years' },
]

function MetricCard({ label, value, icon: Icon }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
      <div className="flex items-center justify-between">
        <div className="text-xs uppercase tracking-wider text-slate-500">
          {label}
        </div>
        <Icon className="w-4 h-4 text-cyan-400" />
      </div>

      <div className="text-3xl font-bold text-white mt-3">
        {value}%
      </div>
    </div>
  )
}

function ModelPerformance() {
  const [symbol, setSymbol] = useState('AAPL')
  const [period, setPeriod] = useState('1y')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadPerformance = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await modelPerformanceAPI.getPerformance(
       symbol,
       period
)

      setData(response.data.data)
    } catch (err) {
      console.error(err)

      setData(null)

      setError(
        err?.response?.data?.detail ||
          'Unable to load model performance.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPerformance()
  }, [])

  const handleSubmit = (event) => {
    event.preventDefault()
    loadPerformance()
  }

  return (
    <div className="min-h-full pb-8">
      {/* HEADER */}

      <div className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center">
                <Brain className="w-5 h-5 text-cyan-400" />
              </div>

              <div>
                <h1 className="text-2xl lg:text-3xl font-bold text-white">
                  Model Performance
                </h1>

                <p className="text-sm text-slate-500 mt-1">
                  Evaluate the historical performance of the AI prediction model
                </p>
              </div>
            </div>
          </div>

          {/* CONTROLS */}

          <form
            onSubmit={handleSubmit}
            className="flex flex-wrap gap-2"
          >
            <input
              value={symbol}
              onChange={(e) =>
                setSymbol(e.target.value.toUpperCase())
              }
              placeholder="AAPL"
              className="w-24 rounded-xl bg-slate-950 border border-white/10 px-3 py-3 text-sm text-white outline-none focus:border-cyan-400/40"
            />

            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="rounded-xl bg-slate-950 border border-white/10 px-3 py-3 text-sm text-white outline-none"
            >
              {PERIODS.map((item) => (
                <option
                  key={item.value}
                  value={item.value}
                >
                  {item.label}
                </option>
              ))}
            </select>

            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 rounded-xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-300 disabled:opacity-50"
            >
              <RefreshCw
                className={`w-4 h-4 ${
                  loading ? 'animate-spin' : ''
                }`}
              />
              Evaluate
            </button>
          </form>
        </div>
      </div>

      {/* ERROR */}

      {error && (
        <div className="mb-6 rounded-xl border border-rose-400/20 bg-rose-400/5 px-4 py-3 text-sm text-rose-300">
          {error}
        </div>
      )}

      {/* LOADING */}

      {loading && !data && (
        <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-10 text-center">
          <RefreshCw className="w-7 h-7 text-cyan-400 animate-spin mx-auto" />
          <p className="text-sm text-slate-400 mt-3">
            Evaluating Random Forest on historical data...
          </p>
        </div>
      )}

      {data && (
        <>
          {/* MODEL INFO */}

          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 mb-6">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="text-xs uppercase tracking-wider text-slate-500">
                  Evaluated Model
                </div>

                <div className="text-xl font-bold text-white mt-1">
                  {data.model}
                </div>

                <div className="text-xs text-slate-500 mt-1">
                  {data.symbol} • {data.evaluation_period} •{' '}
                  {data.train_test_split}
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs text-emerald-400">
                <Activity className="w-4 h-4" />
                Real historical evaluation
              </div>
            </div>
          </div>

          {/* METRICS */}

          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
            <MetricCard
              label="Accuracy"
              value={data.metrics.accuracy}
              icon={Target}
            />

            <MetricCard
              label="Precision"
              value={data.metrics.precision}
              icon={CheckCircle2}
            />

            <MetricCard
              label="Recall"
              value={data.metrics.recall}
              icon={TrendingUp}
            />

            <MetricCard
              label="F1 Score"
              value={data.metrics.f1_score}
              icon={BarChart3}
            />
          </div>

          {/* RESULTS */}

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
            <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                Actual UP
              </div>

              <div className="text-2xl font-bold text-white mt-2">
                {data.results.actual_up}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <TrendingDown className="w-4 h-4 text-rose-400" />
                Actual DOWN
              </div>

              <div className="text-2xl font-bold text-white mt-2">
                {data.results.actual_down}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                Correct
              </div>

              <div className="text-2xl font-bold text-white mt-2">
                {data.results.correct_predictions}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <XCircle className="w-4 h-4 text-rose-400" />
                Incorrect
              </div>

              <div className="text-2xl font-bold text-white mt-2">
                {data.results.incorrect_predictions}
              </div>
            </div>
          </div>

          {/* CONFUSION MATRIX */}

          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 mb-6">
            <div className="flex items-center gap-2 mb-5">
              <BarChart3 className="w-4 h-4 text-cyan-400" />

              <h2 className="text-sm font-bold text-white">
                Confusion Matrix
              </h2>
            </div>

            <div className="grid grid-cols-3 text-center text-xs">
              <div />
              <div className="p-3 text-slate-500">
                Predicted UP
              </div>
              <div className="p-3 text-slate-500">
                Predicted DOWN
              </div>

              <div className="p-3 text-slate-500 text-left">
                Actual UP
              </div>

              <div className="rounded-xl bg-emerald-400/10 border border-emerald-400/10 p-5">
                <div className="text-2xl font-bold text-emerald-400">
                  {data.confusion_matrix.true_up}
                </div>
                <div className="text-[10px] text-slate-500 mt-1">
                  True UP
                </div>
              </div>

              <div className="rounded-xl bg-rose-400/10 border border-rose-400/10 p-5">
                <div className="text-2xl font-bold text-rose-400">
                  {data.confusion_matrix.false_down}
                </div>
                <div className="text-[10px] text-slate-500 mt-1">
                  Missed UP
                </div>
              </div>

              <div className="p-3 text-slate-500 text-left">
                Actual DOWN
              </div>

              <div className="rounded-xl bg-rose-400/10 border border-rose-400/10 p-5">
                <div className="text-2xl font-bold text-rose-400">
                  {data.confusion_matrix.false_up}
                </div>
                <div className="text-[10px] text-slate-500 mt-1">
                  False UP
                </div>
              </div>

              <div className="rounded-xl bg-emerald-400/10 border border-emerald-400/10 p-5">
                <div className="text-2xl font-bold text-emerald-400">
                  {data.confusion_matrix.true_down}
                </div>
                <div className="text-[10px] text-slate-500 mt-1">
                  True DOWN
                </div>
              </div>
            </div>
          </div>

          {/* DATASET INFORMATION */}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
              <h2 className="text-sm font-bold text-white mb-4">
                Evaluation Details
              </h2>

              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-500">
                    Training samples
                  </span>
                  <span className="text-white font-medium">
                    {data.training_samples}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-slate-500">
                    Testing samples
                  </span>
                  <span className="text-white font-medium">
                    {data.testing_samples}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-slate-500">
                    Evaluation period
                  </span>
                  <span className="text-white font-medium">
                    {data.evaluation_period}
                  </span>
                </div>

                <div className="pt-3 border-t border-white/10">
                  <div className="text-xs text-slate-500 mb-2">
                    Model features
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {data.features.map((feature) => (
                      <span
                        key={feature}
                        className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-xs text-slate-300"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-amber-400/10 bg-amber-400/5 p-5">
              <h2 className="text-sm font-bold text-amber-300 mb-3">
                How to interpret this
              </h2>

              <p className="text-sm text-slate-400 leading-6">
                These metrics measure how the Random Forest model
                performed on historical data that was kept separate
                from its training data.
              </p>

              <p className="text-sm text-slate-400 leading-6 mt-3">
                Historical model performance does not guarantee future
                prediction accuracy. Market conditions can change,
                and a model can perform differently on future data.
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default ModelPerformance