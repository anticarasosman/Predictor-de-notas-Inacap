/*  Solo estudiantes activos en el sistema  */
CREATE OR REPLACE VIEW V_Estudiantes_Activos AS
SELECT 
    e.id_estudiante,
    e.rut,
    e.nombre AS nombre_estudiante,
    e.email_institucional,
    e.email_personal,
    e.telefono,
    e.edad,
    e.sexo,
    e.nacionalidad,
    
    c.id_carrera,
    c.codigo_carrera,
    c.nombre_carrera,
    c.mencion,
    c.jornada,
    c.tipo_programa,
    
    i.id_institucion,
    i.tipo_instucion,
    i.nombre_institucion,
    
    aa.id_area_academica,
    aa.nombre_area_academica,
    
    m.id_matricula,
    m.semestre_ingreso,
    m.ultimo_semestre_cursado,
    m.tipo_estudiante,
    m.estado_matricula,
    m.nivel_actual,
    m.es_candidato_a_gratuacion,
    m.es_trabajador,
    m.es_reincorporado,
    m.numero_de_convalidaciones,
    m.numero_de_homologaciones,
    m.cantidad_examenes_competencia,
    m.cantidad_asignaturas_actuales,
    m.fecha_matricula,
    
    pe.codigo_plan_estudio,
    pe.nombre_plan_estudio,
    pe.duracion_estimada_semestres,
    pe.estado AS estado_plan,
    
    e.fecha_creacion AS fecha_creacion_estudiante,
    m.fecha_actualizacion AS ultima_actualizacion_matricula
    
FROM Estudiante e
INNER JOIN Matricula m ON e.id_estudiante = m.id_estudiante
INNER JOIN Carrera c ON m.id_carrera = c.id_carrera
INNER JOIN Institucion i ON c.id_institucion = i.id_institucion
INNER JOIN Area_Academica aa ON c.id_area_academica = aa.id_area_academica
INNER JOIN Plan_Estudio pe ON c.id_plan_estudio = pe.id_plan_estudio
WHERE m.estado_matricula = 'ACTIVA'
  AND c.activa = TRUE
ORDER BY e.nombre, m.semestre_ingreso DESC;