import asyncio
import functools
import typing as t

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout

from services.api import Service
from services.dummy import DummyService
from .service import QServiceList, QServiceView
from .service.service_list import ServiceListModel


class MainWindow(QWidget):
    # GUI
    services_list_widget: QServiceList
    service_view_widget: QServiceView

    # Internal
    services: ServiceListModel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.services = ServiceListModel()
        self.init_ui()
        self.translate()

    def init_ui(self):
        self.setLayout(QHBoxLayout(self))
        self.service_view_widget = QServiceView(self)
        self.services_list_widget = QServiceList(self.services, self)

        self.layout().addWidget(self.services_list_widget)
        self.layout().addWidget(self.service_view_widget)

    def translate(self):
        # noinspection PyTypeChecker
        self.setWindowTitle(self.tr("Messages"))
        self.services_list_widget.translate()
        self.service_view_widget.translate()

    def add_service(self, service: Service):
        self.services.add_service(service)


async def main():
    def close_future(fut, loo):
        loo.call_later(10, fut.cancel)
        fut.cancel("Close Application")

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, 'aboutToQuit'):
        getattr(app, 'aboutToQuit') \
            .connect(functools.partial(close_future, future, loop))

    main_window = MainWindow()
    main_window.add_service(DummyService())
    main_window.add_service(DummyService())
    main_window.add_service(DummyService())
    main_window.show()

    await future

    return True
