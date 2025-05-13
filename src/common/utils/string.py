from typing import Optional


class StringUtils:
    @classmethod
    def format_cpf(cls, cpf: str) -> Optional[str]:
        if cls.is_valid_cpf(cpf):
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return None

    @classmethod
    def is_valid_cpf(cls, cpf: str) -> bool:
        cpf = cpf.replace(".", "").replace("-", "")

        if len(cpf) != 11:
            return False

        if len(set(cpf)) == 1:
            return False

        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)

        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto

        if digito1 != int(cpf[9]):
            return False

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)

        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto

        return digito2 == int(cpf[10])

    @classmethod
    def format_phone(cls, phone: str) -> Optional[str]:
        if cls.is_valid_phone(phone):
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        return None

    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        phone = (
            phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        )
        return len(phone) == 11 and phone.isdigit()

    @classmethod
    def format_license_plate(cls, license_plate: str) -> Optional[str]:
        if cls.is_valid_license_plate(license_plate):
            return f"{license_plate[:3]}-{license_plate[3:]}"
        return None

    @classmethod
    def is_valid_license_plate(cls, license_plate: str) -> bool:
        license_plate = license_plate.replace("-", "")
        if len(license_plate) != 7:
            return False

        return (
            all(c.isalpha() for c in license_plate[:3])
            and license_plate[3].isdigit()
            and license_plate[4].isalnum()
            and all(c.isdigit() for c in license_plate[5:7])
        )
