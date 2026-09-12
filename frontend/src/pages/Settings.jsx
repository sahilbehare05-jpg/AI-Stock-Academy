import React, { useEffect, useState } from 'react'
import { changeLanguage } from '../utils/i18n'
import {
  Settings as SettingsIcon,
  Globe,
  Bell,
  Brain,
  GraduationCap,
  Save,
  RotateCcw,
  CheckCircle2,
} from 'lucide-react'

const DEFAULT_SETTINGS = {
  language: 'English',
  notifications: true,
  predictionConfidence: true,
  simulationMode: true,
}

export default function Settings() {
  const [settings, setSettings] = useState(DEFAULT_SETTINGS)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    try {
      const stored = localStorage.getItem('asa_settings')

      if (stored) {
        setSettings({
          ...DEFAULT_SETTINGS,
          ...JSON.parse(stored),
        })
      }
    } catch (error) {
      console.error('Failed to load settings:', error)
    }
  }, [])

  const updateSetting = (key, value) => {
    setSettings((previous) => ({
      ...previous,
      [key]: value,
    }))

    setSaved(false)
  }

  const saveSettings = () => {
    localStorage.setItem(
      'asa_settings',
      JSON.stringify(settings)
    )

    setSaved(true)

    setTimeout(() => {
      setSaved(false)
    }, 3000)
  }

  const resetSettings = () => {
    setSettings(DEFAULT_SETTINGS)

    localStorage.setItem(
      'asa_settings',
      JSON.stringify(DEFAULT_SETTINGS)
    )

    setSaved(true)

    setTimeout(() => {
      setSaved(false)
    }, 3000)
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <div className="flex items-center gap-3">

          <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
            <SettingsIcon
              size={23}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              Settings
            </h1>

            <p className="text-slate-400 mt-1">
              Manage your AI Stock Academy preferences.
            </p>
          </div>

        </div>
      </div>

      {/* Success Message */}
      {saved && (
        <div className="card p-4 border border-emerald-500/30 bg-emerald-500/5">
          <div className="flex items-center gap-2">

            <CheckCircle2
              size={18}
              className="text-emerald-400"
            />

            <p className="text-sm text-emerald-400">
              Settings saved successfully.
            </p>

          </div>
        </div>
      )}

      {/* General Settings */}
      <div className="card p-6">

        <div className="flex items-center gap-3 mb-6">

          <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
            <Globe
              size={20}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              General
            </h2>

            <p className="text-sm text-slate-500">
              Basic application preferences.
            </p>
          </div>

        </div>

        <div className="space-y-5">

          {/* Language */}
          <SettingRow
            icon={<Globe size={19} />}
            title="Language"
            description="Choose the language used by the application."
          >
            <select
              value={settings.language}
              onChange={(e) => {
  const language = e.target.value

  updateSetting('language', language)

  const languageCodes = {
    English: 'en',
    Hindi: 'hi',
    Marathi: 'mr',
  }

  changeLanguage(languageCodes[language])
}}
              className="input w-full sm:w-48 text-white bg-slate-950 border-slate-700"
            >
              <option value="English">English</option>
              <option value="Hindi">Hindi</option>
              <option value="Marathi">Marathi</option>
            </select>
          </SettingRow>

          {/* Notifications */}
          <SettingRow
            icon={<Bell size={19} />}
            title="Notifications"
            description="Allow application notifications and alerts."
          >
            <Toggle
              checked={settings.notifications}
              onChange={(value) =>
                updateSetting('notifications', value)
              }
            />
          </SettingRow>

        </div>
      </div>

      {/* Prediction Settings */}
      <div className="card p-6">

        <div className="flex items-center gap-3 mb-6">

          <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
            <Brain
              size={20}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              AI Prediction
            </h2>

            <p className="text-sm text-slate-500">
              Configure how prediction information is displayed.
            </p>
          </div>

        </div>

        <SettingRow
          icon={<Brain size={19} />}
          title="Show Model Confidence"
          description="Display the Random Forest classification confidence on prediction pages."
        >
          <Toggle
            checked={settings.predictionConfidence}
            onChange={(value) =>
              updateSetting('predictionConfidence', value)
            }
          />
        </SettingRow>

      </div>

      {/* Learning & Trading */}
      <div className="card p-6">

        <div className="flex items-center gap-3 mb-6">

          <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
            <GraduationCap
              size={20}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              Learning & Trading
            </h2>

            <p className="text-sm text-slate-500">
              Preferences for the educational trading environment.
            </p>
          </div>

        </div>

        <SettingRow
          icon={<GraduationCap size={19} />}
          title="Simulation Mode"
          description="Keep trading activities in virtual/simulated mode for educational practice."
        >
          <Toggle
            checked={settings.simulationMode}
            onChange={(value) =>
              updateSetting('simulationMode', value)
            }
          />
        </SettingRow>

        <div className="mt-5 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
          <p className="text-sm font-medium text-amber-400">
            Educational Simulation
          </p>

          <p className="text-xs text-slate-500 mt-1 leading-5">
            AI Stock Academy uses virtual trading and educational
            predictions. No real-money trading is performed through
            the application.
          </p>
        </div>

      </div>

      {/* Actions */}
      <div className="card p-5">

        <div className="flex flex-col sm:flex-row gap-3 sm:justify-end">

          <button
            onClick={resetSettings}
            className="px-5 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-white/5 flex items-center justify-center gap-2 transition-colors"
          >
            <RotateCcw size={17} />
            Reset Settings
          </button>

          <button
            onClick={saveSettings}
            className="btn btn-primary flex items-center justify-center gap-2"
          >
            <Save size={17} />
            Save Settings
          </button>

        </div>

      </div>

      {/* Information */}
      <div className="card p-5 border border-slate-800">

        <p className="text-sm font-semibold text-white">
          Settings Storage
        </p>

        <p className="text-xs text-slate-500 mt-1 leading-5">
          Your application preferences are stored locally in this
          browser. They do not modify your account credentials or
          virtual trading balance.
        </p>

      </div>

    </div>
  )
}

function SettingRow({
  icon,
  title,
  description,
  children,
}) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/50 p-4">

      <div className="flex items-start gap-3">

        <div className="text-accent-blue mt-0.5">
          {icon}
        </div>

        <div>
          <p className="text-sm font-semibold text-white">
            {title}
          </p>

          <p className="text-xs text-slate-500 mt-1 max-w-xl leading-5">
            {description}
          </p>
        </div>

      </div>

      <div className="shrink-0">
        {children}
      </div>

    </div>
  )
}

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`relative w-12 h-6 rounded-full transition-colors ${
        checked
          ? 'bg-accent-blue'
          : 'bg-slate-700'
      }`}
      aria-pressed={checked}
    >
      <span
        className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all duration-200 ${
          checked
            ? 'right-1'
            : 'left-1'
        }`}
      />
    </button>
  )
}