import { useQuery } from '@tanstack/react-query'
import { Link, Navigate } from 'react-router-dom'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { TicketCard } from '../components/TicketCard'
import { useAuth } from '../context/AuthContext'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'

export function MyTicketsPage() {
  const { isLoggedIn } = useAuth()

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['my-tickets'],
    queryFn: endpoints.myTickets,
    enabled: isLoggedIn,
  })

  useApiErrorToast(isError, error)

  if (!isLoggedIn) {
    return <Navigate to="/login" replace state={{ from: '/my-tickets' }} />
  }

  return (
    <PageShell
      title="My tickets"
      subtitle="Sotib olgan chiptalaringiz."
      action={
        <Link
          to="/tickets"
          className="rounded-xl bg-[var(--color-accent)] px-4 py-3 text-sm font-semibold text-white"
        >
          Buy more
        </Link>
      }
    >
      {isLoading ? <SkeletonGrid count={3} /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState
          title="Hali chipta yo‘q"
          hint="Tickets sahifasidan tadbir tanlab o‘rin oling."
        />
      ) : null}

      <div className="grid gap-5 md:grid-cols-2">
        {data?.map((ticket, i) => (
          <div
            key={ticket.ticket_id}
            className="stagger-item"
            style={{ animationDelay: `${i * 45}ms` }}
          >
            <TicketCard ticket={ticket} />
          </div>
        ))}
      </div>
    </PageShell>
  )
}
