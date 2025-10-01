# Movie Rating Application

A modern, full-featured React SPA for browsing, rating, and reviewing movies. Built with Next.js, TypeScript, and Tailwind CSS with a dark theme.

## Features

### Authentication
- **User Registration & Login** - Secure JWT-based authentication
- **Protected Routes** - Automatic redirection for unauthenticated users
- **Persistent Sessions** - Token stored in localStorage with automatic validation
- **User Context** - Global auth state management via React Context

### Movie Browsing
- **Movie List View** - Responsive grid layout with movie cards
- **Pagination** - Navigate through large movie collections (12 movies per page)
- **Star Rating Display** - Visual 5-star rating system with average scores
- **Rating Count** - See how many users have rated each movie
- **Movie Posters** - High-quality poster images for visual appeal

### Movie Details
- **Comprehensive Movie Info** - Full description, genre, release year, director, cast
- **Rating Statistics** - Average rating and total number of ratings
- **User Reviews** - Complete list of all ratings with reviewer names, scores, and review text
- **Submit/Update Ratings** - Interactive star rating form with optional review text (authenticated users only)
- **Real-time Updates** - Ratings update immediately after submission

### Search & Filter
- **Text Search** - Search movies by title or description
- **Genre Filter** - Filter by specific genres (Action, Drama, Comedy, etc.)
- **Year Range Filter** - Find movies within a specific year range
- **Combined Filters** - Use multiple filters simultaneously
- **URL State Management** - Filters persist in URL for shareable links

### Movie Management
- **Add New Movies** - Protected form for creating new movie entries
- **Form Validation** - Client-side validation for all required fields
- **Genre Selection** - Dropdown with predefined genre options
- **Poster URL Support** - Add custom poster images via URL

### UX Features
- **Loading States** - Skeleton loaders and spinners for async operations
- **Error Handling** - User-friendly error messages for failed requests
- **Responsive Design** - Mobile-first design that works on all screen sizes
- **Smooth Animations** - Hover effects and transitions for better UX
- **Accessible UI** - Semantic HTML and ARIA labels for screen readers

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **State Management**: React Context API
- **HTTP Client**: Native fetch API
- **Routing**: Next.js App Router with dynamic routes
- **Icons**: Lucide React

## Design Choices

### JWT Authentication Approach

**Current Implementation: localStorage**

The app stores JWT tokens in `localStorage` for simplicity and ease of development:

**Pros:**
- Simple implementation
- Works seamlessly with client-side routing
- Easy to access from any component
- No server-side session management needed

**Cons:**
- Vulnerable to XSS attacks
- Token accessible via JavaScript
- Not ideal for production applications

**Alternative: httpOnly Cookies (Recommended for Production)**

For production applications, consider implementing httpOnly cookies:

\`\`\`typescript
// Server-side (API route)
export async function POST(request: Request) {
  // ... authentication logic ...
  
  const response = NextResponse.json({ user });
  response.cookies.set('auth_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 60 * 60 * 24 * 7 // 7 days
  });
  
  return response;
}
\`\`\`

**Benefits of httpOnly cookies:**
- Not accessible via JavaScript (XSS protection)
- Automatically sent with requests
- More secure for production environments
- Can be configured with secure flags

**Implementation Steps:**
1. Modify `/api/auth/login` and `/api/auth/register` to set httpOnly cookies
2. Update `/api/auth/me` to read token from cookies instead of Authorization header
3. Remove localStorage token storage from `auth-context.tsx`
4. Add middleware to refresh tokens automatically

### State Management

**React Context API** is used for global state management:
- **AuthContext**: Manages user authentication state, login/logout functions
- Lightweight and built into React (no external dependencies)
- Sufficient for this app's complexity level
- Easy to understand and maintain

For larger applications, consider Redux Toolkit or Zustand for more advanced state management needs.

### Styling Architecture

**Tailwind CSS v4** with a custom dark theme:
- **Color Palette**: Black backgrounds, white/gray text, subtle blue accents
- **Typography**: Geist Sans for UI, Geist Mono for code
- **Component Library**: shadcn/ui for consistent, accessible components
- **Responsive Design**: Mobile-first approach with breakpoint utilities
- **Dark Theme**: Vercel-inspired aesthetic with high contrast for readability

### API Architecture

**Mock API Routes** (Next.js Route Handlers):
- In-memory data storage for demonstration purposes
- RESTful endpoint design
- Proper HTTP status codes and error handling
- Ready to be replaced with real database integration

**For Production:**
- Replace in-memory storage with a database (PostgreSQL, MongoDB, etc.)
- Add proper validation and sanitization
- Implement rate limiting
- Add comprehensive error logging
- Use environment variables for sensitive data

## Project Structure

\`\`\`
frontend/
├── app/
│   ├── api/
│   │   ├── auth/
│   │   │   ├── login/route.ts
│   │   │   ├── register/route.ts
│   │   │   └── me/route.ts
│   │   └── movies/
│   │       ├── route.ts
│   │       └── [id]/
│   │           ├── route.ts
│   │           └── ratings/route.ts
│   ├── login/page.tsx
│   ├── register/page.tsx
│   ├── movies/
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   ├── add/page.tsx
│   │   └── [id]/page.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── header.tsx
│   ├── movie-card.tsx
│   ├── movie-filters.tsx
│   ├── star-rating.tsx
│   ├── rating-form.tsx
│   ├── rating-list.tsx
│   ├── pagination.tsx
│   └── protected-route.tsx
├── lib/
│   ├── auth-context.tsx
│   ├── types.ts
│   └── utils.ts
└── public/
    └── *.png            # Movie poster images
\`\`\`

## Setup Instructions

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. **Clone or download the project**

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Run the development server**
   \`\`\`bash
   npm run dev
   \`\`\`

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### First Steps

1. **Register a new account** at `/register`
2. **Login** with your credentials at `/login`
3. **Browse movies** at `/movies`
4. **Add a new movie** at `/movies/add` (requires authentication)
5. **Rate and review** movies on their detail pages

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  \`\`\`json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  \`\`\`

- `POST /api/auth/login` - Login user
  \`\`\`json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  \`\`\`

- `GET /api/auth/me` - Get current user (requires Authorization header)

### Movies

- `GET /api/movies` - Get paginated movie list
  - Query params: `page`, `search`, `genre`, `yearFrom`, `yearTo`
  
- `POST /api/movies` - Create new movie (requires authentication)
  \`\`\`json
  {
    "title": "Movie Title",
    "description": "Movie description",
    "genre": "Action",
    "releaseYear": 2024,
    "director": "Director Name",
    "cast": ["Actor 1", "Actor 2"],
    "posterUrl": "https://example.com/poster.jpg"
  }
  \`\`\`

- `GET /api/movies/[id]` - Get movie details

- `POST /api/movies/[id]/ratings` - Submit/update rating (requires authentication)
  \`\`\`json
  {
    "rating": 5,
    "review": "Great movie!"
  }
  \`\`\`

## Environment Variables

No environment variables are required for the mock implementation. For production with a real backend:

\`\`\`env



# API URL (since we are using separate backend)
NEXT_PUBLIC_API_BASE_URL=your_api_base_url_without_the_trailing_slash
\`\`\`



## Contributing

This is a demonstration project. Feel free to fork and modify for your own use cases.

## License

MIT License - feel free to use this project for learning and development purposes.
