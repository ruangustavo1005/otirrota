class CurrencyUtils:
    @classmethod
    def float_to_view(cls, value: float) -> str:
        return "R$ {:.2f}".format(value).replace(".", ",")
