"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Header } from "@/components/header"
import { StarRating } from "@/components/star-rating"
import { RatingForm } from "@/components/rating-form"
import { RatingList } from "@/components/rating-list"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/lib/auth-context"
import type { Movie, Rating, RatingsPaginatedResponse } from "@/lib/types"
import { ArrowLeft, Calendar, Loader2, Users } from "lucide-react"
import Link from "next/link"
import { apiFetch } from "@/lib/utils"

export default function MovieDetailPage() {
  const params = useParams()
  const router = useRouter()
  const { user } = useAuth()
  const [movie, setMovie] = useState<Movie | null>(null)
  const [ratings, setRatings] = useState<Rating[]>([])
  const [userRating, setUserRating] = useState<Rating | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMovieData()
  }, [params.id])

  const fetchMovieData = async () => {
    setIsLoading(true)
    setError(null)

    try {
      // Fetch movie details
      const movieResponse = await apiFetch(`/movies/${params.id}`)
      const movieData = movieResponse
      setMovie(movieData)

      // Fetch ratings
      const ratingsResponse = await apiFetch(`/movies/${params.id}/ratings`)
      const data: RatingsPaginatedResponse = ratingsResponse;
        setRatings(data.ratings)

        // Find user's rating if logged in
        if (user) {
          const userRatingData = data.ratings.find((r: Rating) => `${r.user_id}` === user.id)
          setUserRating(userRatingData || null)
        }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </div>
    )
  }

  if (error || !movie) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-20">
          <div className="text-center space-y-4">
            <p className="text-destructive text-lg">{error || "Movie not found"}</p>
            <Link href="/movies">
              <Button variant="outline">Back to Movies</Button>
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <Link href="/movies">
          <Button variant="ghost" className="mb-6">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Movies
          </Button>
        </Link>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Movie poster and basic info */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <div className="aspect-[2/3] bg-muted rounded-lg overflow-hidden mb-4">
                {/* {movie.posterUrl ? (
                  <img
                    src={movie.posterUrl || "/placeholder.svg"}
                    alt={movie.title}
                    className="object-cover w-full h-full"
                  />
                ) : ( */}
                  <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                    <span className="text-6xl">🎬</span>
                  </div>
                {/* )} */}
              </div>

              <Card>
                <CardContent className="p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Average Rating</span>
                    <StarRating rating={movie.ratings_avg} size="sm" showValue />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Total Ratings</span>
                    <div className="flex items-center gap-1">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm font-medium">{movie.ratings_count}</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Release Year</span>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm font-medium">{movie.release_year}</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Genre</span>
                    <span className="px-2 py-1 bg-secondary rounded text-xs font-medium">{movie.genre}</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Movie details and ratings */}
          <div className="lg:col-span-2 space-y-8">
            <div>
              <h1 className="text-4xl font-bold mb-4 text-balance">{movie.title}</h1>
              <p className="text-muted-foreground leading-relaxed text-pretty">{movie.description}</p>
            </div>

            {/* Rating form for authenticated users */}
            {user && (
              <Card>
                <CardHeader>
                  <CardTitle>{userRating ? "Update Your Rating" : "Rate This Movie"}</CardTitle>
                </CardHeader>
                <CardContent>
                  <RatingForm
                    movieId={`${movie.id}`}
                    existingRating={
                      userRating
                        ? {
                            rating: userRating.rating,
                            review: userRating.review,
                          }
                        : undefined
                    }
                    onSuccess={fetchMovieData}
                  />
                </CardContent>
              </Card>
            )}

            {/* All ratings */}
            <div>
              <h2 className="text-2xl font-bold mb-4">User Reviews</h2>
              <RatingList ratings={ratings} />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
