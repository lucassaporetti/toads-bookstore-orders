import logging
from typing import Any, Generator
import alembic.config
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bookstore_orders.components.config import envs
from bookstore_orders.components.utils.exceptions import UpdateTableException


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


class DataBaseCrud:
    parser: dict = None
    is_active = False
    __table__ = None

    def insert(self, connection: DatabaseService):
        connection.add(self)
        connection.commit()
        return self

    def delete(self, connection: DatabaseService):
        connection.remove(self)
        connection.commit()

    @classmethod
    def list_one(
        cls,
        connection: DatabaseService,
        query_filter: tuple = None,
        order_by: tuple = None,
    ):
        query = connection.query(cls)

        if query_filter:
            query = query.filter(*query_filter)

        if order_by:
            query = (
                query.order_by(asc(getattr(cls, order_by[0])))
                if "asc" in order_by[1]
                else query.order_by(desc(getattr(cls, order_by[0])))
            )

        return query.first()

    @classmethod
    def find_all(
        cls,
        connection: DatabaseService,
        after: int = 0,
        limit: int = 100,
        is_active: Any = True,
    ) -> Generator:
        query = connection.query(cls)

        if "is_active" in dir(cls) and is_active != "all":
            query = query.filter(*(cls.is_active == is_active,))

        yield from query.offset(after).limit(limit)

    @classmethod
    def search(
        cls,
        connection: DatabaseService,
        query_filter: tuple = None,
        after: int = 0,
        limit: int = 100,
        is_active: Any = True,
        order_by: tuple = None,
    ) -> Generator:
        query = connection.query(cls)

        if "is_active" in dir(cls) and is_active != "all":
            query_filter = (*query_filter, cls.is_active == is_active)

        if query_filter:
            query = query.filter(*query_filter)

        if order_by:
            query = (
                query.order_by(asc(getattr(cls, order_by[0])))
                if "asc" in order_by[1]
                else query.order_by(desc(getattr(cls, order_by[0])))
            )

        if after != -1:
            query = query.offset(after).limit(limit)

        yield from query

    @classmethod
    def update(
        cls,
        connection: DatabaseService,
        query_filter: tuple,
        data: dict,
    ) -> list[Any]:
        updated_list = []
        for register in cls.search(
            connection, query_filter=query_filter, after=-1, is_active="all"
        ):
            for column, value in data.items():
                try:
                    getattr(register, column)
                    setattr(register, column, value)
                except AttributeError as update_attribute_exception:
                    raise UpdateTableException(
                        404, f"Coluna {column} não encontrada na tabela {register}"
                    ) from update_attribute_exception
            updated_list.append(register)

        connection.commit()

        return updated_list

    @classmethod
    def join(cls, connection: DatabaseService, table: "DataBaseCrud"):
        return connection.query(cls).join(table)
