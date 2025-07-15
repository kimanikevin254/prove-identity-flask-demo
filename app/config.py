import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    PROVE_API_BASE_URL = os.environ.get('PROVE_API_BASE_URL')
    PROVE_CLIENT_ID = os.environ.get('PROVE_CLIENT_ID')
    PROVE_CLIENT_SECRET = os.environ.get('PROVE_CLIENT_SECRET')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

config = {
    'development': DevelopmentConfig
}