import inspect
import traceback
import typing as t

from PySide6.QtCore import Signal, QAbstractItemModel, QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTreeView, QTreeWidget

from services.api import Server, Service


class RootItem(QStandardItem):
    services: t.List['ServiceItem']

    def __init__(self, services: t.Optional[t.List[Service]] = None, parent=None):
        
        super().__init__(parent)
        self.services = []
        if services is not None:
            for service in services:
                self.add_service(service)

    def add_service(self, service: Service):
        
        self.services.append(ServiceItem(service, self))

    def child(self, row: int, column: int = 0) -> QStandardItem:
        
        try:
            return self.services[row]
        except IndexError:
            return None

    def data(self, role: int = 0) -> t.Any:
        
        return None

    def row(self):
        
        return 0


class ServiceItem(QStandardItem):
    service: Service
    servers: t.List['ServerItem']

    def __init__(self, service: Service, parent=None):
        
        super().__init__(parent)
        self.service = service
        self.servers = []
        for server in service.servers:
            self.add_server(server)

    def add_server(self, server: Server):
        
        self.servers.append(ServerItem(server))

    def child(self, row: int, column: int = 0) -> QStandardItem:
        
        try:
            return self.servers[row]
        except IndexError:
            return None

    def data(self, role: int = Qt.UserRole + 1) -> t.Any:
        
        if role == Qt.DisplayRole:
            return self.service.name
        return None

    def row(self) -> int:
        
        return self.parent().services.index(self)


class ServerItem(QStandardItem):
    server: Server

    def __init__(self, server: Server, parent=None):
        
        super().__init__(parent)
        self.server = server

    def child(self, row: int, column: int = 0) -> QStandardItem:
        
        return None

    def data(self, role: int = Qt.UserRole + 1) -> t.Any:
        
        if role == Qt.DisplayRole:
            return self.server.name
        return None

    def row(self) -> int:
        
        return self.parent().servers.index(self)


class ServiceListModel(QAbstractItemModel):
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.rootItem = RootItem()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        
        return 1

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        
        return 1

    def data(self, index: QModelIndex, role: int = Qt.UserRole + 1) -> t.Any:
        
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def add_service(self, service: Service):
        
        self.rootItem.add_service(service)


class QServiceList(QWidget):
    server_changed = Signal(Server)

    # GUI
    tree: QTreeWidget
    services: ServiceListModel

    def __init__(self, services, parent=None):
        
        super().__init__(parent)
        self.services = services
        self.init_ui()
        self.translate()

    def init_ui(self):
        
        self.setLayout(QHBoxLayout())
        self.tree = QTreeView(self)
        self.tree.setModel(self.services)
        # self.tree.setHeaderHidden(True)
        self.layout().addWidget(self.tree)

    def translate(self):
        
        pass
