import { formatDate, formatPrice } from '../lib/format'
import type { Ticket } from '../types/api'

function formatTime(value?: string | null) {
  if (!value || !/^\d{2}:\d{2}/.test(value)) return null
  return value.slice(0, 5)
}

function SeatBox({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-xl bg-[var(--color-mist)] px-4 py-3 text-center">
      <p className="text-xs uppercase tracking-wide text-[var(--color-ink-soft)]">
        {label}
      </p>
      <p className="font-display text-2xl font-bold">{value}</p>
    </div>
  )
}

export function TicketCard({ ticket }: { ticket: Ticket }) {
  const event = ticket.event
  const time = formatTime(event?.time)
  const where = [event?.place, event?.city].filter(Boolean).join(', ')

  return (
    <div className="overflow-hidden rounded-2xl border border-[var(--color-line)] bg-white/85">
      <div className="bg-[var(--color-ink)] px-5 py-4 text-white">
        <p className="text-xs font-semibold uppercase tracking-wide text-white/70">
          {event?.type === 'concert' ? 'Konsert' : 'Sport o‘yini'} · Chipta #
          {ticket.ticket_id}
        </p>
        <p className="font-display text-2xl font-bold">
          {event?.name || ticket.event_name || 'Event'}
        </p>
        {event?.extra ? (
          <p className="text-sm text-white/80">{event.extra}</p>
        ) : null}
      </div>

      <div className="space-y-4 px-5 py-4">
        <div className="flex flex-wrap gap-x-6 gap-y-1 text-sm">
          {event?.date ? (
            <span>
              📅 {formatDate(event.date)}
              {time ? ` · ${time}` : ''}
            </span>
          ) : null}
          {where ? <span>📍 {where}</span> : null}
        </div>

        {ticket.section ? (
          <div className="grid grid-cols-3 gap-3">
            <SeatBox label="Sektor" value={ticket.section} />
            <SeatBox label="Qator" value={ticket.row ?? '—'} />
            <SeatBox label="O‘rin" value={ticket.seat ?? '—'} />
          </div>
        ) : (
          <p className="text-sm">Seat {ticket.seat_number || 'General'}</p>
        )}

        <div className="flex flex-wrap items-center justify-between gap-2 border-t border-dashed border-[var(--color-line)] pt-3 text-sm">
          <span className="font-semibold">{ticket.category}</span>
          <span className="font-display text-lg font-bold">
            {formatPrice(ticket.price, ticket.currency)}
          </span>
        </div>
        {ticket.purchased_at ? (
          <p className="text-xs text-[var(--color-ink-soft)]">
            Sotib olingan: {formatDate(ticket.purchased_at)}
          </p>
        ) : null}
      </div>
    </div>
  )
}
