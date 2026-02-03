from classes.estudiante import Estudiante

class EstudianteFactory:
    @staticmethod
    def crear_estudiante(datos_estudiante) -> Estudiante:
        nombre = datos_estudiante.nombre_estudiante
        run = datos_estudiante.run_estudiante
        notas_matematica = []
        notas_lenguaje = []
        notas_ingles = []   

        estudiante = Estudiante(nombre=nombre, run=run)
        
        for calificacion, asignatura in zip(datos_estudiante.calificaciones, datos_estudiante.asignaturas):
            # Guardar asignatura con su calificación
            estudiante.asignaturas_calificaciones.append((asignatura, calificacion))
            
            # Clasificar también por categoría
            if asignatura in datos_estudiante.categorias["Matematica"]:
                notas_matematica.append(calificacion)
            elif asignatura in datos_estudiante.categorias["Lenguaje"]:
                notas_lenguaje.append(calificacion)
            elif asignatura in datos_estudiante.categorias["Ingles"]:
                notas_ingles.append(calificacion)
        
        estudiante.notas_matematica = notas_matematica
        estudiante.notas_lenguaje = notas_lenguaje
        estudiante.notas_ingles = notas_ingles
        
        return estudiante