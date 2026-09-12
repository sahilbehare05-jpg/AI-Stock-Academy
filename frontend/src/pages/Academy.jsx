import React, { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BookOpen,
  CheckCircle2,
  ChevronRight,
  GraduationCap,
  Loader2,
  Lock,
  Target,
  Trophy,
} from 'lucide-react'
import { academyAPI } from '../services/api'

const levelStyles = {
  Beginner: {
    badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    icon: 'text-emerald-400',
  },
  Intermediate: {
    badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    icon: 'text-amber-400',
  },
  Advanced: {
    badge: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    icon: 'text-purple-400',
  },
}

export default function Academy() {
  const navigate = useNavigate()

  const [modules, setModules] = useState([])
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadAcademy()
  }, [])

  const loadAcademy = async () => {
    try {
      setLoading(true)
      setError('')

      const [modulesResponse, progressResponse] = await Promise.all([
        academyAPI.getModules(),
        academyAPI.getProgress(),
      ])

      setModules(modulesResponse.data.data || [])
      setProgress(progressResponse.data.data || null)
    } catch (err) {
      console.error('Academy loading failed:', err)
      setError(
        err.response?.data?.detail ||
          'Unable to load the Trading Academy. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const groupedModules = useMemo(() => {
    return {
      Beginner: modules.filter((module) => module.level === 'Beginner'),
      Intermediate: modules.filter(
        (module) => module.level === 'Intermediate'
      ),
      Advanced: modules.filter((module) => module.level === 'Advanced'),
    }
  }, [modules])

  const getLevelNumber = (level) => {
    if (level === 'Beginner') return '01'
    if (level === 'Intermediate') return '02'
    return '03'
  }

  const openModule = (module) => {
    navigate(`/app/academy/module/${module.id}`)
  }

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3 text-slate-400">
          <Loader2 size={32} className="animate-spin text-accent-cyan" />
          <p>Loading Trading Academy...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card p-8 text-center">
        <div className="mx-auto mb-4 w-12 h-12 rounded-2xl bg-red-500/10 flex items-center justify-center">
          <Target className="text-red-400" size={24} />
        </div>

        <h2 className="text-lg font-semibold text-white mb-2">
          Unable to load Academy
        </h2>

        <p className="text-sm text-slate-400 mb-5">{error}</p>

        <button
          onClick={loadAcademy}
          className="btn-primary"
        >
          Try Again
        </button>
      </div>
    )
  }

  const progressPercent = progress?.progress_percent || 0
  const score = progress?.score || 0
  const completedLessons = progress?.completed_lessons || 0
  const totalLessons = progress?.total_lessons || 0

  return (
    <div className="space-y-6 pb-10">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-accent-blue/15 via-navy-900 to-accent-cyan/10 p-6 lg:p-8">
        <div className="absolute -top-24 -right-24 w-64 h-64 rounded-full bg-accent-cyan/10 blur-3xl" />
        <div className="absolute -bottom-24 -left-24 w-64 h-64 rounded-full bg-accent-blue/10 blur-3xl" />

        <div className="relative">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-accent-cyan/20 bg-accent-cyan/10 text-accent-cyan text-xs font-semibold mb-4">
                <GraduationCap size={15} />
                ZERO → HERO
              </div>

              <h1 className="text-2xl lg:text-3xl font-bold text-white">
                Trading Academy
              </h1>

              <p className="mt-2 max-w-2xl text-sm lg:text-base text-slate-400">
                Build your trading knowledge from absolute beginner to
                advanced market analysis through structured lessons,
                practice, quizzes and assessments.
              </p>
            </div>

            <div className="shrink-0 w-28 h-28 rounded-full border-4 border-accent-cyan/20 bg-navy-950/70 flex flex-col items-center justify-center">
              <span className="text-2xl font-bold text-white">
                {Math.round(progressPercent)}%
              </span>
              <span className="text-[11px] text-slate-500">
                Complete
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Progress Cards */}
      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
              <Target className="text-accent-blue" size={20} />
            </div>

            <span className="text-xs text-slate-500">
              Overall
            </span>
          </div>

          <p className="text-2xl font-bold text-white">
            {score.toLocaleString()}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Academy Score / 10,000
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
              <CheckCircle2 className="text-emerald-400" size={20} />
            </div>

            <span className="text-xs text-slate-500">
              Lessons
            </span>
          </div>

          <p className="text-2xl font-bold text-white">
            {completedLessons}
            <span className="text-base text-slate-500">
              {' '}
              / {totalLessons}
            </span>
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Lessons completed
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
              <Trophy className="text-purple-400" size={20} />
            </div>

            <span className="text-xs text-slate-500">
              Journey
            </span>
          </div>

          <p className="text-2xl font-bold text-white">
            {modules.length}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Learning modules
          </p>
        </div>
      </section>

      {/* Overall Progress */}
      <section className="card p-5 lg:p-6">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="font-semibold text-white">
              Your Learning Journey
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Progress through the complete Zero → Hero curriculum.
            </p>
          </div>

          <span className="text-sm font-semibold text-accent-cyan">
            {Math.round(progressPercent)}%
          </span>
        </div>

        <div className="h-3 rounded-full bg-white/5 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-accent-blue to-accent-cyan transition-all duration-700"
            style={{
              width: `${Math.min(progressPercent, 100)}%`,
            }}
          />
        </div>
      </section>

      {/* Modules */}
      {Object.entries(groupedModules).map(([level, levelModules]) => (
        <section key={level}>
          <div className="flex items-center gap-3 mb-4">
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center ${
                level === 'Beginner'
                  ? 'bg-emerald-500/10'
                  : level === 'Intermediate'
                    ? 'bg-amber-500/10'
                    : 'bg-purple-500/10'
              }`}
            >
              <BookOpen
                size={18}
                className={levelStyles[level].icon}
              />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold text-white">
                  {level}
                </h2>

                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold ${
                    levelStyles[level].badge
                  }`}
                >
                  LEVEL {getLevelNumber(level)}
                </span>
              </div>

              <p className="text-xs text-slate-500">
                {level === 'Beginner'
                  ? 'Build your foundation from zero.'
                  : level === 'Intermediate'
                    ? 'Develop analytical and strategic skills.'
                    : 'Master advanced market concepts.'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {levelModules.map((module, index) => (
              <button
                key={module.id}
                onClick={() => openModule(module)}
                className="card p-5 text-left group hover:border-accent-blue/30 transition-all duration-200"
              >
                <div className="flex items-start gap-4">
                  <div className="shrink-0 w-11 h-11 rounded-xl bg-white/5 flex items-center justify-center text-slate-300 font-bold">
                    {String(module.order).padStart(2, '0')}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h3 className="font-semibold text-white group-hover:text-accent-cyan transition-colors">
                          {module.title}
                        </h3>

                        <p className="text-xs text-slate-500 mt-1">
                          {module.lesson_count} lessons
                        </p>
                      </div>

                      <ChevronRight
                        size={18}
                        className="shrink-0 text-slate-600 group-hover:text-accent-cyan transition-colors"
                      />
                    </div>

                    <p className="text-sm text-slate-400 mt-3 line-clamp-2">
                      {module.description}
                    </p>

                    <div className="mt-4 flex items-center gap-2">
                      <span
                        className={`text-[11px] px-2.5 py-1 rounded-full border ${
                          levelStyles[level].badge
                        }`}
                      >
                        {level}
                      </span>

                      {module.order > 1 && level === 'Advanced' && (
                        <span className="text-[11px] text-slate-600 flex items-center gap-1">
                          <Lock size={12} />
                          Advanced
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </section>
      ))}

      {/* Disclaimer */}
      <div className="text-center px-4 pt-2">
        <p className="text-[11px] text-slate-600 max-w-3xl mx-auto">
          Academy content is for educational purposes. Learning about
          trading does not guarantee profits, and market participation
          involves financial risk.
        </p>
      </div>
    </div>
  )
}