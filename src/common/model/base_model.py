from abc import abstractmethod
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional, Type, TypeVar, Union

from sqlalchemy import Column, DateTime, Integer, Select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.session import object_session
from sqlalchemy.sql.expression import ClauseElement

from common.utils.number_utils import NumberUtils
from db import Database

Base = declarative_base()
T = TypeVar("T", bound="BaseModel")


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, info={"title": "ID"})
    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False,
        info={"title": "Data de Criação"},
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        info={"title": "Última Atualização"},
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @abstractmethod
    def get_combo_box_description(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_static_description(cls) -> str:
        pass

    @classmethod
    def _get_listable_columns(cls) -> List[Column]:
        return [
            column
            for column in cls.__table__.columns
            if not (
                hasattr(column, "info")
                and "list" in column.info
                and column.info["list"] is False
            )
        ]

    @classmethod
    def get_table_columns(cls) -> List[str]:
        id_column = None
        date_columns = []
        normal_columns = []

        for column in cls._get_listable_columns():
            if hasattr(column, "info") and "title" in column.info:
                title = column.info["title"]
            else:
                title = column.name.replace("_", " ").title()

            if column.name == "id":
                id_column = title
            elif column.name in ["created_at", "updated_at"]:
                date_columns.append(title)
            else:
                normal_columns.append(title)

        result = []
        if id_column:
            result.append(id_column)
        result.extend(normal_columns)
        result.extend(date_columns)

        return result

    def format_for_table(self) -> List[Any]:
        values_dict = {}

        for column in self._get_listable_columns():
            value = getattr(self, column.name)

            if isinstance(value, datetime):
                value = value.strftime("%d/%m/%Y %H:%M")
            elif isinstance(value, float):
                value = NumberUtils.float_to_str(value)
            elif isinstance(value, bool):
                value = "Sim" if value else "Não"
            elif isinstance(value, int):
                value = str(value)
            elif isinstance(value, BaseModel):
                value = value.get_description()

            values_dict[column.name] = value

        result = []

        if "id" in values_dict:
            result.append(values_dict["id"])
            del values_dict["id"]

        for column in self._get_listable_columns():
            if column.name not in ["id", "created_at", "updated_at"]:
                result.append(values_dict[column.name])

        if "created_at" in values_dict:
            result.append(values_dict["created_at"])
        if "updated_at" in values_dict:
            result.append(values_dict["updated_at"])

        return result

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            **{k: v for k, v in data.items() if k in cls.__table__.columns.keys()}
        )

    @classmethod
    def list_for_combo_box(cls) -> List[Dict[str, Any]]:
        records = cls.query().order_by(cls.id)

        return [
            {"id": record.id, "description": record.get_combo_box_description()}
            for record in records
        ]

    @classmethod
    def get_by_id(
        cls: Type[T], id: int, session: Optional[Session] = None
    ) -> Optional[T]:
        if session:
            return session.query(cls).filter(cls.id == id).first()

        with Database.session_scope() as session:
            return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def query(cls) -> Select:
        with Database.session_scope() as session:
            return session.query(cls)

    def save(self, session: Optional[Session] = None) -> None:
        if session:
            session.add(self)
            return

        with self.__existent_or_new_session() as session_:
            session_.add(self)

    def delete(self, session: Optional[Session] = None) -> None:
        if session:
            session.delete(self)
            return

        with self.__existent_or_new_session() as session_:
            session_.delete(self)

    def update(self, session: Optional[Session] = None, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if session:
            return

        with self.__existent_or_new_session() as session_:
            session_.add(self)

    @contextmanager
    def __existent_or_new_session(self) -> Generator[Session, None, None]:
        if existing_session := object_session(self):
            yield existing_session
            existing_session.commit()
        else:
            with Database.session_scope() as session:
                yield session

    @classmethod
    def create_all(cls):
        Base.metadata.create_all(Database.get_engine())

    @classmethod
    def drop_all(cls):
        Base.metadata.drop_all(Database.get_engine())
