from typing import Any, Dict, Optional, Type

from sqlalchemy.orm import Session

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from db import Database
from domain.companion.model import Companion
from domain.scheduling.change.widget import SchedulingChangeWidget
from domain.scheduling.model import Scheduling
from PySide6.QtCore import QDateTime, QDate, QTime


class SchedulingChangeController(BaseChangeController[Scheduling]):
    _widget: SchedulingChangeWidget

    def _populate_form(self, entity: Scheduling) -> None:
        self._widget.datetime_field.setDateTime(
            QDateTime(
                QDate(entity.datetime.year, entity.datetime.month, entity.datetime.day),
                QTime(entity.datetime.hour, entity.datetime.minute, entity.datetime.second),
            )
        )
        self._widget.average_duration_field.setTime(
            QTime(
                entity.average_duration.hour,
                entity.average_duration.minute,
                entity.average_duration.second,
            )
        )
        self._widget.patient_field.set_selected_model(entity.patient)
        self._widget.location_field.set_selected_model(entity.location)
        self._widget.purpose_field.setCurrentIndexByData(entity.purpose)
        self._widget.sensitive_patient_checkbox.setChecked(entity.sensitive_patient)
        self._widget.description_field.setText(entity.description)
        self._widget.companions_widget.set_companions(entity.companions)

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        location = self._widget.location_field.get_selected_model()
        if not location:
            self._widget.show_info_pop_up("Atenção", "Selecione uma localização")
            return None

        patient = self._widget.patient_field.get_selected_model()
        if not patient:
            self._widget.show_info_pop_up("Atenção", "Selecione um paciente")
            return None

        purpose = self._widget.purpose_field.get_current_data()
        if not purpose:
            self._widget.show_info_pop_up("Atenção", "Selecione uma finalidade")
            return None

        return {
            "datetime": self._widget.datetime_field.dateTime().toPython().replace(second=0, microsecond=0),
            "average_duration": self._widget.average_duration_field.time().toPython(),
            "sensitive_patient": self._widget.sensitive_patient_checkbox.isChecked(),
            "description": self._widget.description_field.toPlainText().strip(),
            "location_id": location.id,
            "purpose_id": purpose.id,
            "patient_id": patient.id,
        }

    def _change(self) -> bool:
        with Database.session_scope() as session:
            try:
                if updates := self._get_model_updates():
                    scheduling = Scheduling.get_by_id(self._entity_id, session=session)
                    scheduling.update(session=session, **updates)
                    self._update_companions(session)
                    session.commit()
                    self._widget.show_info_pop_up(
                        "Sucesso",
                        f"{self._model_class.get_static_description()} alterado(a) com sucesso",
                    )
                    self._widget.close()
                    return True
            except Exception as e:
                self._handle_change_exception(e)
                session.rollback()
                return False

    def _update_companions(self, session: Session) -> None:
        companion_ids = []
        for companion in self._widget.companions_widget.get_companions():
            if companion.id is None:
                companion.scheduling_id = self._entity_id
                companion.save(session)
                session.flush()
            else:
                Companion.get_by_id(companion.id, session=session).update(
                    session=session,
                    name=companion.name,
                    cpf=companion.cpf,
                    phone=companion.phone,
                )
            companion_ids.append(companion.id)
        session.query(Companion).filter(
            Companion.scheduling_id == self._entity_id,
            Companion.id.notin_(companion_ids),
        ).delete()

    def _get_widget_instance(self) -> BaseChangeWidget:
        return SchedulingChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Scheduling
