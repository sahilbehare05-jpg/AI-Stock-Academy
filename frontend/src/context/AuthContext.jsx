import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authAPI } from '../services/api'
import { changeLanguage } from '../utils/i18n'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('asa_user')
    return saved ? JSON.parse(saved) : null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('asa_token')
    if (!token) {
      setLoading(false)
      return
    }
    authAPI
      .me()
      .then((res) => {
        setUser(res.data)
        localStorage.setItem('asa_user', JSON.stringify(res.data))
      })
      .catch(() => {
        localStorage.removeItem('asa_token')
        localStorage.removeItem('asa_user')
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const persistSession = (data) => {
    localStorage.setItem('asa_token', data.access_token)
    localStorage.setItem('asa_user', JSON.stringify(data.user))
    setUser(data.user)
    if (data.user?.preferred_language) {
      changeLanguage(data.user.preferred_language)
    }
  }

  const login = useCallback(async (email, password) => {
    const res = await authAPI.login({ email, password })
    persistSession(res.data)
    return res.data.user
  }, [])

  const register = useCallback(async (name, email, password, preferred_language) => {
    const res = await authAPI.register({ name, email, password, preferred_language })
    persistSession(res.data)
    return res.data.user
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('asa_token')
    localStorage.removeItem('asa_user')
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
