import React from 'react'
import { useTranslation } from 'react-i18next'
import { Construction } from 'lucide-react'

export default function PlaceholderPage({ title, phase }) {
  const { t } = useTranslation()
  return (
    <div className="card p-10 flex flex-col items-center justify-center text-center gap-3 min-h-[60vh]">
      <div className="w-14 h-14 rounded-2xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
        <Construction size={26} className="text-accent-blue" />
      </div>
      <h2 className="text-xl font-bold text-white">{title}</h2>
      <p className="text-slate-400 max-w-md">{t('common.comingSoon')}</p>
      {phase && <span className="badge badge-hold mt-1">{phase}</span>}
    </div>
  )
}
