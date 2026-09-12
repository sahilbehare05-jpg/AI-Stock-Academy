import React, { useState, useRef, useEffect } from 'react'
import {
  Send,
  Trash2,
  Sparkles,
  BookOpen,
  Brain,
  TrendingUp,
  BarChart3,
  ShieldCheck,
  Lightbulb,
  User,
  Bot,
  ChevronDown,
} from 'lucide-react'
import { tutorAPI } from '../services/api'

const LEVELS = [
  {
    value: 'Beginner',
    label: 'Beginner',
    description: 'Simple explanations and examples',
  },
  {
    value: 'Intermediate',
    label: 'Intermediate',
    description: 'Technical concepts with practical context',
  },
  {
    value: 'Advanced',
    label: 'Advanced',
    description: 'Deeper market reasoning',
  },
  {
    value: 'Expert',
    label: 'Expert',
    description: 'Advanced trading concepts',
  },
]

const SUGGESTED_QUESTIONS = [
  {
    icon: BookOpen,
    title: 'Learn Candlesticks',
    question: 'What is a candlestick and how do I read it?',
  },
  {
    icon: TrendingUp,
    title: 'Understand Trends',
    question: 'What is an uptrend and downtrend?',
  },
  {
    icon: BarChart3,
    title: 'Learn RSI',
    question: 'What is RSI and how is it used?',
  },
  {
    icon: ShieldCheck,
    title: 'Manage Risk',
    question: 'What is risk management in trading?',
  },
]

const STARTER_MESSAGES = [
  {
    role: 'assistant',
    content:
      "Hello! I'm your AI Trading Tutor. 👋\n\nAsk me anything about the stock market, trading, candlesticks, technical analysis, indicators, risk management, or other trading concepts.\n\nI'll explain the concept step by step according to your selected learning level.",
  },
]

