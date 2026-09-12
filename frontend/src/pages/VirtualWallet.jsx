import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import {
  Wallet,
  RefreshCw,
  IndianRupee,
  ShieldCheck,
  ArrowUpCircle,
  ArrowDownCircle,
} from 'lucide-react'
import api from '../services/api'

export default function VirtualWallet() {
  const { t, i18n } = useTranslation()
  const [wallet, setWallet] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadWallet = async () => {
    setLoading(true)
    setError('')

    try {
      const [walletResponse, transactionResponse] = await Promise.all([
        api.get('/api/wallet'),
        api.get('/api/wallet/transactions'),
      ])

      setWallet(walletResponse.data.data)
      setTransactions(transactionResponse.data.data || [])
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        t('wallet.loadError')
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadWallet()
  }, [])

  const formatINR = (amount) =>
    new Intl.NumberFormat(i18n.language === 'hi' ? 'hi-IN' : i18n.language === 'mr' ? 'mr-IN' : 'en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 2,
    }).format(Number(amount) || 0)

  const formatDate = (date) => {
    if (!date) return '-'

    return new Date(date).toLocaleString(i18n.language === 'hi' ? 'hi-IN' : i18n.language === 'mr' ? 'mr-IN' : 'en-IN', {
      dateStyle: 'medium',
      timeStyle: 'short',
    })
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
              <Wallet size={22} className="text-accent-blue" />
            </div>

            <div>
              <h1 className="text-2xl font-bold text-white">
                {t('wallet.title')}
              </h1>

              <p className="text-slate-400 text-sm mt-1">
                {t('wallet.subtitle')}
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={loadWallet}
          disabled={loading}
          className="btn-secondary"
        >
          <RefreshCw
            size={16}
            className={loading ? 'animate-spin' : ''}
          />
          {t('common.refresh')}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-5 border border-accent-red/30">
          <p className="text-accent-red text-sm">
            {error}
          </p>
        </div>
      )}

      {/* Main Balance */}
      <div className="card p-7">
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <IndianRupee size={17} />
          {t('wallet.availableBalance')}
        </div>

        {loading ? (
          <div className="h-10 w-52 bg-white/5 rounded-lg animate-pulse mt-4" />
        ) : (
          <p className="text-4xl font-bold text-white mt-4">
            {formatINR(wallet?.balance)}
          </p>
        )}

        <div className="flex items-center gap-2 mt-5 text-sm text-slate-400">
          <ShieldCheck size={16} className="text-accent-green" />
          {t('wallet.simulatedFunds')}
        </div>
      </div>

      {/* Stats */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">

        <div className="card card-hover p-5">
          <p className="text-xs text-slate-400">
            {t('wallet.currentBalance')}
          </p>

          <p className="text-xl font-bold text-white mt-2">
            {loading ? t('common.loading') : formatINR(wallet?.balance)}
          </p>
        </div>

        <div className="card card-hover p-5">
          <p className="text-xs text-slate-400">
            {t('wallet.currency')}
          </p>

          <p className="text-xl font-bold text-white mt-2">
            {wallet?.currency || 'INR'}
          </p>
        </div>

        <div className="card card-hover p-5">
          <p className="text-xs text-slate-400">
            {t('wallet.totalTransactions')}
          </p>

          <p className="text-xl font-bold text-accent-blue mt-2">
            {transactions.length}
          </p>
        </div>

      </div>

      {/* Transaction History */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-lg font-semibold text-white">
              {t('wallet.transactionHistory')}
            </h2>

            <p className="text-slate-500 text-xs mt-1">
              {t('wallet.transactionSubtitle')}
            </p>
          </div>

          <button
            onClick={loadWallet}
            disabled={loading}
            className="text-slate-400 hover:text-white transition-colors"
            title={t('wallet.refreshTransactions')}
          >
            <RefreshCw
              size={18}
              className={loading ? 'animate-spin' : ''}
            />
          </button>
        </div>

        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((item) => (
              <div
                key={item}
                className="h-16 rounded-xl bg-white/5 animate-pulse"
              />
            ))}
          </div>
        ) : transactions.length === 0 ? (
          <div className="rounded-xl border border-dashed border-white/10 p-8 text-center">
            <Wallet
              size={32}
              className="mx-auto text-slate-500 mb-3"
            />

            <p className="text-slate-400 text-sm">
              {t('wallet.noTransactions')}
            </p>

            <p className="text-slate-500 text-xs mt-1">
              {t('wallet.noTransactionsHint')}
            </p>
          </div>
        ) : (
          <div className="space-y-3">

  {transactions.map((transaction) => {
    const isBuy = transaction.type === 'BUY'

    return (
      <div
        key={transaction.id}
        className="rounded-xl border border-white/5 bg-white/[0.02] p-4"
      >

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

          <div className="flex items-center gap-3">

            {isBuy ? (
              <ArrowUpCircle
                size={30}
                className="text-accent-green"
              />
            ) : (
              <ArrowDownCircle
                size={30}
                className="text-accent-red"
              />
            )}

            <div>
              <div className="flex items-center gap-2">

                <span
                  className={`text-sm font-bold ${
                    isBuy
                      ? 'text-accent-green'
                      : 'text-accent-red'
                  }`}
                >
                  {transaction.type}
                </span>

                <span className="text-white font-semibold">
                  {transaction.symbol}
                </span>

              </div>

              <p className="text-xs text-slate-500 mt-1">
                {formatDate(transaction.created_at)}
              </p>
            </div>

          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-5 text-sm">

            <div>
              <p className="text-xs text-slate-500">
                {t('wallet.quantity')}
              </p>

              <p className="text-white font-medium mt-1">
                {transaction.quantity}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                {t('wallet.price')}
              </p>

              <p className="text-white font-medium mt-1">
                {formatINR(transaction.price)}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                {t('wallet.total')}
              </p>

              <p className="text-white font-semibold mt-1">
                {formatINR(transaction.total)}
              </p>
            </div>

            {transaction.type === 'SELL' && (
              <div>
                <p className="text-xs text-slate-500">
                  {t('wallet.realizedPnl')}
                </p>

                <p
                  className={`font-semibold mt-1 ${
                    Number(transaction.realized_pnl || 0) >= 0
                      ? 'text-accent-green'
                      : 'text-accent-red'
                  }`}
                >
                  {Number(transaction.realized_pnl || 0) >= 0 ? '+' : ''}
                  {formatINR(transaction.realized_pnl || 0)}
                </p>

                <p className="text-xs text-slate-500 mt-1">
                  {Number(transaction.realized_pnl_percent || 0) >= 0 ? '+' : ''}
                  {Number(transaction.realized_pnl_percent || 0).toFixed(2)}%
                </p>
              </div>
            )}

          </div>

        </div>

      </div>
    )
     })}

</div>
 )} 
 </div>

      {/* Information */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-white">
          {t('wallet.aboutTitle')}
        </h2>

        <p className="text-slate-400 text-sm leading-6 mt-3">
          {t('wallet.aboutText')}
        </p>
      </div>

    </div>
  )
}