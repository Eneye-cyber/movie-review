import { NextResponse } from "next/server"

export async function GET(request: Request) {
  try {
    const authHeader = request.headers.get("Authorization")
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 })
    }

    const token = authHeader.substring(7)

    // Decode token (simplified - use proper JWT library in production)
    const decoded = JSON.parse(Buffer.from(token, "base64").toString())

    // Return user data (in production, fetch from database)
    return NextResponse.json({
      id: decoded.userId,
      email: decoded.email,
      name: "Demo User", // Fetch from database in production
    })
  } catch (error) {
    console.error("[Logger] Auth verification error:", error)
    return NextResponse.json({ message: "Invalid token" }, { status: 401 })
  }
}
