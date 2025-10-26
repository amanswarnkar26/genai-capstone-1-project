import os
from dataclasses import dataclass

@dataclass
class Settings:
    # GCP / Vertex AI
    gcp_project: str = os.getenv("GCP_PROJECT", "")
    gcp_location: str = os.getenv("GCP_LOCATION", "us-central1")
    vertex_model: str = os.getenv("VERTEX_MODEL", "gemini-1.5-flash-002")
    # Data paths
    sqlite_path: str = os.getenv("SQLITE_PATH", "data/loan.db")
    chroma_path: str = os.getenv("CHROMA_PATH", "data/chroma")
    policies_path: str = os.getenv("POLICIES_PATH", "data/policies")
    # Security / Secrets
    database_uri: str = os.getenv("DATABASE_URI", "sqlite:///data/loan.db")
    # Observability
    langfuse_host: str = os.getenv("LANGFUSE_HOST", "")
    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    enable_google_logging: bool = os.getenv("ENABLE_GOOGLE_LOGGING", "false").lower() == "true"

settings = Settings()
