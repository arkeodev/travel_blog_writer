import os

class Config:
    FIREWORKS_API_KEY: str = os.environ.get("FIREWORKS_API_KEY", "")
