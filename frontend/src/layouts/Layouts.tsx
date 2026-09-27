import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { AppHeader } from '../components/Header'
import { LandingPage } from '../pages/LandingPage'

export function LandingLayout() {
  return <LandingPage />
}

export function AppLayout() {
  return (
    <div className="min-h-screen">
      <AppHeader />
      <Outlet />
    </div>
  )
}

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const token = localStorage.getItem('goticket_access')
  if (!token) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }
  return children
}
