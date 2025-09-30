"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Film, Star, Users, TrendingUp } from "lucide-react"

export default function HomePage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && user) {
      router.push("/movies")
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xl font-semibold">
            <Film className="h-6 w-6 text-primary" />
            <span className="text-foreground">MovieRate</span>
          </div>
          <div className="flex gap-3">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button variant="default">Sign Up</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-5xl font-bold text-balance">Discover, Rate, and Review Your Favorite Movies</h1>
            <p className="text-xl text-muted-foreground text-pretty">
              Join our community of movie enthusiasts. Share your opinions, discover new films, and connect with fellow
              cinephiles.
            </p>
          </div>

          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8">
                Get Started
              </Button>
            </Link>
            <Link href="/movies">
              <Button size="lg" variant="outline" className="text-lg px-8 bg-transparent">
                Browse Movies
              </Button>
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mt-16">
            <div className="p-6 rounded-lg bg-card border border-border">
              <Star className="h-10 w-10 text-primary mb-4 mx-auto" />
              <h3 className="text-lg font-semibold mb-2">Rate Movies</h3>
              <p className="text-sm text-muted-foreground">Share your ratings and help others discover great films</p>
            </div>
            <div className="p-6 rounded-lg bg-card border border-border">
              <Users className="h-10 w-10 text-primary mb-4 mx-auto" />
              <h3 className="text-lg font-semibold mb-2">Join Community</h3>
              <p className="text-sm text-muted-foreground">Connect with movie lovers and discuss your favorites</p>
            </div>
            <div className="p-6 rounded-lg bg-card border border-border">
              <TrendingUp className="h-10 w-10 text-primary mb-4 mx-auto" />
              <h3 className="text-lg font-semibold mb-2">Discover Trends</h3>
              <p className="text-sm text-muted-foreground">Find trending movies and see what everyone is watching</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
