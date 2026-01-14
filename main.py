import sys
import random
from factories.majors_factory import Majors_factory
from factories.students_factory import Students_factory
sys.path.append('load data')
sys.path.append('preprocessing')

from load_data import load_past_student_data

#Inicializar clases
majors_factory = Majors_factory()
students_factory = Students_factory()

# Cargar los datos de entrenamiento
print("\n========================================= Cargando datos pasados =========================================")
df_past_data = load_past_student_data()

print("\n========================================= Asignando categorias a Carreras =========================================\n")
majors = majors_factory.create_majors(df_past_data)
for major in majors:
    if major.math_priority != -1 and major.language_priority != -1 and major.english_priority != -1:
        print("El major:", major.name, "tiene las prioridades -> Matemática:", major.math_priority, ", Lenguaje:", major.language_priority, ", Inglés:", major.english_priority, "\n")

print("========================================= Creando perfiles de alumnos =========================================\n")
students = students_factory.create_students(df_past_data, majors)
#Imprimir algunos estudiantes creados al azar
for i in range(10):
    student = students[random.randint(0, len(students)-1)]
    print("Estudiante:", student.name, "con RUT:", student.rut, "pertenece al major:", student.major.name, "\n")

print("========================================= Buscando alumnos en riesgo academico =========================================\n")


print("========================================= Asignando prioridades a alumnos =========================================\n")