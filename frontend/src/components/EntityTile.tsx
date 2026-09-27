import { mediaUrl } from '../lib/api'

type Props = {
  title: string
  subtitle?: string
  image?: string | null
  meta?: string
  index?: number
}

export function EntityTile({ title, subtitle, image, meta, index = 0 }: Props) {
  const src = mediaUrl(image)

  return (
    <article
      className="stagger-item group overflow-hidden rounded-2xl border border-[var(--color-line)]/80 bg-white/70 shadow-[0_10px_30px_-18px_rgba(12,18,34,0.45)] transition duration-300 hover:-translate-y-1 hover:shadow-[0_18px_40px_-16px_rgba(12,18,34,0.5)]"
      style={{ animationDelay: `${index * 55}ms` }}
    >
      <div className="relative aspect-[16/10] overflow-hidden bg-[linear-gradient(135deg,#1a2336,#0d7377)]">
        {src ? (
          <img
            src={src}
            alt=""
            className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full items-end p-4">
            <span className="font-display text-3xl font-bold text-white/25">
              {title.slice(0, 1)}
            </span>
          </div>
        )}
      </div>
      <div className="space-y-1 p-4">
        <h2 className="font-display text-lg font-semibold leading-snug">
          {title}
        </h2>
        {subtitle ? (
          <p className="text-sm text-[var(--color-ink-soft)]">{subtitle}</p>
        ) : null}
        {meta ? (
          <p className="pt-1 text-xs uppercase tracking-wide text-[var(--color-teal)]">
            {meta}
          </p>
        ) : null}
      </div>
    </article>
  )
}
