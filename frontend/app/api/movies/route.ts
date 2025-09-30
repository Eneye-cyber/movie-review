import { NextResponse } from "next/server"
import type { Movie, PaginatedResponse } from "@/lib/types"

// Mock movie database
const mockMovies: Movie[] = [
  {
    id: "1",
    title: "The Shawshank Redemption",
    description:
      "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    genre: "Drama",
    releaseYear: 1994,
    posterUrl: "/shawshank-redemption-poster.png",
    averageRating: 4.8,
    ratingCount: 1247,
  },
  {
    id: "2",
    title: "The Godfather",
    description:
      "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
    genre: "Crime",
    releaseYear: 1972,
    posterUrl: "/classic-mob-poster.png",
    averageRating: 4.7,
    ratingCount: 1089,
  },
  {
    id: "3",
    title: "The Dark Knight",
    description:
      "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
    genre: "Action",
    releaseYear: 2008,
    posterUrl: "/dark-knight-poster.png",
    averageRating: 4.6,
    ratingCount: 1523,
  },
  {
    id: "4",
    title: "Pulp Fiction",
    description:
      "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
    genre: "Crime",
    releaseYear: 1994,
    posterUrl: "/pulp-fiction-poster.png",
    averageRating: 4.5,
    ratingCount: 987,
  },
  {
    id: "5",
    title: "Forrest Gump",
    description:
      "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.",
    genre: "Drama",
    releaseYear: 1994,
    posterUrl: "/forrest-gump-poster.png",
    averageRating: 4.4,
    ratingCount: 1345,
  },
  {
    id: "6",
    title: "Inception",
    description:
      "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.",
    genre: "Sci-Fi",
    releaseYear: 2010,
    posterUrl: "/inception-movie-poster.png",
    averageRating: 4.6,
    ratingCount: 1678,
  },
  {
    id: "7",
    title: "The Matrix",
    description:
      "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    genre: "Sci-Fi",
    releaseYear: 1999,
    posterUrl: "/matrix-movie-poster.png",
    averageRating: 4.5,
    ratingCount: 1432,
  },
  {
    id: "8",
    title: "Goodfellas",
    description:
      "The story of Henry Hill and his life in the mob, covering his relationship with his wife and his partners in crime.",
    genre: "Crime",
    releaseYear: 1990,
    posterUrl: "/goodfellas-poster.png",
    averageRating: 4.6,
    ratingCount: 876,
  },
  {
    id: "9",
    title: "Interstellar",
    description: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    genre: "Sci-Fi",
    releaseYear: 2014,
    posterUrl: "/interstellar-movie-poster.jpg",
    averageRating: 4.7,
    ratingCount: 1567,
  },
  {
    id: "10",
    title: "The Silence of the Lambs",
    description:
      "A young FBI cadet must receive the help of an incarcerated cannibal killer to catch another serial killer.",
    genre: "Thriller",
    releaseYear: 1991,
    posterUrl: "/silence-of-the-lambs-poster.jpg",
    averageRating: 4.5,
    ratingCount: 923,
  },
  {
    id: "11",
    title: "Saving Private Ryan",
    description:
      "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper.",
    genre: "War",
    releaseYear: 1998,
    posterUrl: "/saving-private-ryan-poster.jpg",
    averageRating: 4.6,
    ratingCount: 1234,
  },
  {
    id: "12",
    title: "The Green Mile",
    description:
      "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder.",
    genre: "Drama",
    releaseYear: 1999,
    posterUrl: "/green-mile-movie-poster.jpg",
    averageRating: 4.5,
    ratingCount: 1098,
  },
  {
    id: "13",
    title: "Parasite",
    description:
      "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    genre: "Thriller",
    releaseYear: 2019,
    posterUrl: "/parasite-movie-poster.png",
    averageRating: 4.6,
    ratingCount: 1456,
  },
  {
    id: "14",
    title: "The Lion King",
    description:
      "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
    genre: "Animation",
    releaseYear: 1994,
    posterUrl: "/generic-african-savanna-poster.png",
    averageRating: 4.4,
    ratingCount: 1789,
  },
  {
    id: "15",
    title: "Gladiator",
    description:
      "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family.",
    genre: "Action",
    releaseYear: 2000,
    posterUrl: "/gladiator-movie-poster.jpg",
    averageRating: 4.5,
    ratingCount: 1345,
  },
]

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const page = Number.parseInt(searchParams.get("page") || "1")
  const pageSize = Number.parseInt(searchParams.get("pageSize") || "12")
  const search = searchParams.get("search")?.toLowerCase()
  const genre = searchParams.get("genre")
  const yearFrom = searchParams.get("yearFrom")
  const yearTo = searchParams.get("yearTo")

  let filteredMovies = [...mockMovies]

  // Text search filter
  if (search) {
    filteredMovies = filteredMovies.filter(
      (movie) => movie.title.toLowerCase().includes(search) || movie.description.toLowerCase().includes(search),
    )
  }

  // Genre filter
  if (genre && genre !== "All Genres") {
    filteredMovies = filteredMovies.filter((movie) => movie.genre === genre)
  }

  // Year range filter
  if (yearFrom) {
    const fromYear = Number.parseInt(yearFrom)
    filteredMovies = filteredMovies.filter((movie) => movie.releaseYear >= fromYear)
  }

  if (yearTo) {
    const toYear = Number.parseInt(yearTo)
    filteredMovies = filteredMovies.filter((movie) => movie.releaseYear <= toYear)
  }

  // Calculate pagination on filtered results
  const startIndex = (page - 1) * pageSize
  const endIndex = startIndex + pageSize
  const paginatedMovies = filteredMovies.slice(startIndex, endIndex)

  const response: PaginatedResponse<Movie> = {
    data: paginatedMovies,
    total: filteredMovies.length,
    page,
    pageSize,
    totalPages: Math.ceil(filteredMovies.length / pageSize),
  }

  return NextResponse.json(response)
}

export async function POST(request: Request) {
  try {
    const authHeader = request.headers.get("Authorization")
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 })
    }

    const { title, description, genre, releaseYear, posterUrl } = await request.json()

    // Validate required fields
    if (!title || !description || !genre || !releaseYear) {
      return NextResponse.json({ message: "Missing required fields" }, { status: 400 })
    }

    // Create new movie
    const newMovie: Movie = {
      id: String(mockMovies.length + 1),
      title,
      description,
      genre,
      releaseYear,
      posterUrl: posterUrl || undefined,
      averageRating: 0,
      ratingCount: 0,
    }

    mockMovies.push(newMovie)

    return NextResponse.json(newMovie, { status: 201 })
  } catch (error) {
    console.error("[Logger] Movie creation error:", error)
    return NextResponse.json({ message: "Internal server error" }, { status: 500 })
  }
}
