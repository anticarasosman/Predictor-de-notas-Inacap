from exceptions.major_name_exception import MajorNameException
from exceptions.major_priorities_exception import MajorPrioritiesException


class Major:
    def __init__(self, name, math_priority = -1, language_priority = -1, english_priority = -1):
        if not isinstance(name, str) or not name.strip():
            raise MajorNameException(name)
        
        self.name = name
        self.math_priority = math_priority
        self.language_priority = language_priority
        self.english_priority = english_priority
    
    def set_priority(self, priorty_type, priority_value):
        if priorty_type == 'matematica':
            self.validar_prioridad('matematica', priority_value)
            self.math_priority = priority_value
        elif priorty_type == 'lenguaje':
            self.validar_prioridad('lenguaje', priority_value)
            self.language_priority = priority_value
        elif priorty_type == 'ingles':
            self.validar_prioridad('ingles', priority_value)
            self.english_priority = priority_value
        else:
            raise ValueError(f"Tipo de prioridad desconocido: {priorty_type}")

    def validar_prioridad(self, nombre_campo, valor):
        if not isinstance(valor, int) or valor < 0:
            raise MajorPrioritiesException(self.name, f"valor inválido para {nombre_campo}")