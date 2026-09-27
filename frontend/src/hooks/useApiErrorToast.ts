import { useEffect } from 'react'
import { toast } from '../components/Toast'
import { getApiErrorMessage } from '../lib/api'

export function useApiErrorToast(isError: boolean, error: unknown) {
  useEffect(() => {
    if (isError) toast(getApiErrorMessage(error))
  }, [isError, error])
}
