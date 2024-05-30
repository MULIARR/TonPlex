
import os

from pydantic.dataclasses import dataclass


@dataclass
class AppConfig:
    BASE_DIR: str
    TEMPLATES_DIR: str
    STATIC_DIR: str


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(base_dir, 'app', 'templates')
static_dir = os.path.join(base_dir, 'static')

app_config = AppConfig(
    BASE_DIR=base_dir,
    TEMPLATES_DIR=templates_dir,
    STATIC_DIR=static_dir
)


# class Settings(BaseSettings):
#     ...
#
#     model_config = SettingsConfigDict(env_file=".env")
#
#
# settings = Settings()
