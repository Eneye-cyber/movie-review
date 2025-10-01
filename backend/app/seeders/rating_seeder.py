from app.seeders.base_seeder import BaseSeeder
from app.models.rating import Rating
from app.models.movie import Movie
from app.models.user import User
import random

class RatingSeeder(BaseSeeder):
    def run(self, users, movies, ratings_per_movie=5):
        print("Seeding ratings...")
        
        created_ratings = []
        
        for movie in movies:
            # Get users who didn't create this movie (can't rate own movie)
            available_users = [user for user in users if user.id != movie.created_by]
            
            # Select random users to rate this movie
            rating_users = random.sample(
                available_users, 
                min(ratings_per_movie, len(available_users))
            )
            
            for user in rating_users:
                # Check if rating already exists
                existing_rating = self.db.query(Rating).filter(
                    Rating.movie_id == movie.id,
                    Rating.user_id == user.id
                ).first()
                
                if not existing_rating:
                    rating_value = self.generate_rating(movie.release_year)
                    review = self.generate_review(rating_value, movie.title)
                    
                    rating = Rating(
                        movie_id=movie.id,
                        user_id=user.id,
                        rating=rating_value,
                        review=review
                    )
                    self.db.add(rating)
                    created_ratings.append(rating)
        
        self.commit()
        
        # Update movie rating statistics
        self.update_movie_stats(movies)
        
        print(f"Created {len(created_ratings)} ratings")
        return created_ratings
    
    def generate_rating(self, release_year):
        """Generate ratings with some logic"""
        current_year = 2024
        movie_age = current_year - release_year
        
        # Older classic movies tend to get higher ratings
        base_rating = random.randint(1, 5)
        if movie_age > 20:
            # Classic movies get bonus
            base_rating = min(5, base_rating + 1)
        elif movie_age < 5:
            # Recent movies have more varied ratings
            base_rating = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 3, 4, 3])[0]
        
        return base_rating
    
    def generate_review(self, rating, movie_title):
        """Generate realistic reviews based on rating"""
        positive_reviews = [
            f"Absolutely loved {movie_title}! One of the best films I've seen.",
            f"{movie_title} is a masterpiece. Highly recommended!",
            f"Fantastic movie! Great acting and storyline.",
            f"Couldn't take my eyes off the screen. {movie_title} is incredible!",
            f"A must-watch! {movie_title} delivers on every level."
        ]
        
        neutral_reviews = [
            f"{movie_title} was decent. Worth watching once.",
            f"Solid movie with some good moments.",
            f"Not bad, but not great either. {movie_title} is okay.",
            f"Had its moments. {movie_title} is a mixed bag.",
            f"Average film. Nothing special but entertaining enough."
        ]
        
        negative_reviews = [
            f"Disappointed with {movie_title}. Expected more.",
            f"{movie_title} was a letdown. Poor execution.",
            f"Not my cup of tea. {movie_title} failed to impress.",
            f"Could have been better. {movie_title} has many flaws.",
            f"Waste of time. {movie_title} didn't live up to the hype."
        ]
        
        if rating >= 4:
            return random.choice(positive_reviews)
        elif rating == 3:
            return random.choice(neutral_reviews)
        else:
            return random.choice(negative_reviews)
    
    def update_movie_stats(self, movies):
        """Update rating statistics for all movies"""
        from sqlalchemy import func
        
        for movie in movies:
            stats = self.db.query(
                func.count(Rating.id).label('count'),
                func.avg(Rating.rating).label('avg')
            ).filter(Rating.movie_id == movie.id).first()
            
            movie.ratings_count = stats.count or 0
            movie.ratings_avg = float(stats.avg or 0.0)
        
        self.commit()