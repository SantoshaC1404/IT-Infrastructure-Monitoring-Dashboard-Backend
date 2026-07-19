from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute(self, command: str) -> str:
        pass

    @abstractmethod
    def execute_with_status(self, command: str):
        pass

    # def __enter__(self):
    #     self.connect()
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.close()
