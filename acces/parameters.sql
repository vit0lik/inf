-- Поиск сотрудника по конкретной фамилии
SELECT * FROM Employees WHERE Last_Name = 'Иванов';

-- Заказы на конкретную дату
SELECT * FROM Orders WHERE Execution_Date = '2026-03-20';

-- Выборка заказов дороже 10 000
SELECT * FROM Orders WHERE Amount > 10000;