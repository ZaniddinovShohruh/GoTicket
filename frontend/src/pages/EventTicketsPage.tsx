import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom'
import { EmptyState, PageShell, SkeletonGrid } from '../components/PageShell'
import { TicketCard } from '../components/TicketCard'
import { toast } from '../components/Toast'
import { useAuth } from '../context/AuthContext'
import { useApiErrorToast } from '../hooks/useApiErrorToast'
import { getApiErrorMessage, mediaUrl } from '../lib/api'
import { endpoints } from '../lib/endpoints'
import { formatDate, formatPrice } from '../lib/format'
import type { EventType, SeatSection, Ticket } from '../types/api'

type Picked = { id: number; row: number; number: number }

function sectionTone(section: SeatSection, active: boolean) {
  if (active) return 'bg-[var(--color-ink)] text-white ring-2 ring-[var(--color-accent)]'
  if (!section.available || !section.price) return 'bg-zinc-200 text-zinc-400'
  if (section.category === 'VIP') return 'bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent-deep)]'
  return 'bg-[var(--color-teal)] text-white hover:opacity-90'
}

export function EventTicketsPage() {
  const { type, id } = useParams<{ type: string; id: string }>()
  const eventType = type as EventType | undefined
  const eventId = Number(id)
  const { isLoggedIn } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const typeOk = eventType === 'club' || eventType === 'concert'
  const idOk = Number.isFinite(eventId)
  const [sectionId, setSectionId] = useState<number | null>(null)
  const [picked, setPicked] = useState<Picked | null>(null)
  const [bought, setBought] = useState<Ticket | null>(null)

  const seatsQuery = useQuery({
    queryKey: ['event-seats', eventType, eventId],
    queryFn: () => endpoints.eventSeats(eventType as string, eventId),
    enabled: typeOk && idOk,
  })

  const sectionQuery = useQuery({
    queryKey: ['section-seats', eventType, eventId, sectionId],
    queryFn: () =>
      endpoints.sectionSeats(eventType as string, eventId, sectionId as number),
    enabled: typeOk && idOk && sectionId != null,
  })

  const looseQuery = useQuery({
    queryKey: ['tickets', eventType, eventId],
    queryFn: () =>
      endpoints.tickets({
        available: '1',
        event_type: eventType,
        event_id: String(eventId),
      }),
    enabled: typeOk && idOk,
  })

  useApiErrorToast(seatsQuery.isError, seatsQuery.error)
  useApiErrorToast(sectionQuery.isError, sectionQuery.error)
  useApiErrorToast(looseQuery.isError, looseQuery.error)

  const onBought = (ticket: Ticket) => {
    toast('Chipta sotib olindi — My tickets da ko‘rinadi', 'success')
    setBought(ticket)
    setPicked(null)
    queryClient.invalidateQueries({ queryKey: ['event-seats'] })
    queryClient.invalidateQueries({ queryKey: ['section-seats'] })
    queryClient.invalidateQueries({ queryKey: ['tickets'] })
    queryClient.invalidateQueries({ queryKey: ['my-tickets'] })
  }

  const buy = useMutation({
    mutationFn: (seatId: number) =>
      endpoints.buySeat({
        event_type: eventType as string,
        event_id: eventId,
        seat_id: seatId,
      }),
    onSuccess: onBought,
    onError: (err) => {
      toast(getApiErrorMessage(err))
      queryClient.invalidateQueries({ queryKey: ['section-seats'] })
    },
  })

  const buyLoose = useMutation({
    mutationFn: (ticketId: number) => endpoints.buyTicket(ticketId),
    onSuccess: onBought,
    onError: (err) => {
      toast(getApiErrorMessage(err))
      queryClient.invalidateQueries({ queryKey: ['tickets'] })
    },
  })

  if (!typeOk) {
    return <Navigate to="/tickets" replace />
  }

  const data = seatsQuery.data
  const event = data?.event
  const section = sectionQuery.data
  const sectionMeta = data?.sections.find((s) => s.id === sectionId)
  const scheme = mediaUrl(data?.scheme)
  const mapped = data?.sections.filter((s) => s.map_x != null && s.map_y != null) ?? []

  const chooseSection = (s: SeatSection) => {
    setSectionId(s.id)
    setPicked(null)
    setBought(null)
  }

  const requireLogin = () => {
    if (isLoggedIn) return false
    navigate('/login', { state: { from: `/tickets/${eventType}/${eventId}` } })
    return true
  }

  const onBuy = () => {
    if (!picked || requireLogin()) return
    buy.mutate(picked.id)
  }

  const onBuyLoose = (ticketId: number) => {
    if (requireLogin()) return
    buyLoose.mutate(ticketId)
  }

  const hasMap = Boolean(data?.sections.length && data?.tariffs.length)
  const looseTickets = looseQuery.data?.filter((t) => !t.section) ?? []
  const loading = seatsQuery.isLoading || looseQuery.isLoading

  const subtitle = [
    event?.date ? formatDate(event.date) : null,
    [data?.place_name, event?.city].filter(Boolean).join(', ') || null,
    data ? `${data.available_count} / ${data.capacity} bo‘sh joy` : null,
  ]
    .filter(Boolean)
    .join(' · ')

  return (
    <PageShell
      title={event?.name || 'Event tickets'}
      subtitle={subtitle || 'Sektor va o‘rindiqni tanlang.'}
      action={
        <Link to="/tickets" className="text-sm font-medium text-[var(--color-accent)]">
          ← All events
        </Link>
      }
    >
      {loading ? <SkeletonGrid count={4} /> : null}
      {!loading && !hasMap && !looseTickets.length ? (
        <EmptyState
          title="Chipta hali ochilmagan"
          hint="Admin: stadionga sektorlar kiriting va Ticket tariffs da VIP/Standart narx qo‘ying yoki Tickets bo‘limida chipta yarating."
        />
      ) : null}

      <div className="space-y-8">
      {looseTickets.length ? (
        <section className="space-y-3">
          <h2 className="font-display text-xl font-semibold">Chiptalar</h2>
          {looseTickets.map((ticket, i) => (
            <div
              key={ticket.ticket_id}
              className="stagger-item flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-[var(--color-line)] bg-white/75 px-5 py-4"
              style={{ animationDelay: `${i * 45}ms` }}
            >
              <div>
                <p className="font-display text-lg font-semibold">{ticket.category}</p>
                <p className="text-sm text-[var(--color-ink-soft)]">
                  Seat {ticket.seat_number || 'General'}
                </p>
              </div>
              <div className="flex items-center gap-4">
                <p className="font-semibold">{formatPrice(ticket.price, ticket.currency)}</p>
                <button
                  type="button"
                  disabled={buyLoose.isPending}
                  onClick={() => onBuyLoose(ticket.ticket_id)}
                  className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[var(--color-accent-deep)] disabled:opacity-60"
                >
                  {buyLoose.isPending ? '…' : 'Buy'}
                </button>
              </div>
            </div>
          ))}
        </section>
      ) : null}

      {data && hasMap ? (
        <div className="space-y-8">
          <section className="space-y-4">
            <h2 className="font-display text-xl font-semibold">1. Sektorni tanlang</h2>

            {scheme ? (
              <div className="relative mx-auto max-w-4xl overflow-hidden rounded-2xl border border-[var(--color-line)] bg-white">
                <img src={scheme} alt={data.place_name ?? 'Stadium'} className="block w-full" />
                {mapped.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    disabled={!s.available || !s.price}
                    onClick={() => chooseSection(s)}
                    style={{ left: `${s.map_x}%`, top: `${s.map_y}%` }}
                    title={`${s.name}: ${s.available} bo‘sh`}
                    className={`absolute -translate-x-1/2 -translate-y-1/2 rounded-md px-2 py-1 text-xs font-bold shadow ${sectionTone(s, s.id === sectionId)}`}
                  >
                    {s.name}
                  </button>
                ))}
              </div>
            ) : null}

            <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-6">
              {data.sections.map((s) => (
                <button
                  key={s.id}
                  type="button"
                  disabled={!s.available || !s.price}
                  onClick={() => chooseSection(s)}
                  className={`rounded-xl px-3 py-2 text-left transition disabled:cursor-not-allowed ${sectionTone(s, s.id === sectionId)}`}
                >
                  <p className="font-display text-lg font-bold">{s.name}</p>
                  <p className="text-xs opacity-90">
                    {s.category} · {s.available}/{s.total}
                  </p>
                  <p className="text-xs font-semibold">
                    {s.price ? formatPrice(s.price, s.currency ?? 'UZS') : 'Narx yo‘q'}
                  </p>
                </button>
              ))}
            </div>
          </section>

          {sectionId != null ? (
            <section className="space-y-4">
              <div className="flex flex-wrap items-end justify-between gap-3">
                <h2 className="font-display text-xl font-semibold">
                  2. {sectionMeta?.name} sektorida o‘rindiq tanlang
                </h2>
                <div className="flex gap-4 text-xs">
                  <span className="flex items-center gap-1">
                    <span className="h-3 w-3 rounded bg-white ring-1 ring-[var(--color-line)]" /> Bo‘sh
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="h-3 w-3 rounded bg-[var(--color-accent)]" /> Tanlangan
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="h-3 w-3 rounded bg-zinc-300" /> Sotilgan
                  </span>
                </div>
              </div>

              {sectionQuery.isLoading ? <SkeletonGrid count={2} /> : null}
              {section ? (
                <div className="space-y-1.5 overflow-x-auto rounded-2xl border border-[var(--color-line)] bg-white/80 p-4">
                  {section.rows.map(({ row, seats }) => (
                    <div key={row} className="flex items-center gap-1.5">
                      <span className="w-16 shrink-0 text-xs font-semibold text-[var(--color-ink-soft)]">
                        {row}-qator
                      </span>
                      <div className="flex gap-1">
                        {seats.map((seat) => {
                          const active = picked?.id === seat.id
                          return (
                            <button
                              key={seat.id}
                              type="button"
                              disabled={seat.sold}
                              title={`${section.name}, ${row}-qator, ${seat.number}-o‘rin`}
                              onClick={() => {
                                setPicked({ id: seat.id, row, number: seat.number })
                                setBought(null)
                              }}
                              className={`h-8 w-8 shrink-0 rounded-md text-[11px] font-semibold transition ${
                                seat.sold
                                  ? 'cursor-not-allowed bg-zinc-300 text-zinc-500'
                                  : active
                                    ? 'bg-[var(--color-accent)] text-white'
                                    : 'bg-white ring-1 ring-[var(--color-line)] hover:bg-[var(--color-accent)]/15'
                              }`}
                            >
                              {seat.number}
                            </button>
                          )
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}
            </section>
          ) : null}

          {picked && section ? (
            <section className="sticky bottom-4 z-10 flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-[var(--color-ink)] px-5 py-4 text-white shadow-xl">
              <div>
                <p className="text-xs uppercase tracking-wide text-white/70">Tanlangan joy</p>
                <p className="font-display text-xl font-bold">
                  Sektor {section.name} · {picked.row}-qator · {picked.number}-o‘rin
                </p>
                <p className="text-sm text-white/80">
                  {section.category} ·{' '}
                  {section.price ? formatPrice(section.price, section.currency ?? 'UZS') : '—'}
                </p>
              </div>
              <button
                type="button"
                disabled={buy.isPending}
                onClick={onBuy}
                className="rounded-lg bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[var(--color-accent-deep)] disabled:opacity-60"
              >
                {buy.isPending ? '…' : 'Sotib olish'}
              </button>
            </section>
          ) : null}
        </div>
      ) : null}

      {bought ? (
        <section className="space-y-3">
          <h2 className="font-display text-xl font-semibold">Sizning chiptangiz</h2>
          <div className="max-w-xl">
            <TicketCard ticket={bought} />
          </div>
          <Link to="/my-tickets" className="inline-block text-sm font-semibold text-[var(--color-accent)]">
            Barcha chiptalarim →
          </Link>
        </section>
      ) : null}
      </div>
    </PageShell>
  )
}
