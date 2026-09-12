import React, { useEffect, useState } from 'react'
import {
  User,
  Mail,
  Calendar,
  ShieldCheck,
  Edit3,
  Save,
  X,
  RefreshCw,
} from 'lucide-react'
import { authAPI } from '../services/api'

export default function Profile() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [editing, setEditing] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [name, setName] = useState('')

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await authAPI.me()
      const profile = response.data.data || response.data

      setUser(profile)
      setName(profile?.name || profile?.full_name || '')
    } catch (err) {
      console.error(err)

      // Fallback to locally stored user information
      try {
        const storedUser = localStorage.getItem('asa_user')

        if (storedUser) {
          const profile = JSON.parse(storedUser)
          setUser(profile)
          setName(profile?.name || profile?.full_name || '')
        } else {
          setError(
            err.response?.data?.detail ||
              'Unable to load profile.'
          )
        }
      } catch {
        setError('Unable to load profile.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSuccess('')
    setError('')

    const cleanName = name.trim()

    if (!cleanName) {
      setError('Name cannot be empty.')
      return
    }

    /*
      The current backend provides /api/auth/me for reading
      profile information but does not provide a profile-update
      endpoint. Therefore, we keep editing local-only until an
      update API is added.
    */

    try {
      setSaving(true)

      const updatedUser = {
        ...user,
        name: cleanName,
      }

      setUser(updatedUser)
      localStorage.setItem(
        'asa_user',
        JSON.stringify(updatedUser)
      )

      setEditing(false)
      setSuccess('Profile information updated locally.')
    } catch (err) {
      console.error(err)
      setError('Unable to update profile.')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setName(user?.name || user?.full_name || '')
    setEditing(false)
    setError('')
    setSuccess('')
  }

  if (loading) {
    return (
      <div className="card p-10 flex flex-col items-center justify-center">
        <RefreshCw
          size={30}
          className="text-accent-blue animate-spin mb-3"
        />

        <p className="text-slate-400">
          Loading profile...
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-accent-blue/10 border border-accent-blue/30 flex items-center justify-center">
            <User
              size={23}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-white">
              Profile
            </h1>

            <p className="text-slate-400 mt-1">
              View and manage your AI Stock Academy profile.
            </p>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-4 border border-red-500/30">
          <p className="text-red-400 text-sm">
            {error}
          </p>
        </div>
      )}

      {/* Success */}
      {success && (
        <div className="card p-4 border border-emerald-500/30">
          <p className="text-emerald-400 text-sm">
            {success}
          </p>
        </div>
      )}

      {/* Profile Card */}
      <div className="card p-6">

        {/* Top */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-5">

          <div className="flex items-center gap-4">

            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-blue to-accent-cyan flex items-center justify-center">
              <User
                size={30}
                className="text-white"
              />
            </div>

            <div>
              <h2 className="text-xl font-bold text-white">
                {user?.name ||
                  user?.full_name ||
                  'AI Stock Academy User'}
              </h2>

              <p className="text-sm text-slate-400 mt-1">
                {user?.email || 'Email not available'}
              </p>
            </div>

          </div>

          {!editing ? (
            <button
              onClick={() => {
                setEditing(true)
                setSuccess('')
                setError('')
              }}
              className="btn btn-primary flex items-center justify-center gap-2"
            >
              <Edit3 size={17} />
              Edit Profile
            </button>
          ) : (
            <div className="flex gap-2">

              <button
                onClick={handleCancel}
                disabled={saving}
                className="px-4 py-2 rounded-xl border border-slate-700 text-slate-300 hover:bg-white/5 flex items-center gap-2"
              >
                <X size={17} />
                Cancel
              </button>

              <button
                onClick={handleSave}
                disabled={saving}
                className="btn btn-primary flex items-center gap-2"
              >
                {saving ? (
                  <RefreshCw
                    size={17}
                    className="animate-spin"
                  />
                ) : (
                  <Save size={17} />
                )}

                {saving ? 'Saving...' : 'Save'}
              </button>

            </div>
          )}

        </div>

        {/* Divider */}
        <div className="border-t border-white/5 my-6" />

        {/* Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* Name */}
          <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-5">

            <div className="flex items-center gap-2 mb-3">
              <User
                size={18}
                className="text-accent-blue"
              />

              <p className="text-sm text-slate-400">
                Name
              </p>
            </div>

            {editing ? (
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                className="input w-full text-white bg-slate-950 border-slate-700"
              />
            ) : (
              <p className="text-white font-semibold">
                {user?.name ||
                  user?.full_name ||
                  'Not provided'}
              </p>
            )}

          </div>

          {/* Email */}
          <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-5">

            <div className="flex items-center gap-2 mb-3">
              <Mail
                size={18}
                className="text-accent-blue"
              />

              <p className="text-sm text-slate-400">
                Email Address
              </p>
            </div>

            <p className="text-white font-semibold break-all">
              {user?.email || 'Not available'}
            </p>

          </div>

          {/* Account ID */}
          <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-5">

            <div className="flex items-center gap-2 mb-3">
              <ShieldCheck
                size={18}
                className="text-accent-blue"
              />

              <p className="text-sm text-slate-400">
                Account ID
              </p>
            </div>

            <p className="text-white font-semibold text-sm break-all">
              {user?.id ||
                user?._id ||
                'Not available'}
            </p>

          </div>

          {/* Account Status */}
          <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-5">

            <div className="flex items-center gap-2 mb-3">
              <ShieldCheck
                size={18}
                className="text-accent-blue"
              />

              <p className="text-sm text-slate-400">
                Account Status
              </p>
            </div>

            <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              Active
            </span>

          </div>

        </div>
      </div>

      {/* Academy Profile Information */}
      <div className="card p-6">

        <div className="flex items-center gap-3 mb-5">
          <div className="w-10 h-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
            <Calendar
              size={20}
              className="text-accent-blue"
            />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              Learning Profile
            </h2>

            <p className="text-sm text-slate-500">
              Your account is connected to the AI Stock Academy learning system.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <InfoCard
            title="Learning Mode"
            value="Educational"
          />

          <InfoCard
            title="Trading Mode"
            value="Virtual / Simulated"
          />

          <InfoCard
            title="Prediction Model"
            value="Random Forest"
          />

        </div>
      </div>

      {/* Security Notice */}
      <div className="card p-5 border border-slate-800">
        <div className="flex gap-3">

          <ShieldCheck
            size={20}
            className="text-accent-blue shrink-0 mt-0.5"
          />

          <div>
            <p className="text-sm font-semibold text-white">
              Account Security
            </p>

            <p className="text-xs text-slate-500 mt-1 leading-5">
              Your account uses authenticated access to protect
              your academy data, prediction history, watchlist
              and virtual trading information.
            </p>
          </div>

        </div>
      </div>

    </div>
  )
}

function InfoCard({ title, value }) {
  return (
    <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
      <p className="text-xs text-slate-500">
        {title}
      </p>

      <p className="text-sm font-semibold text-white mt-1">
        {value}
      </p>
    </div>
  )
}