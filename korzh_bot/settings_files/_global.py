import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)

# Steam
STEAM_LOGIN = os.getenv("STEAM_LOGIN", False)
STEAM_PASSWORD = os.getenv("STEAM_PASSWORD", False)

STEAM_API = os.getenv("STEAM_API", False)
STEAM_SHARED_SECRET = os.getenv("STEAM_SHARED_SECRET", False)


