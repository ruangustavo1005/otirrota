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
from domain.config.model import Config
from domain.roadmap.model import Roadmap
from settings import Settings


class VehicleUseAuthorizationReportController(BaseEntityController[Roadmap]):
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
        config = Config.get_config()
        data["department_name"] = config.department_name
        data["body_name"] = config.body_name
        data["issuer"] = Settings.get_logged_user().get_description()
        with Database.get_session() as session:
            roadmap = (
                session.query(Roadmap)
                .filter(Roadmap.id == self._entity.id)
                .options(joinedload(Roadmap.schedulings))
                .first()
            )
            if roadmap:
                data["vehicle"] = roadmap.vehicle.get_description()
                data["driver_name"] = roadmap.driver.name
                data["driver_registration_number"] = roadmap.driver.registration_number
                data["departure"] = roadmap.departure.strftime("%d/%m/%Y %H:%M")
                data["arrival"] = roadmap.arrival.strftime("%d/%m/%Y %H:%M")
                data["passangers"] = []
                for scheduling in roadmap.schedulings:
                    if scheduling.patient:
                        patient_data = {}
                        patient_data["description"] = "%s, inscrito com o CPF %s" % (
                            scheduling.patient.name,
                            scheduling.patient.format_cpf() or "",
                        )
                        data["passangers"].append(patient_data)
                        if scheduling.companions:
                            for companion in scheduling.companions:
                                companion_data = {}
                                companion_data["description"] = companion.name
                                if companion.cpf:
                                    companion_data["description"] += ", inscrito com o CPF %s" % (
                                        companion.format_cpf() or "",
                                    )
                                data["passangers"].append(companion_data)
        return data

    def __get_report_file_name(self):
        return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_autorizacao_para_uso_de_veiculo_{self._entity.id}.pdf"
