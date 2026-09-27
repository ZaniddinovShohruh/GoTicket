import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { EntityTile } from '../components/EntityTile'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { SearchBar } from '../components/SearchBar'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'

export function CitiesPage() {
  const [search, setSearch] = useState('')
  const params = useMemo(
    () => (search.trim() ? { search: search.trim() } : undefined),
    [search],
  )

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['cities', params],
    queryFn: () => endpoints.cities(params),
  })

  useApiErrorToast(isError, error)

  return (
    <PageShell
      title="Cities"
      subtitle="Where the night happens."
      action={
        <div className="w-full max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search cities…"
          />
        </div>
      }
    >
      {isLoading ? <SkeletonGrid /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState title="No cities found" />
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data?.map((item, i) => (
          <EntityTile
            key={item.city_id}
            index={i}
            title={item.city_name}
            image={item.photo}
          />
        ))}
      </div>
    </PageShell>
  )
}
