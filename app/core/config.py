from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Cambodia DPL Navigator"
    debug: bool = False
    production_mode: bool = False # New setting for production environment
    api_prefix: str = "/api/v1"
    openai_api_key: str
    llm_model_name: str = "gpt-4o"
    llm_temperature: float = 0.7
    vector_db_path: str = "./chroma_db" # Local ChromaDB path

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignore extra fields from .env not defined in Settings

settings = Settings()
