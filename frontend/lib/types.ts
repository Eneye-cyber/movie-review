export interface Movie {
  id: string
  title: string
  description: string
  genre: string
  releaseYear: number
  posterUrl?: string
  averageRating: number
  ratingCount: number
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
  pageSize: number
  totalPages: number
}
