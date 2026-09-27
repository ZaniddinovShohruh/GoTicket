import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { EntityTile } from '../components/EntityTile'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { SearchBar } from '../components/SearchBar'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { endpoints } from '../lib/endpoints'

export function SportsPage() {
  const [search, setSearch] = useState('')
  const params = useMemo(
    () => (search.trim() ? { search: search.trim() } : undefined),
    [search],
  )

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['sports', params],
    queryFn: () => endpoints.sports(params),
  })

  useApiErrorToast(isError, error)

  return (
    <PageShell
      title="Sports"
      subtitle="Pick a sport and find matches worth your night."
      action={
        <div className="w-full max-w-sm">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search sports…"
          />
        </div>
      }
    >
      {isLoading ? <SkeletonGrid /> : null}
      {!isLoading && !data?.length ? (
        <EmptyState
          title="No sports yet"
          hint="Add sports in Django admin or via API."
        />
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data?.map((item, i) => (
          <EntityTile
            key={item.sport_id}
            index={i}
            title={item.sport_name}
            image={item.photo}
          />
        ))}
      </div>
    </PageShell>
  )
}
