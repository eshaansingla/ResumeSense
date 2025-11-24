"""
Configuration settings for ResumeSense backend.
Loads environment variables and sets up database connection.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MySQL Database Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'resumesense')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/resumes')
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    
    # ML Model Configuration
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', 'backend/ml/resume_quality_model.pkl')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf'}


