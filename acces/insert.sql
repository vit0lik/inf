INSERT INTO Post (Title) VALUES ('Менеджер'), ('Техник'), ('Директор');

INSERT INTO Clients (Organization, Phone) 
VALUES ('ООО Вектор', '111-222'), ('ИП Петров', '333-444'), ('ПАО Газ', '555-666');

INSERT INTO Employees (Last_Name, First_Name, Post_ID) 
VALUES ('Иванов', 'Иван', 1), ('Сидоров', 'Олег', 2), ('Кузнецов', 'Антон', 1);

INSERT INTO Orders (Client_ID, Emp_ID, Amount, Execution_Date, Is_Completed)
VALUES (1, 1, 15000.50, '2026-03-10', 1),
       (2, 2, 8900.00, '2026-03-15', 0),
       (3, 1, 45000.00, '2026-03-20', 1);