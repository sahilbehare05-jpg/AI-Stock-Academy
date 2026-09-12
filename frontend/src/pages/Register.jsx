import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { TrendingUp, Mail, Lock, User, UserPlus, AlertCircle, Globe } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { t } = useTranslation()
  const { register } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({ name: '', email: '', password: '', preferred_language: 'en' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(form.name, form.email, form.password, form.preferred_language)
      navigate('/app/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-navy-950 flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-accent-blue to-accent-cyan flex items-center justify-center shadow-glow mb-3">
            <TrendingUp size={22} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white">{t('auth.createAccount')}</h1>
          <p className="text-slate-400 text-sm mt-1">{t('auth.startLearning')}</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-7 space-y-4">
          {error && (
            <div className="flex items-center gap-2 text-sm text-accent-red bg-accent-red/10 border border-accent-red/25 rounded-xl px-3.5 py-2.5">
              <AlertCircle size={16} className="shrink-0" />
              {error}
            </div>
          )}

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">{t('auth.name')}</label>
            <div className="relative">
              <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                required
                minLength={2}
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="input-field pl-10"
                placeholder="Your name"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">{t('auth.email')}</label>
            <div className="relative">
              <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="input-field pl-10"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">{t('auth.password')}</label>
            <div className="relative">
              <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="password"
                required
                minLength={6}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="input-field pl-10"
                placeholder="At least 6 characters"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1.5 block">Preferred Language</label>
            <div className="relative">
              <Globe size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <select
                value={form.preferred_language}
                onChange={(e) => setForm({ ...form, preferred_language: e.target.value })}
                className="input-field pl-10 appearance-none"
              >
                <option value="en">English</option>
                <option value="hi">हिन्दी (Hindi)</option>
                <option value="mr">मराठी (Marathi)</option>
              </select>
            </div>
          </div>

          <p className="text-xs text-slate-500">
            You'll receive ₹1,00,000 in virtual money to practice trading. No real money is used.
          </p>

          <button type="submit" disabled={loading} className="btn-primary w-full py-2.5 mt-1">
            {loading ? t('common.loading') : (<>
              <UserPlus size={17} /> {t('auth.createAccount')}
            </>)}
          </button>

          <p className="text-center text-sm text-slate-400 pt-1">
            {t('auth.haveAccount')}{' '}
            <Link to="/login" className="text-accent-blue font-medium hover:underline">
              {t('auth.login')}
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
