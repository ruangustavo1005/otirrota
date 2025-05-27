from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QLabel, QLineEdit

from common.gui.field.boolean_combo_box import BooleanComboBox
from common.gui.field.cpf_line_edit import CPFLineEdit
from common.gui.widget.base_list_widget import BaseListWidget
from domain.driver.model import Driver


class DriverListWidget(BaseListWidget[Driver]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Driver,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        name_label = QLabel("Nome:")
        name_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        name_label.setFixedWidth(40)
        filter_area_layout.addWidget(name_label)

        self.name_filter = QLineEdit()
        self.name_filter.setFixedWidth(100)
        self.name_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.name_filter)

        cpf_label = QLabel("CPF:")
        cpf_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        cpf_label.setFixedWidth(30)
        filter_area_layout.addWidget(cpf_label)

        self.cpf_filter = CPFLineEdit()
        self.cpf_filter.setFixedWidth(120)
        self.cpf_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.cpf_filter)

        registration_number_label = QLabel("Registro:")
        registration_number_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        registration_number_label.setFixedWidth(50)
        filter_area_layout.addWidget(registration_number_label)

        self.registration_number_filter = QLineEdit()
        self.registration_number_filter.setFixedWidth(100)
        self.registration_number_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.registration_number_filter)

        active_label = QLabel("Ativo?")
        active_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        active_label.setFixedWidth(40)
        filter_area_layout.addWidget(active_label)

        self.active_filter = BooleanComboBox()
        self.active_filter.setCurrentIndexByData(True)
        self.active_filter.setFixedWidth(100)
        self.active_filter.currentIndexChanged.connect(self.update_button.click)
        filter_area_layout.addWidget(self.active_filter)

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()
        self.view_button.setVisible(False)
        return layout

    def _configure_table_columns(self, header: QHeaderView) -> None:
        super()._configure_table_columns(header)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1, 100)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 100)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 70)
