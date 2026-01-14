import sys
import random
from factories.majors_factory import Majors_factory
from factories.students_factory import Students_factory
sys.path.append('load data')
sys.path.append('preprocessing')

from load_data import load_past_student_data
from utils.sorting import sort_students_by_subject

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
    print(f"Estudiante: {student.name}, con RUT: {student.rut}, pertenece al major: {student.major.name}")
    print(f"Promedio Matemática: {student.mean_math_grade}, Promedio Lenguaje: {student.mean_language_grade}, Promedio Inglés: {student.mean_english_grade}\n")

print("========================================= Buscando alumnos en riesgo academico =========================================\n")
for student in students:
    bad_performance = False
    if student.math_performance == "At risk" or student.math_performance == "Bad":
        print(f"Estudiante: {student.name}, con RUT: {student.rut}, tiene rendimiento en Matemática: {student.math_performance} con promedio: {student.mean_math_grade}")
        bad_performance = True
    if student.languaje_performance == "At risk" or student.languaje_performance == "Bad":
        print(f"Estudiante: {student.name}, con RUT: {student.rut}, tiene rendimiento en Lenguaje: {student.languaje_performance} con promedio: {student.mean_language_grade}")
        bad_performance = True
    if student.english_performance == "At risk" or student.english_performance == "Bad":
        print(f"Estudiante: {student.name}, con RUT: {student.rut}, tiene rendimiento en Inglés: {student.english_performance} con promedio: {student.mean_english_grade}")
        bad_performance = True
    if bad_performance:
        print("-------------------------------------------------")

print("========================================= Asignando prioridades a alumnos =========================================\n")

# Listas ordenadas por asignatura (promedio ascendente, empate por prioridad de la carrera)
lista_matematica = sort_students_by_subject(students, 'matematica')
lista_lenguaje = sort_students_by_subject(students, 'lenguaje')
lista_ingles = sort_students_by_subject(students, 'ingles')

print("Top 10 por Matemática (peor a mejor):")
for s in lista_matematica[:10]:
    print(f"- {s.name} | Prom: {s.mean_math_grade} | Prioridad carrera: {s.major.math_priority}")

print("\nTop 10 por Lenguaje (peor a mejor):")
for s in lista_lenguaje[:10]:
    print(f"- {s.name} | Prom: {s.mean_language_grade} | Prioridad carrera: {s.major.language_priority}")

print("\nTop 10 por Inglés (peor a mejor):")
for s in lista_ingles[:10]:
    print(f"- {s.name} | Prom: {s.mean_english_grade} | Prioridad carrera: {s.major.english_priority}")

print("\n========================================= Proceso finalizado =========================================\n")