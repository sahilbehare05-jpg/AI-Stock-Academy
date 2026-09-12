import React from 'react'
import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import {
  LayoutDashboard, LineChart, Sparkles, HelpCircle, Wallet, Briefcase,
  Star, Newspaper, GraduationCap, FlaskConical, MessageCircleQuestion,
   History, BarChart3, User, Settings, TrendingUp, X,
} from 'lucide-react'

const navItems = [
  { key: 'dashboard', to: '/app/dashboard', icon: LayoutDashboard },
  { key: 'stockAnalysis', to: '/app/stock-analysis', icon: LineChart },
  { key: 'aiPrediction', to: '/app/ai-prediction', icon: Sparkles },
  { key: 'whyPrediction', to: '/app/why-prediction', icon: HelpCircle },
  { key: 'wallet', to: '/app/wallet', icon: Wallet },
  { key: 'trading', to: '/app/trading', icon: TrendingUp },
  { key: 'portfolio', to: '/app/portfolio', icon: Briefcase },
  { key: 'watchlist', to: '/app/watchlist', icon: Star },
  { key: 'news', to: '/app/news', icon: Newspaper },
  { key: 'academy', to: '/app/academy', icon: GraduationCap },
  { key: 'practiceLab', to: '/app/practice-lab', icon: FlaskConical },
  { key: 'tutor', to: '/app/tutor', icon: MessageCircleQuestion },
  { key: 'predictionHistory', to: '/app/prediction-history', icon: History },
  { key: 'modelPerformance', to: '/app/model-performance', icon: BarChart3 },
  { key: 'profile', to: '/app/profile', icon: User },
  { key: 'settings', to: '/app/settings', icon: Settings },
]

export default function Sidebar({ open, onClose }) {
  const { t } = useTranslation()

  return (
    <>
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}
      <aside
        className={`fixed z-50 inset-y-0 left-0 w-72 bg-navy-900 border-r border-white/5 flex flex-col
        transform transition-transform duration-300 lg:translate-x-0 lg:static
        ${open ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center justify-between px-5 h-16 border-b border-white/5">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-blue to-accent-cyan flex items-center justify-center shadow-glow">
              <TrendingUp size={19} className="text-white" />
            </div>
            <div>
              <p className="font-bold text-white leading-tight text-sm">AI Stock</p>
              <p className="font-bold text-accent-cyan leading-tight text-sm -mt-0.5">Academy</p>
            </div>
          </div>
          <button onClick={onClose} className="lg:hidden text-slate-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {navItems.map(({ key, to, icon: Icon }) => (
            <NavLink
              key={key}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors
                ${isActive
                  ? 'bg-accent-blue/15 text-accent-blue border border-accent-blue/25'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-white/5 border border-transparent'
                }`
              }
            >
              <Icon size={18} />
              <span>{t(`nav.${key}`)}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-white/5">
          <div className="card px-3 py-2.5 text-xs text-slate-400">
            <span className="badge badge-hold">{t('common.simulation')}</span>
          </div>
        </div>
      </aside>
    </>
  )
}
