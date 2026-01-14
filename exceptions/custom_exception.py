from abc import ABC, abstractmethod

class MajorException(ABC, Exception):
    @property
    @abstractmethod
    def message(self):
        #Subclases deben implementar su propio mensaje
        pass
    
    def printErrorMessage(self):
        print(self.message)