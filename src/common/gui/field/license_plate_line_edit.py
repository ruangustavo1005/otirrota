from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit


class LicensePlateLineEdit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMaxLength(8)
        self.setPlaceholderText("ABC-1D23")

        # Allow only valid characters for each position
        regex = QRegularExpression(r"[A-Za-z]{0,3}[0-9]{0,1}[A-Za-z0-9]{0,1}[0-9]{0,2}")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)

        self.textEdited.connect(self._format_license_plate)

    def _format_license_plate(self, text: str) -> None:
        self.setText(text.upper())
        cursor_pos = self.cursorPosition()

        # Remove any non-alphanumeric characters
        clean_text = "".join(c for c in text if c.isalnum())
        formatted_text = ""

        if len(clean_text) > 7:
            clean_text = clean_text[:7]

        # Apply the format constraints
        current_len = len(clean_text)
        valid_text = ""

        # First 3 characters must be letters
        for i in range(min(3, current_len)):
            if clean_text[i].isalpha():
                valid_text += clean_text[i]

        # Character 4 must be a number
        if current_len > 3:
            if clean_text[3].isdigit():
                valid_text += clean_text[3]

        # Character 5 can be alphanumeric
        if current_len > 4:
            valid_text += clean_text[4]

        # Characters 6-7 must be numbers
        if current_len > 5:
            for i in range(5, min(7, current_len)):
                if clean_text[i].isdigit():
                    valid_text += clean_text[i]

        # Format with hyphen
        if len(valid_text) > 0:
            formatted_text = valid_text[:3]
            if len(valid_text) > 3:
                formatted_text += "-" + valid_text[3:]

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
        if len(license_plate) != 7:
            return False

        # Check format: 3 letters + 1 number + 1 alphanumeric + 2 numbers
        return (
            all(c.isalpha() for c in license_plate[:3])
            and license_plate[3].isdigit()
            and license_plate[4].isalnum()
            and all(c.isdigit() for c in license_plate[5:7])
        )
