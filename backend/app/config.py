from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Enterprise Research & Action Agent"
    environment: str = "development"
    database_url: str
    alpha_vantage_api_key: str
    news_api_key: str
    groq_api_key: str
    #tavily_api_key: str
   #jwt_secret_key: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
