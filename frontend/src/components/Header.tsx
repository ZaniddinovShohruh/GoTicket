import { NavLink, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links = [
  { to: '/sports', label: 'Sports' },
  { to: '/clubs', label: 'Clubs' },
  { to: '/concerts', label: 'Concerts' },
  { to: '/singers', label: 'Singers' },
  { to: '/cities', label: 'Cities' },
  { to: '/places', label: 'Places' },
  { to: '/tickets', label: 'Tickets' },
]

export function SiteHeader() {
  const { isLoggedIn, logout } = useAuth()
  const nav = isLoggedIn
    ? [...links, { to: '/my-tickets', label: 'My tickets' }]
    : links

  return (
    <header className="absolute inset-x-0 top-0 z-40">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-5 md:px-8">
        <Link
          to="/"
          className="font-display text-lg font-semibold tracking-tight text-white drop-shadow md:text-xl"
        >
          GoTicket
        </Link>
        <nav className="hidden items-center gap-5 text-sm text-white/85 lg:flex">
          {nav.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `transition hover:text-white ${isActive ? 'text-white' : ''}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="flex items-center gap-3 text-sm">
          {isLoggedIn ? (
            <>
              <Link
                to="/profile"
                className="rounded-md bg-white/15 px-3 py-1.5 text-white backdrop-blur transition hover:bg-white/25"
              >
                Profile
              </Link>
              <button
                type="button"
                onClick={logout}
                className="text-white/80 transition hover:text-white"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-white/85 hover:text-white">
                Log in
              </Link>
              <Link
                to="/register"
                className="rounded-md bg-[var(--color-accent)] px-3 py-1.5 font-medium text-white transition hover:bg-[var(--color-accent-deep)]"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

export function AppHeader() {
  const { isLoggedIn, logout } = useAuth()
  const nav = isLoggedIn
    ? [...links, { to: '/my-tickets', label: 'My tickets' }]
    : links

  return (
    <header className="border-b border-[var(--color-line)]/70 bg-white/55 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-5 py-4 md:px-8">
        <Link to="/" className="font-display text-xl font-bold tracking-tight">
          GoTicket
        </Link>
        <nav className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-[var(--color-ink-soft)]">
          {nav.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `transition hover:text-[var(--color-accent)] ${
                  isActive ? 'font-semibold text-[var(--color-accent)]' : ''
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="flex items-center gap-3 text-sm">
          {isLoggedIn ? (
            <>
              <Link to="/profile" className="hover:text-[var(--color-accent)]">
                Profile
              </Link>
              <button
                type="button"
                onClick={logout}
                className="text-[var(--color-ink-soft)] hover:text-[var(--color-ink)]"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link
                to="/register"
                className="rounded-md bg-[var(--color-ink)] px-3 py-1.5 text-white"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
