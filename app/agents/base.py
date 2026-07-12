from abc import ABC, abstractmethod


class MonitoringAgent(ABC):

    @abstractmethod
    def get_cpu(self):
        pass

    @abstractmethod
    def get_memory(self):
        pass

    @abstractmethod
    def get_disk(self):
        pass

    @abstractmethod
    def get_system(self):
        pass

    @abstractmethod
    def get_network(self):
        pass
