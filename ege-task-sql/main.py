import pandas as pd
import sqlite3

data_frame = pd.read_excel('data/9.ods', engine='odf')
data_frame.columns = ['a', 'b', 'c']

connection = sqlite3.connect(':memory:')
data_frame.to_sql('triangles', connection, index=False)

query = """
SELECT COUNT(*) 
FROM triangles 
WHERE (a + b > c) 
  AND (a + c > b) 
  AND (b + c > a);
"""

result = connection.execute(query).fetchall()[0][0]

print(f"Ответ: {result}")

connection.close()