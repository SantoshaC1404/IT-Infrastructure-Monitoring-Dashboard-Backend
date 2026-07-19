class WindowsDiscoveryService:

    def __init__(self, connection):

        self.connection = connection

    def discover(self):

        raise NotImplementedError
