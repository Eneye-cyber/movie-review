import re
from fastapi import HTTPException, status
from datetime import datetime


def sanitize_input(text: str, max_length: int = None) -> str:
    """
    Sanitize input to prevent XSS and injection attacks
    """
    if text is None:
        return None
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>&\"\';()]', '', text)
    
    # Trim to max length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_year(year: int) -> bool:
    """Validate year is reasonable"""
    current_year = datetime.now().year 
    return 1888 <= year <= current_year + 5

def validate_rating(rating: int) -> bool:
    """Validate rating is within acceptable range"""
    return 1 <= rating <= 5