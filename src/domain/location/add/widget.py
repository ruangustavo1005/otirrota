from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QApplication,
    QTextBrowser,
)
from PySide6.QtGui import QDesktopServices

from common.gui.widget.base_add_widget import BaseAddWidget
from domain.location.model import Location


class LocationAddWidget(BaseAddWidget):
    def __init__(self, parent=None) -> None:
        self.latitude = -26.96227520245754
        self.longitude = -49.62312637117852

        super().__init__(
            model_class=Location,
            width=600,
            height=300,
            parent=parent,
        )

    def _create_form_fields(self) -> QFormLayout:
        form_layout = QFormLayout()

        self.description_field = QLineEdit()
        form_layout.addRow(QLabel("Descrição:"), self.description_field)

        coord_container = QWidget()
        coord_layout = QHBoxLayout(coord_container)
        coord_layout.setContentsMargins(0, 0, 0, 0)

        self.coordinates_field = QLineEdit()
        self.coordinates_field.setPlaceholderText("latitude, longitude")
        self.coordinates_field.setDisabled(True)
        coord_layout.addWidget(self.coordinates_field, 1)

        self.paste_button = QPushButton("Colar")
        self.paste_button.clicked.connect(self._paste_coordinates)
        coord_layout.addWidget(self.paste_button)

        form_layout.addRow(QLabel("Coordenadas:"), coord_container)

        self.maps_button = QPushButton("Abrir o Google Maps")
        self.maps_button.clicked.connect(self._open_google_maps)
        form_layout.addRow("", self.maps_button)

        instructions = QTextBrowser()
        instructions.setReadOnly(True)
        instructions.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #cccccc;"
        )
        instructions.setOpenExternalLinks(True)

        instructions_html = f"""
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

        form_layout.addRow("Instruções:", instructions)

        return form_layout

    def _paste_coordinates(self) -> None:
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasText():
            text = mime_data.text()
            self.coordinates_field.setText(text)
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
        url = f"https://www.google.com/maps/@{self.latitude},{self.longitude},15z"
        QDesktopServices.openUrl(QUrl(url))
