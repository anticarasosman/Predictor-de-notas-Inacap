import sys

sys.path.append('load data')
from classes.major import Major
from exceptions.custom_exception import MajorException
from load_data import load_major_categories

class Majors_factory:
    def __init__(self):
        self.majors_categories = load_major_categories()

    def create_majors(self, student_data):
        majors_names = []
        majors_list = []
        for _, row in student_data.iterrows():
            if row["programa de estudio"] in majors_names:
                continue

            majors_names.append(row["programa de estudio"])
            
            try:
                major = self.name_major(row["programa de estudio"])
                self.assign_priorities(major)
            except MajorException as e:
                e.printErrorMessage()
                continue

            majors_list.append(major)

        return majors_list
    
    def name_major(self, name):
        major = Major(name)
        return major
    
    def assign_priorities(self, major):
        for _, row in self.majors_categories.iterrows():
            if major.name.lower() == row['programa de estudio'].lower():
                major.set_priority('matematica', row['ramos matematicos'])
                major.set_priority('lenguaje', row['ramos de lenguaje'])
                major.set_priority('ingles', row['ramos de ingles'])
                return major
        print(f"No se encontró la carrera '{major.name}' en las categorías de carreras. Se le asignarán prioridades -1 por defecto. \n")
    
    