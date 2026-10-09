"""Loads settings from the .env file."""
import os
from dotenv import load_dotenv

load_dotenv()

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "")
NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
MODEL_REASONING = os.getenv("MODEL_REASONING", "")
MODEL_FAST = os.getenv("MODEL_FAST", "")
