import math


def sort_students_by_subject(students, subject):
    """Ordena por promedio ascendente y, en empate, por prioridad de la carrera (mayor primero)."""
    subject_map = {
        'matematica': ('mean_math_grade', 'math_priority'),
        'lenguaje': ('mean_language_grade', 'language_priority'),
        'ingles': ('mean_english_grade', 'english_priority'),
    }

    mean_attr, priority_attr = subject_map[subject]

    def key_fn(student):
        grade = getattr(student, mean_attr, None)
        priority = getattr(student.major, priority_attr, -1)

        # Enviar faltantes al final
        grade_nan = grade is None or (isinstance(grade, float) and math.isnan(grade))
        grade_value = grade if not grade_nan else float('inf')

        # Prioridad más alta debe aparecer antes en empate de nota
        priority_value = priority if isinstance(priority, int) else -1

        return (grade_nan, grade_value, -priority_value)

    return sorted(students, key=key_fn)
