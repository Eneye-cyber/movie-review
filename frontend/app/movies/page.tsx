"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import { Header } from "@/components/header"
import { MovieCard } from "@/components/movie-card"
import { MovieFilters } from "@/components/movie-filters"
import { Pagination } from "@/components/pagination"
import type { Movie, MoviesPaginatedResponse, PaginatedResponse } from "@/lib/types"
import { Loader2 } from "lucide-react"
import { apiFetch } from "@/lib/utils"

export default function MoviesPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [movies, setMovies] = useState<Movie[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [pagination, setPagination] = useState({
    page: 1,
    totalPages: 1,
    total: 0,
  })

  // Filter states
  const [searchQuery, setSearchQuery] = useState(searchParams.get("search") || "")
  const [genre, setGenre] = useState(searchParams.get("genre") || "All Genres")
  const [yearFrom, setYearFrom] = useState(searchParams.get("min_year") || "")
  const [yearTo, setYearTo] = useState(searchParams.get("max_year") || "")

  const currentPage = Number.parseInt(searchParams.get("page") || "1")

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchMovies(currentPage)
    }, 300) // Debounce search

    return () => clearTimeout(timer)
  }, [currentPage, searchQuery, genre, yearFrom, yearTo])

  const fetchMovies = async (page: number) => {
    setIsLoading(true)
    setError(null)

    try {
      const params = new URLSearchParams({
        page: String(page),
        limit: "12",
      })

      if (searchQuery) params.append("search", searchQuery)
      if (genre && genre !== "All Genres") params.append("genre", genre)
      if (yearFrom) params.append("min_year", yearFrom)
      if (yearTo) params.append("max_year", yearTo)

      const response = await apiFetch(`/movies?${params.toString()}`)

      const data: MoviesPaginatedResponse = response
      console.log('data', data)
      setMovies(data.movies)
      setPagination({
        page: data.page,
        totalPages: data.total_pages ?? 3,
        total: data.total,
      })

      // Update URL
      updateURL(page)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  const updateURL = (page: number) => {
    const params = new URLSearchParams()
    if (page > 1) params.append("page", String(page))
    if (searchQuery) params.append("search", searchQuery)
    if (genre && genre !== "All Genres") params.append("genre", genre)
    if (yearFrom) params.append("min_year", yearFrom)
    if (yearTo) params.append("max_year", yearTo)

    const queryString = params.toString()
    router.push(`/movies${queryString ? `?${queryString}` : ""}`, { scroll: false })
  }

  const handlePageChange = (page: number) => {
    fetchMovies(page)
  }

  const handleClearFilters = () => {
    setSearchQuery("")
    setGenre("All Genres")
    setYearFrom("")
    setYearTo("")
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Discover Movies</h1>
          <p className="text-muted-foreground">
            {isLoading ? "Loading..." : `Showing ${movies.length} of ${pagination.total} movies`}
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <MovieFilters
                searchQuery={searchQuery}
                genre={genre}
                yearFrom={yearFrom}
                yearTo={yearTo}
                onSearchChange={setSearchQuery}
                onGenreChange={setGenre}
                onYearFromChange={setYearFrom}
                onYearToChange={setYearTo}
                onClearFilters={handleClearFilters}
              />
            </div>
          </div>

          {/* Movies Grid */}
          <div className="lg:col-span-3">
            {isLoading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-20 space-y-4">
                <p className="text-destructive text-lg">{error}</p>
                <button onClick={() => fetchMovies(currentPage)} className="text-primary hover:underline">
                  Try again
                </button>
              </div>
            ) : movies.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 space-y-4">
                <p className="text-muted-foreground text-lg">No movies found</p>
                <button onClick={handleClearFilters} className="text-primary hover:underline">
                  Clear filters
                </button>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
                  {movies.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                  ))}
                </div>

                {pagination.totalPages > 1 && (
                  <div className="mt-12">
                    <Pagination
                      currentPage={pagination.page}
                      totalPages={pagination.totalPages}
                      onPageChange={handlePageChange}
                    />
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
