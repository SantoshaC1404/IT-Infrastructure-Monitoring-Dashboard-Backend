from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class DeviceType(str, Enum):
    LINUX_SERVER = "LINUX_SERVER"
    WINDOWS_SERVER = "WINDOWS_SERVER"

    ROUTER = "ROUTER"
    SWITCH = "SWITCH"
    FIREWALL = "FIREWALL"

    STORAGE = "STORAGE"
    NAS = "NAS"
    SAN = "SAN"

    VMWARE = "VMWARE"
    HYPERV = "HYPERV"

    PRINTER = "PRINTER"
    UPS = "UPS"

    DOCKER_HOST = "DOCKER_HOST"
    KUBERNETES_NODE = "KUBERNETES_NODE"


class ConnectionType(Enum):
    SSH = "SSH"
    WINRM = "WINRM"
    SNMP = "SNMP"
    WMI = "WMI"
    REST = "REST"
    HTTPS = "HTTPS"
    REDFISH = "REDFISH"
    TELNET = "TELNET"


class DeviceStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
