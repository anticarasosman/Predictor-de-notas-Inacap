CREATE TABLE Semestre(
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- Formato de periodo: '20XX primavera' o '20XX otoño'
    periodo VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;