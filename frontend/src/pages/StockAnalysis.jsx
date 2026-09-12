import React, { useMemo, useState } from 'react'
import {
  Search,
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  RefreshCw,
} from 'lucide-react'
import { stocksAPI } from '../services/api'

export default function StockAnalysis() {
  const [symbol, setSymbol] = useState('AAPL')
  const [period, setPeriod] = useState('1mo')
  const [stock, setStock] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchStock = async () => {
    const cleanSymbol = symbol.trim().toUpperCase()

    if (!cleanSymbol) {
      setError('Please enter a stock symbol.')
      return
    }

    try {
      setLoading(true)
      setError('')

      const response = await stocksAPI.getStock(
        cleanSymbol,
        period,
        '1d'
      )

      setStock(response.data.data)
    } catch (err) {
      console.error(err)
      setStock(null)
      setError(
        err.response?.data?.detail ||
          'Unable to fetch stock data. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const chartData = useMemo(() => {
    if (!stock?.history) return []

    return stock.history
      .filter((item) => item.close !== null)
      .slice(-30)
      .map((item) => ({
        date: item.Date || item.Datetime,
        close: Number(item.Close),
      }))
  }, [stock])

  const latest = stock?.latest

  const rsiStatus =
    latest?.rsi_14 == null
      ? 'N/A'
      : latest.rsi_14 >= 70
        ? 'Overbought'
        : latest.rsi_14 <= 30
          ? 'Oversold'
          : 'Neutral'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">
          Stock Analysis
        </h1>
        <p className="text-slate-400 mt-1">
          Analyze stock prices and technical indicators using market data.
        </p>
      </div>

      {/* Search */}
<div className="card p-5">
  <div className="grid grid-cols-1 md:grid-cols-[1fr_150px_140px] gap-3">
    <div className="relative">
      <Search
        size={20}
        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
      />

      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') fetchStock()
        }}
        placeholder="Enter symbol e.g. AAPL or RELIANCE.NS"
        className="input-field pl-10 w-full"
      />
    </div>

    <select
      value={period}
      onChange={(e) => setPeriod(e.target.value)}
      className="input-field w-full"
    >
      <option value="5d">5 Days</option>
      <option value="1mo">1 Month</option>
      <option value="3mo">3 Months</option>
      <option value="6mo">6 Months</option>
      <option value="1y">1 Year</option>
    </select>

    <button
      onClick={fetchStock}
      disabled={loading}
      className="btn-primary w-full min-h-[42px]"
    >
      {loading ? (
        <RefreshCw size={18} className="animate-spin" />
      ) : (
        <Search size={18} />
      )}

      {loading ? 'Loading...' : 'Analyze'}
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

      {/* Empty State */}
      {!stock && !loading && !error && (
        <div className="card p-10 text-center">
          <BarChart3
            size={48}
            className="mx-auto text-accent-blue mb-4"
          />

          <h2 className="text-xl font-bold text-white">
            Analyze a Stock
          </h2>

          <p className="text-slate-400 mt-2">
            Enter a stock symbol above to view price data and technical
            indicators.
          </p>
        </div>
      )}

      {/* Stock Result */}
      {stock && latest && (
        <>
          {/* Stock heading */}
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold text-white">
                {stock.symbol}
              </h2>

              <p className="text-slate-400">
                Latest market data
              </p>
            </div>

            <div className="badge badge-hold">
              {stock.period}
            </div>
          </div>

          {/* Price cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              label="Current Price"
              value={formatNumber(latest.close)}
              icon={<TrendingUp size={20} />}
            />

            <MetricCard
              label="Day High"
              value={formatNumber(latest.high)}
              icon={<TrendingUp size={20} />}
            />

            <MetricCard
              label="Day Low"
              value={formatNumber(latest.low)}
              icon={<TrendingDown size={20} />}
            />

            <MetricCard
              label="Volume"
              value={formatVolume(latest.volume)}
              icon={<BarChart3 size={20} />}
            />
          </div>

          {/* Indicators */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <IndicatorCard
              title="SMA 20"
              value={formatNumber(latest.sma_20)}
            />

            <IndicatorCard
              title="EMA 20"
              value={formatNumber(latest.ema_20)}
            />

            <IndicatorCard
              title="RSI 14"
              value={
                latest.rsi_14 == null
                  ? 'N/A'
                  : latest.rsi_14.toFixed(2)
              }
              subtitle={rsiStatus}
            />
          </div>

          {/* Simple chart */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="font-bold text-white">
                  Price History
                </h3>

                <p className="text-xs text-slate-500 mt-1">
                  Last {chartData.length} available sessions
                </p>
              </div>

              <Activity
                size={20}
                className="text-accent-blue"
              />
            </div>

            <div className="h-72 flex items-end gap-1 overflow-hidden">
              {chartData.map((point, index) => {
                const prices = chartData.map((x) => x.close)
                const min = Math.min(...prices)
                const max = Math.max(...prices)

                const height =
                  max === min
                    ? 50
                    : 10 +
                      ((point.close - min) / (max - min)) * 90

                return (
                  <div
                    key={`${point.date}-${index}`}
                    className="flex-1 min-w-[4px] h-full flex items-end group"
                    title={`${point.date}: ${formatNumber(point.close)}`}
                  >
                    <div
                      className="w-full rounded-t bg-accent-blue/70 group-hover:bg-accent-blue transition-all"
                      style={{ height: `${height}%` }}
                    />
                  </div>
                )
              })}
            </div>
          </div>

          {/* OHLC */}
          <div className="card p-5">
            <h3 className="font-bold text-white mb-4">
              Latest Session
            </h3>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <DataItem label="Open" value={latest.open} />
              <DataItem label="High" value={latest.high} />
              <DataItem label="Low" value={latest.low} />
              <DataItem label="Close" value={latest.close} />
              <DataItem label="Volume" value={latest.volume} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}

function MetricCard({ label, value, icon }) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-400">{label}</span>
        <span className="text-accent-blue">{icon}</span>
      </div>

      <div className="text-2xl font-bold text-white mt-3">
        {value}
      </div>
    </div>
  )
}

function IndicatorCard({ title, value, subtitle }) {
  return (
    <div className="card p-5">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="text-2xl font-bold text-white mt-2">
        {value}
      </p>

      {subtitle && (
        <p className="text-xs text-slate-500 mt-1">
          {subtitle}
        </p>
      )}
    </div>
  )
}

function DataItem({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="font-semibold text-white mt-1">
        {label === 'Volume'
          ? formatVolume(value)
          : formatNumber(value)}
      </p>
    </div>
  )
}

function formatNumber(value) {
  if (value === null || value === undefined) return 'N/A'

  return Number(value).toLocaleString('en-IN', {
    maximumFractionDigits: 2,
  })
}

function formatVolume(value) {
  if (value === null || value === undefined) return 'N/A'

  const number = Number(value)

  if (number >= 10000000) {
    return `${(number / 10000000).toFixed(2)} Cr`
  }

  if (number >= 100000) {
    return `${(number / 100000).toFixed(2)} L`
  }

  if (number >= 1000) {
    return `${(number / 1000).toFixed(2)}K`
  }

  return number.toLocaleString('en-IN')
}