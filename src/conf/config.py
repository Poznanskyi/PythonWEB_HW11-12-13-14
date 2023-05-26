from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = \
        'postgresql+psycopg2://postgres:567234@195.201.150.230:5433/'
    secret_key_jwt: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = "email@email.com"
    mail_password: str = "email_pass"
    mail_from: str = "email@email.com"
    mail_port: int = 465
    mail_server: str = "smtp.server.com"
    redis_host: str = "localhost"
    redis: int = 6379
    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 1029384756
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()