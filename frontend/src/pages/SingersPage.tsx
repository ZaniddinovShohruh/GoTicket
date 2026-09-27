import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { EntityTile } from '../components/EntityTile'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { SearchBar } from '../components/SearchBar'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'
import { formatDate } from '../lib/format'

export function SingersPage() {
  const [search, setSearch] = useState('')
  const params = useMemo(
    () => (search.trim() ? { search: search.trim() } : undefined),
    [search],
  )

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['singers', params],
    queryFn: () => endpoints.singers(params),
  })

  useApiErrorToast(isError, error)

  return (
    <PageShell
      title="Singers"
      subtitle="Artists on the calendar."
      action={
        <div className="w-full max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search singers…"
          />
        </div>
      }
    >
      {isLoading ? <SkeletonGrid /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState title="No singers found" />
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data?.map((item, i) => (
          <EntityTile
            key={item.singer_id}
            index={i}
            title={item.singer_name}
            image={item.photo}
            subtitle={formatDate(item.event_date)}
            meta={item.event_time}
          />
        ))}
      </div>
    </PageShell>
  )
}
