"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Search, X } from "lucide-react"

const GENRES = [
  "All Genres",
  "Action",
  "Adventure",
  "Animation",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Fantasy",
  "Horror",
  "Mystery",
  "Romance",
  "Sci-Fi",
  "Thriller",
  "War",
  "Western",
]

const CURRENT_YEAR = new Date().getFullYear()

interface MovieFiltersProps {
  searchQuery: string
  genre: string
  yearFrom: string
  yearTo: string
  onSearchChange: (value: string) => void
  onGenreChange: (value: string) => void
  onYearFromChange: (value: string) => void
  onYearToChange: (value: string) => void
  onClearFilters: () => void
}

export function MovieFilters({
  searchQuery,
  genre,
  yearFrom,
  yearTo,
  onSearchChange,
  onGenreChange,
  onYearFromChange,
  onYearToChange,
  onClearFilters,
}: MovieFiltersProps) {
  const hasActiveFilters = searchQuery || genre !== "All Genres" || yearFrom || yearTo

  return (
    <div className="bg-card border border-border rounded-lg p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Filters</h2>
        {hasActiveFilters && (
          <Button variant="ghost" size="sm" onClick={onClearFilters}>
            <X className="h-4 w-4 mr-2" />
            Clear All
          </Button>
        )}
      </div>

      <div className="space-y-4">
        {/* Search */}
        <div className="space-y-2">
          <Label htmlFor="search">Search</Label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              id="search"
              placeholder="Search by title or description..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="pl-9"
            />
          </div>
        </div>

        {/* Genre */}
        <div className="space-y-2">
          <Label htmlFor="genre">Genre</Label>
          <Select value={genre} onValueChange={onGenreChange}>
            <SelectTrigger id="genre">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {GENRES.map((g) => (
                <SelectItem key={g} value={g}>
                  {g}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Year Range */}
        <div className="space-y-2">
          <Label>Release Year</Label>
          <div className="grid grid-cols-2 gap-2">
            <div className="space-y-1">
              <Label htmlFor="yearFrom" className="text-xs text-muted-foreground">
                From
              </Label>
              <Input
                id="yearFrom"
                type="number"
                placeholder="1888"
                min="1888"
                max={CURRENT_YEAR}
                value={yearFrom}
                onChange={(e) => onYearFromChange(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="yearTo" className="text-xs text-muted-foreground">
                To
              </Label>
              <Input
                id="yearTo"
                type="number"
                placeholder={String(CURRENT_YEAR)}
                min="1888"
                max={CURRENT_YEAR}
                value={yearTo}
                onChange={(e) => onYearToChange(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
