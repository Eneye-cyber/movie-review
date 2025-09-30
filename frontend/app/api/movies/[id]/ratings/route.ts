import { NextResponse } from "next/server"
import type { Rating } from "@/lib/types"

// Mock ratings database
const mockRatings: Rating[] = [
  {
    id: "1",
    movieId: "1",
    userId: "1",
    userName: "John Doe",
    rating: 5,
    review: "An absolute masterpiece. The storytelling is phenomenal and the performances are outstanding.",
    createdAt: "2024-01-15T10:30:00Z",
  },
  {
    id: "2",
    movieId: "1",
    userId: "2",
    userName: "Jane Smith",
    rating: 5,
    review: "One of the best films ever made. A must-watch for everyone.",
    createdAt: "2024-01-20T14:45:00Z",
  },
  {
    id: "3",
    movieId: "1",
    userId: "3",
    userName: "Mike Johnson",
    rating: 4,
    review: "Great movie with powerful themes. Highly recommended.",
    createdAt: "2024-02-01T09:15:00Z",
  },
]

export async function GET(request: Request, { params }: { params: { id: string } }) {
  const movieRatings = mockRatings.filter((r) => r.movieId === params.id)
  return NextResponse.json(movieRatings)
}

export async function POST(request: Request, { params }: { params: { id: string } }) {
  try {
    const authHeader = request.headers.get("Authorization")
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 })
    }

    const token = authHeader.substring(7)
    const decoded = JSON.parse(Buffer.from(token, "base64").toString())

    const { rating, review } = await request.json()

    // Create new rating
    const newRating: Rating = {
      id: String(mockRatings.length + 1),
      movieId: params.id,
      userId: decoded.userId,
      userName: "Demo User", // In production, fetch from database
      rating,
      review,
      createdAt: new Date().toISOString(),
    }

    mockRatings.push(newRating)

    return NextResponse.json(newRating, { status: 201 })
  } catch (error) {
    console.error("[Logger] Rating submission error:", error)
    return NextResponse.json({ message: "Internal server error" }, { status: 500 })
  }
}

export async function PUT(request: Request, { params }: { params: { id: string } }) {
  try {
    const authHeader = request.headers.get("Authorization")
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 })
    }

    const token = authHeader.substring(7)
    const decoded = JSON.parse(Buffer.from(token, "base64").toString())

    const { rating, review } = await request.json()

    // Find and update existing rating
    const existingRatingIndex = mockRatings.findIndex((r) => r.movieId === params.id && r.userId === decoded.userId)

    if (existingRatingIndex === -1) {
      return NextResponse.json({ message: "Rating not found" }, { status: 404 })
    }

    mockRatings[existingRatingIndex] = {
      ...mockRatings[existingRatingIndex],
      rating,
      review,
    }

    return NextResponse.json(mockRatings[existingRatingIndex])
  } catch (error) {
    console.error("[Logger] Rating update error:", error)
    return NextResponse.json({ message: "Internal server error" }, { status: 500 })
  }
}
