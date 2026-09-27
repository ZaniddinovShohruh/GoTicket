import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { EntityTile } from '../components/EntityTile'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { SearchBar } from '../components/SearchBar'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'
import { formatDate } from '../lib/format'

export function ClubsPage() {
  const [search, setSearch] = useState('')
  const params = useMemo(
    () => (search.trim() ? { search: search.trim() } : undefined),
    [search],
  )

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['clubs', params],
    queryFn: () => endpoints.clubs(params),
  })

  useApiErrorToast(isError, error)

  return (
    <PageShell
      title="Clubs"
      subtitle="Match tanlang va chipta oling."
      action={
        <div className="w-full max-w-sm">
          <SearchBar value={search} onChange={setSearch} placeholder="Search clubs…" />
        </div>
      }
    >
      {isLoading ? <SkeletonGrid /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState title="No clubs found" />
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data?.map((item, i) => (
          <Link key={item.club_id} to={`/tickets/club/${item.club_id}`}>
            <EntityTile
              index={i}
              title={item.club_name}
              image={item.photo}
              subtitle={formatDate(item.event_date)}
              meta="Get tickets →"
            />
          </Link>
        ))}
      </div>
    </PageShell>
  )
}
