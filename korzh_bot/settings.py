import os

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

STEAM_LOGIN = os.getenv("STEAM_LOGIN")
STEAM_PASSWORD = os.getenv("STEAM_PASSWORD")

STEAM_API = os.getenv("STEAM_API")
STEAM_SHARED_SECRET = os.getenv("STEAM_SHARED_SECRET")

PORT = os.getenv("PORT", 8080)
