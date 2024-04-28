from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Этот блок позволяет нам импортировать модели SQLAlchemy из основного приложения
import sys
from os.path import abspath, dirname

sys.path.append(abspath(dirname(dirname(__file__))))
from models import Base

# Этот блок позволяет Alembic использовать объект MetaData вашей базы данных
target_metadata = Base.metadata

# Настройка логгирования
config = context.config
fileConfig(config.config_file_name)


# Этот блок позволяет Alembic использовать подключение к вашей базе данных
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Этот код определяет, какой тип миграции будет использоваться
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
