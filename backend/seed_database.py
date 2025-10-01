#!/usr/bin/env python3
"""
Database seeder script for Movie Rating Platform
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from seeders.cli import main

if __name__ == "__main__":
    main()