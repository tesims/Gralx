import os
from dotenv import load_dotenv
import runpod

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
RUNPOD_ENDPOINT_ID = os.getenv('RUNPOD_ENDPOINT_ID')
RUNPOD_ENDPOINT_URL = os.getenv('RUNPOD_ENDPOINT_URL', 'https://9wqe954kukprc0-8000.proxy.runpod.net/')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')

