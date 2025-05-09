from typing import List

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from domain.companion.model import Companion
from domain.companion.widget.row_widget import CompanionRowWidget


class CompanionsGroupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.companion_rows: List[CompanionRowWidget] = []
        self.companions: List[Companion] = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.group_box = QGroupBox("Acompanhantes")

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(5, 5, 5, 5)

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Nome"), 5)
        header_layout.addWidget(QLabel("CPF"), 3)
        header_layout.addWidget(QLabel("Telefone"), 3)
        header_layout.addWidget(QLabel(""), 2)
        content_layout.addLayout(header_layout)

        self.companions_layout = QVBoxLayout()
        self.companions_layout.setSpacing(5)
        content_layout.addLayout(self.companions_layout)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        self.add_button = QPushButton("Adicionar Linha")
        self.add_button.setFixedWidth(150)
        self.add_button.clicked.connect(self.add_companion_row)
        add_button_layout.addWidget(self.add_button)
        content_layout.addLayout(add_button_layout)

        self.group_box.setLayout(content_layout)
        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

        self.add_companion_row()

    def add_companion_row(self):
        new_row = CompanionRowWidget(is_removable=len(self.companion_rows) > 0)
        new_row.remove_requested.connect(self.remove_companion_row)
        self.companions_layout.addWidget(new_row)
        self.companion_rows.append(new_row)

        if len(self.companion_rows) > 1 and self.companion_rows[0]:
            self.companion_rows[0].set_removable(True)

    def remove_companion_row(self, row):
        if row in self.companion_rows:
            self.companions_layout.removeWidget(row)
            self.companion_rows.remove(row)
            row.deleteLater()

            if len(self.companion_rows) == 1 and self.companion_rows[0]:
                self.companion_rows[0].set_removable(False)

    def get_companions(self) -> List[Companion]:
        companions = []
        for index, row in enumerate(self.companion_rows):
            companion = row.get_data(index)
            if companion:
                companions.append(companion)
        return companions

    def set_companions(self, companions: List[Companion]):
        for row in self.companion_rows[:]:
            self.companions_layout.removeWidget(row)
            self.companion_rows.remove(row)
            row.deleteLater()

        self.companions = companions

        if not companions:
            self.add_companion_row()
        else:
            for companion in companions:
                self.add_companion_row()
                row = self.companion_rows[-1]
                row.set_data(companion)
