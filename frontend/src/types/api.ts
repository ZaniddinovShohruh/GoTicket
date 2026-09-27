export type Sport = {
  sport_id: number
  sport_name: string
  photo?: string | null
}

export type Club = {
  club_id: number
  club_name: string
  photo?: string | null
  event_time?: string
  event_date?: string
  cities?: number
  places?: number
  place_name?: string | null
  place_capacity?: number | null
  sports?: number | null
}

export type Concert = {
  concert_id: number
  concert_name: string
  photo?: string | null
  cities?: number
  places?: number
  place_name?: string | null
  place_capacity?: number | null
  singer?: number
}

export type Singer = {
  singer_id: number
  singer_name: string
  event_time?: string
  event_date?: string
  photo?: string | null
}

export type City = {
  city_id: number
  city_name: string
  photo?: string | null
}

export type Place = {
  place_id: number
  place_name: string
  photo?: string | null
  city?: number
  capacity?: number
}

export type EventType = 'club' | 'concert'

export type Currency = 'USD' | 'EUR' | 'UZS'

export type TicketTariff = {
  category: 'VIP' | 'Standart' | string
  price: string | number
  currency: Currency | string
}

export type EventInfo = {
  name: string
  type: EventType | string
  date?: string | null
  time?: string | null
  place?: string | null
  city?: string | null
  extra?: string | null
  photo?: string | null
}

export type SeatSection = {
  id: number
  name: string
  category: 'VIP' | 'Standart' | string
  map_x?: number | null
  map_y?: number | null
  total: number
  available: number
  price?: string | null
  currency?: Currency | string | null
}

export type EventSeats = {
  event_type: EventType | string
  event_id: number
  event?: EventInfo | null
  place_name?: string | null
  scheme?: string | null
  capacity: number
  available_count: number
  sections: SeatSection[]
  tariffs: TicketTariff[]
}

export type SectionSeat = {
  id: number
  number: number
  sold: boolean
}

export type SectionSeats = {
  id: number
  name: string
  category: string
  price?: string | null
  currency?: Currency | string | null
  rows: { row: number; seats: SectionSeat[] }[]
}

export type Ticket = {
  ticket_id: number
  category: 'VIP' | 'Standart' | string
  price: string | number
  currency?: Currency | string
  seat_number?: string | null
  section?: string | null
  row?: number | null
  seat?: number | null
  is_sold?: boolean
  buyer?: number | null
  purchased_at?: string | null
  event_type?: EventType | string | null
  event_id?: number | null
  event_name?: string | null
  event?: EventInfo | null
}

export type User = {
  id: number
  email: string
  full_name: string
  phone?: string | null
}

export type AuthTokens = {
  access: string
  refresh: string
}

export type ListParams = {
  search?: string
  ordering?: string
  available?: string
  event_type?: string
  event_id?: string
  [key: string]: string | undefined
}
