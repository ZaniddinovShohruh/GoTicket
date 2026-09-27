import { useQuery } from '@tanstack/react-query'
import { Navigate } from 'react-router-dom'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { useAuth } from '../context/AuthContext'
import { getApiErrorMessage } from '../lib/api'
import { endpoints } from '../lib/endpoints'
import { toast } from '../components/Toast'
import { useEffect } from 'react'

export function ProfilePage() {
  const { isLoggedIn } = useAuth()

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['me'],
    queryFn: endpoints.me,
    enabled: isLoggedIn,
  })

  useEffect(() => {
    if (isError) toast(getApiErrorMessage(error))
  }, [isError, error])

  if (!isLoggedIn) {
    return <Navigate to="/login" replace state={{ from: '/profile' }} />
  }

  const user = data?.[0]

  return (
    <PageShell title="Profile" subtitle="Your GoTicket account.">
      {isLoading ? <SkeletonGrid count={1} /> : null}
      {!isLoading && !user ? (
        <EmptyState
          title="Could not load profile"
          hint="Check that your token is valid and /user/get-me is reachable."
        />
      ) : null}
      {user ? (
        <div className="page-enter max-w-lg rounded-2xl border border-[var(--color-line)] bg-white/75 p-6">
          <p className="font-display text-2xl font-bold">{user.full_name}</p>
          <dl className="mt-6 space-y-3 text-sm">
            <div>
              <dt className="text-[var(--color-ink-soft)]">Email</dt>
              <dd className="font-medium">{user.email}</dd>
            </div>
            <div>
              <dt className="text-[var(--color-ink-soft)]">User ID</dt>
              <dd className="font-medium">{user.id}</dd>
            </div>
          </dl>
        </div>
      ) : null}
    </PageShell>
  )
}
