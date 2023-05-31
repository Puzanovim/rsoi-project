import logging
from typing import Any, Dict

from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://program:test@postgres:5432/notes"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


def run_db_migrations(db_config: Dict[str, Any], migration_script_location: str) -> None:
    """
    Функция запускает миграции alembic через API
    :param db_config: Конфигурация для подключения к БД
    :param migration_script_location: Путь до директории со скриптами миграций
    :return:
    """
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", migration_script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    alembic_cfg.set_main_option("standalone", 'false')
    for option in ['db_host', 'db_user', 'db_password', 'db_name']:
        if option not in db_config:
            raise Exception(f"{option} value not set")
        alembic_cfg.set_main_option(option, db_config[option])

    logger.info('Running migrations')
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as exc:
        logger.exception(exc)
        raise Exception("Error while executing migrations: {}".format(exc))
    logger.info('Migrations completed')
