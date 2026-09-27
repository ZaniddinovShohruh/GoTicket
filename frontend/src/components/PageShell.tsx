export function SkeletonGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="h-56 animate-pulse rounded-2xl bg-white/60"
          style={{ animationDelay: `${i * 60}ms` }}
        />
      ))}
    </div>
  )
}

export function EmptyState({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-[var(--color-line)] bg-white/50 px-6 py-16 text-center">
      <p className="font-display text-xl font-semibold">{title}</p>
      {hint ? (
        <p className="mt-2 text-sm text-[var(--color-ink-soft)]">{hint}</p>
      ) : null}
    </div>
  )
}

export function PageShell({
  title,
  subtitle,
  children,
  action,
}: {
  title: string
  subtitle?: string
  children: React.ReactNode
  action?: React.ReactNode
}) {
  return (
    <div className="page-enter mx-auto max-w-6xl px-5 py-10 md:px-8">
      <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold tracking-tight md:text-4xl">
            {title}
          </h1>
          {subtitle ? (
            <p className="mt-2 max-w-xl text-[var(--color-ink-soft)]">
              {subtitle}
            </p>
          ) : null}
        </div>
        {action}
      </div>
      {children}
    </div>
  )
}
