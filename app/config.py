from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_username : str
    database_password : str
    database_port: str
    database_name: str
    database_hostname: str
    secret_key: str 
    algorithm: str
    access_token_expiry: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()