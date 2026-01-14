from classes.student import Student

class Students_factory:
    def create_students(self, student_data, majors):
        students_list = []
        
        for _, row in student_data.iterrows():
            try:
                # Buscar el major correspondiente
                major = self.find_major(row["programa de estudio"], majors)
                
                if major is None:
                    print(f"No se encontró el major '{row['programa de estudio']}' para el estudiante {row['nombre']} (rut: {row['rut']}). Se omitirá este estudiante.\n")
                    continue
                
                # Crear el estudiante
                student = Student(
                    rut=row["rut"],
                    name=row["nombre"],
                    major=major,
                    math_grade=row["promedio notas matemáticas"],
                    language_grade=row["promedio notas lenguaje"],
                    english_grade=row["promedio notas inglés"]
                )
                
                students_list.append(student)
                
            except Exception as e:
                print(f"Error al crear estudiante {row.get('rut', 'desconocido')}: {e}\n")
                continue
        
        return students_list
    
    def find_major(self, major_name, majors):
        """Busca y retorna el objeto Major que coincide con el nombre dado"""
        for major in majors:
            if major.name.lower() == major_name.lower():
                return major
        return None