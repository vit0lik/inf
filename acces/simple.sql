-- Список всех сотрудников с их должностями
SELECT Last_Name, First_Name, Title 
FROM Employees JOIN Post ON Employees.Post_ID = Post.Post_ID;

-- Список всех клиентов и их контактов
SELECT Organization, Phone FROM Clients;

-- Список невыполненных заказов
SELECT * FROM Orders WHERE Is_Completed = 0;