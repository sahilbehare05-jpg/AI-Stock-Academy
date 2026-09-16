import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  CheckCircle2,
  Clock,
  Lightbulb,
  Loader2,
  Target,
} from 'lucide-react'
import { academyAPI } from '../services/api'

export default function AcademyLesson() {
  const { lessonId } = useParams()
  const navigate = useNavigate()

  const [lesson, setLesson] = useState(null)
  const [lessons, setLessons] = useState([])
  const [module, setModule] = useState(null)
  const [loading, setLoading] = useState(true)
  const [completing, setCompleting] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadLesson()
  }, [lessonId])

  const loadLesson = async () => {
    try {
      setLoading(true)
      setError('')

      const modulesResponse = await academyAPI.getModules()
      const modules = modulesResponse.data.data || []

      for (const currentModule of modules) {
        const response = await academyAPI.getModuleLessons(
          currentModule.id
        )

        const data = response.data.data

        const foundLesson = data.lessons?.find(
          (item) => item.id === lessonId
        )

        if (foundLesson) {
          setModule(data.module)
          setLessons(data.lessons || [])
          setLesson(foundLesson)
          break
        }
      }
    } catch (err) {
      console.error('Lesson loading failed:', err)

      setError(
        err.response?.data?.detail ||
          'Unable to load this lesson. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const completeCurrentLesson = async () => {
    if (!lesson || completed || completing) return

    try {
      setCompleting(true)

      await academyAPI.completeLesson(lesson.id)

      setCompleted(true)
    } catch (err) {
      console.error('Lesson completion failed:', err)

      setError(
        err.response?.data?.detail ||
          'Unable to mark the lesson as complete.'
      )
    } finally {
      setCompleting(false)
    }
  }

  const currentIndex = lessons.findIndex(
    (item) => item.id === lessonId
  )

  const nextLesson =
    currentIndex >= 0
      ? lessons[currentIndex + 1]
      : null

  const previousLesson =
    currentIndex > 0
      ? lessons[currentIndex - 1]
      : null

  const goToNextLesson = () => {
    if (nextLesson) {
      navigate(`/app/academy/lesson/${nextLesson.id}`)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else if (module) {
      navigate(`/app/academy/module/${module.id}`)
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
          <p>Loading lesson...</p>
        </div>
      </div>
    )
  }

  if (error || !lesson) {
    return (
      <div className="card p-8 text-center">
        <BookOpen
          size={34}
          className="mx-auto text-slate-600 mb-4"
        />

        <h2 className="text-lg font-semibold text-white mb-2">
          Unable to load lesson
        </h2>

        <p className="text-sm text-slate-400 mb-5">
          {error || 'Lesson not found.'}
        </p>

        <button
          onClick={() =>
            navigate(
              module
                ? `/app/academy/module/${module.id}`
                : '/app/academy'
            )
          }
          className="btn-primary"
        >
          Back to Academy
        </button>
      </div>
    )
  }

  const content = lesson.content || {}

  /* =========================================================
     VISUAL TYPE DETECTION
  ========================================================= */

  const getVisualType = () => {
    const title = lesson.title?.toLowerCase() || ''

    if (
      title.includes('candlestick') ||
      title.includes('candle') ||
      title.includes('bullish') ||
      title.includes('bearish') ||
      title.includes('ohlc')
    ) {
      return 'candlestick'
    }

    if (
      title.includes('uptrend') ||
      title.includes('downtrend') ||
      title.includes('trend')
    ) {
      return 'trend'
    }

    if (
      title.includes('support') ||
      title.includes('resistance')
    ) {
      return 'support-resistance'
    }

    if (
      title.includes('moving average') ||
      title.includes('rsi') ||
      title.includes('macd') ||
      title.includes('bollinger')
    ) {
      return 'indicator'
    }

    if (
      title.includes('breakout') ||
      title.includes('divergence') ||
      title.includes('chart pattern')
    ) {
      return 'advanced-chart'
    }

    if (
      title.includes('call option') ||
      title.includes('put option') ||
      title.includes('option payoff')
    ) {
      return 'options'
    }

    if (
      title.includes('itm') ||
      title.includes('atm') ||
      title.includes('otm') ||
      title.includes('moneyness')
    ) {
      return 'moneyness'
    }

    return null
  }

  const visualType = getVisualType()

  /* =========================================================
     VISUAL LEARNING COMPONENT
  ========================================================= */

  const LearningVisual = ({ type }) => {
    if (!type) return null

    /* =======================================================
       CANDLESTICK
    ======================================================= */

    if (type === 'candlestick') {
      return (
        <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 lg:p-7">

          <h3 className="text-base font-bold text-white mb-2">
            Candlestick Chart Visual
          </h3>

          <p className="text-xs text-slate-500 mb-6">
            A candlestick shows the Open, High, Low and Close
            prices for a period.
          </p>

          <div className="relative h-72 rounded-xl border border-white/10 bg-slate-950 overflow-hidden">

            {/* Grid */}
            <div className="absolute inset-0 opacity-20">
              {[20, 40, 60, 80].map((top) => (
                <div
                  key={top}
                  className="absolute left-0 right-0 border-t border-white/20"
                  style={{ top: `${top}%` }}
                />
              ))}
            </div>

            {/* Candles */}
            <div className="absolute inset-0 flex items-center justify-center gap-7">
              {[
                {
                  body: 'h-16',
                  wick: 'h-28',
                  bullish: false,
                },
                {
                  body: 'h-24',
                  wick: 'h-36',
                  bullish: true,
                },
                {
                  body: 'h-12',
                  wick: 'h-24',
                  bullish: false,
                },
                {
                  body: 'h-28',
                  wick: 'h-40',
                  bullish: true,
                },
                {
                  body: 'h-20',
                  wick: 'h-32',
                  bullish: true,
                },
                {
                  body: 'h-10',
                  wick: 'h-24',
                  bullish: false,
                },
                {
                  body: 'h-32',
                  wick: 'h-44',
                  bullish: true,
                },
              ].map((candle, index) => (
                <div
                  key={index}
                  className="relative w-7 h-48 flex items-center justify-center"
                >

                  {/* Wick */}
                  <div
                    className={`absolute w-0.5 ${candle.wick} ${
                      candle.bullish
                        ? 'bg-emerald-400'
                        : 'bg-rose-400'
                    }`}
                  />

                  {/* Body */}
                  <div
                    className={`relative w-7 ${candle.body} rounded-sm border ${
                      candle.bullish
                        ? 'bg-emerald-400/80 border-emerald-300'
                        : 'bg-rose-400/80 border-rose-300'
                    }`}
                  />

                </div>
              ))}
            </div>

            <div className="absolute top-4 left-5 text-xs text-slate-400">
              High
            </div>

            <div className="absolute bottom-4 left-5 text-xs text-slate-400">
              Low
            </div>

            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 text-[11px] text-white/40">
              Price Movement
            </div>

          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-5 mt-5 text-xs">

            <div className="flex items-center gap-2 text-slate-300">
              <span className="w-3 h-3 rounded-sm bg-emerald-400" />
              Bullish / Up
            </div>

            <div className="flex items-center gap-2 text-slate-300">
              <span className="w-3 h-3 rounded-sm bg-rose-400" />
              Bearish / Down
            </div>

            <div className="flex items-center gap-2 text-slate-400">
              <span className="w-0.5 h-4 bg-slate-400" />
              High / Low Wick
            </div>

          </div>

          {/* OHLC */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">

            {[
              ['O', 'Open', 'Starting price'],
              ['H', 'High', 'Highest price'],
              ['L', 'Low', 'Lowest price'],
              ['C', 'Close', 'Ending price'],
            ].map(([letter, name, description]) => (
              <div
                key={letter}
                className="rounded-xl bg-white/5 border border-white/10 p-3"
              >

                <div className="text-lg font-bold text-accent-cyan">
                  {letter}
                </div>

                <div className="text-sm font-semibold text-white mt-1">
                  {name}
                </div>

                <div className="text-[11px] text-slate-500 mt-1">
                  {description}
                </div>

              </div>
            ))}

          </div>

        </div>
      )
    }

    /* =======================================================
       TREND
    ======================================================= */

    if (type === 'trend') {
      return (
        <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 lg:p-7">

          <h3 className="text-base font-bold text-white mb-2">
            Uptrend vs Downtrend
          </h3>

          <p className="text-xs text-slate-500 mb-6">
            A trend shows the general direction in which price is moving.
          </p>

          <div className="grid md:grid-cols-2 gap-5">

            {/* UP */}
            <div className="rounded-xl border border-emerald-400/20 bg-emerald-400/5 p-4">

              <h4 className="text-sm font-bold text-emerald-400 mb-3">
                Uptrend
              </h4>

              <div className="relative h-48 rounded-lg bg-slate-950 overflow-hidden border border-white/10">

                <svg
                  viewBox="0 0 500 200"
                  className="w-full h-full"
                  preserveAspectRatio="none"
                >
                  <polyline
                    points="20,160 90,135 150,145 220,105 280,115 350,65 420,80 480,30"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="5"
                    className="text-emerald-400"
                  />

                  {[
                    [20, 160],
                    [90, 135],
                    [150, 145],
                    [220, 105],
                    [280, 115],
                    [350, 65],
                    [420, 80],
                    [480, 30],
                  ].map(([cx, cy], index) => (
                    <circle
                      key={index}
                      cx={cx}
                      cy={cy}
                      r="6"
                      className="fill-emerald-400"
                    />
                  ))}
                </svg>

                <div className="absolute bottom-3 left-3 text-[10px] text-slate-500">
                  Higher highs + higher lows
                </div>

              </div>

              <p className="text-xs text-slate-400 mt-3">
                Price generally moves upward over time.
              </p>

            </div>

            {/* DOWN */}
            <div className="rounded-xl border border-rose-400/20 bg-rose-400/5 p-4">

              <h4 className="text-sm font-bold text-rose-400 mb-3">
                Downtrend
              </h4>

              <div className="relative h-48 rounded-lg bg-slate-950 overflow-hidden border border-white/10">

                <svg
                  viewBox="0 0 500 200"
                  className="w-full h-full"
                  preserveAspectRatio="none"
                >
                  <polyline
                    points="20,30 90,60 150,45 220,95 280,80 350,130 420,115 480,170"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="5"
                    className="text-rose-400"
                  />

                  {[
                    [20, 30],
                    [90, 60],
                    [150, 45],
                    [220, 95],
                    [280, 80],
                    [350, 130],
                    [420, 115],
                    [480, 170],
                  ].map(([cx, cy], index) => (
                    <circle
                      key={index}
                      cx={cx}
                      cy={cy}
                      r="6"
                      className="fill-rose-400"
                    />
                  ))}
                </svg>

                <div className="absolute bottom-3 left-3 text-[10px] text-slate-500">
                  Lower highs + lower lows
                </div>

              </div>

              <p className="text-xs text-slate-400 mt-3">
                Price generally moves downward over time.
              </p>

            </div>

          </div>

          <div className="mt-5 rounded-xl bg-white/5 border border-white/10 p-4">

            <p className="text-xs text-slate-400 leading-5">
              <span className="font-semibold text-white">
                Remember:
              </span>{' '}
              Trends describe the general direction of price
              movement. Short-term movements can move against
              the broader trend.
            </p>

          </div>

        </div>
      )
    }

    /* =======================================================
       SUPPORT & RESISTANCE
    ======================================================= */

    if (type === 'support-resistance') {
      return (
        <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5 lg:p-7">

          <h3 className="text-base font-bold text-white mb-2">
            Support & Resistance
          </h3>

          <p className="text-xs text-slate-500 mb-6">
            Support is an area where price may find buying
            interest. Resistance is an area where price may
            face selling pressure.
          </p>

          <div className="relative h-72 rounded-xl border border-white/10 bg-slate-950 overflow-hidden">

            {/* Support */}
            <div className="absolute left-0 right-0 bottom-[25%] border-t-2 border-dashed border-emerald-400/70" />

            {/* Resistance */}
            <div className="absolute left-0 right-0 top-[22%] border-t-2 border-dashed border-rose-400/70" />

            {/* Support Label */}
            <div className="absolute right-4 bottom-[25%] -translate-y-1/2 px-2 py-1 rounded-md bg-emerald-400/10 border border-emerald-400/20">
              <span className="text-[11px] font-semibold text-emerald-400">
                Support
              </span>
            </div>

            {/* Resistance Label */}
            <div className="absolute right-4 top-[22%] -translate-y-1/2 px-2 py-1 rounded-md bg-rose-400/10 border border-rose-400/20">
              <span className="text-[11px] font-semibold text-rose-400">
                Resistance
              </span>
            </div>

            {/* Price Line */}
            <svg
              viewBox="0 0 700 280"
              className="absolute inset-0 w-full h-full"
              preserveAspectRatio="none"
            >
              <polyline
                points="
                  20,205
                  65,155
                  105,185
                  145,105
                  190,55
                  230,105
                  270,180
                  315,215
                  355,165
                  400,70
                  445,105
                  485,190
                  530,215
                  575,150
                  620,65
                  675,105
                "
                fill="none"
                stroke="currentColor"
                strokeWidth="5"
                className="text-accent-cyan"
              />

              <circle
                cx="190"
                cy="55"
                r="7"
                className="fill-rose-400"
              />

              <circle
                cx="315"
                cy="215"
                r="7"
                className="fill-emerald-400"
              />

              <circle
                cx="445"
                cy="105"
                r="7"
                className="fill-rose-400"
              />

              <circle
                cx="530"
                cy="215"
                r="7"
                className="fill-emerald-400"
              />

              <circle
                cx="620"
                cy="65"
                r="7"
                className="fill-rose-400"
              />
            </svg>

            <div className="absolute left-4 top-4 text-[10px] text-slate-600">
              Price
            </div>

            <div className="absolute bottom-3 left-1/2 -translate-x-1/2 text-[10px] text-slate-600">
              Time →
            </div>

          </div>

          {/* Explanation */}
          <div className="grid md:grid-cols-2 gap-4 mt-5">

            <div className="rounded-xl bg-emerald-400/5 border border-emerald-400/20 p-4">

              <h4 className="text-sm font-bold text-emerald-400 mb-2">
                Support
              </h4>

              <p className="text-xs text-slate-400 leading-5">
                A price area where buying interest may increase
                and downward movement may temporarily slow or
                reverse.
              </p>

            </div>

            <div className="rounded-xl bg-rose-400/5 border border-rose-400/20 p-4">

              <h4 className="text-sm font-bold text-rose-400 mb-2">
                Resistance
              </h4>

              <p className="text-xs text-slate-400 leading-5">
                A price area where selling interest may increase
                and upward movement may temporarily slow or
                reverse.
              </p>

            </div>

          </div>

          <div className="mt-5 rounded-xl bg-white/5 border border-white/10 p-4">

            <p className="text-xs text-slate-400 leading-5">
              <span className="font-semibold text-white">
                Remember:
              </span>{' '}
              Support and resistance are areas, not guaranteed
              exact prices. Price can break through either level.
            </p>

          </div>

        </div>
      )
    }

    return null
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">

      {/* Back */}
      <div className="flex items-center justify-between gap-4">

        <button
          onClick={() =>
            navigate(`/app/academy/module/${module.id}`)
          }
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft size={17} />
          Back to {module.title}
        </button>

        <span className="text-xs text-slate-500">
          Lesson {lesson.lesson_order} of {lessons.length}
        </span>

      </div>

      {/* Header */}
      <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-accent-blue/15 via-navy-900 to-accent-cyan/10 p-6 lg:p-8">

        <div className="absolute -top-24 -right-24 w-64 h-64 rounded-full bg-accent-cyan/10 blur-3xl" />

        <div className="relative">

          <div className="flex flex-wrap items-center gap-2 mb-4">

            <span className="text-[11px] px-2.5 py-1 rounded-full bg-accent-cyan/10 border border-accent-cyan/20 text-accent-cyan font-semibold">
              {lesson.level}
            </span>

            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <Clock size={14} />
              {lesson.estimated_minutes} min
            </span>

          </div>

          <h1 className="text-2xl lg:text-4xl font-bold text-white leading-tight">
            {lesson.title}
          </h1>

          <p className="mt-3 text-sm text-slate-500">
            {module.title}
          </p>

        </div>
      </section>

      {/* Objectives */}
      {content.objectives?.length > 0 && (
        <section className="card p-5 lg:p-7">

          <div className="flex items-center gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
              <Target
                size={20}
                className="text-accent-blue"
              />
            </div>

            <div>
              <h2 className="font-bold text-white">
                What You'll Learn
              </h2>

              <p className="text-xs text-slate-500 mt-0.5">
                Learning objectives for this lesson
              </p>
            </div>

          </div>

          <div className="space-y-3">

            {content.objectives.map((objective, index) => (
              <div
                key={index}
                className="flex items-start gap-3"
              >

                <div className="mt-0.5 w-6 h-6 rounded-full bg-accent-cyan/10 flex items-center justify-center shrink-0">
                  <Check
                    size={14}
                    className="text-accent-cyan"
                  />
                </div>

                <p className="text-sm text-slate-300 leading-6">
                  {objective}
                </p>

              </div>
            ))}

          </div>

        </section>
      )}

      {/* Visual Learning */}
      {visualType && (
        <section className="card p-5 lg:p-7">

          <div className="flex items-center gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-accent-cyan/10 flex items-center justify-center">
              <span className="text-lg">
                📊
              </span>
            </div>

            <div>
              <h2 className="font-bold text-white">
                Visual Learning
              </h2>

              <p className="text-xs text-slate-500 mt-0.5">
                Learn the concept visually
              </p>
            </div>

          </div>

          <LearningVisual type={visualType} />

        </section>
      )}

      {/* Explanation */}
      {content.explanation && (
        <section className="card p-5 lg:p-7">

          <div className="flex items-center gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
              <BookOpen
                size={20}
                className="text-purple-400"
              />
            </div>

            <h2 className="font-bold text-white">
              Explanation
            </h2>

          </div>

          <p className="text-sm lg:text-base text-slate-300 leading-7">
            {content.explanation}
          </p>

        </section>
      )}

      {/* Example */}
      {content.example && (
        <section className="rounded-2xl border border-accent-cyan/15 bg-accent-cyan/5 p-5 lg:p-7">

          <div className="flex items-center gap-3 mb-4">

            <div className="w-10 h-10 rounded-xl bg-accent-cyan/10 flex items-center justify-center">
              <Lightbulb
                size={20}
                className="text-accent-cyan"
              />
            </div>

            <div>
              <h2 className="font-bold text-white">
                Simple Example
              </h2>

              <p className="text-xs text-slate-500">
                Understand the concept with an example
              </p>
            </div>

          </div>

          <p className="text-sm text-slate-300 leading-7">
            {content.example}
          </p>

        </section>
      )}

      {/* Key Terms */}
      {content.key_terms?.length > 0 && (
        <section className="card p-5 lg:p-7">

          <h2 className="font-bold text-white mb-4">
            Key Terms
          </h2>

          <div className="flex flex-wrap gap-2">

            {content.key_terms.map((term, index) => (
              <span
                key={index}
                className="px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-sm text-slate-300"
              >
                {term}
              </span>
            ))}

          </div>

        </section>
      )}

      {/* Takeaways */}
      {content.takeaways?.length > 0 && (
        <section className="card p-5 lg:p-7">

          <div className="flex items-center gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
              <CheckCircle2
                size={20}
                className="text-emerald-400"
              />
            </div>

            <h2 className="font-bold text-white">
              Key Takeaways
            </h2>

          </div>

          <div className="space-y-3">

            {content.takeaways.map((takeaway, index) => (
              <div
                key={index}
                className="flex items-start gap-3"
              >

                <span className="text-emerald-400 font-bold">
                  ✓
                </span>

                <p className="text-sm text-slate-300 leading-6">
                  {takeaway}
                </p>

              </div>
            ))}

          </div>

        </section>
      )}

      {/* Complete */}
      <section className="card p-5 lg:p-7">

        {completed ? (
          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">

            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

              <div className="flex items-center gap-3">

                <div className="w-11 h-11 rounded-full bg-emerald-500/10 flex items-center justify-center">
                  <CheckCircle2
                    size={23}
                    className="text-emerald-400"
                  />
                </div>

                <div>

                  <h3 className="font-semibold text-white">
                    Lesson Completed
                  </h3>

                  <p className="text-xs text-slate-500 mt-1">
                    Great job. Your Academy progress has been updated.
                  </p>

                </div>

              </div>

              <button
                onClick={goToNextLesson}
                className="btn-primary flex items-center justify-center gap-2"
              >
                {nextLesson
                  ? 'Next Lesson'
                  : 'Back to Module'}

                <ArrowRight size={17} />
              </button>

            </div>

          </div>
        ) : (
          <div className="text-center">

            <h3 className="font-semibold text-white">
              Finished this lesson?
            </h3>

            <p className="text-xs text-slate-500 mt-1 mb-5">
              Mark it as complete to update your Academy progress.
            </p>

            <button
              onClick={completeCurrentLesson}
              disabled={completing}
              className="btn-primary inline-flex items-center justify-center gap-2 disabled:opacity-60"
            >

              {completing ? (
                <>
                  <Loader2
                    size={17}
                    className="animate-spin"
                  />
                  Saving...
                </>
              ) : (
                <>
                  <CheckCircle2 size={17} />
                  Mark as Complete
                </>
              )}

            </button>

          </div>
        )}

      </section>

      {/* Previous / Next */}
      <div className="flex items-center justify-between gap-3">

        {previousLesson ? (
          <button
            onClick={() =>
              navigate(
                `/app/academy/lesson/${previousLesson.id}`
              )
            }
            className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft size={16} />
            Previous
          </button>
        ) : (
          <div />
        )}

        {nextLesson && (
          <button
            onClick={goToNextLesson}
            className="flex items-center gap-2 text-sm text-slate-400 hover:text-accent-cyan transition-colors"
          >
            Next
            <ArrowRight size={16} />
          </button>
        )}

      </div>

      {/* Disclaimer */}
      <p className="text-center text-[11px] text-slate-600 max-w-3xl mx-auto">
        This lesson is for educational purposes only. Learning
        about financial markets does not guarantee profits, and
        trading involves financial risk.
      </p>

    </div>
  )
}