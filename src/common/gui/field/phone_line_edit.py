from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit


class PhoneLineEdit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMaxLength(15)
        self.setPlaceholderText("(00) 00000-0000")

        regex = QRegularExpression(r"[0-9\.\-]*")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)

        self.textEdited.connect(self._format_phone)

    def _format_phone(self, text: str) -> None:
        cursor_pos = self.cursorPosition()
        clean_text = "".join(filter(str.isdigit, text))
        formatted_text = ""

        if len(clean_text) > 11:
            clean_text = clean_text[:11]

        if len(clean_text) > 0:
            formatted_text = "(" + clean_text[:2]
            if len(clean_text) > 2:
                formatted_text += ") " + clean_text[2:7]
                if len(clean_text) > 7:
                    formatted_text += "-" + clean_text[7:11]

        if formatted_text != text:
            new_pos = cursor_pos

            if cursor_pos > 0:
                new_pos += 1
            if cursor_pos > 3:
                new_pos += 2
            if cursor_pos > 8:
                new_pos += 1

            self.blockSignals(True)
            self.setText(formatted_text)
            self.setCursorPosition(min(new_pos, len(formatted_text)))
            self.blockSignals(False)

    def get_phone_number(self) -> str:
        return "".join(filter(str.isdigit, self.text()))

    def is_valid_phone(self) -> bool:
        return len(self.get_phone_number()) == 11
