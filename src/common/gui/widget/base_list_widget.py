from typing import Generic, Type

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
)

from common.gui.core.table_model_default import TableModelDefault
from common.gui.widget.base_entity_widget import BaseEntityWidget, ModelType


class BaseListWidget(BaseEntityWidget[ModelType], Generic[ModelType]):
    def __init__(
        self,
        model_class: Type[ModelType],
        width: int = 800,
        height: int = 800,
        parent=None,
        flags=Qt.WindowFlags(),
    ):
        super().__init__(
            model_class=model_class,
            title=f"Consulta de {model_class.get_static_description()}",
            width=width,
            height=height,
            parent=parent,
            flags=flags,
        )

    def _init_ui(self) -> None:
        self.base_layout = QVBoxLayout()

        self.filter_area_layout = self._create_filter_area()
        self.base_layout.addLayout(self.filter_area_layout)

        self.actions_area_layout = self._create_actions_area()
        self.disable_row_actions()
        self.base_layout.addLayout(self.actions_area_layout)

        self.table_area_layout = self._create_table_area()
        self.base_layout.addLayout(self.table_area_layout)

        self.pagination_area_layout = self._create_pagination_area()
        self.base_layout.addLayout(self.pagination_area_layout)

        self.setLayout(self.base_layout)

    def _create_filter_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.update_button = QPushButton("Atualizar Consulta")
        self.update_button.setFixedWidth(120)

        self._create_filter_fields(layout)

        button_layout = QHBoxLayout()   
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(self.update_button)

        layout.addLayout(button_layout)

        return layout

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        pass

    def _create_actions_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.add_button = QPushButton("Adicionar")
        self.add_button.setFixedWidth(100)
        layout.addWidget(self.add_button)

        self.change_button = QPushButton("Alterar")
        self.change_button.setFixedWidth(100)
        layout.addWidget(self.change_button)

        self.remove_button = QPushButton("Remover")
        self.remove_button.setFixedWidth(100)
        layout.addWidget(self.remove_button)

        self.view_button = QPushButton("Visualizar")
        self.view_button.setFixedWidth(100)
        layout.addWidget(self.view_button)

        return layout

    def enable_row_actions(self) -> None:
        self.change_button.setDisabled(False)
        self.remove_button.setDisabled(False)
        self.view_button.setDisabled(False)

    def disable_row_actions(self) -> None:
        self.change_button.setDisabled(True)
        self.remove_button.setDisabled(True)
        self.view_button.setDisabled(True)

    def _create_table_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.table_model = self._get_table_model_instance()

        self.table = QTableView()
        self.table.setModel(self.table_model)
        self.table.resizeRowsToContents()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        layout.addWidget(self.table)

        header = self.table.horizontalHeader()
        self._configure_table_columns(header)

        return layout

    def _configure_table_columns(self, header):
        header.setSectionResizeMode(header.ResizeMode.Stretch)
        header.setStretchLastSection(True)

    def _create_pagination_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.first_page_button = QPushButton("<<")
        self.first_page_button.setFixedWidth(30)
        layout.addWidget(self.first_page_button)

        self.before_page_button = QPushButton("<")
        self.before_page_button.setFixedWidth(30)
        layout.addWidget(self.before_page_button)

        self.page_field = QLineEdit()
        self.page_field.setFixedWidth(30)
        self.page_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_field.setValidator(QIntValidator())
        self.page_field.setText("1")
        layout.addWidget(self.page_field)

        bar_label = QLabel("/")
        bar_label.setFixedWidth(5)
        layout.addWidget(bar_label)

        self.last_page_field = QLineEdit()
        self.last_page_field.setFixedWidth(30)
        self.last_page_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_page_field.setDisabled(True)
        layout.addWidget(self.last_page_field)

        self.after_page_button = QPushButton(">")
        self.after_page_button.setFixedWidth(30)
        layout.addWidget(self.after_page_button)

        self.last_page_button = QPushButton(">>")
        self.last_page_button.setFixedWidth(30)
        layout.addWidget(self.last_page_button)

        self.row_count_label = QLabel()
        layout.addWidget(self.row_count_label)

        self.logged_user_label = QLabel("")
        self.logged_user_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.logged_user_label)

        return layout

    def set_page_count(self, page_count: int) -> None:
        self.last_page_field.setText(str(page_count))

    def set_row_count(self, row_count: int, rows_per_page: int) -> None:
        self.row_count_label.setText(
            f"Total de registros: <b>{row_count}</b> ({rows_per_page} por página)"
        )

    def _get_table_model_instance(self) -> TableModelDefault[ModelType]:
        return TableModelDefault(self.model_class)
