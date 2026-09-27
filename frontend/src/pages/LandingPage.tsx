import { Link } from 'react-router-dom'
import { SiteHeader } from '../components/Header'

export function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="absolute inset-0">
        <div
          className="hero-kenburns absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage:
              'linear-gradient(120deg, rgba(12,18,34,0.78) 0%, rgba(12,18,34,0.35) 45%, rgba(12,18,34,0.65) 100%), url(https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?auto=format&fit=crop&w=2000&q=80)',
          }}
        />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(232,93,4,0.28),transparent_40%)]" />
      </div>

      <SiteHeader />

      <main className="relative z-10 flex min-h-screen items-end px-5 pb-16 pt-28 md:items-center md:px-10 md:pb-24 md:pt-20">
        <div className="page-enter mx-auto w-full max-w-6xl">
          <p className="font-display text-5xl font-extrabold tracking-tight text-white drop-shadow-sm sm:text-6xl md:text-8xl">
            GoTicket
          </p>
          <h1 className="mt-4 max-w-xl font-display text-2xl font-semibold leading-tight text-white/95 md:text-3xl">
            Get ticket faster
          </h1>
          <p className="mt-3 max-w-md text-base text-white/75 md:text-lg">
            Sport matches and live concerts — find your seat in moments.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              to="/sports"
              className="rounded-md bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[var(--color-accent-deep)]"
            >
              Browse Sports
            </Link>
            <Link
              to="/concerts"
              className="rounded-md border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white backdrop-blur transition hover:bg-white/20"
            >
              Browse Concerts
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
