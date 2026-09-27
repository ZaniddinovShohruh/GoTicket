import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { ToastHost } from './components/Toast'
import { AuthProvider } from './context/AuthContext'
import { AppLayout, LandingLayout } from './layouts/Layouts'
import { CitiesPage } from './pages/CitiesPage'
import { ClubsPage } from './pages/ClubsPage'
import { ConcertsPage } from './pages/ConcertsPage'
import { LoginPage } from './pages/LoginPage'
import { PlacesPage } from './pages/PlacesPage'
import { ProfilePage } from './pages/ProfilePage'
import { RegisterPage } from './pages/RegisterPage'
import { SingersPage } from './pages/SingersPage'
import { SportsPage } from './pages/SportsPage'
import { TicketsPage } from './pages/TicketsPage'
import { MyTicketsPage } from './pages/MyTicketsPage'
import { EventTicketsPage } from './pages/EventTicketsPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingLayout />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route element={<AppLayout />}>
              <Route path="/sports" element={<SportsPage />} />
              <Route path="/clubs" element={<ClubsPage />} />
              <Route path="/concerts" element={<ConcertsPage />} />
              <Route path="/singers" element={<SingersPage />} />
              <Route path="/cities" element={<CitiesPage />} />
              <Route path="/places" element={<PlacesPage />} />
              <Route path="/tickets" element={<TicketsPage />} />
              <Route
                path="/tickets/:type/:id"
                element={<EventTicketsPage />}
              />
              <Route path="/my-tickets" element={<MyTicketsPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <ToastHost />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}
