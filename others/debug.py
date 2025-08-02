from decouple import config
import os

print("=== Environment Variables Debug ===")
print(f"SECRET_KEY: {config('SECRET_KEY', default='NOT_FOUND')}")
print(f"DEBUG: {config('DEBUG', default='NOT_FOUND')}")
print(f"DB_NAME: {config('DB_NAME', default='NOT_FOUND')}")
print(f"DB_USER: {config('DB_USER', default='NOT_FOUND')}")
print(f"DB_HOST: {config('DB_HOST', default='NOT_FOUND')}")

print("\n=== .env file location ===")
from pathlib import Path
env_path = Path('.env')
print(f"Looking for .env at: {env_path.absolute()}")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    print(f".env file contents:")
    with open('.env', 'r') as f:
        print(f.read())
