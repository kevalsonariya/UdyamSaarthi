import os
from typing import List
from pydantic import BaseModel
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Lightweight stdlib fallback to read .env if present
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if not os.path.exists(env_file):
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
        except Exception:
            pass


class Settings(BaseModel):
    PROJECT_NAME: str = "BizSahayak - UdyamSaarthi"
    TAGLINE: str = "From Business Idea → Business Insight → Financial Plan"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_PREFIX: str = "/api/v1"
    
    # Frontend CORS origins
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ]
    
    # Optional LLM / API credentials loaded securely from environment variables
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")

    # Optional Google Places API credentials for Phase B9 Real Competitor Mapping
    GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY", "") or os.getenv("GOOGLE_MAPS_API_KEY", "")
    COMPETITOR_SEARCH_RADIUS_KM: float = float(os.getenv("COMPETITOR_SEARCH_RADIUS_KM", "5.0"))
    COMPETITOR_MAX_RESULTS: int = int(os.getenv("COMPETITOR_MAX_RESULTS", "4"))

settings = Settings()
