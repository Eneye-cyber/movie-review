from app.seeders.base_seeder import BaseSeeder
from app.models.user import User
from app.auth.jwt import get_password_hash
import random

class UserSeeder(BaseSeeder):
    def run(self, count=20):
        print("Seeding users...")
        
        # Create some specific test users
        test_users = [
            {
                "username": "admin",
                "email": "admin@movierating.com",
                "password": "Admin123!"
            },
            {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "Password123!"
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "password": "Password123!"
            },
            {
                "username": "movie_lover",
                "email": "movielover@example.com",
                "password": "Password123!"
            },
            {
                "username": "cinema_fan",
                "email": "cinemafan@example.com",
                "password": "Password123!"
            }
        ]
        
        created_users = []
        
        # Create test users
        for user_data in test_users:
            if not self.db.query(User).filter(User.username == user_data["username"]).first():
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=get_password_hash(user_data["password"])
                )
                self.db.add(user)
                created_users.append(user)
        
        # Create random users
        for i in range(count - len(test_users)):
            username = self.fake.user_name()
            email = self.fake.email()
            
            # Ensure unique username and email
            while self.db.query(User).filter(User.username == username).first():
                username = self.fake.user_name()
            while self.db.query(User).filter(User.email == email).first():
                email = self.fake.email()
            
            user = User(
                username=username,
                email=email,
                password_hash=get_password_hash("Password123!")
            )
            self.db.add(user)
            created_users.append(user)
        
        self.commit()
        print(f"Created {len(created_users)} users")
        return created_users