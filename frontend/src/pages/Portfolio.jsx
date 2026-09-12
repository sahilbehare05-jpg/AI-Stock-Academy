import React, { useEffect, useState } from 'react'
import {
  Briefcase,
  RefreshCw,
  TrendingUp,
  TrendingDown,
  IndianRupee,
} from 'lucide-react'
import api from '../services/api'

export default function Portfolio() {
  const [portfolio, setPortfolio] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadPortfolio = async (showLoading = true) => {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')

      const response = await api.get('/api/portfolio')
      setPortfolio(response.data.data)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to load portfolio.'
      )
    } finally {
      if (showLoading) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    loadPortfolio()

    // Refresh live P&L every 15 seconds
    const interval = setInterval(() => {
      loadPortfolio(false)
    }, 15000)

    return () => clearInterval(interval)
  }, [])

  const holdings = portfolio?.holdings || []

  const totalInvested = Number(
    portfolio?.total_invested || 0
  )

  const totalValue = Number(
    portfolio?.total_value || 0
  )

  const totalPnl = Number(
    portfolio?.total_pnl || 0
  )

  const totalPnlPercent = Number(
    portfolio?.total_pnl_percent || 0
  )

  const formatINR = (amount) =>
    new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(Number(amount) || 0)

  const isProfit = totalPnl >= 0

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

        <div>
          <div className="flex items-center gap-3">

            <div className="w-11 h-11 rounded-xl bg-accent-blue/10 text-accent-blue flex items-center justify-center">
              <Briefcase size={22} />
            </div>

            <div>
              <h1 className="text-2xl font-bold text-white">
                My Portfolio
              </h1>

              <p className="text-sm text-slate-400 mt-1">
                Track your virtual stock holdings and live performance.
              </p>
            </div>

          </div>
        </div>

        <div className="flex items-center gap-3">

          <span className="text-xs text-slate-500">
            Live P&L updates every 15 sec
          </span>

          <button
            onClick={() => loadPortfolio()}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 text-slate-300 hover:text-white hover:bg-white/5 transition"
          >
            <RefreshCw
              size={16}
              className={loading ? 'animate-spin' : ''}
            />

            Refresh
          </button>

        </div>

      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-accent-red/25 bg-accent-red/10 px-4 py-3 text-sm text-accent-red">
          {error}
        </div>
      )}

      {/* Portfolio Summary */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">

        {/* Invested */}
        <div className="card p-5">

          <p className="text-sm text-slate-400">
            Total Invested
          </p>

          <p className="text-2xl font-bold text-white mt-2">
            {formatINR(totalInvested)}
          </p>

        </div>

        {/* Current Value */}
        <div className="card p-5">

          <p className="text-sm text-slate-400">
            Current Market Value
          </p>

          <p className="text-2xl font-bold text-white mt-2">
            {formatINR(totalValue)}
          </p>

        </div>

        {/* P&L */}
        <div className="card p-5">

          <p className="text-sm text-slate-400">
            Total P&L
          </p>

          <div className="flex items-center gap-2 mt-2">

            {isProfit ? (
              <TrendingUp
                size={22}
                className="text-accent-green"
              />
            ) : (
              <TrendingDown
                size={22}
                className="text-accent-red"
              />
            )}

            <p
              className={`text-2xl font-bold ${
                isProfit
                  ? 'text-accent-green'
                  : 'text-accent-red'
              }`}
            >
              {isProfit ? '+' : ''}
              {formatINR(totalPnl)}
            </p>

          </div>

        </div>

        {/* P&L Percentage */}
        <div className="card p-5">

          <p className="text-sm text-slate-400">
            P&L Percentage
          </p>

          <p
            className={`text-2xl font-bold mt-2 ${
              isProfit
                ? 'text-accent-green'
                : 'text-accent-red'
            }`}
          >
            {isProfit ? '+' : ''}
            {totalPnlPercent.toFixed(2)}%
          </p>

        </div>

      </div>

      {/* Holdings */}
      <div className="card p-6">

        <div className="mb-5">

          <h2 className="text-lg font-semibold text-white">
            Current Holdings
          </h2>

          <p className="text-sm text-slate-400 mt-1">
            Live market value and profit/loss of your virtual holdings.
          </p>

        </div>

        {loading ? (

          <div className="text-center py-12 text-slate-400">
            Loading portfolio...
          </div>

        ) : holdings.length === 0 ? (

          <div className="text-center py-12">

            <Briefcase
              size={38}
              className="mx-auto text-slate-600 mb-3"
            />

            <p className="text-slate-300 font-medium">
              No holdings yet
            </p>

            <p className="text-sm text-slate-500 mt-1">
              Buy stocks from Virtual Trading to see them here.
            </p>

          </div>

        ) : (

          <div className="space-y-3">

            {holdings.map((holding) => {

              const pnl = Number(
                holding.pnl || 0
              )

              const pnlPercent = Number(
                holding.pnl_percent || 0
              )

              const investedValue = Number(
                holding.invested_value || 0
              )

              const marketValue = Number(
                holding.market_value || 0
              )

              const currentPrice = Number(
                holding.current_price || 0
              )

              const averagePrice = Number(
                holding.average_price || 0
              )

              const profitable = pnl >= 0

              return (

                <div
                  key={holding.symbol}
                  className="rounded-xl border border-white/10 p-5 hover:bg-white/[0.02] transition"
                >

                  {/* Stock Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">

                    <div>

                      <div className="flex items-center gap-2">

                        <p className="text-lg font-bold text-white">
                          {holding.symbol}
                        </p>

                        {profitable ? (
                          <TrendingUp
                            size={18}
                            className="text-accent-green"
                          />
                        ) : (
                          <TrendingDown
                            size={18}
                            className="text-accent-red"
                          />
                        )}

                      </div>

                      <p className="text-xs text-slate-500">
                        {holding.quantity} shares
                      </p>

                    </div>

                    <div className="text-right">

                      <p className="text-xs text-slate-500">
                        Current P&L
                      </p>

                      <p
                        className={`text-lg font-bold ${
                          profitable
                            ? 'text-accent-green'
                            : 'text-accent-red'
                        }`}
                      >
                        {profitable ? '+' : ''}
                        {formatINR(pnl)}
                      </p>

                      <p
                        className={`text-xs ${
                          profitable
                            ? 'text-accent-green'
                            : 'text-accent-red'
                        }`}
                      >
                        {profitable ? '+' : ''}
                        {pnlPercent.toFixed(2)}%
                      </p>

                    </div>

                  </div>

                  {/* Holding Details */}
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">

                    <div>

                      <p className="text-xs text-slate-500">
                        Average Buy
                      </p>

                      <p className="text-sm font-semibold text-white mt-1">
                        {formatINR(averagePrice)}
                      </p>

                    </div>

                    <div>

                      <p className="text-xs text-slate-500">
                        Live Price
                      </p>

                      <p className="text-sm font-semibold text-white mt-1 flex items-center gap-1">
                        <IndianRupee size={14} />
                        {currentPrice.toFixed(2)}
                      </p>

                    </div>

                    <div>

                      <p className="text-xs text-slate-500">
                        Invested
                      </p>

                      <p className="text-sm font-semibold text-white mt-1">
                        {formatINR(investedValue)}
                      </p>

                    </div>

                    <div>

                      <p className="text-xs text-slate-500">
                        Market Value
                      </p>

                      <p className="text-sm font-semibold text-white mt-1">
                        {formatINR(marketValue)}
                      </p>

                    </div>

                    <div>

                      <p className="text-xs text-slate-500">
                        Quantity
                      </p>

                      <p className="text-sm font-semibold text-white mt-1">
                        {holding.quantity}
                      </p>

                    </div>

                  </div>

                </div>

              )
            })}

          </div>

        )}

      </div>

    </div>
  )
}