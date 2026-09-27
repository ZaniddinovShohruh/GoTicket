import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { EntityTile } from '../components/EntityTile'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { SearchBar } from '../components/SearchBar'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'

export function ConcertsPage() {
  const [search, setSearch] = useState('')
  const params = useMemo(
    () => (search.trim() ? { search: search.trim() } : undefined),
    [search],
  )

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['concerts', params],
    queryFn: () => endpoints.concerts(params),
  })

  useApiErrorToast(isError, error)

  return (
    <PageShell
      title="Concerts"
      subtitle="Konsert tanlang va chipta oling."
      action={
        <div className="w-full max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search concerts…"
          />
        </div>
      }
    >
      {isLoading ? <SkeletonGrid /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState title="No concerts yet" />
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data?.map((item, i) => (
          <Link key={item.concert_id} to={`/tickets/concert/${item.concert_id}`}>
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
