import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from routines.purpose.list.controller import PurposeListController
from settings import Settings

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(Settings.FAV_ICON_FILE_NAME))

purpose_list_controller = PurposeListController()
purpose_list_controller.show()

sys.exit(app.exec())
