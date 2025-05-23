from abc import abstractmethod
from contextlib import contextmanager
from datetime import date, datetime, time
from typing import Any, Dict, Generator, List, Optional, Type, TypeVar

from sqlalchemy import Column, DateTime, Integer, Select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.session import object_session

from common.utils.number import NumberUtils
from db import Database

Base = declarative_base()
T = TypeVar("T", bound="BaseModel")


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, info={"list": False})
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

    def get_combo_box_description(self) -> str:
        return self.get_description()

    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_static_description(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def _get_all_listable_columns(cls) -> List[Column]:
        return cls._get_model_listable_columns() + [cls.created_at, cls.updated_at]

    @classmethod
    def _get_model_listable_columns(cls) -> List[Column]:
        return [
            column
            for column in cls.__table__.columns
            if column.name not in ["id", "created_at", "updated_at"]
            and cls._isnt_column_listable(column)
        ]

    @classmethod
    def _isnt_column_listable(cls, column: Column) -> bool:
        return not (
            hasattr(column, "info")
            and "list" in column.info
            and column.info["list"] is False
        )

    @classmethod
    def get_table_columns(cls) -> List[str]:
        id_column = None
        date_columns = []
        normal_columns = []

        for column in cls._get_all_listable_columns():
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

        for column in self._get_all_listable_columns():
            value = None

            column_name = column.name
            if len(column.foreign_keys) > 0:
                column_name = list(column.foreign_keys)[0].target_fullname.split(".")[0]

            if hasattr(self, column_name):
                value = getattr(self, column_name)
            elif hasattr(self, f"get_{column_name}") and callable(
                getattr(self, f"get_{column_name}")
            ):
                value = getattr(self, f"get_{column_name}")()

            values_dict[column_name] = self.format_value_for_table(value)

        result = []

        if "id" in values_dict:
            result.append(values_dict["id"])
            del values_dict["id"]

        for column in self._get_all_listable_columns():
            column_name = column.name
            if len(column.foreign_keys) > 0:
                column_name = list(column.foreign_keys)[0].target_fullname.split(".")[0]

            if column_name not in ["id", "created_at", "updated_at"]:
                result.append(values_dict[column_name])

        if "created_at" in values_dict:
            result.append(values_dict["created_at"])
        if "updated_at" in values_dict:
            result.append(values_dict["updated_at"])

        return result

    def format_value_for_table(self, value: Any) -> Any:
        if value is None:
            return ""
        if isinstance(value, BaseModel):
            return value.get_description()
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")
        if isinstance(value, date):
            return value.strftime("%d/%m/%Y")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        if isinstance(value, float):
            return NumberUtils.float_to_str(value)
        if isinstance(value, bool):
            return "Sim" if value else "Não"
        return str(value)

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            **{k: v for k, v in data.items() if k in cls.__table__.columns.keys()}
        )

    @classmethod
    def list_for_combo_box(cls, **kwargs: Any) -> List[T]:
        return [record for record in cls.query().order_by(cls.id)]

    @classmethod
    def get_by_id(
        cls: Type[T], id: int, session: Optional[Session] = None
    ) -> Optional[T]:
        if session:
            return session.query(cls).filter(cls.id == id).first()

        with Database.session_scope(end_with_commit=False) as session:
            return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def apply_text_search_filter(cls, query: Select, search_text: str) -> Select:
        raise NotImplementedError()

    @classmethod
    def query(cls) -> Select:
        with Database.session_scope() as session:
            return session.query(cls)

    def save(self, session: Optional[Session] = None) -> None:
        if session:
            session.add(self)
            session.flush()
            return

        with self.__existent_or_new_session() as session_:
            try:
                session_.add(self)
            except Exception as e:
                session_.rollback()
                raise e
            finally:
                session_.commit()

    def delete(self, session: Optional[Session] = None) -> None:
        if session:
            session.delete(self)
            session.flush()
            return

        with self.__existent_or_new_session() as session_:
            try:
                session_.delete(self)
            except Exception as e:
                session_.rollback()
                raise e
            finally:
                session_.commit()

    def update(self, session: Optional[Session] = None, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if session:
            session.add(self)
            session.flush()
            return

        with self.__existent_or_new_session() as session_:
            try:
                session_.add(self)
            except Exception as e:
                session_.rollback()
                raise e
            finally:
                session_.commit()

    @contextmanager
    def __existent_or_new_session(self) -> Generator[Session, None, None]:
        if existing_session := object_session(self):
            yield existing_session
        else:
            with Database.session_scope() as session:
                yield session

    @classmethod
    def create_all(cls):
        Base.metadata.create_all(Database.get_engine())

    @classmethod
    def drop_all(cls):
        Base.metadata.drop_all(Database.get_engine())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseModel):
            return super().__eq__(other)
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(f"{self.__class__.__name__}-{self.id}")
