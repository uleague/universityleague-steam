import os

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Class for general config
    """

    BACKEND_URL = os.getenv("BACKEND_URL")
    BACKEND_TOKEN = os.getenv("BACKEND_TOKEN")
    PORT = os.getenv("PORT", "8000")


class SteamConfig:
    """
    Class for Steam config
    """

    LOGIN = os.getenv("STEAM_LOGIN")
    PASSWORD = os.getenv("STEAM_PASSWORD")
    API = os.getenv("STEAM_API")
    SHARED_SECRET = os.getenv("STEAM_SHARED_SECRET")
