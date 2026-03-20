CREATE TABLE Post (
    Post_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL
);

CREATE TABLE Employees (
    Emp_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Last_Name TEXT NOT NULL,
    First_Name TEXT NOT NULL,
    Phone TEXT,
    Post_ID INTEGER,
    FOREIGN KEY (Post_ID) REFERENCES Post(Post_ID)
);

CREATE TABLE Clients (
    Client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Organization TEXT NOT NULL,
    Phone TEXT
);

CREATE TABLE Orders (
    Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Client_ID INTEGER,
    Emp_ID INTEGER,
    Amount REAL,
    Execution_Date DATE,
    Is_Completed BOOLEAN DEFAULT 0, -- 0 (нет), 1 (да)
    FOREIGN KEY (Client_ID) REFERENCES Clients(Client_ID),
    FOREIGN KEY (Emp_ID) REFERENCES Employees(Emp_ID)
);