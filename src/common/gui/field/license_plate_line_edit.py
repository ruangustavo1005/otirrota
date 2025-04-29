from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit


class LicensePlateLineEdit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMaxLength(8)
        self.setPlaceholderText("ABC-1D23")

        regex = QRegularExpression(r"[A-Za-z0-9\-]*")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)

        self.textEdited.connect(self._format_license_plate)

    def _format_license_plate(self, text: str) -> None:
        self.setText(text.upper())
        cursor_pos = self.cursorPosition()
        clean_text = "".join(c for c in text if c.isalnum())
        formatted_text = ""

        if len(clean_text) > 7:
            clean_text = clean_text[:7]

        if len(clean_text) > 0:
            formatted_text = clean_text[:3]
            if len(clean_text) > 3:
                formatted_text += "-" + clean_text[3:4]
                if len(clean_text) > 4:
                    formatted_text += clean_text[4:7]

        if formatted_text != text:
            new_pos = cursor_pos

            if cursor_pos > 3:
                new_pos += 1

            self.blockSignals(True)
            self.setText(formatted_text.upper())
            self.setCursorPosition(min(new_pos, len(formatted_text)))
            self.blockSignals(False)

    def get_license_plate_alphanumeric(self) -> str:
        return "".join(filter(str.isalnum, self.text()))

    def is_valid_license_plate(self) -> bool:
        license_plate = self.get_license_plate_alphanumeric()
        return len(license_plate) == 7
