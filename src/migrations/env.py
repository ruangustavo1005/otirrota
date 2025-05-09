# flake8: noqa: E402
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from common.model.base_model import Base
from domain.companion.model import Companion
from domain.driver.model import Driver
from domain.location.model import Location
from domain.patient.model import Patient
from domain.purpose.model import Purpose
from domain.scheduling.model import Scheduling
from domain.user.model import User
from domain.vehicle.model import Vehicle
from settings import Settings

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    "postgresql://{}:{}@{}:{}/{}".format(
        Settings.DB_USER,
        Settings.DB_PASSWORD,
        Settings.DB_HOST,
        Settings.DB_PORT,
        Settings.DB_NAME,
    ),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
