import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  Clock,
  Loader2,
  PlayCircle,
} from 'lucide-react'
import { academyAPI } from '../services/api'

export default function AcademyModule() {
  const { moduleId } = useParams()
  const navigate = useNavigate()

  const [module, setModule] = useState(null)
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadLessons()
  }, [moduleId])

  const loadLessons = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await academyAPI.getModuleLessons(moduleId)

      const data = response.data.data

      setModule(data.module)
      setLessons(data.lessons || [])
    } catch (err) {
      console.error('Module loading failed:', err)

      setError(
        err.response?.data?.detail ||
          'Unable to load this module. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3 text-slate-400">
          <Loader2
            size={32}
            className="animate-spin text-accent-cyan"
          />
          <p>Loading lessons...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card p-8 text-center">
        <h2 className="text-lg font-semibold text-white mb-2">
          Unable to load module
        </h2>

        <p className="text-sm text-slate-400 mb-5">
          {error}
        </p>

        <button
          onClick={() => navigate('/app/academy')}
          className="btn-primary"
        >
          Back to Academy
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6 pb-10">
      {/* Back */}
      <button
        onClick={() => navigate('/app/academy')}
        className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft size={17} />
        Back to Academy
      </button>

      {/* Module Header */}
      <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-accent-blue/15 via-navy-900 to-accent-cyan/10 p-6 lg:p-8">
        <div className="absolute -top-20 -right-20 w-56 h-56 rounded-full bg-accent-cyan/10 blur-3xl" />

        <div className="relative">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 shrink-0 rounded-2xl bg-accent-blue/10 border border-accent-blue/20 flex items-center justify-center">
              <BookOpen
                size={27}
                className="text-accent-cyan"
              />
            </div>

            <div>
              <p className="text-xs font-semibold text-accent-cyan uppercase tracking-wider mb-1">
                {module?.level} Level
              </p>

              <h1 className="text-2xl lg:text-3xl font-bold text-white">
                {module?.title}
              </h1>

              <p className="text-sm text-slate-400 mt-2 max-w-3xl">
                {module?.description}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-5 mt-6 text-sm text-slate-400">
            <span className="flex items-center gap-2">
              <BookOpen size={16} />
              {lessons.length} Lessons
            </span>

            <span className="flex items-center gap-2">
              <PlayCircle size={16} />
              Start Learning
            </span>
          </div>
        </div>
      </section>

      {/* Lessons */}
      <section>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-white">
            Lessons
          </h2>

          <p className="text-xs text-slate-500 mt-1">
            Complete each lesson to progress through this module.
          </p>
        </div>

        <div className="space-y-3">
          {lessons.map((lesson, index) => (
            <button
              key={lesson.id}
              onClick={() =>
                navigate(
                  `/app/academy/lesson/${lesson.id}`
                )
              }
              className="w-full card p-4 lg:p-5 text-left group hover:border-accent-blue/30 transition-all duration-200"
            >
              <div className="flex items-center gap-4">
                {/* Number */}
                <div className="w-11 h-11 shrink-0 rounded-xl bg-white/5 flex items-center justify-center">
                  <span className="text-sm font-bold text-slate-300">
                    {String(index + 1).padStart(2, '0')}
                  </span>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-white group-hover:text-accent-cyan transition-colors">
                      {lesson.title}
                    </h3>

                    {index === 0 && (
                      <span className="hidden sm:inline-flex text-[10px] px-2 py-0.5 rounded-full bg-accent-cyan/10 border border-accent-cyan/20 text-accent-cyan">
                        START HERE
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-4 mt-2 text-xs text-slate-500">
                    <span className="flex items-center gap-1.5">
                      <Clock size={13} />
                      {lesson.estimated_minutes} min
                    </span>

                    <span>
                      {lesson.level}
                    </span>
                  </div>
                </div>

                {/* Status / Arrow */}
                <div className="shrink-0 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                    <ChevronRight
                      size={17}
                      className="text-slate-500 group-hover:text-accent-cyan transition-colors"
                    />
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>

        {lessons.length === 0 && (
          <div className="card p-8 text-center">
            <BookOpen
              size={32}
              className="mx-auto text-slate-600 mb-3"
            />

            <p className="text-sm text-slate-400">
              No lessons are available in this module yet.
            </p>
          </div>
        )}
      </section>

      {/* Footer */}
      <div className="text-center">
        <p className="text-[11px] text-slate-600">
          Complete the lessons in sequence to build your
          knowledge step by step.
        </p>
      </div>
    </div>
  )
}