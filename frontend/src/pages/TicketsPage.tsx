import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { EntityTile } from '../components/EntityTile'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'
import { formatDate } from '../lib/format'
import { useState } from 'react'

type Tab = 'club' | 'concert'

export function TicketsPage() {
  const [tab, setTab] = useState<Tab>('club')

  const clubs = useQuery({
    queryKey: ['clubs'],
    queryFn: () => endpoints.clubs(),
    enabled: tab === 'club',
  })
  const concerts = useQuery({
    queryKey: ['concerts'],
    queryFn: () => endpoints.concerts(),
    enabled: tab === 'concert',
  })

  useApiErrorToast(clubs.isError, clubs.error)
  useApiErrorToast(concerts.isError, concerts.error)

  const loading = tab === 'club' ? clubs.isLoading : concerts.isLoading
  const list = tab === 'club' ? clubs.data : concerts.data

  return (
    <PageShell
      title="Buy tickets"
      subtitle="1) Tadbirni tanlang → 2) O‘rinni tanlang → 3) Sotib oling"
      action={
        <Link
          to="/my-tickets"
          className="rounded-xl bg-[var(--color-ink)] px-4 py-3 text-sm font-semibold text-white"
        >
          My tickets
        </Link>
      }
    >
      <div className="mb-8 flex gap-2">
        <button
          type="button"
          onClick={() => setTab('club')}
          className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
            tab === 'club'
              ? 'bg-[var(--color-accent)] text-white'
              : 'bg-white/70 text-[var(--color-ink-soft)]'
          }`}
        >
          Matches (Clubs)
        </button>
        <button
          type="button"
          onClick={() => setTab('concert')}
          className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
            tab === 'concert'
              ? 'bg-[var(--color-accent)] text-white'
              : 'bg-white/70 text-[var(--color-ink-soft)]'
          }`}
        >
          Concerts
        </button>
      </div>

      {loading ? <SkeletonGrid /> : null}
      {!loading && !list?.length ? (
        <EmptyState
          title={tab === 'club' ? 'No matches yet' : 'No concerts yet'}
          hint="Admin panelda Club yoki Concert yarating, keyin Ticket ulang."
        />
      ) : null}

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {tab === 'club'
          ? clubs.data?.map((item, i) => (
              <Link key={item.club_id} to={`/tickets/club/${item.club_id}`}>
                <EntityTile
                  index={i}
                  title={item.club_name}
                  image={item.photo}
                  subtitle={formatDate(item.event_date)}
                  meta="Get tickets →"
                />
              </Link>
            ))
          : concerts.data?.map((item, i) => (
              <Link
                key={item.concert_id}
                to={`/tickets/concert/${item.concert_id}`}
              >
                <EntityTile
                  index={i}
                  title={item.concert_name}
                  image={item.photo}
                  meta="Get tickets →"
                />
              </Link>
            ))}
      </div>
    </PageShell>
  )
}
