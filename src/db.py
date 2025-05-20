from contextlib import contextmanager
from typing import Generator, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker


class Database:
    _instance: Optional["Database"] = None
    _engine: Optional[Engine] = None
    _session_factory = None

    @classmethod
    def initialize(
        cls, db_user: str, db_password: str, db_host: str, db_port: str, db_name: str
    ):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._engine = create_engine(
                "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                    db_user,
                    db_password,
                    db_host,
                    db_port,
                    db_name,
                ),
                echo=True,
            )
            cls._session_factory = sessionmaker(bind=cls._engine)

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        return super(Database, cls).__new__(cls)

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
    def session_scope(
        cls, autoflush: bool = True, end_with_commit: bool = True
    ) -> Generator[Session, None, None]:
        session = cls.get_session(autoflush=autoflush)
        try:
            yield session
            if end_with_commit:
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

    @classmethod
    def check_connection(cls) -> Tuple[bool, Optional[str]]:
        if cls._engine is None:
            return False, "O banco de dados não foi inicializado"

        try:
            with cls._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True, None
        except OperationalError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"
