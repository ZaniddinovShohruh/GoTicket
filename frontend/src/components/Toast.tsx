import { useEffect, useState } from 'react'

type Toast = { id: number; message: string; tone: 'error' | 'success' }

let pushToast: ((message: string, tone?: 'error' | 'success') => void) | null =
  null

export function toast(message: string, tone: 'error' | 'success' = 'error') {
  pushToast?.(message, tone)
}

export function ToastHost() {
  const [items, setItems] = useState<Toast[]>([])

  useEffect(() => {
    pushToast = (message, tone = 'error') => {
      const id = Date.now()
      setItems((prev) => [...prev, { id, message, tone }])
      window.setTimeout(() => {
        setItems((prev) => prev.filter((t) => t.id !== id))
      }, 4200)
    }
    return () => {
      pushToast = null
    }
  }, [])

  if (!items.length) return null

  return (
    <div className="pointer-events-none fixed bottom-6 right-6 z-[100] flex max-w-sm flex-col gap-2">
      {items.map((t) => (
        <div
          key={t.id}
          className={`pointer-events-auto rounded-lg px-4 py-3 text-sm shadow-lg ${
            t.tone === 'error'
              ? 'bg-[#3b1010] text-[#ffd4d4]'
              : 'bg-[#0f2e24] text-[#c8f5e2]'
          }`}
        >
          {t.message}
        </div>
      ))}
    </div>
  )
}
