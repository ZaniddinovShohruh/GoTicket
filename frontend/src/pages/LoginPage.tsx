import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { AppHeader } from '../components/Header'
import { toast } from '../components/Toast'
import { useAuth } from '../context/AuthContext'
import { getApiErrorMessage } from '../lib/api'

const schema = z.object({
  email: z.string().email('Enter a valid email'),
  password: z.string().min(1, 'Password required'),
})

type FormValues = z.infer<typeof schema>

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from =
    (location.state as { from?: string } | null)?.from || '/'

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) })

  const onSubmit = handleSubmit(async (values) => {
    try {
      await login(values.email, values.password)
      toast('Welcome back', 'success')
      navigate(from, { replace: true })
    } catch (error) {
      toast(getApiErrorMessage(error))
    }
  })

  return (
    <div className="min-h-screen">
      <AppHeader />
      <div className="page-enter mx-auto flex max-w-md flex-col px-5 py-14">
        <h1 className="font-display text-3xl font-bold">Log in</h1>
        <p className="mt-2 text-sm text-[var(--color-ink-soft)]">
          Use your GoTicket email and password.
        </p>
        <form onSubmit={onSubmit} className="mt-8 space-y-4">
          <Field label="Email" error={errors.email?.message}>
            <input
              type="email"
              autoComplete="email"
              className="field"
              {...register('email')}
            />
          </Field>
          <Field label="Password" error={errors.password?.message}>
            <input
              type="password"
              autoComplete="current-password"
              className="field"
              {...register('password')}
            />
          </Field>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-[var(--color-ink)] py-3 text-sm font-semibold text-white transition hover:bg-[var(--color-ink-soft)] disabled:opacity-60"
          >
            {isSubmitting ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <p className="mt-6 text-sm text-[var(--color-ink-soft)]">
          No account?{' '}
          <Link to="/register" className="font-medium text-[var(--color-accent)]">
            Sign up
          </Link>
        </p>
      </div>
      <style>{`
        .field {
          width: 100%;
          border-radius: 0.75rem;
          border: 1px solid var(--color-line);
          background: rgba(255,255,255,0.85);
          padding: 0.75rem 1rem;
          font-size: 0.875rem;
          outline: none;
        }
        .field:focus { box-shadow: 0 0 0 2px var(--color-accent); }
      `}</style>
    </div>
  )
}

function Field({
  label,
  error,
  children,
}: {
  label: string
  error?: string
  children: React.ReactNode
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-medium">{label}</span>
      {children}
      {error ? <span className="text-xs text-red-600">{error}</span> : null}
    </label>
  )
}
