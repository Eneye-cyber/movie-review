"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { StarRating } from "@/components/star-rating"
import { useToast } from "@/hooks/use-toast"
import { Loader2 } from "lucide-react"

interface RatingFormProps {
  movieId: string
  existingRating?: {
    rating: number
    review?: string
  }
  onSuccess: () => void
}

export function RatingForm({ movieId, existingRating, onSuccess }: RatingFormProps) {
  const [rating, setRating] = useState(existingRating?.rating || 0)
  const [review, setReview] = useState(existingRating?.review || "")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (rating === 0) {
      toast({
        title: "Rating required",
        description: "Please select a star rating",
        variant: "destructive",
      })
      return
    }

    setIsSubmitting(true)

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`/api/movies/${movieId}/ratings`, {
        method: existingRating ? "PUT" : "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ rating, review }),
      })

      if (!response.ok) {
        throw new Error("Failed to submit rating")
      }

      toast({
        title: existingRating ? "Rating updated" : "Rating submitted",
        description: "Thank you for your feedback!",
      })

      onSuccess()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit rating",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label>Your Rating</Label>
        <StarRating rating={rating} interactive onRatingChange={setRating} size="lg" />
      </div>

      <div className="space-y-2">
        <Label htmlFor="review">Review (Optional)</Label>
        <Textarea
          id="review"
          placeholder="Share your thoughts about this movie..."
          value={review}
          onChange={(e) => setReview(e.target.value)}
          rows={4}
          disabled={isSubmitting}
        />
      </div>

      <Button type="submit" disabled={isSubmitting || rating === 0}>
        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {existingRating ? "Update Rating" : "Submit Rating"}
      </Button>
    </form>
  )
}
