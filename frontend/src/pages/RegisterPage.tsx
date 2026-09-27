import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { AppHeader } from '../components/Header'
import { toast } from '../components/Toast'
import { getApiErrorMessage } from '../lib/api'
import { endpoints } from '../lib/endpoints'
import { useAuth } from '../context/AuthContext'

const schema = z.object({
  full_name: z.string().min(2, 'Name is too short'),
  email: z.string().email('Enter a valid email'),
  phone: z.string().optional(),
  password: z.string().min(6, 'At least 6 characters'),
})

type FormValues = z.infer<typeof schema>

export function RegisterPage() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) })

  const onSubmit = handleSubmit(async (values) => {
    try {
      await endpoints.register({
        email: values.email,
        password: values.password,
        full_name: values.full_name,
        phone: values.phone || undefined,
      })
      try {
        await login(values.email, values.password)
      } catch {
        // Register may require admin on backend — still guide to login
      }
      toast('Account created', 'success')
      navigate('/')
    } catch (error) {
      toast(getApiErrorMessage(error))
    }
  })

  return (
    <div className="min-h-screen">
      <AppHeader />
      <div className="page-enter mx-auto flex max-w-md flex-col px-5 py-14">
        <h1 className="font-display text-3xl font-bold">Create account</h1>
        <p className="mt-2 text-sm text-[var(--color-ink-soft)]">
          Join GoTicket and grab seats faster.
        </p>
        <form onSubmit={onSubmit} className="mt-8 space-y-4">
          <Field label="Full name" error={errors.full_name?.message}>
            <input className="field" {...register('full_name')} />
          </Field>
          <Field label="Email" error={errors.email?.message}>
            <input type="email" className="field" {...register('email')} />
          </Field>
          <Field label="Phone (optional)" error={errors.phone?.message}>
            <input className="field" {...register('phone')} />
          </Field>
          <Field label="Password" error={errors.password?.message}>
            <input
              type="password"
              autoComplete="new-password"
              className="field"
              {...register('password')}
            />
          </Field>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-[var(--color-accent)] py-3 text-sm font-semibold text-white transition hover:bg-[var(--color-accent-deep)] disabled:opacity-60"
          >
            {isSubmitting ? 'Creating…' : 'Sign up'}
          </button>
        </form>
        <p className="mt-6 text-sm text-[var(--color-ink-soft)]">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-[var(--color-accent)]">
            Log in
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
