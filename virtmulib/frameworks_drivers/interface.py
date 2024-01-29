from abc import ABC, abstractmethod
from attrs import define


@define
class CloudDB:
    @abstractmethod
    def set(self, item: dict, path):
        pass

    @abstractmethod
    def push(self, item: dict, path):
        pass

    @abstractmethod
    def get(self, path):
        pass

    @abstractmethod
    def update(self, item: dict, path):
        pass

    @abstractmethod
    def delete(self, path):
        pass
