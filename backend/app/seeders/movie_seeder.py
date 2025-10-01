from app.seeders.base_seeder import BaseSeeder
from app.models.movie import Movie
from app.models.user import User
import random
from datetime import datetime

class MovieSeeder(BaseSeeder):
    def __init__(self):
        super().__init__()
        self.genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime", 
            "Documentary", "Drama", "Fantasy", "Historical", "Horror",
            "Mystery", "Romance", "Sci-Fi", "Thriller", "Western",
            "Biography", "Musical", "Family", "War", "Sports"
        ]
        
        # Popular movies with realistic data
        self.popular_movies = [
            {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
            {"title": "The Godfather", "genre": "Crime", "year": 1972, "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
            {"title": "The Dark Knight", "genre": "Action", "year": 2008, "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests."},
            {"title": "Pulp Fiction", "genre": "Crime", "year": 1994, "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
            {"title": "Forrest Gump", "genre": "Drama", "year": 1994, "description": "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man."},
            {"title": "Inception", "genre": "Sci-Fi", "year": 2010, "description": "A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea into the mind of a C.E.O."},
            {"title": "The Matrix", "genre": "Sci-Fi", "year": 1999, "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."},
            {"title": "Goodfellas", "genre": "Crime", "year": 1990, "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners."},
            {"title": "The Silence of the Lambs", "genre": "Thriller", "year": 1991, "description": "A young F.B.I. cadet must receive the help of an incarcerated cannibal killer to help catch another serial killer."},
            {"title": "Parasite", "genre": "Drama", "year": 2019, "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."}
        ]
    
    def run(self, users, count=50):
        print("Seeding movies...")
        
        created_movies = []
        
        # Create popular movies
        for movie_data in self.popular_movies:
            if not self.db.query(Movie).filter(Movie.title == movie_data["title"]).first():
                creator = random.choice(users)
                movie = Movie(
                    title=movie_data["title"],
                    genre=movie_data["genre"],
                    release_year=movie_data["year"],
                    description=movie_data["description"],
                    created_by=creator.id
                )
                self.db.add(movie)
                created_movies.append(movie)
        
        # Create random movies
        for i in range(count - len(self.popular_movies)):
            creator = random.choice(users)
            genre = random.choice(self.genres)
            
            movie = Movie(
                title=self.generate_movie_title(genre),
                genre=genre,
                release_year=random.randint(1970, 2024),
                description=self.fake.paragraph(nb_sentences=3),
                created_by=creator.id
            )
            self.db.add(movie)
            created_movies.append(movie)
        
        self.commit()
        print(f"Created {len(created_movies)} movies")
        return created_movies
    
    def generate_movie_title(self, genre):
        """Generate realistic movie titles based on genre"""
        prefixes = {
            "Action": ["The Last", "Operation", "Final", "Rogue", "Shadow", "Blood", "Deadly"],
            "Comedy": ["The Great", "Funny", "Crazy", "Happy", "Silly", "Laughing"],
            "Drama": ["The Last", "Eternal", "Broken", "Lost", "Silent", "Quiet"],
            "Horror": ["The Haunting", "Night of", "Dark", "Evil", "Cursed", "Terror"],
            "Sci-Fi": ["Star", "Galaxy", "Future", "Cyber", "Quantum", "Space"],
            "Romance": ["Eternal", "Forever", "Love", "Heart", "Beautiful", "Passion"]
        }
        
        suffixes = {
            "Action": ["Hunter", "Mission", "Strike", "Force", "Game", "Killer"],
            "Comedy": ["Adventure", "Trip", "Party", "Story", "Days", "Night"],
            "Drama": ["Promise", "Memories", "Dreams", "Hope", "Journey", "Road"],
            "Horror": ["House", "Night", "Curse", "Scream", "Blood", "Death"],
            "Sci-Fi": ["Wars", "Quest", "Odyssey", "Genesis", "Nexus", "Matrix"],
            "Romance": ["Story", "Affair", "Promise", "Destiny", "Moments", "Whisper"]
        }
        
        default_prefixes = ["The", "A", "My", "Our", "Their"]
        default_suffixes = ["Story", "Journey", "Dream", "Hope", "Legacy"]
        
        prefix_list = prefixes.get(genre, default_prefixes)
        suffix_list = suffixes.get(genre, default_suffixes)
        
        return f"{random.choice(prefix_list)} {random.choice(suffix_list)}"