import typing as t


class User:
    name: str

    def __init__(self, name):
        self.name = name


class Message:
    author: User
    text: str

    def __init__(self, author: User, text: str):
        self.author = author
        self.text = text


class Channel:
    name: str
    messages: t.List[Message]

    def __init__(self, name: str, messages: t.Optional[t.List[Message]] = None):
        self.name = name
        self.messages = []
        if messages is not None:
            self.messages.extend(messages)


class Server:
    name: str
    users: t.List[User]
    channels: t.List[Channel]

    def __init__(self, name: str, users: t.Optional[t.List[User]] = None, channels: t.Optional[t.List[Channel]] = None):
        self.name = name
        self.users = []
        if users is not None:
            self.users.extend(users)
        self.channels = []
        if channels is not None:
            self.channels.extend(channels)


class Service:
    name: str
    servers: t.List[Server]

    def __init__(self, servers: t.Optional[t.List[Server]] = None):
        self.servers = []
        if servers is not None:
            self.servers.extend(servers)
