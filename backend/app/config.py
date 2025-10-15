import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///pokemon_battle.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    POKEAPI_BASE_URL = os.getenv('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')