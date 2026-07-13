from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    frontend_origin: str = "http://localhost:5173"
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    database_url: str = "postgresql+psycopg2://dpdp:dpdp_secret@localhost:5432/dpdp"
    jwt_secret: str = "change-me-in-production"
    jwt_expire_hours: int = 72

    @computed_field  # type: ignore[prop-decorator]
    @property
    def corpus_dir(self) -> Path:
        return self.data_dir / "corpus"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sources_dir(self) -> Path:
        return self.data_dir / "sources"


settings = Settings()
