from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit

from common.utils.string import StringUtils


class CPFLineEdit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMaxLength(14)
        self.setPlaceholderText("000.000.000-00")

        regex = QRegularExpression(r"[0-9\.\-]*")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)

        self.textEdited.connect(self._format_cpf)

    def _format_cpf(self, text: str) -> None:
        cursor_pos = self.cursorPosition()
        clean_text = "".join(filter(str.isdigit, text))
        formatted_text = ""

        if len(clean_text) > 11:
            clean_text = clean_text[:11]

        if len(clean_text) > 0:
            formatted_text = clean_text[:3]
            if len(clean_text) > 3:
                formatted_text += "." + clean_text[3:6]
                if len(clean_text) > 6:
                    formatted_text += "." + clean_text[6:9]
                    if len(clean_text) > 9:
                        formatted_text += "-" + clean_text[9:11]

        if formatted_text != text:
            new_pos = cursor_pos

            if cursor_pos > 3:
                new_pos += 1
            if cursor_pos > 7:
                new_pos += 1
            if cursor_pos > 11:
                new_pos += 1

            self.blockSignals(True)
            self.setText(formatted_text)
            self.setCursorPosition(min(new_pos, len(formatted_text)))
            self.blockSignals(False)

    def get_cpf_numbers(self) -> str:
        return "".join(filter(str.isdigit, self.text()))

    def is_valid_cpf(self) -> bool:
        return StringUtils.is_valid_cpf(self.get_cpf_numbers())
