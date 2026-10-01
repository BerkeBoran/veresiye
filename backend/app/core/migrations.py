from alembic import command
from alembic.config import Config

from app.core.config import MIGRATIONS_DIR, settings


def upgrade_database() -> None:
    config = Config()
    config.set_main_option("script_location", str(MIGRATIONS_DIR))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{settings.database_path.as_posix()}")
    command.upgrade(config, "head")