function Tutor() {
  const [messages, setMessages] = useState(STARTER_MESSAGES)
  const [question, setQuestion] = useState('')
  const [level, setLevel] = useState('Beginner')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    })
  }, [messages, loading])

  const askQuestion = async (text = question) => {
    const trimmedQuestion = text.trim()

    if (!trimmedQuestion || loading) return

    setError('')

    const userMessage = {
      role: 'user',
      content: trimmedQuestion,
    }

    setMessages((prev) => [...prev, userMessage])
    setQuestion('')
    setLoading(true)

    try {
      const response = await tutorAPI.chat({
        question: trimmedQuestion,
        level,
        context: '',
      })

      const answer =
        response?.data?.answer ||
        response?.data?.data?.answer ||
        response?.data?.message ||
        'I could not generate an answer right now.'

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: answer,
        },
      ])
    } catch (err) {
      console.error('Tutor error:', err)

      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Unable to connect to the AI Trading Tutor.'

      setError(message)

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            'Sorry, I could not process that question right now. Please try again.',
          error: true,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    askQuestion()
  }

  const clearChat = () => {
    setMessages(STARTER_MESSAGES)
    setQuestion('')
    setError('')
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit(event)
    }
  }

  const formatMessage = (content) => {
    const lines = content.split('\n')

    return lines.map((line, index) => {
      const trimmed = line.trim()

      if (!trimmed) {
        return <div key={index} className="h-2" />
      }

      if (trimmed.startsWith('### ')) {
        return (
          <h3
            key={index}
            className="text-base font-bold text-white mt-2 mb-2"
          >
            {trimmed.replace('### ', '')}
          </h3>
        )
      }

      if (trimmed.startsWith('## ')) {
        return (
          <h3
            key={index}
            className="text-base font-bold text-white mt-2 mb-2"
          >
            {trimmed.replace('## ', '')}
          </h3>
        )
      }

      if (trimmed.startsWith('- ')) {
        return (
          <div
            key={index}
            className="flex gap-2 text-sm text-slate-300 mb-1"
          >
            <span className="text-cyan-400">•</span>
            <span>{trimmed.substring(2)}</span>
          </div>
        )
      }

      if (/^\d+\.\s/.test(trimmed)) {
        const match = trimmed.match(/^(\d+)\.\s(.*)$/)

        return (
          <div
            key={index}
            className="flex gap-2 text-sm text-slate-300 mb-1"
          >
            <span className="text-cyan-400 font-semibold">
              {match[1]}.
            </span>
            <span>{match[2]}</span>
          </div>
        )
      }

      const parts = trimmed.split(/(\*\*.*?\*\*)/g)

      return (
        <p
          key={index}
          className="text-sm text-slate-300 leading-6 mb-1"
        >
          {parts.map((part, i) => {
            if (
              part.startsWith('**') &&
              part.endsWith('**')
            ) {
              return (
                <strong key={i} className="text-white font-semibold">
                  {part.slice(2, -2)}
                </strong>
              )
            }

            return <React.Fragment key={i}>{part}</React.Fragment>
          })}
        </p>
      )
    })
  }

  return (
    <div className="min-h-full pb-8">
      {/* ===================================================== */}
      {/* HEADER */}
      {/* ===================================================== */}

      <div className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-11 h-11 rounded-xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-cyan-400" />
              </div>

              <div>
                <h1 className="text-2xl lg:text-3xl font-bold text-white">
                  AI Trading Tutor
                </h1>

                <p className="text-sm text-slate-500 mt-1">
                  Your personal trading education assistant
                </p>
              </div>
            </div>
          </div>

          {/* LEVEL SELECTOR */}

          <div className="relative">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1.5">
              Learning Level
            </div>

            <div className="relative">
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="appearance-none min-w-[190px] bg-slate-900 border border-white/10 rounded-xl px-4 py-3 pr-10 text-sm text-white outline-none focus:border-cyan-400/40 cursor-pointer"
              >
                {LEVELS.map((item) => (
                  <option
                    key={item.value}
                    value={item.value}
                    className="bg-slate-900"
                  >
                    {item.label}
                  </option>
                ))}
              </select>

              <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
            </div>
          </div>
        </div>
      </div>

      {/* ===================================================== */}
      {/* INFO CARDS */}
      {/* ===================================================== */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="rounded-2xl border border-white/10 bg-slate-900/50 p-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-cyan-400/10 flex items-center justify-center">
              <Brain className="w-4 h-4 text-cyan-400" />
            </div>

            <div>
              <div className="text-sm font-semibold text-white">
                Learn Step by Step
              </div>
              <div className="text-xs text-slate-500 mt-0.5">
                From basics to advanced concepts
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-white/10 bg-slate-900/50 p-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-400/10 flex items-center justify-center">
              <Lightbulb className="w-4 h-4 text-emerald-400" />
            </div>

            <div>
              <div className="text-sm font-semibold text-white">
                Practical Examples
              </div>
              <div className="text-xs text-slate-500 mt-0.5">
                Understand concepts with examples
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-white/10 bg-slate-900/50 p-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-violet-400/10 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4 text-violet-400" />
            </div>

            <div>
              <div className="text-sm font-semibold text-white">
                Risk Aware
              </div>
              <div className="text-xs text-slate-500 mt-0.5">
                Education, not guaranteed signals
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ===================================================== */}
      {/* MAIN CHAT */}
      {/* ===================================================== */}

      <div className="grid lg:grid-cols-[1fr_300px] gap-6">
        <div className="rounded-2xl border border-white/10 bg-slate-950/60 overflow-hidden flex flex-col min-h-[650px]">
          {/* CHAT HEADER */}

          <div className="flex items-center justify-between px-5 py-4 border-b border-white/10 bg-slate-900/40">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-10 h-10 rounded-xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-cyan-400" />
                </div>

                <span className="absolute -right-0.5 -bottom-0.5 w-3 h-3 rounded-full bg-emerald-400 border-2 border-slate-950" />
              </div>

              <div>
                <div className="text-sm font-bold text-white">
                  Trading Tutor
                </div>

                <div className="text-xs text-emerald-400 mt-0.5">
                  Ready to teach • {level}
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={clearChat}
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-slate-400 hover:text-white hover:bg-white/5 transition"
              title="Clear conversation"
            >
              <Trash2 className="w-4 h-4" />
              <span className="hidden sm:inline">
                Clear
              </span>
            </button>
          </div>

          {/* MESSAGES */}

          <div className="flex-1 overflow-y-auto p-5 space-y-5 max-h-[570px]">
            {messages.map((message, index) => {
              const isUser = message.role === 'user'

              return (
                <div
                  key={index}
                  className={`flex gap-3 ${
                    isUser ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {!isUser && (
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-cyan-400" />
                    </div>
                  )}

                  <div
                    className={`max-w-[85%] ${
                      isUser
                        ? 'rounded-2xl rounded-tr-md bg-cyan-400/10 border border-cyan-400/20'
                        : 'rounded-2xl rounded-tl-md bg-white/[0.03] border border-white/10'
                    } px-4 py-3`}
                  >
                    {isUser ? (
                      <p className="text-sm text-slate-200 leading-6 whitespace-pre-wrap">
                        {message.content}
                      </p>
                    ) : (
                      <div>
                        {formatMessage(message.content)}

                        {message.error && (
                          <div className="mt-3 text-xs text-rose-400">
                            Please try again.
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {isUser && (
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-violet-400/10 border border-violet-400/20 flex items-center justify-center">
                      <User className="w-4 h-4 text-violet-300" />
                    </div>
                  )}
                </div>
              )
            })}

            {loading && (
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-cyan-400" />
                </div>

                <div className="rounded-2xl rounded-tl-md bg-white/[0.03] border border-white/10 px-4 py-4">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" />
                    <span
                      className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce"
                      style={{ animationDelay: '150ms' }}
                    />
                    <span
                      className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce"
                      style={{ animationDelay: '300ms' }}
                    />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* ERROR */}

          {error && (
            <div className="mx-5 mb-3 rounded-xl border border-rose-400/20 bg-rose-400/5 px-4 py-3 text-xs text-rose-300">
              {error}
            </div>
          )}

          {/* INPUT */}

          <div className="border-t border-white/10 p-4 bg-slate-900/30">
            <form
              onSubmit={handleSubmit}
              className="flex items-end gap-3"
            >
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={2}
                disabled={loading}
                placeholder="Ask your trading question..."
                className="flex-1 resize-none rounded-xl bg-slate-950 border border-white/10 px-4 py-3 text-sm text-white placeholder:text-slate-600 outline-none focus:border-cyan-400/40 transition disabled:opacity-50"
              />

              <button
                type="submit"
                disabled={!question.trim() || loading}
                className="flex-shrink-0 w-12 h-12 rounded-xl bg-cyan-400 text-slate-950 flex items-center justify-center hover:bg-cyan-300 transition disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>

            <div className="flex items-center justify-between mt-2 px-1">
              <span className="text-[10px] text-slate-600">
                Press Enter to send • Shift + Enter for new line
              </span>

              <span className="text-[10px] text-slate-600">
                Educational use only
              </span>
            </div>
          </div>
        </div>

        {/* ================================================= */}
        {/* SUGGESTED QUESTIONS */}
        {/* ================================================= */}

        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-4 h-4 text-cyan-400" />

              <h2 className="text-sm font-bold text-white">
                Suggested Questions
              </h2>
            </div>

            <div className="space-y-2">
              {SUGGESTED_QUESTIONS.map((item) => {
                const Icon = item.icon

                return (
                  <button
                    key={item.title}
                    type="button"
                    onClick={() => askQuestion(item.question)}
                    disabled={loading}
                    className="w-full text-left rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.05] hover:border-cyan-400/20 p-3 transition disabled:opacity-50"
                  >
                    <div className="flex gap-3">
                      <div className="w-8 h-8 flex-shrink-0 rounded-lg bg-cyan-400/10 flex items-center justify-center">
                        <Icon className="w-4 h-4 text-cyan-400" />
                      </div>

                      <div>
                        <div className="text-xs font-semibold text-white">
                          {item.title}
                        </div>

                        <div className="text-[11px] text-slate-500 mt-1 leading-4">
                          {item.question}
                        </div>
                      </div>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

          {/* LEARNING LEVEL */}

          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
            <h2 className="text-sm font-bold text-white mb-3">
              Current Level
            </h2>

            {(() => {
              const current = LEVELS.find(
                (item) => item.value === level
              )

              return (
                <div className="rounded-xl bg-cyan-400/5 border border-cyan-400/10 p-4">
                  <div className="text-sm font-bold text-cyan-400">
                    {current?.label}
                  </div>

                  <div className="text-xs text-slate-500 mt-1 leading-5">
                    {current?.description}
                  </div>
                </div>
              )
            })()}
          </div>

          {/* TUTOR RULE */}

          <div className="rounded-2xl border border-amber-400/10 bg-amber-400/5 p-4">
            <div className="flex gap-3">
              <ShieldCheck className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />

              <div>
                <div className="text-xs font-semibold text-amber-300">
                  Remember
                </div>

                <p className="text-[11px] text-slate-500 mt-1 leading-5">
                  The Tutor is designed for education. It does not
                  guarantee profits or provide guaranteed trading
                  signals.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Tutor