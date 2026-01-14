from exceptions.custom_exception import MajorException

class MajorPrioritiesException(MajorException):
    def __init__(self, major_name, categorie):
        self.major_name = major_name
        self.message = f"La carrera '{self.major_name}' no tiene una prioridad válida para ramos de '{categorie}'. Se le asignará prioridad -1 por defecto."