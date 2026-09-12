import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Landing from './pages/Landing.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Dashboard from './pages/Dashboard.jsx'
import DashboardLayout from './layouts/DashboardLayout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import PlaceholderPage from './components/PlaceholderPage.jsx'
import StockAnalysis from './pages/StockAnalysis.jsx'
import WhyPrediction from './pages/WhyPrediction.jsx'
import AIPrediction from './pages/AIPrediction.jsx'
import VirtualWallet from './pages/VirtualWallet.jsx'
import VirtualTrading from './pages/VirtualTrading.jsx'
import Portfolio from './pages/Portfolio.jsx'
import Watchlist from './pages/Watchlist.jsx'
import PredictionHistory from './pages/PredictionHistory.jsx'
import News from './pages/News.jsx'
import Academy from './pages/Academy.jsx'
import AcademyModule from './pages/AcademyModule.jsx'
import AcademyLesson from './pages/AcademyLesson.jsx'
import PracticeLab from './pages/PracticeLab.jsx'
import Tutor from './pages/Tutor.jsx'
import ModelPerformance from './pages/ModelPerformance.jsx'
import Profile from './pages/Profile.jsx'
import Settings from './pages/Settings.jsx'

// Pages not yet built are rendered as clearly-labeled placeholders per
// the phased development roadmap (see docs/ROADMAP.md). Each will be
// implemented in its corresponding phase (4-13).
const placeholders = [
  { path: 'academy', title: 'Trading Academy', phase: 'Phase 8 — Trading Academy' },

  
]

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />


      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="stock-analysis" element={<StockAnalysis />} />
        <Route path="why-prediction" element={<WhyPrediction />} />
        <Route path="ai-prediction" element={<AIPrediction />} />
        <Route path="wallet" element={<VirtualWallet />} />
        <Route path="trading" element={<VirtualTrading />} />
        <Route path="portfolio" element={<Portfolio />} />
        <Route path="prediction-history" element={<PredictionHistory />} />
        <Route path="watchlist" element={<Watchlist />} />
        <Route path="news" element={<News />} />
        <Route path="practice-lab" element={<PracticeLab />} />
        <Route path="tutor" element={<Tutor />} />
        <Route path="model-performance" element={<ModelPerformance />} />
        <Route path="academy" element={<Academy />} />
        <Route path="profile" element={<Profile />} />
        <Route path="settings" element={<Settings />} />
        <Route
               path="academy/module/:moduleId"
               element={<AcademyModule />}
        />
        <Route
               path="academy/lesson/:lessonId"
               element={<AcademyLesson />}
        />
        {placeholders.map((p) => (
          <Route
            key={p.path}
            path={p.path}
            element={<PlaceholderPage title={p.title} phase={p.phase} />}
          />
        ))}
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
