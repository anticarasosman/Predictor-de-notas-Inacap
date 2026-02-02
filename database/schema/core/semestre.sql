CREATE TABLE Semestre(
    id_semestre INT PRIMARY KEY AUTO_INCREMENT,

    --El formato de periodo es (OTOÑO/PRIMAVERA) (AÑO), por ejemplo: 'PRIMAVERA 2025'
    periodo VARCHAR(20) NOT NULL UNIQUE,
)