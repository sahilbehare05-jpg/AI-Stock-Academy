import { useEffect, useState } from 'react'
import {
  Star,
  RefreshCw,
  Plus,
  Trash2,
  TrendingUp,
  TrendingDown,
  Search,
} from 'lucide-react'
import api from '../services/api'

export default function Watchlist() {
  const [watchlist, setWatchlist] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const loadWatchlist = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await api.get('/api/watchlist')
      setWatchlist(response.data.data || [])
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to load watchlist.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadWatchlist()
  }, [])

  const addStock = async () => {
    const symbol = search.trim().toUpperCase()

    if (!symbol) {
      setError('Enter a stock symbol.')
      return
    }

    setAdding(true)
    setError('')
    setMessage('')

    try {
      const response = await api.post(
        '/api/watchlist',
        { symbol }
      )

      setMessage(
        response.data.data.message ||
        `${symbol} added to watchlist.`
      )

      setSearch('')
      await loadWatchlist()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to add stock.'
      )
    } finally {
      setAdding(false)
    }
  }

  const removeStock = async (symbol) => {
    setError('')
    setMessage('')

    try {
      const response = await api.delete(
        `/api/watchlist/${encodeURIComponent(symbol)}`
      )

      setMessage(
        response.data.data.message ||
        `${symbol} removed from watchlist.`
      )

      setWatchlist((current) =>
        current.filter(
          (item) => item.symbol !== symbol
        )
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to remove stock.'
      )
    }
  }

  const formatINR = (amount) => {
    if (
      amount === null ||
      amount === undefined
    ) {
      return '-'
    }

    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 2,
    }).format(Number(amount) || 0)
  }

  const formatPercent = (amount) => {
    if (
      amount === null ||
      amount === undefined
    ) {
      return '-'
    }

    const value = Number(amount)

    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }

  const formatChange = (amount) => {
    if (
      amount === null ||
      amount === undefined
    ) {
      return '-'
    }

    const value = Number(amount)

    return `${value >= 0 ? '+' : ''}${formatINR(value)}`
  }

  return (
    <div className="space-y-6 pb-10">

      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">

        <div className="flex items-center gap-3">

          <div className="w-11 h-11 rounded-xl bg-yellow-400/10 border border-yellow-400/20 flex items-center justify-center">
            <Star
              size={22}
              className="text-yellow-400"
              fill="currentColor"
            />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              Watchlist
            </h1>

            <p className="text-slate-400 text-sm mt-1">
              Track your favourite stocks and live market performance.
            </p>
          </div>

        </div>

        <button
          onClick={loadWatchlist}
          disabled={loading}
          className="btn-secondary"
        >
          <RefreshCw
            size={16}
            className={
              loading
                ? 'animate-spin'
                : ''
            }
          />

          Refresh
        </button>

      </div>

      {/* Add Stock */}
      <div className="card p-5">

        <div className="flex flex-col sm:flex-row gap-3">

          <div className="relative flex-1">

            <Search
              size={18}
               className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 pointer-events-none z-10"
            />

            <input
              type="text"
              value={search}
              onChange={(e) =>
                setSearch(e.target.value.toUpperCase())
              }
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  addStock()
                }
              }}
              placeholder="Enter stock symbol e.g. AAPL or RELIANCE.NS"
              className="w-full h-12 rounded-xl bg-slate-950 border border-slate-700 pl-12 pr-4 text-white placeholder:text-slate-300 placeholder:opacity-100 outline-none transition-colors focus:border-accent-blue/60 focus:ring-2 focus:ring-accent-blue/20"
  
            />

          </div>

          <button
            onClick={addStock}
            disabled={adding}
            className="btn-primary sm:min-w-[150px]"
          >
            <Plus size={17} />

            {adding
              ? 'Adding...'
              : 'Add to Watchlist'}
          </button>

        </div>

        <p className="text-xs text-slate-500 mt-3">
          Examples: AAPL, TSLA, MSFT, RELIANCE.NS, TCS.NS
        </p>

      </div>

      {/* Messages */}
      {error && (
        <div className="card p-4 border border-accent-red/30">
          <p className="text-accent-red text-sm">
            {error}
          </p>
        </div>
      )}

      {message && (
        <div className="card p-4 border border-accent-green/30">
          <p className="text-accent-green text-sm">
            {message}
          </p>
        </div>
      )}

      {/* Watchlist */}
      <div className="card p-6">

        <div className="flex items-center justify-between mb-5">

          <div>
            <h2 className="text-lg font-semibold text-white">
              My Stocks
            </h2>

            <p className="text-xs text-slate-500 mt-1">
              Live market data
            </p>
          </div>

          <span className="text-xs text-slate-500">
            {watchlist.length} stock
            {watchlist.length === 1 ? '' : 's'}
          </span>

        </div>

        {loading ? (

          <div className="space-y-3">

            {[1, 2, 3].map((item) => (
              <div
                key={item}
                className="h-20 rounded-xl bg-white/5 animate-pulse"
              />
            ))}

          </div>

        ) : watchlist.length === 0 ? (

          <div className="rounded-xl border border-dashed border-white/10 p-10 text-center">

            <Star
              size={34}
              className="mx-auto text-slate-600 mb-3"
            />

            <p className="text-slate-400 text-sm">
              Your watchlist is empty.
            </p>

            <p className="text-slate-500 text-xs mt-1">
              Add a stock above to start tracking it.
            </p>

          </div>

        ) : (

          <div className="space-y-3">

            {watchlist.map((stock) => {

              const positive =
                Number(stock.change || 0) >= 0

              return (

                <div
                  key={stock.id}
                  className="rounded-xl border border-white/5 bg-white/[0.02] p-4 hover:bg-white/[0.04] transition-colors"
                >

                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">

                    {/* Stock */}
                    <div className="flex items-center gap-3 min-w-[180px]">

                      <div className="w-10 h-10 rounded-lg bg-yellow-400/10 border border-yellow-400/20 flex items-center justify-center">
                        <Star
                          size={18}
                          className="text-yellow-400"
                          fill="currentColor"
                        />
                      </div>

                      <div>
                        <p className="text-white font-semibold">
                          {stock.symbol}
                        </p>

                        <p className="text-xs text-slate-500">
                          Live market
                        </p>
                      </div>

                    </div>

                    {/* Data */}
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5 flex-1">

                      <div>
                        <p className="text-xs text-slate-500">
                          Current Price
                        </p>

                        <p className="text-white font-semibold mt-1">
                          {formatINR(stock.price)}
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-slate-500">
                          Change
                        </p>

                        <div
                          className={`flex items-center gap-1 font-semibold mt-1 ${
                            positive
                              ? 'text-accent-green'
                              : 'text-accent-red'
                          }`}
                        >

                          {positive ? (
                            <TrendingUp size={15} />
                          ) : (
                            <TrendingDown size={15} />
                          )}

                          {formatChange(stock.change)}

                        </div>

                      </div>

                      <div>
                        <p className="text-xs text-slate-500">
                          Change %
                        </p>

                        <p
                          className={`font-semibold mt-1 ${
                            positive
                              ? 'text-accent-green'
                              : 'text-accent-red'
                          }`}
                        >
                          {formatPercent(
                            stock.change_percent
                          )}
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-slate-500">
                          Previous Close
                        </p>

                        <p className="text-white font-medium mt-1">
                          {formatINR(
                            stock.previous_close
                          )}
                        </p>
                      </div>

                    </div>

                    {/* Remove */}
                    <button
                      onClick={() =>
                        removeStock(stock.symbol)
                      }
                      className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-accent-red/20 bg-accent-red/10 text-accent-red hover:bg-accent-red/15 transition-colors"
                    >
                      <Trash2 size={16} />
                      Remove
                    </button>

                  </div>

                </div>

              )
            })}

          </div>

        )}

      </div>

      {/* Information */}
      <div className="card p-5">

        <div className="flex items-start gap-3">

          <Star
            size={18}
            className="text-yellow-400 mt-0.5"
          />

          <div>

            <h3 className="text-sm font-semibold text-white">
              About Watchlist
            </h3>

            <p className="text-xs text-slate-500 leading-5 mt-1">
              Your watchlist helps you track stocks without
              buying them. Prices and market changes are
              retrieved from the live stock data service.
            </p>

          </div>

        </div>

      </div>

    </div>
  )
}