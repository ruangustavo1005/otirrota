from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from settings import Settings


class Database:
    _instance: Optional["Database"] = None
    _engine: Optional[Engine] = None
    _session_factory = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._engine = create_engine(
                "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                    Settings.DB_USER,
                    Settings.DB_PASSWORD,
                    Settings.DB_HOST,
                    Settings.DB_PORT,
                    Settings.DB_NAME,
                ),
                echo=True,
            )
            cls._session_factory = sessionmaker(bind=cls._engine)
        return cls._instance

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._instance is None:
            cls()
        return cls._engine

    @classmethod
    def get_session(cls, autoflush: bool = True) -> Session:
        if cls._instance is None:
            cls()
        return cls._session_factory(autoflush=autoflush)

    @classmethod
    @contextmanager
    def session_scope(cls, autoflush: bool = True) -> Generator[Session, None, None]:
        session = cls.get_session(autoflush=autoflush)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def get_session_factory(cls):
        if cls._instance is None:
            cls()
        return cls._session_factory
