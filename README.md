

````markdown
# 🎬 Movie Review App

A full-stack movie review application built with:

- **Frontend**: Next.js (React, TypeScript, Shadcn/UI)
- **Backend**: FastAPI (Python, SQLAlchemy, Pydantic)
- **Database**: (configure inside backend `database.py`)
- **Containerized**: Docker & Docker Compose

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/movie-review.git
cd movie-review
````

### 2. Run with Docker

Make sure you have **Docker** and **Docker Compose** installed.

```bash
docker-compose up --build
```

This starts:

* **Frontend** → [http://localhost:3000](http://localhost:3000)
* **Backend API** → [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Stop containers

```bash
docker-compose down
```

---

## 📂 Project Structure

```
movie-review/
├── backend/         # FastAPI backend
├── frontend/        # Next.js frontend
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Development Notes

* The backend runs with **Uvicorn + autoreload**.
* The frontend runs with **Next.js dev server**.
* Both services mount source code as volumes for live reload.

---

## 🛠️ Useful Commands

Rebuild containers:

```bash
docker-compose up --build
```

Run only backend:

```bash
docker-compose up backend
```

Run only frontend:

```bash
docker-compose up frontend
```

---

## ✅ Next Steps

* Configure **database URL** in `backend/app/database.py`.
* Add `.env` files for secrets (both backend & frontend).

