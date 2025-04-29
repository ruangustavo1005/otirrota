class StringUtils:
    @classmethod
    def format_cpf(cls, cpf: str) -> str:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @classmethod
    def format_phone(cls, phone: str) -> str:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"

    @classmethod
    def format_license_plate(cls, license_plate: str) -> str:
        return f"{license_plate[:3]}-{license_plate[3:]}"
