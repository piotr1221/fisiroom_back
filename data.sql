INSERT INTO fisi_room_db.courses_category
VALUES
(1, 'Ciencias de la Computación', '', 'cc'),
(2, 'Ingeniería de Software', '', 'is'),
(3, 'Economía', '', 'eco'),
(4, 'Gestión', '', 'ges'),
(5, 'Física','', 'fis'),
(6, 'Química','', 'qui'),
(7, 'Matemática','', 'mat');

INSERT INTO fisi_room_db.courses_course
VALUES
-- Cambiar el ultimo numero por el id del dueño del curso
(1, 'Algorítmica I', 'Programación estructurada', '1', '08:00:00', '13:00:00', 1, 1),
(2, 'Calidad de Software', 'Métricas y técnicas de evaluación de software', '2', '08:00:00', '13:00:00', 1, 1),
(3, 'Econometría', 'Análisis económico matemático', '3', '08:00:00', '13:00:00', 1, 1),
(4, 'Álgebra Lineal', 'Manipulación de matrices y vectores', '7', '08:00:00', '13:00:00', 1, 1);

INSERT INTO courses_course_enrolled (course_id, user_id)
VALUES 
-- El primer valor es el id del curso, el segundo valor el id del usuario estudiante a matricularse
(1, 11);