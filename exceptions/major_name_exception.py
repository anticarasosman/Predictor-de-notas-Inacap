from exceptions.custom_exception import MajorException

class MajorNameException(MajorException):
    def __init__(self, major_name):
        self.major_name = major_name
        self.message = f"La carrera '{self.major_name}' no existe en el sistema."