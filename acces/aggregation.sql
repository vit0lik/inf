-- Общее количество заказов у каждого сотрудника
SELECT Emp_ID, COUNT(Order_ID) AS Total_Count 
FROM Orders GROUP BY Emp_ID;

-- Общая сумма заказов по каждой организации
SELECT Client_ID, SUM(Amount) AS Total_Spent 
FROM Orders GROUP BY Client_ID;

-- Средний чек по всем выполненным заказам
SELECT AVG(Amount) FROM Orders WHERE Is_Completed = 1;