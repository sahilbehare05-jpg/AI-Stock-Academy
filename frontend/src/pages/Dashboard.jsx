import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Wallet, Briefcase, TrendingUp, GraduationCap, Sparkles } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import api, { academyAPI } from '../services/api'

function StatCard({ icon: Icon, label, value, accent }) {
  return (
    <div className="card card-hover p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-slate-400">{label}</span>
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${accent}`}>
          <Icon size={16} />
        </div>
      </div>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  )
}

export default function Dashboard() {
  const { t } = useTranslation()
  const { user } = useAuth()
  const [prediction, setPrediction] = useState(null)
const [predictionLoading, setPredictionLoading] = useState(true)
const [predictionError, setPredictionError] = useState('')
const [portfolio, setPortfolio] = useState(null)
const [academyProgress, setAcademyProgress] = useState(null)

useEffect(() => {
  const loadPrediction = async () => {
    try {
      setPredictionLoading(true)
      setPredictionError('')

      const response = await api.get('/api/prediction/AAPL')

      setPrediction(response.data.data)
    } catch (err) {
      setPredictionError(
        err.response?.data?.detail ||
        'Unable to load prediction.',
      )
    } finally {
      setPredictionLoading(false)
    }
  }

  loadPrediction()
}, [])
useEffect(() => {
  const loadPortfolio = async () => {
    try {
      const response = await api.get('/api/portfolio')
      setPortfolio(response.data.data)
    } catch (err) {
      console.error('Unable to load portfolio:', err)
    }
  }

  loadPortfolio()

  const interval = setInterval(() => {
    loadPortfolio()
  }, 15000)

  return () => clearInterval(interval)
}, [])
useEffect(() => {
  const loadAcademyProgress = async () => {
    try {
      const response = await academyAPI.getProgress()
      setAcademyProgress(response.data.data)
    } catch (err) {
      console.error('Unable to load academy progress:', err)
    }
  }

  loadAcademyProgress()
}, [])

  const formatINR = (n) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(n || 0)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">
          {t('dashboard.welcome')}, {user?.name?.split(' ')[0]}
        </h1>
        <p className="text-slate-400 text-sm mt-1">Here's your simulated trading & learning snapshot.</p>
      </div>

      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard
          icon={Wallet}
          label={t('dashboard.virtualBalance')}
          value={formatINR(user?.virtual_balance)}
          accent="bg-accent-blue/10 text-accent-blue"
        />
        <StatCard
          icon={Briefcase}
          label={t('dashboard.portfolioValue')}
          value={formatINR(portfolio?.total_value)}
          accent="bg-accent-cyan/10 text-accent-cyan"
        />
        <StatCard
          icon={TrendingUp}
          label={t('dashboard.totalPnl')}
          value={formatINR(portfolio?.total_pnl)}
          accent="bg-accent-green/10 text-accent-green"
        />
        <StatCard
          icon={GraduationCap}
          label={t('dashboard.trainingProgress')}
          value={`${academyProgress?.score ?? 0} / 10,000`}
          accent="bg-accent-gold/10 text-accent-gold"
        />
      </div>

      <div className="card p-6">
  <div className="flex items-center justify-between mb-4">
    <div className="flex items-center gap-2">
      <Sparkles size={18} className="text-accent-blue" />
      <h2 className="font-semibold text-white">
        AI Stock Prediction
      </h2>
    </div>

    <span className="badge badge-hold">
      AI Model
    </span>
  </div>

  {predictionLoading ? (
    <div className="rounded-xl border border-white/10 p-8 text-center">
      <p className="text-slate-400 text-sm">
        Loading AI prediction...
      </p>
    </div>
  ) : predictionError ? (
    <div className="rounded-xl border border-red-500/20 p-8 text-center">
      <p className="text-red-400 text-sm">
        {predictionError}
      </p>
    </div>
  ) : prediction ? (
    <div className="grid sm:grid-cols-3 gap-4">
      <div className="rounded-xl border border-white/10 p-5">
        <p className="text-xs text-slate-500">
          Stock
        </p>
        <p className="text-xl font-bold text-white mt-1">
          {prediction.symbol || 'AAPL'}
        </p>
      </div>

      <div className="rounded-xl border border-white/10 p-5">
        <p className="text-xs text-slate-500">
          Prediction
        </p>
        <p className="text-xl font-bold text-accent-blue mt-1">
          {prediction.prediction || 'N/A'}
        </p>
      </div>

      <div className="rounded-xl border border-white/10 p-5">
        <p className="text-xs text-slate-500">
          Confidence
        </p>
        <p className="text-xl font-bold text-white mt-1">
          {Number.isFinite(Number(prediction.confidence))
            ? `${Number(prediction.confidence).toFixed(1)}%`
            : 'N/A'}
        </p>
      </div>
    </div>
  ) : (
    <div className="rounded-xl border border-white/10 p-8 text-center">
      <p className="text-slate-400 text-sm">
        No prediction available.
      </p>
    </div>
  )}

  <p className="text-xs text-slate-500 mt-4">
    Educational prediction generated using the current AI model.
  </p>
</div>
    </div>
  )
}
