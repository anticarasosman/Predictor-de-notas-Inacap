CREATE TABLE Semestre(
    id_semestre INT PRIMARY KEY AUTO_INCREMENT,
    -- Formato de periodo: 'PRIMAVERA 2025' o 'OTONO 2025'
    periodo VARCHAR(20) NOT NULL UNIQUE
);