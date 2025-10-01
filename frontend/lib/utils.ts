import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL!

export async function apiFetch(path: string, options?: RequestInit) {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`
  const res = await fetch(url, options)

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`)
  }

  return res.json()
}