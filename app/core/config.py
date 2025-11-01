from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "Article Recommendation System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # RL Agent settings
    epsilon: float = 0.1  # Exploration rate
    learning_rate: float = 0.01
    discount_factor: float = 0.9
    
    # API settings
    max_recommendations: int = 10
    
    class Config:
        env_file = ".env"


settings = Settings()
