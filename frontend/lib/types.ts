export interface Movie {
  id: number
  title: string
  genre: string
  release_year: number
  description: string
  created_by: number
  created_at: string // ISO timestamp
  ratings_count: number
  ratings_avg: number
}
export interface Rating {
  id: string
  movieId: string
  userId: string
  userName: string
  rating: number
  review?: string
  createdAt: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  total_pages: number
}

export type MoviesPaginatedResponse = Omit<PaginatedResponse<Movie>, "data"> & {
  movies: Movie[]
}
