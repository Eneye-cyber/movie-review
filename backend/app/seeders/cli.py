import argparse
from app.seeders.main_seeder import MainSeeder

def main():
    parser = argparse.ArgumentParser(description='Seed the database with sample data')
    parser.add_argument('--users', type=int, default=20, help='Number of users to create')
    parser.add_argument('--movies', type=int, default=50, help='Number of movies to create')
    parser.add_argument('--ratings-per-movie', type=int, default=5, help='Ratings per movie')
    
    args = parser.parse_args()
    
    seeder = MainSeeder()
    seeder.run(
        user_count=args.users,
        movie_count=args.movies,
        ratings_per_movie=args.ratings_per_movie
    )

if __name__ == "__main__":
    main()