from PySide6.QtCore import QTime
from PySide6.QtWidgets import QTimeEdit


class TimeEdit(QTimeEdit):
    def __init__(self, parent=None, step_minutes=30):
        super().__init__(parent)
        self.step_minutes = step_minutes

    def stepBy(self, steps):
        current_time = self.time()
        h = current_time.hour()
        m = current_time.minute()

        # Calcular novos minutos baseado no step_minutes
        new_minutes = m + steps * self.step_minutes

        # Ajustar horas e minutos
        extra_hours = new_minutes // 60
        new_minutes = new_minutes % 60
        new_hours = (h + extra_hours) % 24

        # Não permitir valores negativos
        if new_minutes < 0:
            new_minutes += 60
            new_hours -= 1
        if new_hours < 0:
            new_hours += 24

        # Definir o novo tempo
        self.setTime(QTime(new_hours, new_minutes))
