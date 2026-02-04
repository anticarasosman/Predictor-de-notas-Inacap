from abc import ABC, abstractmethod

class Sheet(ABC):

    @abstractmethod
    def add_sheet(self, workbook, data: dict):
        pass