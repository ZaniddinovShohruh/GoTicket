type Props = {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export function SearchBar({
  value,
  onChange,
  placeholder = 'Search…',
}: Props) {
  return (
    <label className="block">
      <span className="sr-only">Search</span>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-[var(--color-line)] bg-white/80 px-4 py-3 text-sm outline-none ring-[var(--color-accent)] transition focus:ring-2"
      />
    </label>
  )
}
