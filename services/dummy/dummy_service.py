from services.api import Service, Server, User, Message, Channel



class DummyChannel(Channel):
    pass


class DummyMessage(Message):
    pass


class DummyUser(User):
    pass


class DummyServer(Server):
    pass


class DummyService(Service):
    name = "Dummy"
    def __init__(self):
        super().__init__()
        common_users = []
        for i in range(20):
            common_users.append(DummyUser(f"Common user {i}"))
        for i in range(10):
            channels = []
            for j in range(20):
                channels.append(DummyChannel(f"Channel {i}/{j}"))
            users = []
            for j in range(50):
                users.append(DummyUser("Server user {i}/{j}"))
            self.servers.append(DummyServer(f"Server {i}", common_users + users, channels))

