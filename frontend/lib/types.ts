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
  id: number
  movie_id: number
  user_id: number
  rating: number
  review: string
  created_at: string // ISO timestamp
  updated_at: string // ISO timestamp
  username: string
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

export type RatingsPaginatedResponse = Omit<PaginatedResponse<Rating>, "data"> & {
  ratings: Rating[]
}
