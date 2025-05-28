from datetime import datetime
import os
from typing import Any, Dict
from sqlalchemy.orm import joinedload
from PySide6.QtWidgets import QMessageBox
from common.controller.base_entity_controller import BaseEntityController
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_entity_widget import BaseEntityWidget
from common.gui.widget.base_widget import BaseWidget
from common.utils.pdf_report import PDFReport
from db import Database
from domain.roadmap.model import Roadmap


class TrafficReportController(BaseEntityController[Roadmap]):
    def __init__(
        self, entity: Roadmap, caller: BaseListController | None = None
    ) -> None:
        super().__init__(caller)
        self._entity = entity
        self._pdf_report = PDFReport(
            template_path=os.path.join(os.path.dirname(__file__), "template.html")
        )

    def _get_widget_instance(self) -> BaseEntityWidget[Roadmap]:
        return None

    def _get_model_class(self) -> Roadmap:
        return Roadmap

    def generate_report(self) -> None:
        success, output_filepath = self._pdf_report.render_and_save(
            data=self.__get_report_data(),
            output_filename=self.__get_report_file_name(),
        )
        if success:
            option = BaseWidget.show_question_pop_up(
                "Relatório gerado com sucesso",
                "Deseja abrir o relatório?",
            )
            if option == QMessageBox.StandardButton.Ok:
                os.startfile(output_filepath)
        else:
            BaseWidget.show_error_pop_up(
                "Erro ao gerar relatório", "Entre em contato com o suporte"
            )

    def __get_report_data(self) -> Dict[str, Any]:
        data = {}
        with Database.get_session() as session:
            roadmap = (
                session.query(Roadmap)
                .filter(Roadmap.id == self._entity.id)
                .options(joinedload(Roadmap.schedulings))
                .first()
            )
            if roadmap:
                data["vehicle"] = roadmap.vehicle.get_description()
                data["driver"] = "%s - %s" % (
                    roadmap.driver.registration_number,
                    roadmap.driver.get_description(),
                )
                data["date"] = roadmap.departure.strftime("%d/%m/%Y")
                data["departure"] = roadmap.departure.strftime("%H:%M")
                data["arrival"] = roadmap.arrival.strftime("%H:%M")
                data["schedulings"] = []
                for scheduling in roadmap.schedulings:
                    sheduling_data = {}
                    sheduling_data["datetime"] = scheduling.datetime.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    sheduling_data["average_duration"] = scheduling.average_duration
                    sheduling_data["location"] = scheduling.location.get_description()
                    sheduling_data["purpose"] = scheduling.purpose.get_description()
                    sheduling_data["description"] = scheduling.description
                    sheduling_data["passengers"] = []
                    if scheduling.patient:
                        patient_data = {}
                        patient_data["name"] = scheduling.patient.name
                        patient_data["cpf"] = scheduling.patient.format_cpf()
                        patient_data["phone"] = scheduling.patient.format_phone()
                        sheduling_data["passengers"].append(patient_data)
                        if scheduling.companions:
                            for companion in scheduling.companions:
                                companion_data = {}
                                companion_data["name"] = companion.name
                                companion_data["cpf"] = companion.format_cpf()
                                companion_data["phone"] = companion.format_phone()
                                sheduling_data["passengers"].append(companion_data)
                    data["schedulings"].append(sheduling_data)
        return data

    def __get_report_file_name(self):
        return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_relatorio_de_trafego_{self._entity.id}.pdf"
