import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import {
  Sparkles, Wallet, GraduationCap, MessageCircleQuestion, FlaskConical,
  Languages, TrendingUp, ArrowRight, ShieldAlert,
} from 'lucide-react'

const features = [
  { icon: Sparkles, title: 'AI Prediction', desc: 'Random Forest, XGBoost & LSTM models forecast price movement with transparent confidence scores.' },
  { icon: Wallet, title: 'Virtual Trading', desc: 'Practice buying and selling with a ₹1,00,000 virtual wallet — zero real-money risk.' },
  { icon: GraduationCap, title: 'Trading Academy', desc: 'A structured 0 → 10,000 XP curriculum from market basics to AI-assisted analysis.' },
  { icon: MessageCircleQuestion, title: 'AI Tutor', desc: 'Ask trading questions in English, Hindi, or Marathi and get level-adjusted answers.' },
  { icon: FlaskConical, title: 'Practice Lab', desc: 'Quizzes, chart reading, and scenario simulations that adapt to your progress.' },
  { icon: Languages, title: 'Multilingual', desc: 'The entire platform — lessons, quizzes, and tutor — works in three languages.' },
]

export default function Landing() {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-navy-950 text-slate-100 overflow-hidden">
      <div className="absolute inset-0 pointer-events-none opacity-40" style={{
        background: 'radial-gradient(circle at 20% 10%, rgba(59,130,246,0.15), transparent 40%), radial-gradient(circle at 80% 30%, rgba(34,211,238,0.12), transparent 40%)'
      }} />

      <header className="relative z-10 flex items-center justify-between px-6 lg:px-12 h-20">
        <div className="flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-blue to-accent-cyan flex items-center justify-center shadow-glow">
            <TrendingUp size={20} className="text-white" />
          </div>
          <span className="font-bold text-white text-lg">{t('appName')}</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" className="btn-secondary px-4 py-2 text-sm">{t('auth.login')}</Link>
          <Link to="/register" className="btn-primary px-4 py-2 text-sm">{t('auth.register')}</Link>
        </div>
      </header>

      <section className="relative z-10 px-6 lg:px-12 pt-16 pb-24 text-center max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <span className="badge badge-buy mb-6">Final-Year BTech Data Science Project</span>
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white leading-tight tracking-tight">
            {t('tagline')}
          </h1>
          <p className="mt-5 text-lg text-slate-400 max-w-2xl mx-auto">
            {t('subtitle')}
          </p>
          <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
            <Link to="/register" className="btn-primary px-6 py-3">
              {t('landing.startLearning')} <ArrowRight size={18} />
            </Link>
            <Link to="/register" className="btn-secondary px-6 py-3">
              {t('landing.exploreAI')}
            </Link>
          </div>
        </motion.div>
      </section>

      <section className="relative z-10 px-6 lg:px-12 pb-20 max-w-6xl mx-auto">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.06 }}
              className="card card-hover p-6"
            >
              <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/25 flex items-center justify-center mb-4">
                <f.icon size={20} className="text-accent-blue" />
              </div>
              <h3 className="font-semibold text-white mb-1.5">{f.title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="relative z-10 px-6 lg:px-12 pb-16 max-w-4xl mx-auto">
        <div className="card p-5 flex items-start gap-3 border-accent-gold/20">
          <ShieldAlert size={20} className="text-accent-gold shrink-0 mt-0.5" />
          <p className="text-sm text-slate-400">{t('landing.disclaimer')}</p>
        </div>
      </section>
    </div>
  )
}
