import os
import secrets
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    google_api_key: str = "dummy_google_key"
    database_url: str = "sqlite:///ruralai.db"
    environment: str = "development"
    secret_key: Optional[str] = None
    openweather_api_key: str = "dummy_weather_key"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # Support common alternate environment variables from different stages
    gemini_api_key: Optional[str] = None

    def model_post_init(self, __context) -> None:
        """Post-initialization to resolve alias overrides and secret generation."""
        # Resolve aliases
        if self.gemini_api_key and (self.google_api_key == "dummy_google_key" or not self.google_api_key):
            self.google_api_key = self.gemini_api_key

        if not self.secret_key:
            # TODO(security): Generate ephemeral secret when secret key is not provided in env.
            # In production, this should fail-close if a static key is not provided.
            logging.warning("SECRET_KEY environment variable not set. Generating a random ephemeral secret key.")
            self.secret_key = secrets.token_hex(32)

settings = Settings()
