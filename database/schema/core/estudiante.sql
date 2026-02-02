CREATE TABLE Estudiante (
    rut VARCHAR(12) PRIMARY KEY,

    secciones_curriculares INT,
    secciones_online INT,
    deuda INT DEFAULT 0,
    asistencia_promedio INT,

    nombre VARCHAR(200) NOT NULL,
    programa_estudio VARCHAR(100),
    nombre_apoderado VARCHAR(200),

    terminal BOOLEAN DEFAULT FALSE,
    tiene_gratuidad BOOLEAN DEFAULT FALSE,
    solicitud_interrupcion_estudios BOOLEAN DEFAULT FALSE,
    solicitud_interrupcion_estudio_pendiente BOOLEAN DEFAULT FALSE,
    interrupcion_estudio_pendiente BOOLEAN DEFAULT FALSE,
    beca_stem BOOLEAN DEFAULT FALSE,

    tipo_alumno ENUM("NUEVO", "VIEJO"),
    estado_matricula ENUM("ACTIVO", "PENDIENTE", "EN POSTULACION", "MATRICULADO", "LISTA DE ESPERA", "CANCELADO"),

    promedio_media_matematica DECIMAL(2,1),
    promedio_media_lenguaje DECIMAL(2,1),
    promedio_media_ingles DECIMAL(2,1),
    
    ultima_asistencia DATE,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)