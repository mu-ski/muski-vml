from abc import ABC, abstractmethod
from attrs import define

@define
class CloudDB:

    @abstractmethod
    def create(self, item: dict):
        pass

    @abstractmethod
    def read(self, item: dict):
        pass

    @abstractmethod
    def update(self, item: dict):
        pass

    @abstractmethod
    def delete(self, item: dict):
        pass
