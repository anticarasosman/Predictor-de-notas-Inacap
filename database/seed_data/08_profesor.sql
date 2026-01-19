-- Seed data para Profesor
-- Basado en profesores.txt

INSERT INTO Profesor (nombre, rut, email_institucional, telefono, fecha_nacimiento, edad, sexo) VALUES
-- Profesores de Matemáticas
('Rojas Silva Pedro Eladio', '12345678-9', 'pedro.rojas@inacap.cl', '+56912345678', '1980-05-15', 45, 'MASCULINO'),
('Carrasco Soto Cristhian Arcadio', '12345679-7', 'cristhian.carrasco@inacap.cl', '+56912345679', '1985-08-20', 40, 'MASCULINO'),
('Barros Rojas Rosalba Margot', '12345680-0', 'rosalba.barros@inacap.cl', '+56912345680', '1978-03-10', 47, 'FEMENINO'),

-- Profesores de Inglés
('Maldonado Almonacid Diandra Alejandra', '12345681-9', 'diandra.maldonado@inacap.cl', '+56912345681', '1990-11-25', 35, 'FEMENINO'),
('Zúñiga Vera Yinnia Valeska', '12345682-7', 'yinnia.zuniga@inacap.cl', '+56912345682', '1988-07-14', 37, 'FEMENINO'),
('Molina Garrido Ricardo Andres', '12345683-5', 'ricardo.molina@inacap.cl', '+56912345683', '1982-02-28', 43, 'MASCULINO'),

-- Profesores de Comunicación
('Gonzalez Frychel Claudia Andrea', '12345684-3', 'claudia.gonzalez@inacap.cl', '+56912345684', '1986-09-05', 39, 'FEMENINO'),
('Fontecha Bórquez Tatiana Lorena', '12345685-1', 'tatiana.fontecha@inacap.cl', '+56912345685', '1992-12-18', 33, 'FEMENINO'),
('Inzulza Reyes Marcelo Osvaldo Antonio', '12345686-K', 'marcelo.inzulza@inacap.cl', '+56912345686', '1975-04-22', 50, 'MASCULINO');
