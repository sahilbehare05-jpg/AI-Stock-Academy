import React, { useEffect, useState } from 'react'
import {
  Newspaper,
  RefreshCw,
  Search,
  ExternalLink,
  TrendingUp,
  TrendingDown,
  Minus,
} from 'lucide-react'
import api from '../services/api'

export default function News() {
  const [news, setNews] = useState([])
  const [search, setSearch] = useState('')
  const [activeSymbol, setActiveSymbol] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadNews = async (symbol = '') => {
    setLoading(true)
    setError('')

    try {
      const endpoint = symbol
        ? `/api/news?symbol=${encodeURIComponent(symbol)}&limit=20`
        : '/api/news?limit=20'

      const response = await api.get(endpoint)

      setNews(response.data.data || [])
      setActiveSymbol(symbol)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to load market news.'
      )
      setNews([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadNews()
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()

    const symbol = search.trim().toUpperCase()

    loadNews(symbol)
  }

  const clearSearch = () => {
    setSearch('')
    loadNews()
  }

  const formatDate = (value) => {
    if (!value) return '-'

    if (/^\d{14}$/.test(value)) {
      const year = value.slice(0, 4)
      const month = value.slice(4, 6)
      const day = value.slice(6, 8)
      const hour = value.slice(9, 11)
      const minute = value.slice(11, 13)

      return new Date(
        `${year}-${month}-${day}T${hour}:${minute}:00`
      ).toLocaleString('en-IN', {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    }

    return new Date(value).toLocaleString('en-IN', {
      dateStyle: 'medium',
      timeStyle: 'short',
    })
  }

  const getSentiment = (article) => {
    const ticker = article.tickers?.[0]

    if (!ticker) {
      return {
        label: 'Neutral',
        icon: Minus,
        className: 'text-slate-400 bg-white/5 border-white/10',
      }
    }

    const label = ticker.ticker_sentiment_label || 'Neutral'

    if (label.toLowerCase().includes('bullish')) {
      return {
        label,
        icon: TrendingUp,
        className:
          'text-accent-green bg-accent-green/10 border-accent-green/20',
      }
    }

    if (label.toLowerCase().includes('bearish')) {
      return {
        label,
        icon: TrendingDown,
        className:
          'text-accent-red bg-accent-red/10 border-accent-red/20',
      }
    }

    return {
      label,
      icon: Minus,
      className: 'text-slate-400 bg-white/5 border-white/10',
    }
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
            <Newspaper
              size={22}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              Market News
            </h1>

            <p className="text-slate-400 text-sm mt-1">
              Latest financial and stock market updates.
            </p>
          </div>
        </div>

        <button
          onClick={() => loadNews(activeSymbol)}
          disabled={loading}
          className="btn-secondary"
        >
          <RefreshCw
            size={16}
            className={loading ? 'animate-spin' : ''}
          />
          Refresh
        </button>
      </div>

      {/* Search */}
      <div className="card p-5">
        <form
          onSubmit={handleSearch}
          className="flex flex-col sm:flex-row gap-3"
        >
         <div className="relative flex-1">
  <Search
    size={19}
    strokeWidth={2}
    className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none z-10"
  />

  <input
    type="text"
    value={search}
    onChange={(e) => setSearch(e.target.value)}
    placeholder="Enter stock symbol e.g. AAPL"
    className="w-full h-11 rounded-xl bg-slate-950 border border-slate-700 pl-12 pr-4 text-white placeholder:text-slate-400 outline-none transition-all focus:border-accent-blue/60 focus:ring-2 focus:ring-accent-blue/20"
  />
</div>

          <button
            type="submit"
            disabled={loading || !search.trim()}
            className="btn-primary"
          >
            Search
          </button>

          {activeSymbol && (
            <button
              type="button"
              onClick={clearSearch}
              className="btn-secondary"
            >
              All News
            </button>
          )}
        </form>

        {activeSymbol && (
          <p className="text-xs text-slate-500 mt-3">
            Showing news related to{' '}
            <span className="text-accent-blue font-semibold">
              {activeSymbol}
            </span>
          </p>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="card p-5 border border-accent-red/30">
          <p className="text-accent-red text-sm">
            {error}
          </p>
        </div>
      )}

      {/* News */}
      <div className="card p-6">

        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-lg font-semibold text-white">
              {activeSymbol
                ? `${activeSymbol} News`
                : 'Latest Market News'}
            </h2>

            <p className="text-xs text-slate-500 mt-1">
              Real financial news and market sentiment
            </p>
          </div>

          {!loading && (
            <span className="text-xs text-slate-500">
              {news.length} articles
            </span>
          )}
        </div>

        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="h-36 rounded-xl bg-white/5 animate-pulse"
              />
            ))}
          </div>
        ) : news.length === 0 ? (
          <div className="rounded-xl border border-dashed border-white/10 p-10 text-center">
            <Newspaper
              size={36}
              className="mx-auto text-slate-500 mb-3"
            />

            <p className="text-slate-400 text-sm">
              No market news found.
            </p>

            <p className="text-slate-500 text-xs mt-1">
              Try another stock symbol.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {news.map((article, index) => {
              const sentiment = getSentiment(article)
              const SentimentIcon = sentiment.icon

              const ticker =
                article.tickers?.[0]?.ticker || null

              return (
                <article
                  key={`${article.url}-${index}`}
                  className="rounded-xl border border-white/5 bg-white/[0.02] p-5 hover:bg-white/[0.04] transition-colors"
                >
                  <div className="flex flex-col gap-4">

                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-3">

                      <div className="flex-1">
                        <h3 className="text-base font-semibold text-white leading-6">
                          {article.title || 'Untitled article'}
                        </h3>

                        <div className="flex flex-wrap items-center gap-2 mt-3">
                          {article.source && (
                            <span className="text-xs text-slate-400">
                              {article.source}
                            </span>
                          )}

                          {ticker && (
                            <span className="px-2 py-1 rounded-md text-xs font-semibold bg-accent-blue/10 text-accent-blue border border-accent-blue/20">
                              {ticker}
                            </span>
                          )}

                          <span className="text-xs text-slate-500">
                            {formatDate(article.published_at)}
                          </span>

                          <span
                            className={`inline-flex items-center gap-1 px-2 py-1 rounded-md border text-xs font-medium ${sentiment.className}`}
                          >
                            <SentimentIcon size={13} />
                            {sentiment.label}
                          </span>
                        </div>
                      </div>

                      {article.url && (
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 text-sm text-accent-blue hover:text-accent-cyan transition-colors"
                        >
                          Read More
                          <ExternalLink size={14} />
                        </a>
                      )}
                    </div>

                    {article.summary && (
                      <p className="text-sm text-slate-400 leading-6 line-clamp-3">
                        {article.summary}
                      </p>
                    )}

                  </div>
                </article>
              )
            })}
          </div>
        )}

      </div>

      {/* Disclaimer */}
      <div className="card p-5">
        <p className="text-xs text-slate-500 leading-5">
          Market news is provided for educational and informational
          purposes only. News sentiment should not be considered
          financial advice or a guarantee of future price movement.
        </p>
      </div>

    </div>
  )
}