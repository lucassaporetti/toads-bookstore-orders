import logging
import alembic.config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bookstore_orders.components.config import envs


logger = logging.getLogger()

Base = declarative_base()
SQLALCHEMY_URI = (
    f"{envs.DB_SERVICE}://{envs.DB_USER}:{envs.DB_PASSWORD}"
    f"@{envs.DB_HOST}:{envs.DB_PORT}/{envs.DB_DATABASE}"
)
engine_default = create_engine(
    SQLALCHEMY_URI,
    pool_pre_ping=True,
    echo=envs.SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_default, expire_on_commit=False
)


class DatabaseService:
    def __init__(self):
        self._session = SessionLocal()

    @property
    def query(self):
        return self._session.query

    @property
    def add(self):
        return self._session.add

    @property
    def remove(self):
        return self._session.delete

    def commit(self):
        self._session.commit()

    def flush(self):
        self._session.flush()

    def __enter__(self):
        return self

    def __exit__(self, except_type, except_value, except_table):
        if except_type:
            logger.error(f"{except_type}: {except_value}")
            self._session.rollback()
        else:
            self.commit()
        self._session.close()

    @staticmethod
    def migrate_upgrade(version: str = None):
        """
        Run migrations
        """
        version = "head" if not version else version

        alembic_args = [
            "--raiseerr",
            "upgrade",
            version,
        ]
        alembic.config.main(argv=alembic_args)

    @staticmethod
    def migrate_downgrade(version: str = None):
        """
        Run migrations
        """
        version = "-1" if not version else version

        alembic_args = [
            "--raiseerr",
            "downgrade",
            version,
        ]
        alembic.config.main(argv=alembic_args)

    @staticmethod
    def clear_database(engine=engine_default):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            meta.drop_all(engine, [table], checkfirst=True)
        meta.create_all(engine)
