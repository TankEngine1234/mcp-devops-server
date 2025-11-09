from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional # <--- ADD THIS

class Settings(BaseSettings):
    # This tells pydantic to load from a .env file
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # --- App Settings ---
    USE_MOCK: bool = True
    
    # --- API Keys ---
    GITHUB_TOKEN: Optional[str] = None # <--- CHANGED
    DATADOG_API_KEY: Optional[str] = None # <--- CHANGED
    LAUNCHDARKLY_API_KEY: Optional[str] = None # <--- CHANGED

# @lru_cache() makes it so the .env file is only read once
@lru_cache()
def get_settings():
    return Settings()