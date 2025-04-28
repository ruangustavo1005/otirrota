import os
from typing import Optional

from dotenv import load_dotenv

from domain.user.model import User

load_dotenv()


class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    FAV_ICON_FILE_NAME = "src/fav.ico"

    __logged_user: Optional[User] = None

    @classmethod
    def set_logged_user(cls, user: User) -> None:
        cls.__logged_user = user

    @classmethod
    def get_logged_user(cls) -> Optional[User]:
        return cls.__logged_user
