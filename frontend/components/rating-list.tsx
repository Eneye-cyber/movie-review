import { StarRating } from "@/components/star-rating"
import type { Rating } from "@/lib/types"
import { Card, CardContent } from "@/components/ui/card"
import { User } from "lucide-react"

interface RatingListProps {
  ratings: Rating[]
}

export function RatingList({ ratings }: RatingListProps) {
  if (ratings.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p>No ratings yet. Be the first to rate this movie!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {ratings.map((rating) => (
        <Card key={rating.id}>
          <CardContent className="p-4 space-y-3">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
                  <User className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="font-medium text-sm">{rating.userName}</p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(rating.createdAt).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </p>
                </div>
              </div>
              <StarRating rating={rating.rating} size="sm" />
            </div>
            {rating.review && <p className="text-sm text-foreground leading-relaxed">{rating.review}</p>}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
