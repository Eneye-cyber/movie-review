from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.jwt import get_password_hash
import random
from faker import Faker

fake = Faker()

class BaseSeeder:
    def __init__(self):
        self.fake = fake
        self.db = SessionLocal()
    
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")
    
    def close(self):
        self.db.close()
    
    def commit(self):
        self.db.commit()