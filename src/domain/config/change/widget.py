from typing import Optional
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QDoubleSpinBox,
    QHBoxLayout,
    QWidget,
    QTextBrowser,
    QApplication,
    QMessageBox,
)

from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.config.model import Config


class ConfigChangeWidget(BaseChangeWidget):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Config,
            width=600,
            height=550,
            parent=parent,
        )
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None

    def _create_form_fields(self) -> QLayout:
        layout = QVBoxLayout()

        layout.addWidget(self._create_report_box())
        layout.addWidget(self._create_roadmap_box())

        return layout

    def _create_report_box(self):
        report_table_layout = QFormLayout()

        self.department_name_field = QLineEdit()
        report_table_layout.addRow(
            QLabel("Nome da Secretaria Municipal:"), self.department_name_field
        )

        self.body_name_field = QLineEdit()
        report_table_layout.addRow(
            QLabel("Nome do Órgão Municipal:"), self.body_name_field
        )

        report_box = QGroupBox("Configurações de Relatórios")
        report_box.setLayout(report_table_layout)

        return report_box

    def _create_roadmap_box(self):
        roadmap_table_layout = QFormLayout()

        self.eplison_field = QDoubleSpinBox()
        self.eplison_field.setSingleStep(0.01)
        self.eplison_field.setDecimals(2)
        roadmap_table_layout.addRow(QLabel("Epsilon:"), self.eplison_field)

        self.minpts_field = QSpinBox()
        roadmap_table_layout.addRow(QLabel("Minpts:"), self.minpts_field)

        self.distance_matrix_api_key_field = QLineEdit()
        roadmap_table_layout.addRow(
            QLabel("Chave da Distance Matrix API:"),
            self.distance_matrix_api_key_field,
        )

        coord_container = QWidget()
        coord_layout = QHBoxLayout(coord_container)
        coord_layout.setContentsMargins(0, 0, 0, 0)

        self.departure_coordinates_field = QLineEdit()
        self.departure_coordinates_field.setPlaceholderText("latitude, longitude")
        self.departure_coordinates_field.setDisabled(True)
        coord_layout.addWidget(self.departure_coordinates_field, 1)

        self.paste_button = QPushButton("Colar")
        self.paste_button.clicked.connect(self._paste_coordinates)
        coord_layout.addWidget(self.paste_button)

        roadmap_table_layout.addRow(
            QLabel("Coordenadas do Ponto de Saída:"), coord_container
        )

        self.maps_button = QPushButton("Abrir o Google Maps")
        self.maps_button.clicked.connect(self._open_google_maps)
        roadmap_table_layout.addRow("", self.maps_button)

        instructions = QTextBrowser()
        instructions.setReadOnly(True)
        instructions.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #cccccc;"
        )
        instructions.setOpenExternalLinks(True)

        instructions_html = """
        <div style="font-size: 12px; padding: 5px;">
            <p><b>Como obter coordenadas:</b></p>
            <ol>
                <li>Abra o Google Maps no navegador</li>
                <li>Pesquise o local desejado ou navegue pelo mapa</li>
                <li>Clique com o botão direito do mouse no local desejado</li>
                <li>A primeira opção do menu são as coordenadas do local selecionado</li>
                <li>Clique com o botão esquerdo do mouse para copiar as coordenadas</li>
                <li>Volte aqui e clique em "Colar"</li>
            </ol>
        </div>
        """
        instructions.setHtml(instructions_html)

        roadmap_table_layout.addRow("Instruções:", instructions)

        roadmap_box = QGroupBox("Configurações do Otimizador de Rotas")
        roadmap_box.setLayout(roadmap_table_layout)

        return roadmap_box

    def _paste_coordinates(self) -> None:
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasText():
            text = mime_data.text()
            self.departure_coordinates_field.setText(text)
            self._parse_coordinates(text)

    def _parse_coordinates(self, text: str) -> None:
        text = text.strip()
        coordinates = text.split(",")
        if len(coordinates) == 2:
            lat, lng = coordinates
            if self._are_valid_coordinates(float(lat), float(lng)):
                self._update_coordinates(float(lat), float(lng))
        else:
            QMessageBox.warning(
                self,
                "Formato de coordenadas inválido",
                'O formato de coordenadas deve ser "latitude, longitude".',
            )

    def _are_valid_coordinates(self, lat: float, lng: float) -> bool:
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return True

        QMessageBox.warning(
            self,
            "Coordenadas inválidas",
            "As coordenadas estão fora dos limites válidos. Latitude deve estar entre -90 e 90, e longitude entre -180 e 180.",
        )
        return False

    def _update_coordinates(self, lat: float, lng: float) -> None:
        self.latitude = lat
        self.longitude = lng

    def _open_google_maps(self) -> None:
        if self.latitude and self.longitude:
            url = f"https://www.google.com/maps?q={self.latitude},{self.longitude}&z=18"
        else:
            url = "https://www.google.com/maps"
        QDesktopServices.openUrl(QUrl(url))
