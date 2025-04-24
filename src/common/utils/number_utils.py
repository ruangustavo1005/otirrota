class NumberUtils():
    @classmethod
    def float_to_str(cls, value: float) -> str:
        return str(value).replace('.', ',')

    @classmethod
    def str_to_float(cls, value: str) -> float:
        return float(value.replace(',', '.'))
