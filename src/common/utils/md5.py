import hashlib


class Md5Utils:
    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.strip().encode()).hexdigest()
