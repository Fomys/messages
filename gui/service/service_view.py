from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QListView


class QServiceView(QWidget):
    service = property()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = None
        self.init_ui()
        self.translate()

    def init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QListView())

    def translate(self):
        pass

    def update_service(self):
        pass

    @service.setter
    def service(self, value):
        self._service = value
