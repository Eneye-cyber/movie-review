import { NextResponse } from "next/server"

// Mock user database - replace with real database
const users: Array<{ id: string; name: string; email: string; password: string }> = []

export async function POST(request: Request) {
  try {
    const { name, email, password } = await request.json()

    // Check if user already exists
    const existingUser = users.find((u) => u.email === email)
    if (existingUser) {
      return NextResponse.json({ message: "User already exists" }, { status: 400 })
    }

    // Create new user
    const newUser = {
      id: String(users.length + 1),
      name,
      email,
      password, // In production, hash the password
    }
    users.push(newUser)

    // Generate JWT token (simplified - use proper JWT library in production)
    const token = Buffer.from(JSON.stringify({ userId: newUser.id, email: newUser.email })).toString("base64")

    return NextResponse.json({
      token,
      user: {
        id: newUser.id,
        name: newUser.name,
        email: newUser.email,
      },
    })
  } catch (error) {
    console.error("[Logger] Registration error:", error)
    return NextResponse.json({ message: "Internal server error" }, { status: 500 })
  }
}
