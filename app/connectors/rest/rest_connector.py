from app.connectors.base.base_connector import BaseConnector


class RESTConnector(BaseConnector):

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def execute(self, command: str):
        raise NotImplementedError()

    def execute_with_status(self, command: str):
        raise NotImplementedError()
