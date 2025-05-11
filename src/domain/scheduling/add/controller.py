from typing import Optional, Type

from sqlalchemy.orm import Session

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from db import Database
from domain.location.add.controller import LocationAddController
from domain.location.model import Location
from domain.patient.add.controller import PatientAddController
from domain.patient.model import Patient
from domain.scheduling.add.widget import SchedulingAddWidget
from domain.scheduling.model import Scheduling


class SchedulingAddController(BaseAddController[Scheduling]):
    _widget: SchedulingAddWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_add_action: Optional[str] = None

    def _get_populated_model(self) -> Optional[Scheduling]:
        datetime = (
            self._widget.datetime_field.dateTime()
            .toPython()
            .replace(second=0, microsecond=0)
        )
        if datetime < datetime.now():
            self._widget.show_info_pop_up(
                "Atenção",
                "A data e hora do agendamento tem que ser maior que a data e hora atual",
            )
            return None

        location = self._widget.location_field.get_selected_model()
        if not location:
            self._widget.show_info_pop_up("Atenção", "Selecione uma localização")
            return None

        purpose = self._widget.purpose_field.get_current_data()
        if not purpose:
            self._widget.show_info_pop_up("Atenção", "Selecione uma finalidade")
            return None

        patient = self._widget.patient_field.get_selected_model()
        return Scheduling(
            datetime=datetime,
            location_id=location.id,
            purpose_id=purpose.id,
            average_duration=self._widget.average_duration_field.time().toPython(),
            patient_id=patient.id if patient else None,
            sensitive_patient=self._widget.sensitive_patient_checkbox.isChecked() if patient else None,
            description=self._widget.description_field.toPlainText().strip(),
        )

    def _save(self) -> bool:
        with Database.session_scope() as session:
            try:
                if model := self._get_populated_model():
                    model.save(session)
                    session.flush()
                    self.save_companions(model, session)
                    self._widget.show_info_pop_up(
                        "Sucesso",
                        f"{self._model_class.get_static_description()} criado(a) com sucesso",
                    )
                    self._widget.close()
                    return True
            except ValueError as e:
                self._widget.show_info_pop_up("Atenção", str(e))
                session.rollback()
                return False
            except Exception as e:
                self._handle_add_exception(e)
                session.rollback()
                return False

    def save_companions(self, scheduling: Scheduling, session: Session) -> None:
        companions = self._widget.companions_widget.get_companions()
        for companion in companions:
            companion.scheduling_id = scheduling.id
            companion.save(session)

    def _get_widget_instance(self) -> BaseAddWidget:
        return SchedulingAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Scheduling

    def show(self) -> None:
        self._widget.add_patient_button.clicked.connect(self._on_add_patient_clicked)
        self._widget.add_location_button.clicked.connect(self._on_add_location_clicked)
        super().show()

    def _on_add_patient_clicked(self) -> None:
        self._patient_add_controller = PatientAddController(self)
        self._last_add_action = "patient"
        self._patient_add_controller.show()

    def _on_add_location_clicked(self) -> None:
        self._location_add_controller = LocationAddController(self)
        self._last_add_action = "location"
        self._location_add_controller.show()

    def callee_finalized(self) -> None:
        if self._last_add_action == "patient":
            self._widget.patient_field.set_selected_model(
                Patient.query().order_by(Patient.id.desc()).first()
            )
        elif self._last_add_action == "location":
            self._widget.location_field.set_selected_model(
                Location.query().order_by(Location.id.desc()).first()
            )
