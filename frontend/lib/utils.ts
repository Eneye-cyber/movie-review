import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL!
export async function apiFetch<T = any>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`

  let res: Response
  try {
    res = await fetch(url, options)
  } catch (err) {
    // Network or fetch-level error (server down, CORS, etc.)
    throw new Error(`Network error: ${(err as Error).message}`)
    console.log(1)
  }

  let data: any
  try {
    // Try to parse response (even on errors)
    const text = await res.text()
    data = text ? JSON.parse(text) : null

  } catch {
    data = null
    console.log(3)
  }

  if (!res.ok) {
    // Extract useful info
    const errorMessage =
      (data && (data.detail || data.message || data.error)) ||
      `API error: ${res.status} ${res.statusText}`
    const error = new Error(errorMessage) as Error & { status?: number; body?: any }
    error.status = res.status
    error.body = data
    throw error
  }

  return data as T
}
