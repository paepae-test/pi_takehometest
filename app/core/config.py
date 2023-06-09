from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "pi_takehometest"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    TEST_APP_USER_USERNAME: str = "test"
    TEST_APP_USER_PASSWORD: str = "password"

    class Config:
        env_file = ".env"


settings = Settings()
