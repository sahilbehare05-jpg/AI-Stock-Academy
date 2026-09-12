import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Menu, Search, Bell, ChevronDown, LogOut,  } from 'lucide-react'
import { useAuth } from '../context/AuthContext'



export default function Header({ onMenuClick }) {
  const { t, i18n } = useTranslation()
  const { user, logout } = useAuth()
  const [profileOpen, setProfileOpen] = useState(false)

  return (
    <header className="h-16 border-b border-white/5 bg-navy-950/80 backdrop-blur-sm sticky top-0 z-30 flex items-center gap-4 px-4 lg:px-6">
      <button onClick={onMenuClick} className="lg:hidden text-slate-300">
        <Menu size={22} />
      </button>

      <div className="hidden md:flex items-center flex-1 max-w-md relative">
        <Search size={16} className="absolute left-3.5 text-slate-500" />
        <input
          type="text"
          placeholder="Search stocks e.g. RELIANCE, TCS..."
          className="input-field pl-10 py-2"
        />
      </div>

      <div className="flex-1 md:hidden" />

      <div className="flex items-center gap-2 lg:gap-3">
        <div className="relative">
          
        </div>

        <button className="relative w-9 h-9 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-slate-300 hover:bg-white/10">
          <Bell size={17} />
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-accent-red" />
        </button>

        <div className="relative">
          <button
            onClick={() => setProfileOpen((v) => !v)}
            className="flex items-center gap-2 pl-1 pr-2.5 py-1 rounded-xl hover:bg-white/5"
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent-blue to-accent-cyan flex items-center justify-center text-xs font-bold text-white">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </div>
            <span className="hidden sm:block text-sm text-slate-200 font-medium">{user?.name}</span>
            <ChevronDown size={14} className="hidden sm:block text-slate-400" />
          </button>
          {profileOpen && (
            <div className="absolute right-0 mt-2 w-44 card p-1.5 z-40">
              <button
                onClick={logout}
                className="w-full flex items-center gap-2 text-left px-3 py-2 rounded-lg text-sm text-accent-red hover:bg-accent-red/10"
              >
                <LogOut size={15} />
                {t('auth.logout')}
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
