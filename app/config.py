from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./nutriwell.db"
    API_URL: str = "http://localhost:8000"
    MODEL_PATH: str = "models/model_prediction.pkl"


settings = Settings()
