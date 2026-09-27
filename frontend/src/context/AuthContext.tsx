import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { clearTokens, getAccessToken, setTokens } from '../lib/authStorage'
import { endpoints } from '../lib/endpoints'

type AuthContextValue = {
  isLoggedIn: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(() => Boolean(getAccessToken()))

  const login = useCallback(async (email: string, password: string) => {
    const tokens = await endpoints.login(email, password)
    setTokens(tokens.access, tokens.refresh)
    setIsLoggedIn(true)
  }, [])

  const logout = useCallback(() => {
    clearTokens()
    setIsLoggedIn(false)
  }, [])

  const value = useMemo(
    () => ({ isLoggedIn, login, logout }),
    [isLoggedIn, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
