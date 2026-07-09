from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class ServerType(str, Enum):
    LINUX = "LINUX"
    WINDOWS = "WINDOWS"


class ServerStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
