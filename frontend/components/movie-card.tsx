import Link from "next/link"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { StarRating } from "@/components/star-rating"
import type { Movie } from "@/lib/types"
import { Calendar, Users } from "lucide-react"

interface MovieCardProps {
  movie: Movie
}

export function MovieCard({ movie }: MovieCardProps) {
  return (
    <Link href={`/movies/${movie.id}`}>
      <Card className="overflow-hidden hover:border-primary/50 transition-colors h-full group">
        <div className="aspect-[2/3] bg-muted relative overflow-hidden">
          {movie.posterUrl ? (
            <img
              src={movie.posterUrl || "/placeholder.svg"}
              alt={movie.title}
              className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-muted-foreground">
              <span className="text-4xl">🎬</span>
            </div>
          )}
        </div>
        <CardContent className="p-4 space-y-2">
          <h3 className="font-semibold text-lg line-clamp-1 group-hover:text-primary transition-colors">
            {movie.title}
          </h3>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              <span>{movie.releaseYear}</span>
            </div>
            <span className="px-2 py-0.5 bg-secondary rounded text-xs">{movie.genre}</span>
          </div>
        </CardContent>
        <CardFooter className="p-4 pt-0 flex items-center justify-between">
          <StarRating rating={movie.averageRating} size="sm" showValue />
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Users className="h-3 w-3" />
            <span>{movie.ratingCount}</span>
          </div>
        </CardFooter>
      </Card>
    </Link>
  )
}
