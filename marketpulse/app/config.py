from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "MARKETPULSE"
    APP_ENV: str = "development"

    META_API_KEY: str = ""
    META_BASE_URL: str = "https://api.meta.ai/v1"
    META_MUSE_WONDER_MODEL: str = "muse-wonder-1.0"  # Dedicated to Research Director
    META_SPARK_MODEL: str = "spark-1.3"  # Dedicated to all specialist research agents


    # Web Search Provider (Tavily Search API)
    TAVILY_API_KEY: str = ""
    TAVILY_SEARCH_DEPTH: str = "basic"  # 'basic', 'advanced'
    TAVILY_MAX_RESULTS: int = 8
    TAVILY_INCLUDE_RAW_CONTENT: bool = False
    TAVILY_TOPIC: str = "general"  # 'general', 'news', 'finance'

    # Search Budget & Cost Optimization
    MAX_SEARCHES_PER_RESEARCH: int = 15
    MAX_RESULTS_PER_SEARCH: int = 8
    MAX_FOLLOWUP_SEARCHES: int = 4
    SEARCH_CACHE_TTL_HOURS: int = 24
    SEARCH_CACHE_ENABLED: bool = True

    DATABASE_URL: str = "sqlite:///./marketpulse.db"

    ENABLE_MOCK_MODE: bool = False

    MAX_PARALLEL_AGENTS: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()